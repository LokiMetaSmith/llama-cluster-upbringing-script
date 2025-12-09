import pytest
import sys
import os
from unittest.mock import MagicMock, patch, AsyncMock

# To handle relative imports (from .mcp_tool import MCP_Tool), we need to import
# archivist_tool as part of a package.
# We add the parent directory of 'tools' to sys.path.
tools_parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files'))
if tools_parent_dir not in sys.path:
    sys.path.insert(0, tools_parent_dir)

# Now we can import from tools.archivist_tool
from tools.archivist_tool import ArchivistTool

@pytest.mark.asyncio
async def test_archivist_tool_initialization():
    tool = ArchivistTool(archivist_url="http://test:1234")
    assert tool.name == "archivist"
    assert tool.archivist_url == "http://test:1234"

@pytest.mark.asyncio
async def test_run_success():
    tool = ArchivistTool()
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {"content": "Found some history."}

    # Mock aiohttp.ClientSession
    with patch('aiohttp.ClientSession') as MockSession:
        mock_session_instance = MockSession.return_value
        # Async context manager support (__aenter__ and __aexit__)
        mock_session_instance.__aenter__.return_value = mock_session_instance
        mock_session_instance.__aexit__.return_value = None

        mock_post = mock_session_instance.post.return_value
        mock_post.__aenter__.return_value = mock_response
        mock_post.__aexit__.return_value = None

        result = await tool.run("test query")
        assert result == "Found some history."

@pytest.mark.asyncio
async def test_run_error_status():
    tool = ArchivistTool()
    mock_response = AsyncMock()
    mock_response.status = 500
    mock_response.text.return_value = "Internal Server Error"

    with patch('aiohttp.ClientSession') as MockSession:
        mock_session_instance = MockSession.return_value
        mock_session_instance.__aenter__.return_value = mock_session_instance
        mock_session_instance.__aexit__.return_value = None

        mock_post = mock_session_instance.post.return_value
        mock_post.__aenter__.return_value = mock_response
        mock_post.__aexit__.return_value = None

        result = await tool.run("test query")
        assert "Error querying Archivist: 500" in result
        assert "Internal Server Error" in result

@pytest.mark.asyncio
async def test_run_connection_failure():
    tool = ArchivistTool()
    # Mocking the __aenter__ to raise an exception simulates a connection error during session creation or usage
    with patch('aiohttp.ClientSession') as MockSession:
        mock_session_instance = MockSession.return_value
        mock_session_instance.__aenter__.side_effect = Exception("Connection refused")

        result = await tool.run("test query")
        assert "Failed to connect to Archivist service" in result
