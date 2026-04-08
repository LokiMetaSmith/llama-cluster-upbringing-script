import pytest
from unittest.mock import patch, MagicMock
from pipecatapp.tools.opencode_provider_tool import OpenCodeProviderTool

def test_parse_opencode_output():
    tool = OpenCodeProviderTool()

    mock_logs = """
OpenCode AI v1.0.0
> Analyzing the repository...
Thinking... this might be complex
Executing tool: read_file
Error: file not found
Finished the task successfully.
"""
    parsed = tool._parse_opencode_output(mock_logs)

    assert parsed["agent_type"] == "opencode_cli"
    assert parsed["events_count"] == 5

    events = parsed["events"]
    assert events[0]["type"] == "thought"
    assert events[1]["type"] == "thought"
    assert events[2]["type"] == "tool_execution"
    assert events[3]["type"] == "error"
    assert events[4]["type"] == "text"

@patch('pipecatapp.tools.opencode_provider_tool.requests.post')
@patch('pipecatapp.tools.opencode_provider_tool.requests.get')
@patch('pipecatapp.tools.opencode_provider_tool.requests.delete')
def test_opencode_provider_run_success(mock_delete, mock_get, mock_post):
    tool = OpenCodeProviderTool()

    # Mock Post (Job Registration)
    mock_post_response = MagicMock()
    mock_post_response.status_code = 200
    mock_post.return_value = mock_post_response

    # Mock Get (Allocations and Logs)
    mock_allocs_response = MagicMock()
    mock_allocs_response.status_code = 200
    mock_allocs_response.json.return_value = [{"ID": "alloc-123", "ClientStatus": "complete"}]

    mock_logs_response = MagicMock()
    mock_logs_response.status_code = 200
    mock_logs_response.text = "> Thinking... \\nFinished!"

    # Side effect: first call is for allocations, second and third for stdout/stderr logs
    mock_get.side_effect = [mock_allocs_response, mock_logs_response, MagicMock(status_code=200, text="")]

    result = tool.run("write a hello world script")

    assert "final_output" in result
    assert result["agent_events"][0]["type"] == "thought"
    assert "Finished!" in result["final_output"]
