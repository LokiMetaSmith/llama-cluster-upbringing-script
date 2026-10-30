import pytest
from unittest.mock import MagicMock
from pipecatapp.tools.file_editor_tool import FileEditorTool

@pytest.fixture
def mock_code_graph_tool():
    mock_tool = MagicMock()
    mock_tool.preflight.return_value = "=== Preflight Edit Checklist ===\nMock Preflight"
    mock_tool.repository_tests.return_value = "=== Connected Repository Tests ===\nMock Test"
    return mock_tool

@pytest.fixture
def file_editor(mock_code_graph_tool):
    return FileEditorTool(root_dir="/opt/pipecatapp", code_graph_tool=mock_code_graph_tool)

@pytest.mark.asyncio
async def test_file_editor_preflight_on_write(file_editor, mock_code_graph_tool):
    file_editor.write_file = MagicMock(return_value="Successfully wrote")

    res = await file_editor.execute(action="write", filepath="test.py", content="print('hello')", verify_preflight=True)

    assert "Mock Preflight" in res
    assert "Mock Test" in res
    mock_code_graph_tool.preflight.assert_called_once_with(filepath="test.py")
    mock_code_graph_tool.repository_tests.assert_called_once_with(filepath="test.py")

@pytest.mark.asyncio
async def test_file_editor_no_preflight(file_editor, mock_code_graph_tool):
    file_editor.write_file = MagicMock(return_value="Successfully wrote")

    res = await file_editor.execute(action="write", filepath="test.py", content="print('hello')", verify_preflight=False)

    assert "Mock Preflight" not in res
    assert "Mock Test" not in res
    mock_code_graph_tool.preflight.assert_not_called()
    mock_code_graph_tool.repository_tests.assert_not_called()
