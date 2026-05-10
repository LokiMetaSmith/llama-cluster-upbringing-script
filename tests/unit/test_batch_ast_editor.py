import pytest
import os
import asyncio
from pipecatapp.tools.ast_editor_tool import ASTEditorTool

@pytest.fixture
def temp_dir(tmpdir):
    return str(tmpdir)

@pytest.fixture
def ast_editor(temp_dir):
    return ASTEditorTool(root_dir=temp_dir)

@pytest.mark.asyncio
async def test_batch_edit(ast_editor, temp_dir):
    file1_path = os.path.join(temp_dir, "file1.py")
    file2_path = os.path.join(temp_dir, "file2.py")

    with open(file1_path, "w") as f:
        f.write("def foo():\n    pass\n")

    with open(file2_path, "w") as f:
        f.write("print('hello')\n")

    batch_operations = [
        {
            "action": "rename_symbol",
            "filepath": "file1.py",
            "old_name": "foo",
            "new_name": "bar"
        },
        {
            "action": "add_import",
            "filepath": "file2.py",
            "import_statement": "import os"
        }
    ]

    result = await ast_editor.execute("batch_edit", batch_operations=batch_operations)

    with open(file1_path, "r") as f:
        c1 = f.read()
    assert "def bar():" in c1

    with open(file2_path, "r") as f:
        c2 = f.read()
    assert "import os" in c2
