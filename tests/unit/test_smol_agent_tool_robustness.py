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
def test_regex_variations(mock_agent_cls, mock_model_cls, mock_which, smol_tool):
    mock_which.return_value = "/usr/bin/deno"
    mock_agent = mock_agent_cls.return_value

    # Test case: code block with 'py'
    mock_agent.memory = [
        {"role": "user", "content": "task"},
        {"role": "assistant", "content": "```py\nprint('py')\n```"}
    ]
    with patch.object(smol_tool, '_execute_in_sandbox', return_value="Output: py") as mock_exec:
        result = smol_tool.run("task")
        mock_exec.assert_called_with("print('py')")

    # Test case: code block with 'PYTHON' (case insensitive)
    mock_agent.memory = [
        {"role": "user", "content": "task"},
        {"role": "assistant", "content": "```PYTHON\nprint('PYTHON')\n```"}
    ]
    with patch.object(smol_tool, '_execute_in_sandbox', return_value="Output: PYTHON") as mock_exec:
        result = smol_tool.run("task")
        mock_exec.assert_called_with("print('PYTHON')")

@patch('smol_agent_tool.shutil.which')
@patch('smol_agent_tool.LiteLLMModel')
@patch('smol_agent_tool.CodeAgent')
def test_syntax_validation(mock_agent_cls, mock_model_cls, mock_which, smol_tool):
    """Test that invalid python syntax is caught before execution."""
    mock_which.return_value = "/usr/bin/deno"
    mock_agent = mock_agent_cls.return_value

    # Test case: invalid python syntax (missing closing parenthesis)
    mock_agent.memory = [
        {"role": "user", "content": "task"},
        {"role": "assistant", "content": "```python\nprint('hello'\n```"}
    ]

    with patch.object(smol_tool, '_execute_in_sandbox', return_value="Success") as mock_exec:
        result = smol_tool.run("task")

        # Verify that the result contains a syntax error message
        assert "Error: The generated code has a syntax error" in result

        # Verify that _execute_in_sandbox was NOT called
        mock_exec.assert_not_called()
