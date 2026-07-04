import pytest
import asyncio
from pipecatapp.llm_clients import ExternalLLMClient
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_ds4_think_stripping():
    client = ExternalLLMClient(base_url="http://ds4-server", api_key="test", model="ds4-model")

    mock_response = {
        "choices": [
            {
                "message": {
                    "content": "<think>\nI should answer this question directly.\n</think>\nThis is the actual answer."
                }
            }
        ]
    }

    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_response_obj = AsyncMock()
        mock_response_obj.json.return_value = mock_response
        mock_response_obj.status = 200
        mock_response_obj.__aenter__.return_value = mock_response_obj
        mock_post.return_value = mock_response_obj

        result = await client.process_text("Hello")

        assert result == "This is the actual answer."
        assert "<think>" not in result
        assert "I should answer" not in result

@pytest.mark.asyncio
async def test_no_think_stripping():
    client = ExternalLLMClient(base_url="http://other-server", api_key="test", model="other-model")

    mock_response = {
        "choices": [
            {
                "message": {
                    "content": "Just a normal response."
                }
            }
        ]
    }

    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_response_obj = AsyncMock()
        mock_response_obj.json.return_value = mock_response
        mock_response_obj.status = 200
        mock_response_obj.__aenter__.return_value = mock_response_obj
        mock_post.return_value = mock_response_obj

        result = await client.process_text("Hello")

        assert result == "Just a normal response."
