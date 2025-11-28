import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from smol_agent_tool import SmolAgentTool

@pytest.fixture
def smol_tool():
    return SmolAgentTool()

@patch('smol_agent_tool.shutil.which')
@patch('smol_agent_tool.LiteLLMModel')
@patch('smol_agent_tool.CodeAgent')
def test_run_success(mock_agent_cls, mock_model_cls, mock_which, smol_tool):
    mock_which.return_value = "/usr/bin/deno"

    mock_agent = mock_agent_cls.return_value
    # Mock memory with escaped newlines as expected by the tool
    mock_agent.memory = [
        {"role": "user", "content": "task"},
        {"role": "assistant", "content": "```python\\nprint('hello')\\n```"}
    ]

    with patch.object(smol_tool, '_execute_in_sandbox', return_value="Output: hello") as mock_exec:
        result = smol_tool.run("task description")

        assert result == "Output: hello"
        # The extracted code will have \\n if split worked on \\n
        mock_exec.assert_called_once_with("print('hello')\\n")

@patch('smol_agent_tool.shutil.which')
def test_deno_missing(mock_which, smol_tool):
    mock_which.return_value = None
    result = smol_tool.run("task")
    assert "Error: A required dependency is missing" in result

def test_empty_task(smol_tool):
    result = smol_tool.run("")
    assert "Error: Task description must be a non-empty string." in result
