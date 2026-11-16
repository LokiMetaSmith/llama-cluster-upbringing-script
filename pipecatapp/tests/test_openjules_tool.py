import asyncio
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from pipecatapp.tools.openjules_tool import OpenJulesTool

def test_openjules_tool_schema_and_info():
    tool = OpenJulesTool()
    schema = tool.get_schema()
    assert schema["type"] == "function"
    assert schema["function"]["name"] == "openjules"
    assert "submit_task" in schema["function"]["parameters"]["properties"]["action"]["enum"]

    info = tool.get_info()
    assert info["name"] == "openjules"

def test_openjules_tool_ssrf_validation():
    tool = OpenJulesTool()
    assert tool._validate_url("http://127.0.0.1:8000") is True
    assert tool._validate_url("https://github.com") is True
    assert tool._validate_url("http://169.254.169.254") is False
    assert tool._validate_url("http://metadata.google.internal") is False
    assert tool._validate_url("ftp://example.com") is False
    assert tool._validate_url("invalid-url") is False

def test_openjules_tool_async_execution():
    async def _test():
        tool = OpenJulesTool(base_url="http://127.0.0.1:8000")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"status": "ok"}'

        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get, \
             patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_get.return_value = mock_response
            mock_post.return_value = mock_response

            # Health
            res = await tool.execute_async("health")
            assert "Health: 200" in res

            # Capabilities
            res = await tool.execute_async("capabilities", repository="example/repo")
            assert '{"status": "ok"}' in res

            # Submit task
            res = await tool.execute_async("submit_task", task="Fix bug in foo.py", repository="example/repo")
            assert "OpenJules task successfully submitted" in res

            # Observe worker
            res = await tool.execute_async("observe_worker", worker_id="worker-01")
            assert '{"status": "ok"}' in res

            # Drain worker
            res = await tool.execute_async("drain_worker", worker_id="worker-01")
            assert "Drain worker worker-01: 200" in res

            # Stop worker
            res = await tool.execute_async("stop_worker", worker_id="worker-01")
            assert "Stop worker worker-01: 200" in res

    asyncio.run(_test())

def test_openjules_tool_validation_errors():
    async def _test():
        tool = OpenJulesTool(base_url="http://127.0.0.1:8000")
        assert "required" in await tool.execute_async("submit_task")
        assert "required" in await tool.execute_async("observe_worker")
        assert "required" in await tool.execute_async("drain_worker")
        assert "required" in await tool.execute_async("stop_worker")
        assert "Unknown action" in await tool.execute_async("fake_action")

    asyncio.run(_test())

def test_openjules_sync_execute_wrapper():
    tool = OpenJulesTool(base_url="http://127.0.0.1:8000")
    with patch.object(tool, "execute_async", new_callable=AsyncMock) as mock_async:
        mock_async.return_value = "Mocked Result"
        res = tool.execute("health")
        assert res == "Mocked Result"
