import pytest
import sys
import os
from unittest.mock import MagicMock

# Mock heavy dependencies
sys.modules['extism'] = MagicMock()
sys.modules['torch'] = MagicMock()
sys.modules['fitz'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['paramiko'] = MagicMock()
sys.modules['llm_sandbox'] = MagicMock()
sys.modules['playwright'] = MagicMock()
sys.modules['playwright.async_api'] = MagicMock()
sys.modules['sentence_transformers'] = MagicMock()
sys.modules['langchain_community'] = MagicMock()
sys.modules['langchain'] = MagicMock()
sys.modules['langchain_openai'] = MagicMock()
sys.modules['langchain_core'] = MagicMock()
sys.modules['faiss'] = MagicMock()
sys.modules['chromadb'] = MagicMock()
sys.modules['git'] = MagicMock()
sys.modules['docker'] = MagicMock()
sys.modules['atproto'] = MagicMock()

from pipecatapp.skill_library import SkillLibrary
from pipecatapp.tools.set_operational_mode_tool import SetOperationalModeTool
from pipecatapp.tools.project_mapper_tool import ProjectMapperTool

@pytest.fixture
def skill_lib(tmp_path):
    db_path = tmp_path / "test_skills.sqlite"
    lib = SkillLibrary(db_path=str(db_path))
    return lib

def test_skill_ingestion_and_retrieval(skill_lib):
    skill_lib.save_skill("test_skill", "test desc", "test content")
    skill = skill_lib.get_skill("test_skill")
    assert skill["name"] == "test_skill"
    assert skill["description"] == "test desc"
    assert skill["content"] == "test content"

def test_set_operational_mode_tool(skill_lib, tmp_path):
    db_path = tmp_path / "test_skills.sqlite"
    skill_lib.save_skill("backpass", "backpass desc", "backpass content")

    tool = SetOperationalModeTool(db_path=str(db_path))
    result = tool.run("backpass")

    assert "MODE ACTIVATED: backpass" in result
    assert "backpass content" in result

def test_set_operational_mode_not_found(skill_lib, tmp_path):
    db_path = tmp_path / "test_skills.sqlite"
    tool = SetOperationalModeTool(db_path=str(db_path))
    result = tool.run("nonexistent")
    assert "Error: Mode 'nonexistent' not found" in result

def test_project_mapper_scan(tmp_path):
    # Create a dummy file
    (tmp_path / "dummy.py").write_text("import os\ndef hello(): pass")

    mapper = ProjectMapperTool(root_dir=str(tmp_path))
    result = mapper.scan(".")

    assert "root" in result
    assert "map_data" in result
    assert any(item["path"].endswith("dummy.py") for item in result["map_data"])
