import unittest
from unittest.mock import patch, mock_open
import json
import os

# Assume power_tool is in the same directory
from power_tool import Power_Tool

class TestPowerTool(unittest.TestCase):

    def setUp(self):
        """Set up the tool instance before each test."""
        self.power_tool = Power_Tool()
        self.power_tool.config_path = "/fake/path/config.json"

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_set_idle_threshold_for_new_service(self, mock_file, mock_exists):
        """Test setting an idle threshold for a new service when config is new."""
        # Simulate that the config directory exists but the file does not.
        def exists_side_effect(path):
            if path == os.path.dirname(self.power_tool.config_path):
                return True
            if path == self.power_tool.config_path:
                return False
            return False
        mock_exists.side_effect = exists_side_effect

        result = self.power_tool.set_idle_threshold(service_port=8080, idle_seconds=300)

        # Verify the result message
        self.assertIn("Successfully set idle threshold", result)

        # Verify the file was written to with the correct content
        mock_file.assert_called_once_with(self.power_tool.config_path, 'w')
        handle = mock_file.return_value

        # json.dump with indent calls write multiple times, so we need to join the args
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)
        written_json = json.loads(written_data)

        expected_json = {
            "monitored_services": {
                "8080": {
                    "idle_threshold_seconds": 300
                }
            }
        }
        self.assertEqual(written_json, expected_json)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_set_idle_threshold_for_existing_service(self, mock_file, mock_exists):
        """Test updating an idle threshold for an existing service."""
        # Initial config content
        initial_config = {
            "monitored_services": {
                "8080": {"idle_threshold_seconds": 100},
                "9090": {"idle_threshold_seconds": 200}
            }
        }
        # Set up the mock to read the initial config, then call the tool
        m = mock_open(read_data=json.dumps(initial_config))
        with patch('builtins.open', m):
            result = self.power_tool.set_idle_threshold(service_port=8080, idle_seconds=500)

            self.assertIn("Successfully set idle threshold", result)

            # Verify the written content
            m.assert_called_with(self.power_tool.config_path, 'w')
            handle = m.return_value
            written_data = "".join(call.args[0] for call in handle.write.call_args_list)
            written_json = json.loads(written_data)

            # Check that the value was updated and other values remain
            self.assertEqual(written_json["monitored_services"]["8080"]["idle_threshold_seconds"], 500)
            self.assertEqual(written_json["monitored_services"]["9090"]["idle_threshold_seconds"], 200)

    @patch('os.path.exists', return_value=False)
    def test_config_directory_not_found(self, mock_exists):
        """Test the error case where the config directory doesn't exist."""
        result = self.power_tool.set_idle_threshold(service_port=8080, idle_seconds=300)
        self.assertIn("Error: Power manager config directory not found", result)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_file_io_error(self, mock_file, mock_exists):
        """Test handling of an IOError during file operations."""
        result = self.power_tool.set_idle_threshold(service_port=8080, idle_seconds=300)
        self.assertIn("An error occurred while setting the power policy: Permission denied", result)

if __name__ == '__main__':
    unittest.main()