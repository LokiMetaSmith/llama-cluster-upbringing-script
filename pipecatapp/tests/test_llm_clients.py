import pytest
import asyncio
from pipecatapp.llm_clients import ExternalLLMClient
from unittest.mock import AsyncMock, patch, MagicMock

@pytest.mark.asyncio
async def test_cost_tracker():
    from pipecatapp.llm_clients import global_cost_tracker

    # Reset state for testing
    global_cost_tracker.total_cost = 0.0
    global_cost_tracker.usage_by_model = {}

    client = ExternalLLMClient(base_url="http://test", api_key="test", model="gpt-3.5-turbo")

    mock_response = {
        "choices": [
            {
                "message": {
                    "content": "Test response"
                }
            }
        ],
        "usage": {
            "prompt_tokens": 1000,
            "completion_tokens": 2000,
            "total_tokens": 3000
        }
    }

    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_response_obj = AsyncMock()
        mock_response_obj.json.return_value = mock_response
        mock_response_obj.raise_for_status = MagicMock()
        mock_response_obj.__aenter__.return_value = mock_response_obj
        mock_post.return_value = mock_response_obj

        result = await client.process_text("Hello")

        assert result == "Test response"

        # Verify usage was tracked
        summary = global_cost_tracker.get_summary()
        assert "gpt-3.5-turbo" in summary["usage_by_model"]
        model_usage = summary["usage_by_model"]["gpt-3.5-turbo"]

        assert model_usage["prompt_tokens"] == 1000
        assert model_usage["completion_tokens"] == 2000
        assert model_usage["total_tokens"] == 3000

        # Rate for gpt-3.5-turbo is 0.50 per 1M input, 1.50 per 1M output
        # 1000 input = $0.0005
        # 2000 output = $0.003
        # total = $0.0035
        assert abs(model_usage["estimated_cost"] - 0.0035) < 1e-6
        assert abs(summary["total_cost"] - 0.0035) < 1e-6

@pytest.mark.asyncio
async def test_downshifting():
    from pipecatapp.llm_clients import global_cost_tracker

    global_cost_tracker.total_cost = 10.0 # Exceeds budget
    global_cost_tracker.usage_by_model = {}

    client = ExternalLLMClient(
        base_url="http://test",
        api_key="test",
        model="gpt-4",
        budget_limit=5.0,
        fallback_model="gpt-3.5-turbo"
    )

    mock_response = {
        "choices": [{"message": {"content": "Downshifted response"}}],
        "usage": {"prompt_tokens": 100, "completion_tokens": 100, "total_tokens": 200}
    }

    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_response_obj = AsyncMock()
        mock_response_obj.json.return_value = mock_response
        mock_response_obj.raise_for_status = MagicMock()
        mock_response_obj.__aenter__.return_value = mock_response_obj
        mock_post.return_value = mock_response_obj

        result = await client.process_text("Hello")

        assert result == "Downshifted response"

        # Verify the API request was made with the fallback model
        _, kwargs = mock_post.call_args
        assert kwargs["json"]["model"] == "gpt-3.5-turbo"

        # Verify usage was tracked against the fallback model
        summary = global_cost_tracker.get_summary()
        assert "gpt-3.5-turbo" in summary["usage_by_model"]
        assert "gpt-4" not in summary["usage_by_model"]

@pytest.mark.asyncio
async def test_suspension():
    from pipecatapp.llm_clients import global_cost_tracker

    global_cost_tracker.total_cost = 10.0 # Exceeds budget
    global_cost_tracker.usage_by_model = {}

    client = ExternalLLMClient(
        base_url="http://test",
        api_key="test",
        model="gpt-4",
        budget_limit=5.0
        # No fallback model
    )

    with patch("aiohttp.ClientSession.post") as mock_post:
        result = await client.process_text("Hello")

        # The request shouldn't have been made
        mock_post.assert_not_called()
        assert result == "Error: Budget limit reached. Request suspended."

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
        mock_response_obj.raise_for_status = MagicMock()
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
        mock_response_obj.raise_for_status = MagicMock()
        mock_response_obj.__aenter__.return_value = mock_response_obj
        mock_post.return_value = mock_response_obj

        result = await client.process_text("Hello")

        assert result == "Just a normal response."
