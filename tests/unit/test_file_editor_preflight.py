import pytest
import os
import asyncio
import tempfile
from pipecatapp.tools.file_editor_tool import FileEditorTool
from pipecatapp.tools.code_graph_tool import CodeGraphTool

@pytest.fixture
def temp_workspace():
    with tempfile.TemporaryDirectory() as tmpdir:
        src_file = os.path.join(tmpdir, "main.py")
        with open(src_file, "w", encoding="utf-8") as f:
            f.write('''def helper_func():
    return 42

def run():
    return helper_func()
''')
        cg_tool = CodeGraphTool(root_dir=tmpdir)
        fe_tool = FileEditorTool(root_dir=tmpdir, code_graph_tool=cg_tool)
        yield fe_tool, tmpdir

def test_write_with_preflight(temp_workspace):
    fe_tool, tmpdir = temp_workspace
    res = asyncio.run(fe_tool.execute(
        action="write",
        filepath="main.py",
        content="def helper_func():\n    return 100\n",
        verify_preflight=True
    ))
    assert "=== Preflight Edit Checklist ===" in res
    assert "Successfully wrote to main.py" in res

def test_patch_with_preflight(temp_workspace):
    fe_tool, tmpdir = temp_workspace
    res = asyncio.run(fe_tool.execute(
        action="patch",
        filepath="main.py",
        search_block="return 42",
        replace_block="return 99",
        verify_preflight=True
    ))
    assert "=== Preflight Edit Checklist ===" in res
    assert "Successfully patched main.py" in res
