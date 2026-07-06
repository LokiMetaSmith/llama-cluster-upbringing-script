import sys
from unittest.mock import MagicMock, AsyncMock

# Mock dependencies before importing web_server
sys.modules['opentelemetry'] = MagicMock()
sys.modules['opentelemetry.trace'] = MagicMock()
sys.modules['opentelemetry.sdk.trace'] = MagicMock()
sys.modules['opentelemetry.sdk.trace.export'] = MagicMock()
sys.modules['opentelemetry.exporter.otlp.proto.grpc.trace_exporter'] = MagicMock()
sys.modules['opentelemetry.instrumentation.fastapi'] = MagicMock()
sys.modules['opentelemetry.instrumentation.httpx'] = MagicMock()
sys.modules['opentelemetry.sdk.resources'] = MagicMock()
sys.modules['pipecatapp.workflow.runner'] = MagicMock()
sys.modules['workflow.runner'] = MagicMock()
sys.modules['pipecatapp.workflow.history'] = MagicMock()
sys.modules['workflow.history'] = MagicMock()
sys.modules['pipecatapp.api_keys'] = MagicMock()
sys.modules['api_keys'] = MagicMock()
sys.modules['pipecatapp.security'] = MagicMock()
sys.modules['security'] = MagicMock()
sys.modules['pipecatapp.rate_limiter'] = MagicMock()
sys.modules['rate_limiter'] = MagicMock()
sys.modules['pipecatapp.net_utils'] = MagicMock()
sys.modules['net_utils'] = MagicMock()

import asyncio
import json
import base64
import pytest
from fastapi.testclient import TestClient
from pipecatapp.web_server import app, get_api_key, standard_limiter

# Bypass API key security and rate limiting for tests
app.dependency_overrides[get_api_key] = lambda: "test-key"
app.dependency_overrides[standard_limiter] = lambda: None

client = TestClient(app)

@pytest.mark.asyncio
async def test_webring_routes(mocker):
    # Mock service_discovery_client
    mock_httpx = mocker.patch("pipecatapp.web_server.service_discovery_client")

    # Mock get members
    members = [{"name": "Site A", "url": "http://site-a.com"}]
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"Value": base64.b64encode(json.dumps(members).encode()).decode()}]
    mock_httpx.get = AsyncMock(return_value=mock_response)

    # Test GET /api/webring/members
    response = client.get("/api/webring/members")
    assert response.status_code == 200
    assert response.json() == members

    # Test POST /api/webring/members
    mock_httpx.put = AsyncMock(return_value=MagicMock(status_code=200))
    new_members = [{"name": "Site B", "url": "http://site-b.com"}]
    response = client.post("/api/webring/members", json=new_members)
    assert response.status_code == 200

    # Test /webring/random
    response = client.get("/webring/random", follow_redirects=False)
    assert response.status_code in [302, 307]
    assert response.headers["location"] in ["http://site-a.com", "http://site-b.com"]

@pytest.mark.asyncio
async def test_webring_navigation(mocker):
    members = [
        {"name": "A", "url": "http://a.com"},
        {"name": "B", "url": "http://b.com"},
        {"name": "C", "url": "http://c.com"}
    ]

    mocker.patch("pipecatapp.web_server.get_ouroboros_members", return_value=members)

    # Next from A should be B
    response = client.get("/webring/next?from=http://a.com", follow_redirects=False)
    assert response.status_code in [302, 307]
    assert response.headers["location"] == "http://b.com"

    # Next from C should be A (circular)
    response = client.get("/webring/next?from=http://c.com", follow_redirects=False)
    assert response.status_code in [302, 307]
    assert response.headers["location"] == "http://a.com"

    # Prev from A should be C
    response = client.get("/webring/prev?from=http://a.com", follow_redirects=False)
    assert response.status_code in [302, 307]
    assert response.headers["location"] == "http://c.com"
