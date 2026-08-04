from fastapi.testclient import TestClient
from pipecatapp.web_server import app
import os
from unittest.mock import patch, MagicMock

client = TestClient(app)

from pipecatapp.web_server import get_api_key
app.dependency_overrides[get_api_key] = lambda: "dev_key_123"

def test_health_check_init():
    """Test health check when not ready."""
    app.state.is_ready = False
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "initializing"}

def test_health_check_ready():
    """Test health check when ready."""
    app.state.is_ready = True
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_web_ui_routes():
    """Test that main UI routes return HTML."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    response = client.get("/cluster")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

@patch("httpx.AsyncClient.get")
def test_cluster_metrics(mock_get):
    """Test the cluster metrics endpoint with mocked Prometheus response."""
    # Mock CPU response
    mock_cpu_resp = MagicMock()
    mock_cpu_resp.status_code = 200
    mock_cpu_resp.json.return_value = {
        "status": "success",
        "data": {
            "result": [
                {
                    "metric": {"task": "test-service"},
                    "value": [1234567890, "0.5"]
                }
            ]
        }
    }

    # Mock Memory response
    mock_mem_resp = MagicMock()
    mock_mem_resp.status_code = 200
    mock_mem_resp.json.return_value = {
        "status": "success",
        "data": {
            "result": [
                {
                    "metric": {"task": "test-service"},
                    "value": [1234567890, "1048576"]
                }
            ]
        }
    }

    # Bolt ⚡ Update: Handle concurrent requests by checking query params
    async def side_effect(*args, **kwargs):
        params = kwargs.get("params", {})
        query = params.get("query", "")
        if "cpu" in query:
            return mock_cpu_resp
        elif "memory" in query:
            return mock_mem_resp
        return MagicMock(status_code=404)

    mock_get.side_effect = side_effect

    response = client.get("/api/cluster/metrics", headers={"Authorization": "Bearer dev_key_123"})
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == "test-service"
    assert data[0]["cpu"] == 0.5
    assert data[0]["mem"] == 1048576
    assert data[0]["status"] == "running"

@patch("workflow.runner.ActiveWorkflows.get_all_states")
def test_active_workflows_sanitization(mock_get_all_states):
    """Test that active workflows output is sanitized."""
    def mock_get_all_states_func(sanitize=False):
        state = {
            "runner1": {
                "global_inputs": {"key": "sk-1234567890abcdef1234567890abcdef"},
                "node_outputs": {}
            }
        }
        if sanitize:
            state["runner1"]["global_inputs"]["key"] = "sk-[REDACTED]"
        return state
    mock_get_all_states.side_effect = mock_get_all_states_func

    response = client.get("/api/workflows/active", headers={"Authorization": "Bearer dev_key_123"})
    assert response.status_code == 200
    data = response.json()

    # Check that redaction occurred
    assert data["runner1"]["global_inputs"]["key"] == "sk-[REDACTED]"
