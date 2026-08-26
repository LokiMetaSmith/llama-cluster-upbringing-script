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

    with patch.dict(sys.modules, {'pipecatapp.web_server': mock_web_server, 'web_server': mock_web_server}):
        res = asyncio.run(tool.execute("Main"))
        assert "Navigating user to Main" in res

def test_execute_failure():
    tool = VRTool()

    mock_web_server = MagicMock()
    mock_web_server.manager = MagicMock()

    async def mock_broadcast(msg): raise Exception("Network error")
    mock_web_server.manager.broadcast = mock_broadcast

    with patch.dict(sys.modules, {'pipecatapp.web_server': mock_web_server, 'web_server': mock_web_server}):
        res = asyncio.run(tool.execute("Main"))
        assert "Failed to send navigation command" in res

def test_vr_spatial_mapping_and_trajectories():
    tool = VRTool()
    node_ids = ["node1", "node2", "node3", "node4"]
    grid = tool.compute_spatial_grid(node_ids)
    assert len(grid) == 4
    assert "node1" in grid
    assert "x" in grid["node1"] and "y" in grid["node1"] and "z" in grid["node1"]

    trajectory = tool.emit_signal_trajectory("node1", "node2", "polyphony_baton")
    assert trajectory["type"] == "signal_trajectory"
    assert trajectory["signal_type"] == "polyphony_baton"
    assert trajectory["source"]["agent_id"] == "node1"
    assert trajectory["target"]["agent_id"] == "node2"
