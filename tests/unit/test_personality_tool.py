import pytest
import json
from unittest.mock import patch, MagicMock
from pipecatapp.tools.personality_tool import PersonalityTool

@patch('pipecatapp.tools.personality_tool.requests.post')
def test_set_personality(mock_post):
    tool = PersonalityTool(api_url="http://fake-api")
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    result = tool.set_personality("assistant", 0.5)

    assert "Successfully set personality" in result
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert args[0] == "http://fake-api/control-vectors"
    payload = kwargs['json']
    assert len(payload) == 1
    assert payload[0]['fname'] == "/opt/nomad/models/vectors/assistant.gguf"
    assert payload[0]['strength'] == 0.5

@patch('pipecatapp.tools.personality_tool.requests.post')
def test_reset_personality(mock_post):
    tool = PersonalityTool(api_url="http://fake-api")
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    result = tool.reset_personality()

    assert "reset to neutral" in result
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert args[0] == "http://fake-api/control-vectors"
    assert kwargs['json'] == []

@patch('pipecatapp.tools.personality_tool.requests.get')
def test_get_current_personality(mock_get):
    tool = PersonalityTool(api_url="http://fake-api")
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = [{"fname": "assistant.gguf", "strength": 0.5}]
    mock_get.return_value = mock_response

    result = tool.get_current_personality()

    assert "Current configuration" in result
    assert "assistant.gguf" in result
    mock_get.assert_called_once_with("http://fake-api/control-vectors")
