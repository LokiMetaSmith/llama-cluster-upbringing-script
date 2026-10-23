import os
import signal
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

# Ensure script path can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../ansible/roles/ipmi_fan_control/files")))

from asrock_ipmi_fan_control import ASRockIPMIFanController  # noqa: E402


class TestASRockIPMIFanController(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.metrics_file = os.path.join(self.temp_dir.name, "ipmi_fan_metrics.prom")
        self.controller = ASRockIPMIFanController(
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
        # Temp <= min_temp -> min_fan_speed (30)
        self.assertEqual(self.controller.calculate_fan_speed(35.0), 30)
        self.assertEqual(self.controller.calculate_fan_speed(40.0), 30)

        # Temp >= critical_temp -> 100
        self.assertEqual(self.controller.calculate_fan_speed(85.0), 100)
        self.assertEqual(self.controller.calculate_fan_speed(90.0), 100)

        # Interpolation midway (62.5°C) -> ~65%
        # slope = (100 - 30) / (85 - 40) = 70 / 45 = 1.555...
        # calc_speed = 30 + int(22.5 * 1.555...) = 30 + 35 = 65
        self.assertEqual(self.controller.calculate_fan_speed(62.5), 65)

    @patch.object(ASRockIPMIFanController, "run_ipmi_cmd")
    def test_set_fan_speed(self, mock_ipmi):
        mock_ipmi.return_value = (True, "")
        success = self.controller.set_fan_speed(channel=1, percentage=50)
        self.assertTrue(success)
        mock_ipmi.assert_called_once_with(["0x3a", "0x01", "0x01", "0x32"])

    @patch.object(ASRockIPMIFanController, "run_ipmi_cmd")
    def test_restore_bmc_auto(self, mock_ipmi):
        mock_ipmi.return_value = (True, "")
        success = self.controller.restore_bmc_auto()
        self.assertTrue(success)
        self.assertTrue(self.controller.auto_mode)
        mock_ipmi.assert_called_once_with(["0x3a", "0x02", "0x00"])

    @patch.object(ASRockIPMIFanController, "get_cpu_temp")
    @patch.object(ASRockIPMIFanController, "get_gpu_temp")
    @patch.object(ASRockIPMIFanController, "set_all_fans")
    def test_update_control_loop_normal(self, mock_set_fans, mock_gpu, mock_cpu):
        mock_cpu.return_value = 50.0
        mock_gpu.return_value = 55.0

        cpu, gpu, speed = self.controller.update_control_loop()
        self.assertEqual(cpu, 50.0)
        self.assertEqual(gpu, 55.0)
        # Temp 55°C: 30 + int((55 - 40) * (70 / 45)) = 30 + 23 = 53
        self.assertEqual(speed, 53)
        mock_set_fans.assert_called_once_with(53)

        # Verify metrics written
        self.assertTrue(os.path.exists(self.metrics_file))
        with open(self.metrics_file, "r") as f:
            content = f.read()
            self.assertIn('ipmi_fan_sensor_temperature_celsius{sensor="cpu_max"} 50.0', content)
            self.assertIn('ipmi_fan_sensor_temperature_celsius{sensor="gpu_max"} 55.0', content)
            self.assertIn('ipmi_fan_speed_percent{channel="fan1"} 53', content)

    @patch.object(ASRockIPMIFanController, "get_cpu_temp")
    @patch.object(ASRockIPMIFanController, "get_gpu_temp")
    @patch.object(ASRockIPMIFanController, "restore_bmc_auto")
    def test_update_control_loop_critical_temp(self, mock_bmc_auto, mock_gpu, mock_cpu):
        mock_cpu.return_value = 88.0
        mock_gpu.return_value = 60.0

        cpu, gpu, speed = self.controller.update_control_loop()
        self.assertEqual(speed, 100)
        mock_bmc_auto.assert_called_once()

    @patch.object(ASRockIPMIFanController, "get_cpu_temp")
    @patch.object(ASRockIPMIFanController, "get_gpu_temp")
    @patch.object(ASRockIPMIFanController, "set_all_fans")
    def test_update_control_loop_no_sensors(self, mock_set_fans, mock_gpu, mock_cpu):
        mock_cpu.return_value = None
        mock_gpu.return_value = None

        cpu, gpu, speed = self.controller.update_control_loop()
        self.assertEqual(speed, 100)
        mock_set_fans.assert_called_once_with(100)


if __name__ == "__main__":
    unittest.main()
