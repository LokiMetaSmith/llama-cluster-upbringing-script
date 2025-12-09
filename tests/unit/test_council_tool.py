import pytest
import sys
import os
import aiohttp
from unittest.mock import MagicMock, patch, AsyncMock

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from council_tool import CouncilTool

# Mock TwinService
class MockTwinService:
    def __init__(self):
        self.consul_http_addr = "http://localhost:8500"

@pytest.fixture
def council_tool():
    twin_service = MockTwinService()
    return CouncilTool(twin_service)

@pytest.mark.asyncio
async def test_discover_local_experts(council_tool):
    with patch('aiohttp.ClientSession.get') as mock_get:
        # Mock successful Consul response
        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp.json.return_value = [{'Service': {'Address': '127.0.0.1', 'Port': 8000}}]
        mock_get.return_value.__aenter__.return_value = mock_resp

        experts = await council_tool._discover_local_experts()

        # We expect it to try to find experts.
        # Since I'm mocking the return value for all calls to be the same,
        # it will find all known experts pointing to the same address.
        assert "main" in experts
        assert experts["main"] == "http://127.0.0.1:8000/v1"

@pytest.mark.asyncio
async def test_convene_council_no_experts(council_tool):
    with patch.object(council_tool, '_discover_local_experts', return_value={}):
        council_tool.openrouter_api_key = None
        council_tool.openrouter_models = []

        result = await council_tool.convene("test query")
        assert "no experts" in result

@pytest.mark.asyncio
async def test_query_model_success(council_tool):
    model_info = {"url": "http://test", "model": "test-model", "name": "test"}
    expected_response = "I am a model"

    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp.json.return_value = {'choices': [{'message': {'content': expected_response}}]}
        mock_post.return_value.__aenter__.return_value = mock_resp

        result = await council_tool._query_model(model_info, "hello")
        assert result == expected_response

@pytest.mark.asyncio
async def test_convene_council_full_flow(council_tool):
    # Mock finding one local expert
    with patch.object(council_tool, '_discover_local_experts', return_value={'main': 'http://local:8000/v1'}):

        # Mock _query_model to avoid actual HTTP calls
        # We need it to return different things for different stages if possible,
        # or just a standard response.
        with patch.object(council_tool, '_query_model', side_effect=[
            "Opinion 1", # Stage 1
            "Review 1",  # Stage 2
            "Final Answer" # Stage 3
        ]) as mock_query:

            result = await council_tool.convene("test query")

            assert result == "Final Answer"
            assert mock_query.call_count == 3
            # 1 (Stage 1) + 1 (Stage 2) + 1 (Stage 3) = 3 calls because only 1 expert
