import pytest
import sys
import os
from unittest.mock import MagicMock, patch, AsyncMock

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from swarm_tool import SwarmTool

@pytest.mark.asyncio
async def test_swarm_tool_initialization():
    tool = SwarmTool(nomad_url="http://nomad.test:4646")
    assert tool.nomad_url == "http://nomad.test:4646"

@pytest.mark.asyncio
async def test_spawn_workers_success():
    tool = SwarmTool()
    tasks = [{"id": "1", "prompt": "do something"}, {"id": "2", "prompt": "do something else"}]

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None

    with patch('httpx.AsyncClient') as MockClient:
        mock_client_instance = MockClient.return_value
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__.return_value = None

        # post must be awaitable
        mock_client_instance.post = AsyncMock(return_value=mock_response)

        result = await tool.spawn_workers(tasks)

        assert "Successfully dispatched 2 workers" in result
        assert mock_client_instance.post.call_count == 2

@pytest.mark.asyncio
async def test_spawn_workers_partial_failure():
    tool = SwarmTool()
    tasks = [{"id": "1", "prompt": "success"}, {"id": "2", "prompt": "fail"}]

    mock_response_ok = MagicMock()
    mock_response_ok.status_code = 200
    mock_response_ok.raise_for_status.return_value = None

    with patch('httpx.AsyncClient') as MockClient:
        mock_client_instance = MockClient.return_value
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__.return_value = None

        # side_effect for post
        async def side_effect(*args, **kwargs):
            # Check the json payload to decide success or fail.
            # kwargs['json'] contains the job payload.
            payload = kwargs.get('json', {})
            # We encoded the task id in the env vars
            task_env = payload.get("Job", {}).get("TaskGroups", [])[0].get("Tasks", [])[0].get("Env", {})
            task_id = task_env.get("WORKER_TASK_ID")

            if task_id == "2":
                raise Exception("Nomad Error")
            return mock_response_ok

        mock_client_instance.post = AsyncMock(side_effect=side_effect)

        result = await tool.spawn_workers(tasks)

        assert "Successfully dispatched 1 workers" in result
        assert "Errors: Failed to dispatch" in result

@pytest.mark.asyncio
async def test_kill_worker_success():
    tool = SwarmTool()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None

    with patch('httpx.AsyncClient') as MockClient:
        mock_client_instance = MockClient.return_value
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__.return_value = None

        mock_client_instance.delete = AsyncMock(return_value=mock_response)

        result = await tool.kill_worker("job-123")

        assert "Successfully killed worker: job-123" in result

@pytest.mark.asyncio
async def test_kill_worker_failure():
    tool = SwarmTool()

    with patch('httpx.AsyncClient') as MockClient:
        mock_client_instance = MockClient.return_value
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__.return_value = None

        mock_client_instance.delete = AsyncMock(side_effect=Exception("Not found"))

        result = await tool.kill_worker("job-123")

        assert "Failed to kill worker job-123" in result
