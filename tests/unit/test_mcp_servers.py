import pytest
import sys
import os
from unittest.mock import patch

from mcp.server.fastmcp import FastMCP

@pytest.mark.asyncio
async def test_file_editor_server():
    from pipecatapp.servers.file_editor_server import mcp as file_editor_mcp
    tools = [t.name for t in await file_editor_mcp.list_tools()]
    expected_tools = ["read_file", "write_file", "apply_patch", "apply_hash_edits", "undo_edit", "append_to_file", "flag_megafile"]
    for tool in expected_tools:
        assert tool in tools

@pytest.mark.asyncio
async def test_code_runner_server():
    from pipecatapp.servers.code_runner_server import mcp as code_runner_mcp
    tools = [t.name for t in await code_runner_mcp.list_tools()]
    expected_tools = ["run_python_code", "run_code_in_sandbox", "run_interactive_python"]
    for tool in expected_tools:
        assert tool in tools

@pytest.mark.asyncio
async def test_document_server():
    with patch('os.path.exists', return_value=True):
        from pipecatapp.servers.document_server import mcp as document_mcp
        tools = [t.name for t in await document_mcp.list_tools()]
        expected_tools = ["search", "get_text", "add_bookmark", "list_bookmarks"]
        for tool in expected_tools:
            assert tool in tools

@pytest.mark.asyncio
async def test_rag_server():
    from pipecatapp.servers.rag_server import mcp as rag_mcp
    tools = [t.name for t in await rag_mcp.list_tools()]
    expected_tools = ["scan_directory", "search", "add_document", "search_knowledge_base", "set_scope"]
    for tool in expected_tools:
        assert tool in tools
