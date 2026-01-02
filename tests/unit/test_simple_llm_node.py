import sys
from unittest.mock import MagicMock

# Mock pipecat before importing the module under test
sys.modules["pipecat"] = MagicMock()
sys.modules["pipecat.services"] = MagicMock()
sys.modules["pipecat.services.openai"] = MagicMock()
sys.modules["pipecat.services.openai.llm"] = MagicMock()

import unittest
import os
from unittest.mock import AsyncMock, patch
# Now we can import
from ansible.roles.pipecatapp.files.workflow.nodes.llm_nodes import SimpleLLMNode
from ansible.roles.pipecatapp.files.workflow.context import WorkflowContext

class TestSimpleLLMNode(unittest.IsolatedAsyncioTestCase):
    async def test_fast_tier_execution(self):
        # Setup
        node_config = {"id": "test_node", "type": "SimpleLLMNode", "model_tier": "fast"}
        node = SimpleLLMNode(node_config)

        context = WorkflowContext({})
        context.global_inputs["consul_http_addr"] = "http://localhost:8500"

        # Mocking
        with patch("httpx.AsyncClient") as MockClient:
            mock_client_instance = AsyncMock()
            MockClient.return_value.__aenter__.return_value = mock_client_instance

            # Mock Consul Discovery Response
            mock_consul_resp = MagicMock()
            mock_consul_resp.json.return_value = [{
                "Service": {"Address": "10.0.0.5", "Port": 8080}
            }]
            mock_consul_resp.raise_for_status.return_value = None

            # Mock LLM Chat Response
            mock_llm_resp = MagicMock()
            mock_llm_resp.json.return_value = {
                "choices": [{"message": {"content": "Fast Response"}}]
            }
            mock_llm_resp.raise_for_status.return_value = None

            # Set up side_effect to return distinct responses for distinct calls
            mock_client_instance.get.return_value = mock_consul_resp
            mock_client_instance.post.return_value = mock_llm_resp

            node.get_input = MagicMock(side_effect=lambda ctx, name: "Hello World" if name == "user_text" else None)

            await node.execute(context)

            # Verification
            # Check if Consul was queried for the correct service
            mock_client_instance.get.assert_called_with("http://localhost:8500/v1/health/service/llamacpp-rpc-router?passing")

            # Check Output
            self.assertEqual(context.node_outputs["test_node"]["response"], "Fast Response")

    async def test_balanced_tier_execution(self):
        # Setup
        node_config = {"id": "test_node_2", "type": "SimpleLLMNode", "model_tier": "balanced"}
        node = SimpleLLMNode(node_config)
        context = WorkflowContext({})
        context.global_inputs["consul_http_addr"] = "http://localhost:8500"

        # Mocking
        with patch("httpx.AsyncClient") as MockClient:
            mock_client_instance = AsyncMock()
            MockClient.return_value.__aenter__.return_value = mock_client_instance

            mock_consul_resp = MagicMock()
            port = int(os.getenv("ROUTER_PORT", 8081))
            mock_consul_resp.json.return_value = [{"Service": {"Address": "10.0.0.5", "Port": port}}]
            mock_client_instance.get.return_value = mock_consul_resp

            mock_llm_resp = MagicMock()
            mock_llm_resp.json.return_value = {"choices": [{"message": {"content": "Balanced Response"}}]}
            mock_client_instance.post.return_value = mock_llm_resp

            node.get_input = MagicMock(side_effect=lambda ctx, name: "Hello" if name == "user_text" else None)

            await node.execute(context)

            # Check if Consul was queried for the MAIN service
            mock_client_instance.get.assert_called_with("http://localhost:8500/v1/health/service/llamacpp-rpc-main?passing")

if __name__ == '__main__':
    unittest.main()
