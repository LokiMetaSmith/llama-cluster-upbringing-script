import pytest
import asyncio
import sys
from unittest.mock import MagicMock, patch

# Mock the OpenClawClient before importing
sys.modules['integrations'] = MagicMock()
sys.modules['integrations.openclaw'] = MagicMock()

from pipecatapp.tools.openclaw_tool import OpenClawTool

def test_openclaw_tool_initialization():
    with patch('pipecatapp.tools.openclaw_tool.OpenClawClient'):
        tool = OpenClawTool("http://mock")
        assert tool.name == "openclaw"

def test_send_message_success():
    with patch('pipecatapp.tools.openclaw_tool.OpenClawClient') as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        tool = OpenClawTool("http://mock")

        # In the test we need to mock the async functions properly
        async def mock_connect(): pass
        async def mock_send(*args, **kwargs): return {"ok": True, "payload": "Success"}

        tool.client.connect = mock_connect
        tool.client.send_message = mock_send

        res = asyncio.run(tool.send_message("target", "message"))
        assert "Message sent successfully" in res

def test_send_message_failure():
    with patch('pipecatapp.tools.openclaw_tool.OpenClawClient') as mock_client_class:
        tool = OpenClawTool("http://mock")

        async def mock_connect(): pass
        async def mock_send(*args, **kwargs): return {"ok": False, "error": "Bad target"}

        tool.client.connect = mock_connect
        tool.client.send_message = mock_send

        res = asyncio.run(tool.send_message("target", "message"))
        assert "Failed to send message" in res
        assert "Bad target" in res
