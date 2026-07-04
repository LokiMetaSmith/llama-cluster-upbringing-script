import pytest
import asyncio
import aiohttp
from pipecatapp.llm_clients import ExternalLLMClient
from unittest.mock import MagicMock, patch

@pytest.mark.asyncio
async def test_external_llm_client_success():
    client = ExternalLLMClient(base_url="http://mock-api.com", api_key="test-key", model="test-model")

    mock_response_json = {
        "choices": [{"message": {"content": "Hello from mock!"}}]
    }

    class MockAsyncResponse:
        def __init__(self):
            self.status = 200
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass
        def raise_for_status(self):
            pass
        async def json(self):
            return mock_response_json

    with patch('aiohttp.ClientSession.post', return_value=MockAsyncResponse()):
        response = await client.process_text("Hi")
        assert response == "Hello from mock!"

    await client.close()

@pytest.mark.asyncio
async def test_external_llm_client_missing_key():
    client = ExternalLLMClient(base_url="http://mock-api.com", api_key="", model="test-model")
    response = await client.process_text("Hi")
    assert "Error: API key not configured" in response

@pytest.mark.asyncio
async def test_external_llm_client_error():
    client = ExternalLLMClient(base_url="http://mock-api.com", api_key="test-key", model="test-model")

    with patch('aiohttp.ClientSession.post', side_effect=aiohttp.ClientError("Connection failed")):
        response = await client.process_text("Hi")
        assert "Error: Could not connect" in response

    await client.close()
