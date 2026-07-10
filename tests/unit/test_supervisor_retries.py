import os
import sys
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import time

# Add repo root and pipecatapp to path to resolve imports correctly
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO_ROOT)
sys.path.insert(0, os.path.join(REPO_ROOT, "pipecatapp"))

from task_supervisor import TaskSupervisor
from pmm_memory_client import PMMMemoryClient

class TestTaskSupervisorRetries(unittest.IsolatedAsyncioTestCase):
    async def test_check_tasks_detects_timeout_and_retries(self):
        # 1. Setup mock twin service and tools
        mock_twin_service = MagicMock()
        mock_swarm_tool = MagicMock()
        mock_swarm_tool.kill_worker = AsyncMock(return_value="Success")
        mock_swarm_tool.spawn_workers = AsyncMock(return_value="Spawned")

        mock_twin_service.tools = {
            "swarm": mock_swarm_tool
        }

        # 2. Mock Shared Memory Client
        mock_memory_client = MagicMock()
        mock_twin_service.long_term_memory = mock_memory_client

        # Mock event list containing a worker_started event
        events = [
            {
                "kind": "worker_started",
                "timestamp": time.time(),
                "meta": {
                    "task_id": "task-abc",
                    "agent_type": "worker",
                    "nomad_job_id": "swarm-worker-task-abc-12345",
                    "prompt": "Optimize this database index",
                    "context": "SQLite"
                }
            }
        ]
        mock_memory_client.get_events = AsyncMock(return_value=events)

        # 3. Instantiate TaskSupervisor
        supervisor = TaskSupervisor(mock_twin_service)

        # 4. Patch isinstance to bypass type check on memory client mock
        with patch("task_supervisor.isinstance", return_value=True):
            # Run first check with standard timeout: registers the task without timing out
            supervisor.task_timeout = 300
            await supervisor._check_tasks()

            self.assertIn("task-abc", supervisor.active_tasks)
            self.assertEqual(supervisor.active_tasks["task-abc"]["nomad_job_id"], "swarm-worker-task-abc-12345")

            # Force timeout and run second check: triggers corrective actions and retry
            supervisor.task_timeout = -1
            await supervisor._check_tasks()

        # Assert task is removed from active
        self.assertNotIn("task-abc", supervisor.active_tasks)

        # Assert kill_worker was called with correct Job UUID
        mock_swarm_tool.kill_worker.assert_called_once_with("swarm-worker-task-abc-12345")

        # Assert spawn_workers was called with correct retry definition
        mock_swarm_tool.spawn_workers.assert_called_once_with(
            tasks=[{
                "id": "task-abc",
                "prompt": "Optimize this database index",
                "context": "SQLite"
            }],
            agent_type="worker"
        )

if __name__ == "__main__":
    unittest.main()
