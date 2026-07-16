import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from pipecatapp.task_supervisor import TaskSupervisor
from pipecatapp.concurrency.queue_manager import ConcurrencyPolicy, JobQueuePolicy

@pytest.mark.asyncio
async def test_task_supervisor_policy_integration_prefer_old():
    # Setup mock twin service and tools
    mock_twin_service = MagicMock()
    mock_swarm_tool = AsyncMock()

    # We must simulate a running task by sleeping in the executor/spawn_workers mock
    async def slow_spawn(*args, **kwargs):
        await asyncio.sleep(0.2)
        return "Spawned successfully"

    mock_swarm_tool.spawn_workers.side_effect = slow_spawn
    mock_swarm_tool.kill_worker.return_value = "Killed successfully"

    mock_twin_service.tools = {"swarm": mock_swarm_tool}
    mock_twin_service.long_term_memory = MagicMock()

    # Instantiate TaskSupervisor
    supervisor = TaskSupervisor(mock_twin_service)

    # Configure PREFER_OLD policy with limit 1
    supervisor.set_job_policy("repack-job", JobQueuePolicy(ConcurrencyPolicy.PREFER_OLD, concurrency_limit=1))

    # 1. Spawn a task
    fut1 = await supervisor.spawn_task_with_policy(
        job_key="repack-job",
        task_id="task-wholesale-weekend-1",
        prompt="Wholesale repack Git repository",
        context="weekend",
        agent_type="worker"
    )
    assert fut1 is not None

    # Let it enter executor and start sleeping
    await asyncio.sleep(0.01)

    # 2. Try to spawn another while the first is active
    fut2 = await supervisor.spawn_task_with_policy(
        job_key="repack-job",
        task_id="task-wholesale-weekend-2",
        prompt="Wholesale repack Git repository",
        context="weekend-trigger-2",
        agent_type="worker"
    )

    # Under PREFER_OLD, fut2 should be dropped (None)
    assert fut2 is None

    # Verify swarm_tool.spawn_workers was called exactly once (for the first task)
    mock_swarm_tool.spawn_workers.assert_called_once_with(
        tasks=[{"id": "task-wholesale-weekend-1", "prompt": "Wholesale repack Git repository", "context": "weekend"}],
        agent_type="worker"
    )

    res = await fut1
    assert res == "Spawned successfully"


@pytest.mark.asyncio
async def test_task_supervisor_policy_integration_prefer_new():
    # Setup mock twin service and tools
    mock_twin_service = MagicMock()
    mock_swarm_tool = AsyncMock()

    async def slow_spawn(*args, **kwargs):
        await asyncio.sleep(0.5)
        return "Spawned successfully"

    mock_swarm_tool.spawn_workers.side_effect = slow_spawn
    mock_swarm_tool.kill_worker.return_value = "Killed successfully"

    mock_twin_service.tools = {"swarm": mock_swarm_tool}
    mock_twin_service.long_term_memory = MagicMock()

    # Instantiate TaskSupervisor
    supervisor = TaskSupervisor(mock_twin_service)

    # Configure PREFER_NEW policy with limit 1
    supervisor.set_job_policy("repack-job", JobQueuePolicy(ConcurrencyPolicy.PREFER_NEW, concurrency_limit=1))

    # 1. Spawn first task
    fut1 = await supervisor.spawn_task_with_policy(
        job_key="repack-job",
        task_id="task-1",
        prompt="Prompt 1",
        context="ctx-1",
        agent_type="worker"
    )
    assert fut1 is not None

    # Let it enter executor and start sleeping
    await asyncio.sleep(0.01)

    # 2. Spawn second task (should cancel the first)
    fut2 = await supervisor.spawn_task_with_policy(
        job_key="repack-job",
        task_id="task-2",
        prompt="Prompt 2",
        context="ctx-2",
        agent_type="worker"
    )
    assert fut2 is not None

    # First task should raise CancelledError
    with pytest.raises(asyncio.CancelledError):
        await fut1

    # Verify that the cancel hook (kill_worker) was called for task-1
    mock_swarm_tool.kill_worker.assert_called_with("worker-task-1")

    # Let the second task complete
    res = await fut2
    assert res == "Spawned successfully"
