#!/usr/bin/env python3
"""
ASRock Rack IPMI Fan Control & Monitoring Daemon

Provides dynamic temperature tracking (CPU + GPU), raw IPMI fan speed control
for ASRock Rack motherboards using NetFn 0x3a, Prometheus metric export for Telegraf,
and automatic BMC fallback on exit/crash or critical thermal events.
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


class ASRockIPMIFanController:
    def __init__(
        self,
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
        self.interface = interface
        self.host = host
        self.user = user
        self.password = password
        self.min_temp = min_temp
        self.target_temp = target_temp
        self.critical_temp = critical_temp
        self.min_fan_speed = max(0, min(100, min_fan_speed))
        self.max_fan_speed = max(0, min(100, max_fan_speed))
        self.fan_channels = fan_channels if fan_channels else [1, 2, 3, 4, 5, 6]
        self.metrics_file = metrics_file
        self.auto_mode = False
        self._running = True

    def _build_ipmi_cmd(self, raw_bytes: List[str]) -> List[str]:
        cmd = ["ipmitool", "-I", self.interface]
        if self.interface == "lanplus" and self.host:
            cmd.extend(["-H", self.host])
            if self.user:
                cmd.extend(["-U", self.user])
            if self.password:
                cmd.extend(["-P", self.password])
        cmd.append("raw")
        cmd.extend(raw_bytes)
        return cmd

    def run_ipmi_cmd(self, raw_bytes: List[str]) -> Tuple[bool, str]:
        cmd = self._build_ipmi_cmd(raw_bytes)
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True, res.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            err_msg = getattr(e, "stderr", str(e))
            logging.error(f"IPMI command failed ({' '.join(cmd)}): {err_msg}")
            return False, str(err_msg)

    def set_fan_speed(self, channel: int, percentage: int) -> bool:
        """Sets fan speed for specified channel (1-8) to a given percentage (0-100)."""
        percentage = max(0, min(100, percentage))
        speed_hex = f"0x{percentage:02x}"
        channel_hex = f"0x{channel:02x}"
        # ASRock Rack NetFn 0x3a, Cmd 0x01: Set Fan Speed
        success, _ = self.run_ipmi_cmd(["0x3a", "0x01", channel_hex, speed_hex])
        return success

    def set_all_fans(self, percentage: int) -> bool:
        all_success = True
        for ch in self.fan_channels:
            if not self.set_fan_speed(ch, percentage):
                all_success = False
        return all_success

    def restore_bmc_auto(self) -> bool:
        """Restores BMC automatic fan control mode (NetFn 0x3a, Cmd 0x02 or set 100%)."""
        logging.info("Restoring BMC automatic fan control mode...")
        self.auto_mode = True
        # NetFn 0x3a 0x02 sets BMC auto mode on ASRock Rack
        success, _ = self.run_ipmi_cmd(["0x3a", "0x02", "0x00"])
        if not success:
            logging.warning("Failed to issue BMC auto command. Setting fans to 100% safety default.")
            self.set_all_fans(100)
        return success

    def get_cpu_temp(self) -> Optional[float]:
        """Reads CPU temperature from sysfs /sys/class/hwmon."""
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
        """Reads GPU temperature from nvidia-smi, rocm-smi, or sysfs."""
        temps = []
        # Try nvidia-smi
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

        # Try rocm-smi
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

        # Try sysfs drm hwmon
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
        """Calculates fan speed percentage based on max temperature."""
        if max_temp >= self.critical_temp:
            return 100
        if max_temp <= self.min_temp:
            return self.min_fan_speed

        # Linear interpolation between min_temp and critical_temp
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
        """Exports metrics in Prometheus format for Telegraf monitoring."""
        lines = [
            "# HELP ipmi_fan_speed_percent Current IPMI fan speed percentage",
            "# TYPE ipmi_fan_speed_percent gauge",
        ]
        for ch in self.fan_channels:
            lines.append(f'ipmi_fan_speed_percent{{channel="fan{ch}"}} {current_speed}')

        lines.extend([
            "# HELP ipmi_fan_sensor_temperature_celsius Temperature sensor readings in Celsius",
            "# TYPE ipmi_fan_sensor_temperature_celsius gauge",
            f'ipmi_fan_sensor_temperature_celsius{{sensor="cpu_max"}} {cpu_temp if cpu_temp is not None else -1.0}',
            f'ipmi_fan_sensor_temperature_celsius{{sensor="gpu_max"}} {gpu_temp if gpu_temp is not None else -1.0}',
            "# HELP ipmi_fan_control_auto_mode Indicates if fan control is currently in BMC auto/fallback mode",
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
                "Triggering emergency 100% fans and BMC auto mode fallback."
            )
            self.restore_bmc_auto()
            self.export_metrics(cpu_temp, gpu_temp, 100, is_auto=True)
            return cpu_temp, gpu_temp, 100

        target_speed = self.calculate_fan_speed(max_temp)
        self.set_all_fans(target_speed)
        self.auto_mode = False
        self.export_metrics(cpu_temp, gpu_temp, target_speed, is_auto=False)
        return cpu_temp, gpu_temp, target_speed

    def stop(self) -> None:
        self._running = False
        self.restore_bmc_auto()


def main():
    parser = argparse.ArgumentParser(description="ASRock IPMI Fan Controller Daemon")
    parser.add_argument("--config", default="/etc/ipmi-fan-control/config.ini", help="Path to config file")
    parser.add_argument("--stop", action="store_true", help="Restore BMC auto mode and exit")
    args = parser.parse_args()

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

    controller = ASRockIPMIFanController(
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
        logging.info("Stop flag received. Restoring BMC auto fan control mode...")
        controller.restore_bmc_auto()
        sys.exit(0)

    def handle_signal(sig, frame):
        logging.info(f"Received signal {sig}. Stopping fan controller and reverting to BMC auto...")
        controller.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    logging.info("Starting ASRock IPMI Fan Controller Daemon loop...")
    try:
        while controller._running:
            cpu, gpu, speed = controller.update_control_loop()
            logging.info(
                f"Status: CPU={cpu if cpu else 'N/A'}°C, GPU={gpu if gpu else 'N/A'}°C => Fan Speed={speed}%"
            )
            time.sleep(interval)
    except Exception as e:
        logging.error(f"Unhandled exception in controller loop: {e}")
        controller.restore_bmc_auto()
        raise


if __name__ == "__main__":
    main()
