import os
import sqlite3
import pytest
from pipecatapp.skill_library import SkillLibrary
from pipecatapp.tools.save_skill_tool import SaveSkillTool
from pipecatapp.tools.search_skills_tool import SearchSkillsTool

@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_skills.sqlite"
    return str(db_file)

def test_skill_library_save_and_retrieve(temp_db):
    lib = SkillLibrary(db_path=temp_db)
    success = lib.save_skill("test_skill", "A test description", "print('hello world')")
    assert success is True

    skill = lib.get_skill("test_skill")
    assert skill is not None
    assert skill["name"] == "test_skill"
    assert skill["description"] == "A test description"
    assert skill["content"] == "print('hello world')"

def test_skill_library_update(temp_db):
    lib = SkillLibrary(db_path=temp_db)
    lib.save_skill("test_skill", "A test description", "print('hello world')")
    lib.save_skill("test_skill", "An updated description", "print('hello updated')")

    skill = lib.get_skill("test_skill")
    assert skill["description"] == "An updated description"
    assert skill["content"] == "print('hello updated')"

def test_skill_library_search(temp_db):
    lib = SkillLibrary(db_path=temp_db)
    lib.save_skill("docker_deploy", "Deploy docker", "docker compose up")
    lib.save_skill("python_script", "Run python", "python main.py")

    results = lib.search_skills("docker")
    assert len(results) == 1
    assert results[0]["name"] == "docker_deploy"

    results = lib.search_skills("run")
    assert len(results) == 1
    assert results[0]["name"] == "python_script"

def test_save_skill_tool(temp_db):
    tool = SaveSkillTool(db_path=temp_db)
    result = tool.run("my_skill", "my desc", "my content")
    assert "Successfully saved" in result

def test_search_skills_tool(temp_db):
    save_tool = SaveSkillTool(db_path=temp_db)
    save_tool.run("docker_nginx", "how to docker nginx", "docker run nginx")

    search_tool = SearchSkillsTool(db_path=temp_db)
    result = search_tool.run("nginx")
    assert "Found 1 skill(s)" in result
    assert "docker_nginx" in result

    result_none = search_tool.run("apache")
    assert "No skills found" in result_none
