import pytest
import time
import asyncio
from fastapi import FastAPI, Depends, Request
from fastapi.testclient import TestClient
from pipecatapp.rate_limiter import RateLimiter
from dataclasses import dataclass

def test_rate_limiter():
    app = FastAPI()
    # Limit: 2 requests per 1 second
    limiter = RateLimiter(limit=2, window=1)

    @app.get("/test")
    async def test_endpoint(request: Request, limit: None = Depends(limiter)):
        return {"status": "ok"}

    client = TestClient(app)

    # 1st request - OK
    response = client.get("/test")
    assert response.status_code == 200

    # 2nd request - OK
    response = client.get("/test")
    assert response.status_code == 200

    # 3rd request - Blocked
    response = client.get("/test")
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.json()["detail"]

    # Wait for window to expire
    time.sleep(1.1)

    # 4th request - OK (after window reset)
    response = client.get("/test")
    assert response.status_code == 200

@dataclass
class MockClient:
    host: str

@dataclass
class MockRequest:
    client: MockClient

@pytest.mark.asyncio
async def test_rate_limiter_cleanup():
    # Limit: 10 requests, window: 0.1s, cleanup: 0.1s
    limiter = RateLimiter(limit=10, window=0.1, cleanup_interval=0.1)

    # Add requests from different IPs
    for i in range(10):
        req = MockRequest(client=MockClient(host=f"1.2.3.{i}"))
        await limiter(req)

    assert len(limiter.requests) == 10

    # Wait for window and cleanup interval to pass
    await asyncio.sleep(0.2)

    # Trigger one more request to force cleanup
    req = MockRequest(client=MockClient(host="1.2.3.100"))
    await limiter(req)

    # Should be 1 (the new one)
    assert len(limiter.requests) == 1
