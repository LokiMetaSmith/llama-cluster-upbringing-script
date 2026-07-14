import os
import sys
import pytest
from unittest.mock import AsyncMock, MagicMock

# Append repository paths so we can import from pipecatapp
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(REPO_ROOT)
sys.path.append(os.path.join(REPO_ROOT, "pipecatapp"))

from pipecatapp.task_supervisor import TaskSupervisor

@pytest.mark.asyncio
async def test_task_supervisor_heartbeat_execution_loop():
    # 1. Create a mocked twin_service
    mock_twin_service = MagicMock()
    mock_swarm_tool = AsyncMock()
    mock_swarm_tool.spawn_workers.return_value = "Spawned successfully"
    mock_swarm_tool.kill_worker.return_value = "Killed successfully"

    # Register mock swarm tool
    mock_twin_service.tools = {"swarm": mock_swarm_tool}
    mock_twin_service.long_term_memory = MagicMock()

    # 2. Instantiate TaskSupervisor
    supervisor = TaskSupervisor(mock_twin_service)

    # Confirm initial empty queue
    assert len(supervisor.heartbeat_queue) == 0

    # 3. Add a task to the heartbeat queue
    task_id = "test-heartbeat-task-123"
    prompt = "Process the pending task on heartbeat"
    await supervisor.add_heartbeat_task(
        task_id=task_id,
        prompt=prompt,
        context="some-context",
        agent_type="worker"
    )

    assert len(supervisor.heartbeat_queue) == 1
    assert supervisor.heartbeat_queue[0]["id"] == task_id

    # 4. Trigger one scheduled heartbeat iteration
    await supervisor.run_heartbeat()

    # 5. Verify the worker was woken up via SwarmTool.spawn_workers
    mock_swarm_tool.spawn_workers.assert_called_once_with(
        tasks=[{"id": task_id, "prompt": prompt, "context": "some-context"}],
        agent_type="worker"
    )

    # 6. Verify the worker was subsequently put back to sleep via kill_worker
    expected_nomad_job_id = f"worker-{task_id}"
    mock_swarm_tool.kill_worker.assert_called_once_with(expected_nomad_job_id)

    # 7. Verify the queue was correctly cleared
    assert len(supervisor.heartbeat_queue) == 0
