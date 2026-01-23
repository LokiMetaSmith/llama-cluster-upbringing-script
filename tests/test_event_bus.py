import os
import sys
import asyncio
import time
import requests
import threading
import uvicorn
from multiprocessing import Process

# Adjust path to include pipecatapp
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../pipecatapp")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../pipecatapp/memory_graph_service")))

# Mock mcp_server if needed, but since we are running server.py which imports it...
# We might need to mock it if dependencies are missing.
# server.py handles ImportError for mcp_server gracefully.

from pipecatapp.memory_graph_service.server import app

PORT = 8123
BASE_URL = f"http://localhost:{PORT}"

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="error")

def test_event_bus_flow():
    # 1. Start Server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Wait for startup
    time.sleep(2)

    try:
        # 2. Check Health
        resp = requests.get(f"{BASE_URL}/health")
        assert resp.status_code == 200, "Health check failed"
        print("Health check passed.")

        # 3. Post Event (Worker Style)
        payload = {
            "kind": "worker_started",
            "content": "Test worker starting",
            "meta": {
                "task_id": "test-task-1",
                "agent": "worker-1"
            }
        }
        resp = requests.post(f"{BASE_URL}/events", json=payload)
        assert resp.status_code == 200, f"Post event failed: {resp.text}"
        print("Post event passed.")

        # 4. Read Events (Manager Style)
        resp = requests.get(f"{BASE_URL}/events")
        assert resp.status_code == 200
        events = resp.json()
        assert len(events) >= 1
        assert events[0]["kind"] == "worker_started"
        assert events[0]["task_id"] == "test-task-1"
        print("Read events passed.")

        # 5. Read Specific Task
        resp = requests.get(f"{BASE_URL}/tasks/test-task-1")
        assert resp.status_code == 200
        task_events = resp.json()
        assert len(task_events) == 1
        print("Read task events passed.")

    finally:
        # Cleanup isn't strict here as it's a daemon thread
        pass

if __name__ == "__main__":
    test_event_bus_flow()
