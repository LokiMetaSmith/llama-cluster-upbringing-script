import unittest
import os
from unittest.mock import AsyncMock, patch, MagicMock

from pipecatapp.workflow.nodes.llm_nodes import discover_main_llm_service, SimpleLLMNode
from pipecatapp.workflow.context import WorkflowContext
from scripts.healer import HealerAgent


class TestVLLMDiscovery(unittest.IsolatedAsyncioTestCase):
    async def test_discover_main_llm_service_finds_vllm_main(self):
        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = mock_client

            # Return passing response for vllm-main
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = [{"Service": {"Address": "192.168.1.100", "Port": 8000}}]
            mock_client.get.return_value = mock_resp

            url = await discover_main_llm_service("http://localhost:8500")
            self.assertEqual(url, "http://192.168.1.100:8000/v1")
            mock_client.get.assert_called_with("http://localhost:8500/v1/health/service/vllm-main?passing", headers={}, timeout=2.0)

    async def test_simple_llm_node_discovers_vllm_main(self):
        node_config = {"id": "test_vllm_node", "type": "SimpleLLMNode", "model_tier": "balanced"}
        node = SimpleLLMNode(node_config)
        context = WorkflowContext({})
        context.global_inputs["consul_http_addr"] = "http://localhost:8500"

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = mock_client

            mock_consul_resp = MagicMock()
            mock_consul_resp.status_code = 200
            mock_consul_resp.json.return_value = [{"Service": {"Address": "10.0.0.10", "Port": 8000}}]
            mock_client.get.return_value = mock_consul_resp

            mock_llm_resp = MagicMock()
            mock_llm_resp.status_code = 200
            mock_llm_resp.json.return_value = {"choices": [{"message": {"content": "vLLM Response"}}]}
            mock_client.post.return_value = mock_llm_resp

            node.get_input = MagicMock(side_effect=lambda ctx, name: "Hello vLLM" if name == "user_text" else None)

            await node.execute(context)

            # Check that vllm-main was checked first
            mock_client.get.assert_called_with("http://localhost:8500/v1/health/service/vllm-main?passing", timeout=2.0)
            self.assertEqual(context.node_outputs["test_vllm_node"]["response"], "vLLM Response")

    async def test_healer_agent_resolves_vllm_main_fallback(self):
        agent = HealerAgent(consul_addr="http://localhost:8500", token="")
        with patch("scripts.healer.requests.get") as mock_get:
            # First call for primary service (e.g. rpc-coding) returns empty list
            resp_empty = MagicMock()
            resp_empty.status_code = 200
            resp_empty.json.return_value = []

            # Second call for fallback vllm-main returns service instance
            resp_vllm = MagicMock()
            resp_vllm.status_code = 200
            resp_vllm.json.return_value = [{"Service": {"Address": "10.0.0.20", "Port": 8000}}]

            mock_get.side_effect = [resp_empty, resp_vllm]

            base_url = await agent._resolve_service("rpc-coding")
            self.assertIsNone(base_url)

            # Check fallback loop logic in chat method
            base_url_fallback = await agent._resolve_service("vllm-main")
            self.assertEqual(base_url_fallback, "http://10.0.0.20:8000/v1")


if __name__ == "__main__":
    unittest.main()
