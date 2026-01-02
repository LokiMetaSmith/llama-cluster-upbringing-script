import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import sys
import os
import asyncio

# Add the path to the app files directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ansible/roles/pipecatapp/files')))

from tools.prompt_improver_tool import PromptImproverTool

class TestPromptImproverTool(unittest.TestCase):
    def setUp(self):
        self.mock_twin_service = MagicMock()
        self.mock_twin_service.consul_http_addr = "http://localhost:8500"
        self.tool = PromptImproverTool(self.mock_twin_service)

    @patch('tools.prompt_improver_tool.httpx.AsyncClient')
    def test_create_prompt_plan(self, mock_async_client):
        # Mock client context manager
        mock_client_instance = AsyncMock()
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        mock_async_client.return_value.__aexit__.return_value = None

        # Mock discovery response
        mock_discovery_response = MagicMock()
        port = int(os.getenv("ROUTER_PORT", 8081))
        mock_discovery_response.json.return_value = [{
            'Service': {'Address': '127.0.0.1', 'Port': port}
        }]
        mock_discovery_response.raise_for_status = MagicMock()

        # Mock LLM responses
        mock_llm_response_1 = MagicMock()
        mock_llm_response_1.json.return_value = {"choices": [{"message": {"content": "One Pager Content"}}]}
        mock_llm_response_1.raise_for_status = MagicMock()

        mock_llm_response_2 = MagicMock()
        mock_llm_response_2.json.return_value = {"choices": [{"message": {"content": "Dev Spec Content"}}]}
        mock_llm_response_2.raise_for_status = MagicMock()

        mock_llm_response_3 = MagicMock()
        mock_llm_response_3.json.return_value = {"choices": [{"message": {"content": "Prompt Plan Content"}}]}
        mock_llm_response_3.raise_for_status = MagicMock()

        # Configure side effects for get and post
        # Note: get is called for discovery before each post
        mock_client_instance.get.return_value = mock_discovery_response
        mock_client_instance.post.side_effect = [mock_llm_response_1, mock_llm_response_2, mock_llm_response_3]

        # Run async test
        result = asyncio.run(self.tool.create_prompt_plan("My idea"))

        self.assertEqual(result, "Prompt Plan Content")
        self.assertEqual(mock_client_instance.get.call_count, 3) # Discovery called 3 times
        self.assertEqual(mock_client_instance.post.call_count, 3) # LLM called 3 times

    @patch('tools.prompt_improver_tool.httpx.AsyncClient')
    def test_discover_llm_failure(self, mock_async_client):
        # Mock client context manager
        mock_client_instance = AsyncMock()
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance
        mock_async_client.return_value.__aexit__.return_value = None

        mock_client_instance.get.side_effect = Exception("Consul error")

        # Use _call_llm directly to test discovery failure handling
        result = asyncio.run(self.tool._call_llm("test"))
        self.assertEqual(result, "Error: LLM service not found.")

if __name__ == '__main__':
    unittest.main()
