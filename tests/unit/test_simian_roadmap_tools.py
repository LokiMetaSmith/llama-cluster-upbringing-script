import os
import pytest
from pipecatapp.tools.git_coordination_tool import GitCoordinationTool
from pipecatapp.tools.skill_builder_tool import SkillBuilderTool
from pipecatapp.memory import MemoryStore

def test_git_coordination_tool(tmp_path):
    base_dir = str(tmp_path / "projects")
    tool = GitCoordinationTool(base_dir=base_dir)

    # Test writing artifact
    res_write = tool.execute(project="test_proj", artifact="PLAN", action="write", content="# Plan Header\n1. Step One")
    assert "Successfully updated" in res_write

    # Test reading artifact
    res_read = tool.execute(project="test_proj", artifact="PLAN", action="read")
    assert "# Plan Header" in res_read
    assert "Step One" in res_read

    # Test appending artifact
    res_append = tool.execute(project="test_proj", artifact="PLAN", action="append", content="2. Step Two")
    assert "Successfully updated" in res_append

    res_read_after = tool.execute(project="test_proj", artifact="PLAN", action="read")
    assert "2. Step Two" in res_read_after

def test_skill_builder_governed_skill(mocker):
    mock_memory = mocker.MagicMock()
    mock_memory.get_skill.side_effect = lambda name: {
        "code-reviewer/SKILL": {"content": "Execute tasks under strict evidence criteria"},
        "code-reviewer/SPEC": {"content": "Review code against security rules"},
        "code-reviewer/EVAL": {"content": "Pytest log showing 100% pass"}
    }.get(name)

    builder = SkillBuilderTool(memory_store=mock_memory)

    res = builder.execute(
        action="scaffold_governed_skill",
        name="code-reviewer",
        description="Inspects PR diffs and evaluates complexity.",
        intent="Review code against security rules.",
        evidence="Pytest log showing 100% pass."
    )
    assert "successfully scaffolded" in res
    assert mock_memory.save_skill.call_count == 3

    skill_doc = mock_memory.get_skill("code-reviewer/SKILL")
    assert skill_doc is not None
    assert "Execute tasks under strict evidence criteria" in skill_doc["content"]

    spec_doc = mock_memory.get_skill("code-reviewer/SPEC")
    assert spec_doc is not None
    assert "Review code against security rules" in spec_doc["content"]

    eval_doc = mock_memory.get_skill("code-reviewer/EVAL")
    assert eval_doc is not None
    assert "Pytest log showing 100% pass" in eval_doc["content"]
