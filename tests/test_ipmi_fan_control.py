import os
import signal
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../ansible/roles/ipmi_fan_control/files")))

from asrock_ipmi_fan_control import (  # noqa: E402
    ASRockIPMIDriver,
    DellIPMIDriver,
    IPMIHelper,
    SupermicroIPMIDriver,
    SysfsPWMDriver,
    SystemFanController,
)


class TestSystemFanController(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.metrics_file = os.path.join(self.temp_dir.name, "ipmi_fan_metrics.prom")
        self.controller = SystemFanController(
            driver_type="asrock_ipmi",
            interface="open",
            min_temp=40.0,
            target_temp=60.0,
            critical_temp=85.0,
            min_fan_speed=30,
            max_fan_speed=100,
            fan_channels=[1, 2, 3, 4],
            metrics_file=self.metrics_file,
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_calculate_fan_speed(self):
        self.assertEqual(self.controller.calculate_fan_speed(35.0), 30)
        self.assertEqual(self.controller.calculate_fan_speed(40.0), 30)
        self.assertEqual(self.controller.calculate_fan_speed(85.0), 100)
        self.assertEqual(self.controller.calculate_fan_speed(90.0), 100)
        self.assertEqual(self.controller.calculate_fan_speed(62.5), 65)

    @patch.object(IPMIHelper, "run_cmd")
    def test_asrock_driver(self, mock_run):
        mock_run.return_value = (True, "")
        driver = ASRockIPMIDriver(interface="open")
        self.assertTrue(driver.set_fan_speed(1, 50))
        mock_run.assert_called_with("open", ["0x3a", "0x01", "0x01", "0x32"], None, None, None)

        self.assertTrue(driver.restore_auto())
        mock_run.assert_called_with("open", ["0x3a", "0x02", "0x00"], None, None, None)

    @patch.object(IPMIHelper, "run_cmd")
    def test_supermicro_driver(self, mock_run):
        mock_run.return_value = (True, "")
        driver = SupermicroIPMIDriver(interface="open")
        self.assertTrue(driver.set_fan_speed(1, 50))
        mock_run.assert_called_with("open", ["0x30", "0x70", "0x66", "0x01", "0x00", "0x32"], None, None, None)

    @patch.object(IPMIHelper, "run_cmd")
    def test_dell_driver(self, mock_run):
        mock_run.return_value = (True, "")
        driver = DellIPMIDriver(interface="open")
        self.assertTrue(driver.set_fan_speed(1, 50))
        mock_run.assert_called_with("open", ["0x30", "0x30", "0x02", "0xff", "0x32"], None, None, None)

    @patch("glob.glob")
    def test_sysfs_pwm_driver(self, mock_glob):
        pwm_path = os.path.join(self.temp_dir.name, "pwm1")
        enable_path = os.path.join(self.temp_dir.name, "pwm1_enable")

        with open(pwm_path, "w") as f:
            f.write("0")
        with open(enable_path, "w") as f:
            f.write("2")

        mock_glob.return_value = [pwm_path]

        driver = SysfsPWMDriver()
        self.assertTrue(driver.is_available())
        self.assertTrue(driver.set_fan_speed(1, 50))

        with open(pwm_path, "r") as f:
            self.assertEqual(f.read().strip(), "127")
        with open(enable_path, "r") as f:
            self.assertEqual(f.read().strip(), "1")

        self.assertTrue(driver.restore_auto())
        with open(enable_path, "r") as f:
            self.assertEqual(f.read().strip(), "2")

    @patch.object(SystemFanController, "get_cpu_temp")
    @patch.object(SystemFanController, "get_gpu_temp")
    @patch.object(SystemFanController, "set_all_fans")
    def test_update_control_loop_normal(self, mock_set_fans, mock_gpu, mock_cpu):
        mock_cpu.return_value = 50.0
        mock_gpu.return_value = 55.0

        cpu, gpu, speed = self.controller.update_control_loop()
        self.assertEqual(cpu, 50.0)
        self.assertEqual(gpu, 55.0)
        self.assertEqual(speed, 53)
        mock_set_fans.assert_called_once_with(53)

        self.assertTrue(os.path.exists(self.metrics_file))
        with open(self.metrics_file, "r") as f:
            content = f.read()
            self.assertIn('ipmi_fan_sensor_temperature_celsius{sensor="cpu_max"} 50.0', content)
            self.assertIn('ipmi_fan_sensor_temperature_celsius{sensor="gpu_max"} 55.0', content)


if __name__ == "__main__":
    unittest.main()
