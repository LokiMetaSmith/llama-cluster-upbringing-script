import pytest
import os
import tempfile
import asyncio
from pipecatapp.tools.ast_editor_tool import ASTEditorTool

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as td:
        yield td

@pytest.fixture
def ast_editor(temp_dir):
    return ASTEditorTool(root_dir=temp_dir)

@pytest.mark.asyncio
async def test_extract_function(ast_editor, temp_dir):
    source_file = os.path.join(temp_dir, "source.py")
    target_file = os.path.join(temp_dir, "target.py")

    with open(source_file, "w") as f:
        f.write("def foo():\n    print('foo')\n\n@decorator\ndef bar():\n    print('bar')\n\ndef baz():\n    pass\n")

    result = await ast_editor.execute(
        action="extract_function",
        filepath=source_file,
        func_name="bar",
        target_filepath=target_file
    )

    assert "Successfully extracted 'bar'" in result

    with open(source_file, "r") as f:
        source_content = f.read()

    # Assert bar is gone, foo and baz remain
    assert "def foo():" in source_content
    assert "def baz():" in source_content
    assert "def bar():" not in source_content
    assert "@decorator" not in source_content

    with open(target_file, "r") as f:
        target_content = f.read()

    # Assert bar is in target
    assert "@decorator\ndef bar():\n    print('bar')\n" in target_content

@pytest.mark.asyncio
async def test_rename_symbol(ast_editor, temp_dir):
    source_file = os.path.join(temp_dir, "rename_test.py")
    with open(source_file, "w") as f:
        f.write("def old_function():\n    pass\n\nold_function()\n")

    result = await ast_editor.execute(
        action="rename_symbol",
        filepath=source_file,
        old_name="old_function",
        new_name="new_function"
    )

    assert "Successfully renamed" in result

    with open(source_file, "r") as f:
        content = f.read()

    assert "def new_function():" in content
    assert "new_function()" in content
    assert "old_function" not in content

@pytest.mark.asyncio
async def test_add_import(ast_editor, temp_dir):
    source_file = os.path.join(temp_dir, "import_test.py")
    with open(source_file, "w") as f:
        f.write("\"\"\"Docstring\"\"\"\nimport os\n\ndef my_func():\n    pass\n")

    result = await ast_editor.execute(
        action="add_import",
        filepath=source_file,
        import_statement="import sys"
    )

    assert "Successfully added import" in result

    with open(source_file, "r") as f:
        content = f.read()

    assert "import sys" in content
    assert "\"\"\"Docstring\"\"\"" in content

    # Adding same import again
    result2 = await ast_editor.execute(
        action="add_import",
        filepath=source_file,
        import_statement="import sys"
    )
    assert "Import already exists" in result2

@pytest.mark.asyncio
async def test_invalid_syntax_aborts_edit(ast_editor, temp_dir):
    source_file = os.path.join(temp_dir, "invalid.py")
    # This file has valid syntax
    with open(source_file, "w") as f:
        f.write("def my_func():\n    pass\n")

    # Rename symbol to something invalid
    result = await ast_editor.execute(
        action="rename_symbol",
        filepath=source_file,
        old_name="my_func",
        new_name="123invalid"  # Invalid identifier
    )

    assert "Error: Renaming symbol resulted in invalid syntax" in result

    with open(source_file, "r") as f:
        content = f.read()

    # Content shouldn't have changed
    assert "def my_func():" in content
