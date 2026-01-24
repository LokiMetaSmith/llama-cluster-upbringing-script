
import os
import importlib
import pytest
from fastapi import Request
from fastapi.testclient import TestClient
import logging

# Configure logging to see our info messages
logging.basicConfig(level=logging.INFO)

def test_proxy_headers_respected_when_configured():
    """
    Verify that when TRUSTED_PROXIES is set, X-Forwarded-For is respected.
    """
    # Set the env var BEFORE reloading
    os.environ["TRUSTED_PROXIES"] = "*"

    import web_server
    importlib.reload(web_server)

    # Verify middleware is present (optional but good for debugging)
    middleware_names = [m.cls.__name__ for m in web_server.app.user_middleware]
    print(f"Middleware stack with TRUSTED_PROXIES=*: {middleware_names}")
    assert "ProxyHeadersMiddleware" in middleware_names

    client = TestClient(web_server.app)

    @web_server.app.get("/debug_ip_test_secure")
    def get_ip(request: Request):
        return {"ip": request.client.host if request.client else "unknown"}

    # Simulate request with X-Forwarded-For
    response = client.get("/debug_ip_test_secure", headers={"X-Forwarded-For": "203.0.113.195"})

    assert response.status_code == 200
    data = response.json()

    # It SHOULD match the header because middleware is enabled and trusted
    assert data["ip"] == "203.0.113.195"

def test_proxy_headers_ignored_when_disabled():
    """
    Verify that when TRUSTED_PROXIES is NOT set, X-Forwarded-For is ignored.
    """
    # Unset env var
    if "TRUSTED_PROXIES" in os.environ:
        del os.environ["TRUSTED_PROXIES"]

    import web_server
    importlib.reload(web_server)

    # Verify middleware is NOT present
    middleware_names = [m.cls.__name__ for m in web_server.app.user_middleware]
    print(f"Middleware stack without TRUSTED_PROXIES: {middleware_names}")
    assert "ProxyHeadersMiddleware" not in middleware_names

    client = TestClient(web_server.app)

    @web_server.app.get("/debug_ip_test_insecure")
    def get_ip(request: Request):
        return {"ip": request.client.host if request.client else "unknown"}

    response = client.get("/debug_ip_test_insecure", headers={"X-Forwarded-For": "203.0.113.195"})

    assert response.status_code == 200
    data = response.json()

    # It should NOT match because middleware is missing
    assert data["ip"] != "203.0.113.195"
