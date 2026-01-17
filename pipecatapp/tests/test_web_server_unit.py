from fastapi.testclient import TestClient
from web_server import app
import os
from unittest.mock import patch, MagicMock

client = TestClient(app)

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

    mock_get.side_effect = [mock_cpu_resp, mock_mem_resp]

    response = client.get("/api/cluster/metrics")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == "test-service"
    assert data[0]["cpu"] == 0.5
    assert data[0]["mem"] == 1048576
    assert data[0]["status"] == "running"
