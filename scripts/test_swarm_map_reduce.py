import asyncio
import json
import sys
import os

# Add pipecatapp to sys.path so internal imports like 'from tools...' work
sys.path.append(os.path.abspath("pipecatapp"))

from unittest.mock import MagicMock, AsyncMock, patch
from pipecatapp.tools.swarm_tool import SwarmTool

# Mock Memory Client
class MockMemoryClient:
    def __init__(self):
        self.events = []

    async def get_events(self, limit=100):
        return self.events

    async def add_event(self, kind, content, meta=None):
        self.events.append({
            "kind": kind,
            "content": content,
            "meta": meta or {},
            "timestamp": 1234567890
        })

    async def get_agent_stats(self, agent_id):
        return {"total_tasks": 10, "success_rate": 90}

    async def create_work_item(self, **kwargs):
        return "work-item-123"

    async def update_work_item(self, *args, **kwargs):
        pass

async def test_swarm_map_reduce():
    print("Testing Swarm Map-Reduce Logic...")

    # 1. Setup Mocks
    mock_memory = MockMemoryClient()

    # Mock httpx for SwarmTool to avoid real network calls
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        # Mock responses for spawn_workers
        mock_client.post.return_value.status_code = 200

        # Initialize SwarmTool with mock memory
        swarm_tool = SwarmTool(memory_client=mock_memory)

        # 2. Simulate Dispatch
        tasks = [
            {"id": "task-1", "prompt": "Task 1", "context": ""},
            {"id": "task-2", "prompt": "Task 2", "context": ""}
        ]

        print("Dispatching workers...")
        spawn_result_json = await swarm_tool.spawn_workers(tasks)
        spawn_result = json.loads(spawn_result_json)
        task_ids = spawn_result["task_ids"]
        print(f"Spawned Task IDs: {task_ids}")

        # 3. Simulate Worker Completion (Background Task)
        async def simulate_workers():
            await asyncio.sleep(1)
            print("Simulating worker completion...")
            await mock_memory.add_event("worker_result", "Result 1", {"task_id": "task-1"})
            await asyncio.sleep(1)
            await mock_memory.add_event("worker_result", "Result 2", {"task_id": "task-2"})

        # 4. Wait for Results (Map-Reduce)
        # We run the simulation concurrently with the waiting
        wait_task = asyncio.create_task(swarm_tool.wait_for_results(task_ids, timeout=5, poll_interval=1))
        sim_task = asyncio.create_task(simulate_workers())

        results_json = await wait_task
        await sim_task

        results = json.loads(results_json)
        print(f"Reduce Results: {results}")

        # Assertions
        assert results["status"] == "complete"
        assert results["results"]["task-1"] == "Result 1"
        assert results["results"]["task-2"] == "Result 2"
        print("SUCCESS: Map-Reduce logic verified.")

if __name__ == "__main__":
    asyncio.run(test_swarm_map_reduce())
