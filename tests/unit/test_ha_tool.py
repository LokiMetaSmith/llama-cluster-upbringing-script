import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import requests

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pipecatapp', 'tools')))

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

@patch('pipecatapp.tools.ha_tool.requests.post')
def test_call_ai_task_failure(mock_post):
    tool = HA_Tool("http://ha", "token")
    class MockRequestException(Exception): pass
    mock_post.side_effect = MockRequestException("Error")
    with patch('pipecatapp.tools.ha_tool.requests.exceptions.RequestException', MockRequestException):
        result = tool.call_ai_task("turn on lights")
    assert "Error calling Home Assistant API: Error" in result
