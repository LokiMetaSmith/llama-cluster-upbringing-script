import pytest
import sys
import os
from unittest.mock import patch, mock_open
import json

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from power_tool import Power_Tool

@pytest.fixture
def power_tool():
    tool = Power_Tool()
    tool.config_path = "/fake/path/config.json"
    return tool

@patch('os.path.exists')
@patch('builtins.open', new_callable=mock_open)
def test_set_idle_threshold_for_new_service(mock_file, mock_exists, power_tool):
    """Test setting an idle threshold for a new service when config is new."""
    def exists_side_effect(path):
        if path == os.path.dirname(power_tool.config_path):
            return True
        if path == power_tool.config_path:
            return False
        return False
    mock_exists.side_effect = exists_side_effect

    result = power_tool.set_idle_threshold(service_port=8081, idle_seconds=300)

    assert "Successfully set idle threshold" in result

    mock_file.assert_called_once_with(power_tool.config_path, 'w')
    handle = mock_file.return_value
    written_data = "".join(call.args[0] for call in handle.write.call_args_list)
    written_json = json.loads(written_data)

    expected_json = {
        "monitored_services": {
            "8081": {
                "idle_threshold_seconds": 300
            }
        }
    }
    assert written_json == expected_json

@patch('os.path.exists', return_value=True)
@patch('builtins.open', new_callable=mock_open)
def test_set_idle_threshold_for_existing_service(mock_file, mock_exists, power_tool):
    """Test updating an idle threshold for an existing service."""
    initial_config = {
        "monitored_services": {
            "8081": {"idle_threshold_seconds": 100},
            "9090": {"idle_threshold_seconds": 200}
        }
    }

    m = mock_open(read_data=json.dumps(initial_config))
    with patch('builtins.open', m):
        result = power_tool.set_idle_threshold(service_port=8081, idle_seconds=500)

        assert "Successfully set idle threshold" in result

        m.assert_called_with(power_tool.config_path, 'w')
        handle = m.return_value
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)
        written_json = json.loads(written_data)

        assert written_json["monitored_services"]["8081"]["idle_threshold_seconds"] == 500
        assert written_json["monitored_services"]["9090"]["idle_threshold_seconds"] == 200

@patch('os.path.exists', return_value=False)
def test_config_directory_not_found(mock_exists, power_tool):
    """Test the error case where the config directory doesn't exist."""
    result = power_tool.set_idle_threshold(service_port=8081, idle_seconds=300)
    assert "Error: Power manager config directory not found" in result

@patch('os.path.exists', return_value=True)
@patch('builtins.open', side_effect=IOError("Permission denied"))
def test_file_io_error(mock_file, mock_exists, power_tool):
    """Test handling of an IOError during file operations."""
    result = power_tool.set_idle_threshold(service_port=8081, idle_seconds=300)
    assert "An error occurred while setting the power policy: Permission denied" in result
