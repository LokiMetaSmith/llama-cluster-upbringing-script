import pytest
from unittest.mock import MagicMock, patch
from pipecatapp.tools.save_skill_tool import SaveSkillTool

def test_save_skill_tool_initialization():
    with patch("pipecatapp.tools.save_skill_tool.SkillLibrary"):
        tool = SaveSkillTool()
        assert tool.name == "save_skill"
        assert "name" in tool.input_schema["properties"]

def test_save_skill_success():
    with patch("pipecatapp.tools.save_skill_tool.SkillLibrary") as MockLib:
        mock_lib = MagicMock()
        mock_lib.save_skill.return_value = True
        MockLib.return_value = mock_lib

        tool = SaveSkillTool()
        res = tool.run("my_skill", "desc", "content")

        assert "Successfully saved skill" in res
        mock_lib.save_skill.assert_called_with("my_skill", "desc", "content")

def test_save_skill_failure():
    with patch("pipecatapp.tools.save_skill_tool.SkillLibrary") as MockLib:
        mock_lib = MagicMock()
        mock_lib.save_skill.return_value = False
        MockLib.return_value = mock_lib

        tool = SaveSkillTool()
        res = tool.run("my_skill", "desc", "content")

        assert "Failed to save skill" in res
        mock_lib.save_skill.assert_called_with("my_skill", "desc", "content")
