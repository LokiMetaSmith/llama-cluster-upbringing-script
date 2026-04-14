import os
import sys
import time
import threading
import uvicorn
import requests
from unittest.mock import patch, MagicMock

PORT = 8123
BASE_URL = f"http://localhost:{PORT}"

def test_event_bus_flow():
    with patch('requests.get') as mock_get, patch('requests.post') as mock_post:
        # Mock responses
        mock_get.side_effect = [
            # 1. Health Check
            MagicMock(status_code=200, text="OK"),
            # 2. Read Events
            MagicMock(status_code=200, json=lambda: [{"kind": "worker_started", "task_id": "test-task-1"}]),
            # 3. Read Specific Task
            MagicMock(status_code=200, json=lambda: [{"kind": "worker_started", "task_id": "test-task-1"}])
        ]
        mock_post.return_value = MagicMock(status_code=200, text="OK")

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

if __name__ == "__main__":
    test_event_bus_flow()
