import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from pipecatapp.task_supervisor import TaskSupervisor

@pytest.mark.asyncio
async def test_handle_gateway_exhaustion_success():
    # Setup mocks
    mock_twin = MagicMock()
    mock_twin.tools = {}
    mock_twin.long_term_memory = AsyncMock()

    mock_swarm = AsyncMock()
    mock_swarm.spawn_workers = AsyncMock(return_value="spawned-ok")
    mock_twin.tools["swarm"] = mock_swarm

    supervisor = TaskSupervisor(mock_twin)

    # Trigger failover scaling
    result = await supervisor.handle_gateway_exhaustion("openai_gpt4")

    assert result is True
    # Ensure spawn_workers was called
    mock_swarm.spawn_workers.assert_awaited_once()
    args, kwargs = mock_swarm.spawn_workers.call_args
    assert kwargs["agent_type"] == "worker"
    assert "openai_gpt4" in kwargs["tasks"][0]["prompt"]

@pytest.mark.asyncio
async def test_handle_gateway_exhaustion_failure():
    # Setup mock to raise error
    mock_twin = MagicMock()
    mock_twin.tools = {}
    mock_twin.long_term_memory = AsyncMock()

    mock_swarm = AsyncMock()
    mock_swarm.spawn_workers.side_effect = Exception("Nomad API error")
    mock_twin.tools["swarm"] = mock_swarm

    supervisor = TaskSupervisor(mock_twin)

    result = await supervisor.handle_gateway_exhaustion("openrouter_claude_sonnet")

    assert result is False
