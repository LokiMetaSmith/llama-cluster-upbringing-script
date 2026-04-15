import pytest
from unittest.mock import MagicMock, patch
from pipecatapp.tools.search_skills_tool import SearchSkillsTool

def test_search_skills_tool_initialization():
    with patch("pipecatapp.tools.search_skills_tool.SkillLibrary"):
        tool = SearchSkillsTool()
        assert tool.name == "search_skills"
        assert "query" in tool.input_schema["properties"]

def test_search_skills_run_success():
    with patch("pipecatapp.tools.search_skills_tool.SkillLibrary") as MockLib:
        mock_lib = MagicMock()
        mock_lib.search_skills.return_value = [{"name": "skill1", "description": "desc1", "content": "cont1"}]
        MockLib.return_value = mock_lib

        tool = SearchSkillsTool()
        res = tool.run("query")

        assert "skill1" in res
        assert "desc1" in res
        assert "cont1" in res
        mock_lib.search_skills.assert_called_with("query")

def test_search_skills_run_empty():
    with patch("pipecatapp.tools.search_skills_tool.SkillLibrary") as MockLib:
        mock_lib = MagicMock()
        mock_lib.search_skills.return_value = []
        MockLib.return_value = mock_lib

        tool = SearchSkillsTool()
        res = tool.run("query")

        assert "No skills found" in res
