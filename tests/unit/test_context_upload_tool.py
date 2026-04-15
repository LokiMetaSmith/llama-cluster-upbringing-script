import pytest
import os
import asyncio
from unittest.mock import patch, mock_open
from pipecatapp.tools.context_upload_tool import ContextUploadTool

def test_context_upload_tool_initialization():
    tool = ContextUploadTool()
    assert tool.sandbox_dir == os.path.realpath("/tmp/pipecat_context")

def test_context_upload_tool_get_definition():
    tool = ContextUploadTool()
    definition = tool.get_definition()
    assert definition["type"] == "function"
    assert definition["function"]["name"] == "upload_context"

def test_context_upload_tool_execute_missing_args():
    tool = ContextUploadTool()
    res = asyncio.run(tool.execute("", "filename"))
    assert "Error:" in res

@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_context_upload_tool_execute_success(mock_makedirs, mock_file):
    tool = ContextUploadTool()
    res = asyncio.run(tool.execute("content", "test.txt"))
    assert "Successfully saved context" in res
    mock_file.assert_called_with(os.path.join(tool.sandbox_dir, "test.txt"), "w", encoding="utf-8")
