import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import aiohttp

# Add repo root to sys.path to allow importing pipecatapp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pipecatapp.tools.ha_tool import HA_Tool

def test_init_success():
    with patch.dict(os.environ, {'HA_URL': 'http://ha', 'HA_TOKEN': 'token'}):
        tool = HA_Tool()
        assert tool.ha_url == 'http://ha'

def test_init_failure():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError):
            HA_Tool()

@pytest.mark.asyncio
async def test_call_ai_task_success():
    tool = HA_Tool("http://ha", "token")

    class MockAsyncResponse:
        def __init__(self):
            self.status = 200
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass
        def raise_for_status(self):
            pass

    with patch('aiohttp.ClientSession.post', return_value=MockAsyncResponse()):
        result = await tool.call_ai_task("turn on lights")
        assert "Successfully sent command" in result

@pytest.mark.asyncio
async def test_call_ai_task_failure():
    tool = HA_Tool("http://ha", "token")


    class MockAsyncSession:
        def post(self, *args, **kwargs):
            raise Exception("Error")

    with patch.object(tool, '_get_session', return_value=MockAsyncSession()):

        result = await tool.call_ai_task("turn on lights")
    assert "Error" in result
