#!/usr/bin/env python3
"""
System Fan Control & Telemetry Daemon

Provides dynamic temperature tracking (CPU + GPU), multi-backend fan speed control
(ASRock Rack IPMI, Supermicro IPMI, Dell iDRAC IPMI, sysfs PWM), Prometheus metric export
for Telegraf, and conservative automatic fallback on exit, crash, or critical thermal events.
"""

import argparse
import configparser
import glob
import logging
import os
import signal
import subprocess
import sys
import time
from typing import Dict, List, Optional, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


class BaseFanDriver:
    """Base interface for fan control drivers."""

    def __init__(self, interface: str = "open", host: Optional[str] = None,
                 user: Optional[str] = None, password: Optional[str] = None):
        self.interface = interface
        self.host = host
        self.user = user
        self.password = password

    def set_fan_speed(self, channel: int, percentage: int) -> bool:
        raise NotImplementedError

    def restore_auto(self) -> bool:
        raise NotImplementedError

    def is_available(self) -> bool:
        return True


class IPMIHelper:
    @staticmethod
    def build_cmd(interface: str, raw_bytes: List[str], host: Optional[str] = None,
                  user: Optional[str] = None, password: Optional[str] = None) -> List[str]:
        cmd = ["ipmitool", "-I", interface]
        if interface == "lanplus" and host:
            cmd.extend(["-H", host])
            if user:
                cmd.extend(["-U", user])
            if password:
                cmd.extend(["-P", password])
        cmd.append("raw")
        cmd.extend(raw_bytes)
        return cmd

    @staticmethod
    def run_cmd(interface: str, raw_bytes: List[str], host: Optional[str] = None,
                user: Optional[str] = None, password: Optional[str] = None) -> Tuple[bool, str]:
        cmd = IPMIHelper.build_cmd(interface, raw_bytes, host, user, password)
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True, res.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            err_msg = getattr(e, "stderr", str(e))
            return False, str(err_msg)


class ASRockIPMIDriver(BaseFanDriver):
    """ASRock Rack IPMI Driver (NetFn 0x3a)."""

    def set_fan_speed(self, channel: int, percentage: int) -> bool:
        percentage = max(0, min(100, percentage))
        speed_hex = f"0x{percentage:02x}"
        channel_hex = f"0x{channel:02x}"
        success, _ = IPMIHelper.run_cmd(
            self.interface, ["0x3a", "0x01", channel_hex, speed_hex],
            self.host, self.user, self.password
        )
        return success

    def restore_auto(self) -> bool:
        success, _ = IPMIHelper.run_cmd(
            self.interface, ["0x3a", "0x02", "0x00"],
            self.host, self.user, self.password
        )
        return success


class SupermicroIPMIDriver(BaseFanDriver):
    """Supermicro IPMI Driver (NetFn 0x30 0x70)."""

    def set_fan_speed(self, channel: int, percentage: int) -> bool:
        percentage = max(0, min(100, percentage))
        speed_hex = f"0x{percentage:02x}"
        # Zone 0x00 = CPU/System, Zone 0x01 = Peripheral
        zone = "0x00" if channel <= 2 else "0x01"
        success, _ = IPMIHelper.run_cmd(
            self.interface, ["0x30", "0x70", "0x66", "0x01", zone, speed_hex],
            self.host, self.user, self.password
        )
        return success

    def restore_auto(self) -> bool:
        success, _ = IPMIHelper.run_cmd(
            self.interface, ["0x30", "0x70", "0x66", "0x01", "0x00", "0x00"],
            self.host, self.user, self.password
        )
        return success


class DellIPMIDriver(BaseFanDriver):
    """Dell iDRAC IPMI Driver (NetFn 0x30 0x30)."""

    def set_fan_speed(self, channel: int, percentage: int) -> bool:
        percentage = max(0, min(100, percentage))
        speed_hex = f"0x{percentage:02x}"
        # First enable manual fan control mode
        IPMIHelper.run_cmd(
            self.interface, ["0x30", "0x30", "0x01", "0x00"],
            self.host, self.user, self.password
        )
        # Set fan speed across all fans (0x18 = 24 / all)
        success, _ = IPMIHelper.run_cmd(
            self.interface, ["0x30", "0x30", "0x02", "0xff", speed_hex],
            self.host, self.user, self.password
        )
        return success

    def restore_auto(self) -> bool:
        # Restore iDRAC dynamic fan control mode
        success, _ = IPMIHelper.run_cmd(
            self.interface, ["0x30", "0x30", "0x01", "0x01"],
            self.host, self.user, self.password
        )
        return success


class SysfsPWMDriver(BaseFanDriver):
    """Linux sysfs PWM Driver (/sys/class/hwmon/hwmon*/pwm*)."""

    def is_available(self) -> bool:
        return len(glob.glob("/sys/class/hwmon/hwmon*/pwm*")) > 0

    def set_fan_speed(self, channel: int, percentage: int) -> bool:
        percentage = max(0, min(100, percentage))
        pwm_val = int((percentage / 100.0) * 255)
        pwms = sorted(glob.glob("/sys/class/hwmon/hwmon*/pwm[1-8]"))
        if not pwms:
            return False

        target_pwm = pwms[(channel - 1) % len(pwms)]
        enable_path = f"{target_pwm}_enable"

        try:
            if os.path.exists(enable_path):
                # Mode 1 = manual control
                with open(enable_path, "w") as f:
                    f.write("1")
            with open(target_pwm, "w") as f:
                f.write(str(pwm_val))
            return True
        except Exception as e:
            logging.error(f"Failed to set sysfs PWM {target_pwm}: {e}")
            return False

    def restore_auto(self) -> bool:
        all_restored = True
        for pwm in glob.glob("/sys/class/hwmon/hwmon*/pwm[1-8]"):
            enable_path = f"{pwm}_enable"
            try:
                if os.path.exists(enable_path):
                    # Mode 2 = automatic control
                    with open(enable_path, "w") as f:
                        f.write("2")
                else:
                    # Conservative fallback: set PWM to full speed (255)
                    with open(pwm, "w") as f:
                        f.write("255")
            except Exception as e:
                logging.warning(f"Could not restore auto mode for sysfs PWM {pwm}: {e}")
                all_restored = False
        return all_restored


class AutoDriver(BaseFanDriver):
    """Auto-detecting Fan Driver."""

    def __init__(self, interface: str = "open", host: Optional[str] = None,
                 user: Optional[str] = None, password: Optional[str] = None):
        super().__init__(interface, host, user, password)
        self.active_driver = self._detect_driver()

    def _detect_driver(self) -> BaseFanDriver:
        # Check ASRock IPMI
        success, _ = IPMIHelper.run_cmd(self.interface, ["0x3a", "0x02", "0x00"], self.host, self.user, self.password)
        if success:
            logging.info("Auto-detected fan driver: ASRock IPMI")
            return ASRockIPMIDriver(self.interface, self.host, self.user, self.password)

        # Check Sysfs PWM
        sysfs_drv = SysfsPWMDriver(self.interface, self.host, self.user, self.password)
        if sysfs_drv.is_available():
            logging.info("Auto-detected fan driver: Sysfs PWM")
            return sysfs_drv

        # Fallback to ASRock IPMI
        logging.info("Defaulting to ASRock IPMI driver")
        return ASRockIPMIDriver(self.interface, self.host, self.user, self.password)

    def set_fan_speed(self, channel: int, percentage: int) -> bool:
        return self.active_driver.set_fan_speed(channel, percentage)

    def restore_auto(self) -> bool:
        return self.active_driver.restore_auto()


DRIVER_MAP = {
    "asrock_ipmi": ASRockIPMIDriver,
    "supermicro_ipmi": SupermicroIPMIDriver,
    "dell_ipmi": DellIPMIDriver,
    "sysfs_pwm": SysfsPWMDriver,
    "auto": AutoDriver,
}


class SystemFanController:
    def __init__(
        self,
        driver_type: str = "auto",
        interface: str = "open",
        host: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        min_temp: float = 40.0,
        target_temp: float = 65.0,
        critical_temp: float = 85.0,
        min_fan_speed: int = 30,
        max_fan_speed: int = 100,
        fan_channels: Optional[List[int]] = None,
        metrics_file: str = "/var/lib/telegraf/ipmi_fan_metrics.prom",
    ):
        self.driver_class = DRIVER_MAP.get(driver_type.lower(), AutoDriver)
        self.driver = self.driver_class(interface=interface, host=host, user=user, password=password)
        self.min_temp = min_temp
        self.target_temp = target_temp
        self.critical_temp = critical_temp
        self.min_fan_speed = max(0, min(100, min_fan_speed))
        self.max_fan_speed = max(0, min(100, max_fan_speed))
        self.fan_channels = fan_channels if fan_channels else [1, 2, 3, 4, 5, 6]
        self.metrics_file = metrics_file
        self.auto_mode = False
        self._running = True

    def set_fan_speed(self, channel: int, percentage: int) -> bool:
        return self.driver.set_fan_speed(channel, percentage)

    def set_all_fans(self, percentage: int) -> bool:
        all_success = True
        for ch in self.fan_channels:
            if not self.set_fan_speed(ch, percentage):
                all_success = False
        return all_success

    def restore_auto(self) -> bool:
        logging.info("Restoring automatic fan control mode...")
        self.auto_mode = True
        success = self.driver.restore_auto()
        if not success:
            logging.warning("Failed to restore driver auto mode. Setting fans to 100% safety default.")
            self.set_all_fans(100)
        return success

    def get_cpu_temp(self) -> Optional[float]:
        temps = []
        for path in glob.glob("/sys/class/hwmon/hwmon*/temp*_input"):
            try:
                with open(path, "r") as f:
                    val = float(f.read().strip()) / 1000.0
                    if 0.0 < val < 125.0:
                        temps.append(val)
            except Exception:
                continue
        return max(temps) if temps else None

    def get_gpu_temp(self) -> Optional[float]:
        temps = []
        try:
            res = subprocess.run(
                ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"],
                capture_output=True, text=True, check=True
            )
            for line in res.stdout.strip().split("\n"):
                if line.strip().isdigit():
                    temps.append(float(line.strip()))
        except Exception:
            pass

        if not temps:
            try:
                res = subprocess.run(
                    ["rocm-smi", "--showtemp"],
                    capture_output=True, text=True, check=True
                )
                for line in res.stdout.splitlines():
                    if "Temperature (Sensor edge)" in line or "Temperature (Sensor junction)" in line:
                        parts = line.split(":")
                        if len(parts) > 1:
                            val_str = parts[1].strip().replace("c", "").replace("C", "")
                            try:
                                temps.append(float(val_str))
                            except ValueError:
                                pass
            except Exception:
                pass

        if not temps:
            for path in glob.glob("/sys/class/drm/card*/device/hwmon/hwmon*/temp1_input"):
                try:
                    with open(path, "r") as f:
                        val = float(f.read().strip()) / 1000.0
                        if 0.0 < val < 125.0:
                            temps.append(val)
                except Exception:
                    continue

        return max(temps) if temps else None

    def calculate_fan_speed(self, max_temp: float) -> int:
        if max_temp >= self.critical_temp:
            return 100
        if max_temp <= self.min_temp:
            return self.min_fan_speed

        temp_range = self.critical_temp - self.min_temp
        speed_range = self.max_fan_speed - self.min_fan_speed
        slope = speed_range / temp_range
        calc_speed = self.min_fan_speed + int((max_temp - self.min_temp) * slope)
        return max(self.min_fan_speed, min(self.max_fan_speed, calc_speed))

    def export_metrics(
        self,
        cpu_temp: Optional[float],
        gpu_temp: Optional[float],
        current_speed: int,
        is_auto: bool
    ) -> None:
        lines = [
            "# HELP ipmi_fan_speed_percent Current IPMI/System fan speed percentage",
            "# TYPE ipmi_fan_speed_percent gauge",
        ]
        for ch in self.fan_channels:
            lines.append(f'ipmi_fan_speed_percent{{channel="fan{ch}"}} {current_speed}')

        lines.extend([
            "# HELP ipmi_fan_sensor_temperature_celsius Temperature sensor readings in Celsius",
            "# TYPE ipmi_fan_sensor_temperature_celsius gauge",
            f'ipmi_fan_sensor_temperature_celsius{{sensor="cpu_max"}} {cpu_temp if cpu_temp is not None else -1.0}',
            f'ipmi_fan_sensor_temperature_celsius{{sensor="gpu_max"}} {gpu_temp if gpu_temp is not None else -1.0}',
            "# HELP ipmi_fan_control_auto_mode Indicates if fan control is currently in auto/fallback mode",
            "# TYPE ipmi_fan_control_auto_mode gauge",
            f'ipmi_fan_control_auto_mode {1 if is_auto else 0}',
        ])

        try:
            os.makedirs(os.path.dirname(self.metrics_file), exist_ok=True)
            tmp_file = f"{self.metrics_file}.tmp"
            with open(tmp_file, "w") as f:
                f.write("\n".join(lines) + "\n")
            os.replace(tmp_file, self.metrics_file)
        except Exception as e:
            logging.error(f"Failed to write metrics to {self.metrics_file}: {e}")

    def update_control_loop(self) -> Tuple[Optional[float], Optional[float], int]:
        cpu_temp = self.get_cpu_temp()
        gpu_temp = self.get_gpu_temp()

        active_temps = [t for t in (cpu_temp, gpu_temp) if t is not None]

        if not active_temps:
            logging.warning("No temperature sensors accessible! Defaulting to 100% fan speed for safety.")
            self.set_all_fans(100)
            self.export_metrics(cpu_temp, gpu_temp, 100, is_auto=False)
            return cpu_temp, gpu_temp, 100

        max_temp = max(active_temps)

        if max_temp >= self.critical_temp:
            logging.critical(
                f"Critical temperature reached ({max_temp:.1f}°C >= {self.critical_temp}°C)! "
                "Triggering emergency 100% fans and auto mode fallback."
            )
            self.restore_auto()
            self.export_metrics(cpu_temp, gpu_temp, 100, is_auto=True)
            return cpu_temp, gpu_temp, 100

        target_speed = self.calculate_fan_speed(max_temp)
        self.set_all_fans(target_speed)
        self.auto_mode = False
        self.export_metrics(cpu_temp, gpu_temp, target_speed, is_auto=False)
        return cpu_temp, gpu_temp, target_speed

    def stop(self) -> None:
        self._running = False
        self.restore_auto()


# Backwards compatibility alias
ASRockIPMIFanController = SystemFanController


def main():
    parser = argparse.ArgumentParser(description="System IPMI & Sysfs Fan Controller Daemon")
    parser.add_argument("--config", default="/etc/ipmi-fan-control/config.ini", help="Path to config file")
    parser.add_argument("--stop", action="store_true", help="Restore auto mode and exit")
    args = parser.parse_args()

    driver_type = "auto"
    interface = "open"
    host = None
    user = None
    password = None
    min_temp = 40.0
    target_temp = 65.0
    critical_temp = 85.0
    min_fan_speed = 30
    max_fan_speed = 100
    interval = 10
    fan_channels = [1, 2, 3, 4, 5, 6]
    metrics_file = "/var/lib/telegraf/ipmi_fan_metrics.prom"

    if os.path.exists(args.config):
        cfg = configparser.ConfigParser()
        cfg.read(args.config)
        if "Settings" in cfg:
            driver_type = cfg["Settings"].get("driver", driver_type)
            interface = cfg["Settings"].get("interface", interface)
            host = cfg["Settings"].get("host", host)
            user = cfg["Settings"].get("user", user)
            password = cfg["Settings"].get("password", password)
            interval = cfg["Settings"].getint("interval", interval)
            metrics_file = cfg["Settings"].get("metrics_file", metrics_file)

        if "Temperatures" in cfg:
            min_temp = cfg["Temperatures"].getfloat("min_temp", min_temp)
            target_temp = cfg["Temperatures"].getfloat("target_temp", target_temp)
            critical_temp = cfg["Temperatures"].getfloat("critical_temp", critical_temp)

        if "FanSpeeds" in cfg:
            min_fan_speed = cfg["FanSpeeds"].getint("min_fan_speed", min_fan_speed)
            max_fan_speed = cfg["FanSpeeds"].getint("max_fan_speed", max_fan_speed)
            channels_str = cfg["FanSpeeds"].get("channels", "1,2,3,4,5,6")
            parsed_channels = []
            for c in channels_str.split(","):
                clean_c = c.strip().lower().replace("fan", "")
                if clean_c.isdigit():
                    parsed_channels.append(int(clean_c))
            if parsed_channels:
                fan_channels = parsed_channels

    controller = SystemFanController(
        driver_type=driver_type,
        interface=interface,
        host=host,
        user=user,
        password=password,
        min_temp=min_temp,
        target_temp=target_temp,
        critical_temp=critical_temp,
        min_fan_speed=min_fan_speed,
        max_fan_speed=max_fan_speed,
        fan_channels=fan_channels,
        metrics_file=metrics_file,
    )

    if args.stop:
        logging.info("Stop flag received. Restoring automatic fan control mode...")
        controller.restore_auto()
        sys.exit(0)

    def handle_signal(sig, frame):
        logging.info(f"Received signal {sig}. Stopping fan controller and reverting to auto mode...")
        controller.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    logging.info("Starting System Fan Controller Daemon loop...")
    try:
        while controller._running:
            cpu, gpu, speed = controller.update_control_loop()
            logging.info(
                f"Status: CPU={cpu if cpu else 'N/A'}°C, GPU={gpu if gpu else 'N/A'}°C => Fan Speed={speed}%"
            )
            time.sleep(interval)
    except Exception as e:
        logging.error(f"Unhandled exception in controller loop: {e}")
        controller.restore_auto()
        raise


if __name__ == "__main__":
    main()
