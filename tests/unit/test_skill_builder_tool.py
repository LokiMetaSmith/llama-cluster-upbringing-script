import pytest
import json
import sys
from unittest.mock import MagicMock

# Mock memory dependencies to avoid cryptography requirement
sys.modules['pipecatapp.memory'] = MagicMock()

from pipecatapp.tools.skill_builder_tool import SkillBuilderTool

def test_skill_builder_tool_initialization():
    mock_memory = MagicMock()
    tool = SkillBuilderTool(memory_store=mock_memory)
    assert tool.memory_store == mock_memory

def test_execute_create():
    mock_memory = MagicMock()
    tool = SkillBuilderTool(memory_store=mock_memory)

    res = tool.execute("create", name="skill", description="desc", content="code")
    assert "successfully created" in res
    mock_memory.save_skill.assert_called_with("skill", "desc", "code")

def test_execute_create_missing_params():
    mock_memory = MagicMock()
    tool = SkillBuilderTool(memory_store=mock_memory)
    res = tool.execute("create", name="skill")
    assert "Error" in res

def test_execute_read():
    mock_memory = MagicMock()
    mock_memory.get_skill.return_value = {"name": "skill"}
    tool = SkillBuilderTool(memory_store=mock_memory)

    res = tool.execute("read", name="skill")
    res_json = json.loads(res)
    assert res_json["name"] == "skill"
    mock_memory.get_skill.assert_called_with("skill")

def test_execute_read_not_found():
    mock_memory = MagicMock()
    mock_memory.get_skill.return_value = None
    tool = SkillBuilderTool(memory_store=mock_memory)

    res = tool.execute("read", name="missing")
    assert "not found" in res

def test_execute_list():
    mock_memory = MagicMock()
    mock_memory.list_skills.return_value = [{"name": "skill1"}]
    tool = SkillBuilderTool(memory_store=mock_memory)

    res = tool.execute("list")
    res_json = json.loads(res)
    assert len(res_json) == 1
    assert res_json[0]["name"] == "skill1"

def test_execute_delete():
    mock_memory = MagicMock()
    mock_memory.delete_skill.return_value = True
    tool = SkillBuilderTool(memory_store=mock_memory)

    res = tool.execute("delete", name="skill")
    assert "deleted successfully" in res
    mock_memory.delete_skill.assert_called_with("skill")

def test_execute_delete_not_found():
    mock_memory = MagicMock()
    mock_memory.delete_skill.return_value = False
    tool = SkillBuilderTool(memory_store=mock_memory)

    res = tool.execute("delete", name="skill")
    assert "not found" in res

def test_execute_unknown_action():
    tool = SkillBuilderTool(memory_store=MagicMock())
    res = tool.execute("unknown")
    assert "Unknown action" in res
