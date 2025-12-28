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
    # Mock memory with proper newlines
    mock_agent.memory = [
        {"role": "user", "content": "task"},
        {"role": "assistant", "content": "```python\nprint('hello')\n```"}
    ]

    with patch.object(smol_tool, '_execute_in_sandbox', return_value="Output: hello") as mock_exec:
        result = smol_tool.run("task description")

        assert result == "Output: hello"
        # The extracted code should be just the code
        mock_exec.assert_called_once_with("print('hello')")

@patch('smol_agent_tool.shutil.which')
@patch('smol_agent_tool.LiteLLMModel')
@patch('smol_agent_tool.CodeAgent')
def test_run_multiple_code_blocks(mock_agent_cls, mock_model_cls, mock_which, smol_tool):
    mock_which.return_value = "/usr/bin/deno"

    mock_agent = mock_agent_cls.return_value
    # Mock memory with multiple code blocks in one message
    mock_agent.memory = [
        {"role": "user", "content": "task"},
        {"role": "assistant", "content": "Here is step 1:\n```python\nvar1 = 10\n```\nAnd step 2:\n```python\nprint(var1 * 2)\n```"}
    ]

    with patch.object(smol_tool, '_execute_in_sandbox', return_value="Output: 20") as mock_exec:
        result = smol_tool.run("task description")

        assert result == "Output: 20"
        # The extracted code should be the concatenation of both blocks
        mock_exec.assert_called_once_with("var1 = 10\nprint(var1 * 2)")

@patch('smol_agent_tool.shutil.which')
def test_deno_missing(mock_which, smol_tool):
    mock_which.return_value = None
    result = smol_tool.run("task")
    assert "Error: A required dependency is missing" in result

def test_empty_task(smol_tool):
    result = smol_tool.run("")
    assert "Error: Task description must be a non-empty string." in result

@patch('smol_agent_tool.shutil.which')
@patch('smol_agent_tool.LiteLLMModel')
@patch('smol_agent_tool.CodeAgent')
def test_run_py_language_specifier(mock_agent_cls, mock_model_cls, mock_which, smol_tool):
    """Test that the 'py' language specifier is handled correctly."""
    mock_which.return_value = "/usr/bin/deno"
    mock_agent = mock_agent_cls.return_value
    mock_agent.memory = [{"role": "assistant", "content": "```py\nprint('py specifier')\n```"}]

    with patch.object(smol_tool, '_execute_in_sandbox', return_value="Output: py specifier") as mock_exec:
        result = smol_tool.run("task description")
        assert result == "Output: py specifier"
        mock_exec.assert_called_once_with("print('py specifier')")

@patch('smol_agent_tool.shutil.which')
@patch('smol_agent_tool.LiteLLMModel')
@patch('smol_agent_tool.CodeAgent')
def test_run_no_language_specifier(mock_agent_cls, mock_model_cls, mock_which, smol_tool):
    """Test that code blocks with no language specifier are handled."""
    mock_which.return_value = "/usr/bin/deno"
    mock_agent = mock_agent_cls.return_value
    mock_agent.memory = [{"role": "assistant", "content": "```\nprint('no specifier')\n```"}]

    with patch.object(smol_tool, '_execute_in_sandbox', return_value="Output: no specifier") as mock_exec:
        result = smol_tool.run("task description")
        assert result == "Output: no specifier"
        mock_exec.assert_called_once_with("print('no specifier')")
