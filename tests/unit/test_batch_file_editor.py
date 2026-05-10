import pytest
import os
import asyncio
from pipecatapp.tools.file_editor_tool import FileEditorTool
from pipecatapp.utils.file_utils import calculate_line_hash

@pytest.fixture
def temp_dir(tmpdir):
    return str(tmpdir)

@pytest.fixture
def file_editor(temp_dir):
    return FileEditorTool(root_dir=temp_dir)

@pytest.mark.asyncio
async def test_batch_hash_replace(file_editor, temp_dir):
    file1_path = os.path.join(temp_dir, "file1.txt")
    file2_path = os.path.join(temp_dir, "file2.txt")

    with open(file1_path, "w") as f:
        f.write("line 1\nline 2\nline 3")

    with open(file2_path, "w") as f:
        f.write("apple\nbanana\ncherry")

    h1 = calculate_line_hash("line 2")
    h2 = calculate_line_hash("banana")

    batch_edits = [
        {
            "filepath": "file1.txt",
            "edits": [
                {"type": "replace", "id": f"2:{h1}", "content": "replaced 2"}
            ]
        },
        {
            "filepath": "file2.txt",
            "edits": [
                {"type": "replace", "id": f"2:{h2}", "content": "orange"}
            ]
        }
    ]

    result = await file_editor.execute("batch_hash_replace", batch_edits=batch_edits)

    with open(file1_path, "r") as f:
        c1 = f.read()
    assert "replaced 2" in c1

    with open(file2_path, "r") as f:
        c2 = f.read()
    assert "orange" in c2
