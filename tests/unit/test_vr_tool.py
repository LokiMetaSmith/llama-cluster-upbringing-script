import pytest
import asyncio
import sys
from unittest.mock import MagicMock, patch

from pipecatapp.tools.vr_tool import VRTool

def test_vr_tool_initialization():
    tool = VRTool()
    assert "Main" in tool.available_rooms

def test_vr_tool_get_def():
    tool = VRTool()
    definition = tool.get_tool_def()
    assert definition["type"] == "function"
    assert definition["function"]["name"] == "vr_navigate"

def test_execute_invalid_room():
    tool = VRTool()
    res = asyncio.run(tool.execute("Invalid Room"))
    assert "Error: Room 'Invalid Room' not found" in res

def test_execute_success():
    tool = VRTool()

    mock_web_server = MagicMock()
    mock_web_server.manager = MagicMock()

    async def mock_broadcast(msg): pass
    mock_web_server.manager.broadcast = mock_broadcast

    with patch.dict(sys.modules, {'web_server': mock_web_server}):
        res = asyncio.run(tool.execute("Main"))
        assert "Navigating user to Main" in res

def test_execute_failure():
    tool = VRTool()

    mock_web_server = MagicMock()
    mock_web_server.manager = MagicMock()

    async def mock_broadcast(msg): raise Exception("Network error")
    mock_web_server.manager.broadcast = mock_broadcast

    with patch.dict(sys.modules, {'web_server': mock_web_server}):
        res = asyncio.run(tool.execute("Main"))
        assert "Failed to send navigation command" in res
