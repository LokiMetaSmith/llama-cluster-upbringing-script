
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add pipecatapp to path so we can import web_server
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from web_server import app

client = TestClient(app)

@patch("httpx.AsyncClient.get")
def test_metrics_caching_behavior(mock_get):
    """
    Test that /api/cluster/metrics is cached.
    """
    # Mock response
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "status": "success",
        "data": {
            "result": []
        }
    }
    mock_get.return_value = mock_resp

    # First request
    response1 = client.get("/api/cluster/metrics")
    assert response1.status_code == 200, "First request failed"

    # Check call count. Should be 2 (one for CPU, one for Memory)
    first_call_count = mock_get.call_count
    print(f"Call count after first request: {first_call_count}")

    # Second request
    response2 = client.get("/api/cluster/metrics")
    assert response2.status_code == 200, "Second request failed (Cache Hit)"

    # Check call count.
    total_call_count = mock_get.call_count
    print(f"Total call count after second request: {total_call_count}")

    assert first_call_count == 2, "Expected 2 calls per request (CPU + Mem)"

    # Caching enabled: Second request should NOT increase call count
    assert total_call_count == 2, "Expected 2 calls total (Caching Enabled)"
