import pytest
from fastapi.testclient import TestClient
import time
import sys
import os

# Add the repository root to the sys.path so we can import from cluster_cache
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from cluster_cache.app import app, active_nodes, cleanup_expired_nodes

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_state():
    """Reset the active_nodes dictionary before each test."""
    active_nodes.clear()
    yield
    active_nodes.clear()

def test_get_nodes_empty():
    response = client.get("/nodes")
    assert response.status_code == 200
    assert response.json() == {"nodes": []}

def test_register_node_client_ip():
    # Test client IP registration
    response = client.post("/register")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    # TestClient's default client IP is "testclient"
    assert response.json()["ip_address"] == "testclient"

    response = client.get("/nodes")
    assert response.status_code == 200
    assert "testclient" in response.json()["nodes"]

def test_register_node_explicit_ip():
    test_ip = "192.168.1.100"
    response = client.post("/register", json={"ip_address": test_ip})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "ip_address": test_ip}

    response = client.get("/nodes")
    assert response.status_code == 200
    assert test_ip in response.json()["nodes"]

def test_node_expiration(monkeypatch):
    # Register a node
    test_ip = "192.168.1.50"
    client.post("/register", json={"ip_address": test_ip})

    response = client.get("/nodes")
    assert test_ip in response.json()["nodes"]

    # Mock time.time to simulate expiration
    original_time = time.time

    # Fast forward time beyond NODE_TTL (300 seconds)
    monkeypatch.setattr(time, 'time', lambda: original_time() + 400)

    # Querying should trigger cleanup
    response = client.get("/nodes")
    assert response.status_code == 200
    assert test_ip not in response.json()["nodes"]
    assert response.json() == {"nodes": []}
