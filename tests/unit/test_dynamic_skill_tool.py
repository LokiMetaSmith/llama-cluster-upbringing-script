import pytest
from unittest.mock import MagicMock
from pipecatapp.tools.dynamic_skill_tool import DynamicSkillTool

def test_dynamic_skill_tool_initialization():
    tool = DynamicSkillTool("name", "desc", "content", None)
    assert tool.name == "name"

def test_execute_no_code_runner():
    tool = DynamicSkillTool("name", "desc", "content", None)
    res = tool.execute("{}")
    assert "No CodeRunnerTool" in res

def test_execute_no_python_blocks():
    mock_runner = MagicMock()
    tool = DynamicSkillTool("name", "desc", "No code here", mock_runner)
    res = tool.execute("{}")
    assert "knowledge mode" in res

def test_execute_with_python_blocks():
    mock_runner = MagicMock()
    mock_runner.execute.return_value = "Success"

    content = "```python\nprint('Hello')\n```"
    tool = DynamicSkillTool("name", "desc", content, mock_runner)

    res = tool.execute('{"key": "value"}')
    assert res == "Success"
    mock_runner.execute.assert_called_once()

    # Check that PARAMS was injected
    args, kwargs = mock_runner.execute.call_args
    assert "PARAMS" in kwargs["code"]
    assert "print('Hello')" in kwargs["code"]
