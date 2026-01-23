import os
import sys
import asyncio
import time
import requests
import threading
import uvicorn
import httpx
from pipecatapp.memory_graph_service.server import app

# Add path to include agents
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../pipecatapp")))

from pipecatapp.manager_agent import ManagerAgent

PORT = 8124
BASE_URL = f"http://localhost:{PORT}"

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="error")

async def mock_technician_task(task_id: str, duration: int = 2, agent_type: str = "technician"):
    """Simulates a technician or judge doing work and reporting back."""
    await asyncio.sleep(duration)
    try:
        # Start
        requests.post(f"{BASE_URL}/events", json={
            "kind": f"{agent_type}_started", # judge_started or worker_started
            "content": f"Started {task_id}",
            "meta": {"task_id": task_id, "agent_type": agent_type}
        })

        await asyncio.sleep(1)

        if agent_type == "judge":
            # Judge Result
            requests.post(f"{BASE_URL}/events", json={
                "kind": "judge_pass",
                "content": "VERDICT: PASS",
                "meta": {"task_id": task_id, "status": "success"}
            })
        else:
            # Technician Result
            requests.post(f"{BASE_URL}/events", json={
                "kind": "worker_result",
                "content": f"Result for {task_id}: SUCCESS",
                "meta": {"task_id": task_id, "status": "success"}
            })
    except Exception as e:
        print(f"Mock {agent_type} failed: {e}")

class MockSwarmTool:
    """Mocks SwarmTool to spawn our local mock tasks instead of Nomad jobs."""
    async def spawn_workers(self, tasks: list, agent_type: str = "worker"):
        for task in tasks:
            # Fire and forget the mock task
            asyncio.create_task(mock_technician_task(task['id'], agent_type=agent_type))
        return f"Mock dispatched {len(tasks)}"

class TestManagerFlow:
    async def test_flow(self):
        # 1. Start Event Bus
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        await asyncio.sleep(2)

        print("Event Bus started.")

        # 2. Configure Manager
        agent = ManagerAgent()
        agent.prompt = "Test Mission"
        agent.context = "Test Context"
        agent.memory_url = BASE_URL # Override discovery
        # Mock LLM to avoid external deps
        agent.llm_base_url = None

        # Mock discover_services to prevent overwriting memory_url
        agent.discover_services = lambda: None

        # Mock Map Phase to return fixed subtasks
        async def mock_map():
            return [
                {"id": "task-A", "prompt": "Do A", "context": ""},
                {"id": "task-B", "prompt": "Do B", "context": ""}
            ]
        agent.map_phase = mock_map

        # Mock Dispatch to use our local mock runner
        async def mock_dispatch(subtasks):
            swarm = MockSwarmTool()
            agent.swarm_tool = swarm # Ensure agent has reference for verify_phase
            await swarm.spawn_workers(subtasks)
            return [t['id'] for t in subtasks]
        agent.dispatch_phase = mock_dispatch

        # Run!
        print("Starting Manager Agent Run...")
        await agent.run()
        print("Manager Agent Run Complete.")

        # Verify Results in DB
        resp = requests.get(f"{BASE_URL}/events")
        events = resp.json()

        print("DEBUG: All Events found in DB:")
        for e in events:
            print(f" - {e['kind']} (Task: {e.get('task_id')})")

        # Check for manager_complete (not just intermediate manager_result)
        complete_results = [e for e in events if e['kind'] == 'manager_complete']
        assert len(complete_results) == 1, "Manager did not report completion"

        final_content = complete_results[0]['content']
        assert "VERIFICATION PASSED" in final_content
        print(f"Final Report verified: {final_content[:50]}...")
        print("Manager reported final result.")

if __name__ == "__main__":
    t = TestManagerFlow()
    asyncio.run(t.test_flow())
