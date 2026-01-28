import pytest
import asyncio
from unittest.mock import MagicMock, patch
from httpx import AsyncClient, ASGITransport
from pipecatapp.web_server import app, sync_response_store

# Mock the API key dependency to bypass auth
# Since we run with PYTHONPATH=pipecatapp, api_keys is imported as top-level by web_server
try:
    from api_keys import get_api_key
except ImportError:
    from pipecatapp.api_keys import get_api_key

app.dependency_overrides[get_api_key] = lambda: "valid_key"

@pytest.mark.asyncio
async def test_internal_chat_sync_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # We need a way to trigger the response while the request is pending.
        # Since the request awaits, we can use a background task to set the event.

        request_id = "test_req_1"
        payload = {"text": "Hello", "request_id": request_id, "response_url": "http://dummy"}

        # Define a background task that waits for the request to register in the store
        async def responder():
            for _ in range(10):
                if request_id in sync_response_store:
                    sync_response_store[request_id]["response"] = "Agent Response"
                    sync_response_store[request_id]["event"].set()
                    return
                await asyncio.sleep(0.1)

        # Start responder
        task = asyncio.create_task(responder())

        # Make request
        response = await ac.post("/internal/chat/sync", json=payload)

        # Wait for responder to finish (ensure it ran)
        await task

        assert response.status_code == 200
        assert response.json() == {"response": "Agent Response"}

@pytest.mark.asyncio
async def test_internal_chat_sync_timeout():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Patch wait_for to timeout immediately
        with patch("asyncio.wait_for", side_effect=asyncio.TimeoutError):
             response = await ac.post("/internal/chat/sync", json={"text": "Timeout Test", "request_id": "req_timeout", "response_url": "http://dummy"})
             assert response.status_code == 504
