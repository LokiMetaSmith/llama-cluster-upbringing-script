import pytest
import json
import os
from unittest.mock import MagicMock, AsyncMock, patch
from ansible.roles.pipecatapp.files.tools.planner_tool import PlannerTool

@pytest.fixture
def mock_twin_service():
    service = MagicMock()
    service.tools = {}
    service.router_llm = MagicMock()
    service.router_llm._client.base_url = "http://mock-llm:8000/v1"
    # Important: explicit None for attributes we test fallback on
    service.llm_base_url = None
    service.app_config = {}
    service.consul_http_addr = "http://localhost:8500"
    return service

@pytest.fixture
def planner_tool(mock_twin_service):
    return PlannerTool(mock_twin_service)

@pytest.mark.asyncio
async def test_discover_llm_url_router_llm(planner_tool):
    url = await planner_tool._discover_llm_url()
    assert url == "http://mock-llm:8000/v1"

@pytest.mark.asyncio
async def test_discover_llm_url_fallback(planner_tool):
    # Remove router_llm to trigger fallback
    del planner_tool.twin_service.router_llm

    # Ensure other attributes don't interfere
    planner_tool.twin_service.llm_base_url = None

    # Mock fallback to default
    url = await planner_tool._discover_llm_url()
    port = os.getenv("ROUTER_PORT", "8081")
    assert url == f"http://localhost:{port}/v1"

@pytest.mark.asyncio
async def test_discover_llm_url_env_var(planner_tool):
    # Remove router_llm to trigger fallback
    del planner_tool.twin_service.router_llm
    planner_tool.twin_service.llm_base_url = None

    # Mock env var
    with patch.dict(os.environ, {"LLAMA_API_URL": "http://env-override:9999/v1"}):
        url = await planner_tool._discover_llm_url()
        assert url == "http://env-override:9999/v1"

@pytest.mark.asyncio
async def test_call_llm_success(planner_tool):
    mock_response = {
        "choices": [{
            "message": {
                "content": "```json\n[{\"id\": \"task1\", \"prompt\": \"do work\"}]\n```"
            }
        }]
    }

    # Mock _discover_llm_url to avoid side effects
    planner_tool._discover_llm_url = AsyncMock(return_value="http://mock-llm:8000/v1")

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        # Create a MagicMock for the response object, NOT an AsyncMock
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.json.return_value = mock_response
        response_mock.raise_for_status = MagicMock()

        # When await client.post() is called, it returns this response_mock
        mock_post.return_value = response_mock

        plan = await planner_tool._call_llm("test prompt")
        assert len(plan) == 1
        assert plan[0]["id"] == "task1"

@pytest.mark.asyncio
async def test_plan_and_execute_success(planner_tool):
    # Mock ProjectMapper
    mock_mapper = MagicMock()
    mock_mapper.scan.return_value = {"root": "/", "files": [{"path": "file1.py"}]}
    planner_tool.twin_service.tools["project_mapper"] = mock_mapper

    # Mock Swarm
    mock_swarm = MagicMock()
    mock_swarm.spawn_workers = AsyncMock(return_value="Workers done")
    planner_tool.twin_service.tools["swarm"] = mock_swarm

    # Mock _call_llm
    planner_tool._call_llm = AsyncMock(return_value=[{"id": "task1", "prompt": "do it"}])

    result = await planner_tool.plan_and_execute("my goal")

    assert "Planner executed" in result
    assert "Workers done" in result
    planner_tool._call_llm.assert_called_once()
    mock_swarm.spawn_workers.assert_called_once()

@pytest.mark.asyncio
async def test_plan_and_execute_fallback(planner_tool):
    # Mock ProjectMapper
    mock_mapper = MagicMock()
    mock_mapper.scan.return_value = {"root": "/", "files": [{"path": "file1.py"}]}
    planner_tool.twin_service.tools["project_mapper"] = mock_mapper

    # Mock Swarm
    mock_swarm = MagicMock()
    mock_swarm.spawn_workers = AsyncMock(return_value="Workers done")
    planner_tool.twin_service.tools["swarm"] = mock_swarm

    # Mock _call_llm to fail/return None
    planner_tool._call_llm = AsyncMock(return_value=None)

    result = await planner_tool.plan_and_execute("my goal")

    assert "Planner executed" in result
    # It should have used fallback plan
    mock_swarm.spawn_workers.assert_called_once()
    args, _ = mock_swarm.spawn_workers.call_args
    assert args[0][0]["id"] == "default_task"
