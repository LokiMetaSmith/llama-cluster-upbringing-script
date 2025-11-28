import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import requests

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from ha_tool import HA_Tool

def test_init_success():
    with patch.dict(os.environ, {'HA_URL': 'http://ha', 'HA_TOKEN': 'token'}):
        tool = HA_Tool()
        assert tool.ha_url == 'http://ha'

def test_init_failure():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError):
            HA_Tool()

@patch('requests.post')
def test_call_ai_task_success(mock_post):
    tool = HA_Tool("http://ha", "token")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    result = tool.call_ai_task("turn on lights")
    assert "Successfully sent command" in result
    mock_post.assert_called_once()

@patch('requests.post')
def test_call_ai_task_failure(mock_post):
    tool = HA_Tool("http://ha", "token")
    mock_post.side_effect = requests.exceptions.RequestException("Error")

    result = tool.call_ai_task("turn on lights")
    assert "Error calling Home Assistant API: Error" in result
