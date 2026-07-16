import pytest
import sys
import os
from unittest.mock import MagicMock, AsyncMock, patch

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pipecatapp')))

from tools.mcp_client_adapter import MCPClientAdapter

@pytest.mark.asyncio
async def test_mcp_client_adapter_lazy_loading_success():
    """Test that when mcp is successfully imported, execute runs successfully."""
    # Create mock ClientSession
    mock_session = AsyncMock()
    mock_tools_response = MagicMock()
    mock_tools_response.tools = [MagicMock(name="dummy_tool")]
    mock_tools_response.tools[0].name = "dummy_tool"
    mock_session.list_tools.return_value = mock_tools_response

    # Prepare response from calling a tool
    mock_call_result = MagicMock()
    mock_call_result.isError = False
    mock_text_content = MagicMock()
    mock_text_content.type = "text"
    mock_text_content.text = "Hello from MCP!"
    mock_call_result.content = [mock_text_content]
    mock_session.call_tool.return_value = mock_call_result

    # Mock the ClientSession and stdio_client classes/contexts
    # stdio_client(server_params) returns an async context manager
    mock_stdio_context = AsyncMock()
    mock_stdio_context.__aenter__.return_value = ("read_stream", "write_stream")
    mock_stdio_client = MagicMock(return_value=mock_stdio_context)

    # ClientSession(read, write) returns an async context manager whose __aenter__ returns mock_session
    mock_session_context = AsyncMock()
    mock_session_context.__aenter__.return_value = mock_session
    mock_client_session_cls = MagicMock(return_value=mock_session_context)

    with patch("mcp.client.stdio.stdio_client", mock_stdio_client), \
         patch("mcp.client.session.ClientSession", mock_client_session_cls):

        adapter = MCPClientAdapter(
            name="test_mcp",
            server_command="node",
            server_args=["server.js"]
        )

        result = await adapter.execute("dummy_tool", param="value")
        assert result == "Hello from MCP!"
        assert adapter._available_tools == {"dummy_tool"}


@pytest.mark.asyncio
async def test_mcp_client_adapter_missing_mcp_library():
    """Test that if the mcp library is missing, execute returns a graceful error instead of crashing."""
    adapter = MCPClientAdapter(
        name="test_mcp",
        server_command="node",
        server_args=["server.js"]
    )

    # Force ImportError by removing/mocking sys.modules to raise ImportError
    # We can patch builtins.__import__ to raise ImportError specifically for mcp
    import builtins
    original_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if "mcp" in name:
            raise ImportError("Mocked import error for mcp")
        return original_import(name, *args, **kwargs)

    with patch("builtins.__import__", mock_import):
        result = await adapter.execute("dummy_tool", param="value")
        assert "Error:" in result
        assert "missing" in result or "dependencies" in result
