import pytest
import time
from fastapi import FastAPI, Depends, Request
from fastapi.testclient import TestClient
from pipecatapp.rate_limiter import RateLimiter

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
