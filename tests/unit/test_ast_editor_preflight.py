import pytest
from unittest.mock import MagicMock
import os
import json
from pipecatapp.tools.ast_editor_tool import ASTEditorTool

@pytest.fixture
def mock_code_graph_tool():
    mock_tool = MagicMock()
    mock_tool.preflight.return_value = "=== Preflight Edit Checklist ===\nMock Preflight"
    mock_tool.repository_tests.return_value = "=== Connected Repository Tests ===\nMock Test"
    return mock_tool

@pytest.fixture
def ast_editor(mock_code_graph_tool):
    return ASTEditorTool(root_dir="/opt/pipecatapp", code_graph_tool=mock_code_graph_tool)

@pytest.mark.asyncio
async def test_ast_editor_preflight_on_write(ast_editor, mock_code_graph_tool):
    ast_editor.extract_function = MagicMock(return_value="Successfully extracted")

    res = await ast_editor.execute(action="extract_function", filepath="test.py", func_name="test_func", target_filepath="test_dest.py", verify_preflight=True)

    assert "Mock Preflight" in res
    assert "Mock Test" in res
    mock_code_graph_tool.preflight.assert_called_once_with(filepath="test.py")
    mock_code_graph_tool.repository_tests.assert_called_once_with(filepath="test.py")

@pytest.mark.asyncio
async def test_ast_editor_no_preflight(ast_editor, mock_code_graph_tool):
    ast_editor.extract_function = MagicMock(return_value="Successfully extracted")

    res = await ast_editor.execute(action="extract_function", filepath="test.py", func_name="test_func", target_filepath="test_dest.py", verify_preflight=False)

    assert "Mock Preflight" not in res
    assert "Mock Test" not in res
    mock_code_graph_tool.preflight.assert_not_called()
    mock_code_graph_tool.repository_tests.assert_not_called()
