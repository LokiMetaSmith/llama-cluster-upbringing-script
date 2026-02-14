import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from pipecatapp.workflow.nodes.llm_nodes import LoopedReasoningNode
from pipecatapp.workflow.context import WorkflowContext

class MockWorkflowContext:
    def __init__(self):
        self.global_inputs = {"consul_http_addr": "http://localhost:8500"}
        self.node_outputs = {}
        # Minimal structure to satisfy get_input
        self.workflow_definition = {
            "nodes": [
                {
                    "id": "test_node",
                    "type": "LoopedReasoningNode",
                    "config": {"iterations": 2, "model_service": "rpc-main"},
                    "inputs": [{"name": "user_text", "value": "Test query"}]
                }
            ]
        }

    def get_input(self, node_id, name):
        if name == "user_text":
            return "Test query"
        return None

    def set_output(self, node_id, name, value):
        if node_id not in self.node_outputs:
            self.node_outputs[node_id] = {}
        self.node_outputs[node_id][name] = value


@pytest.mark.asyncio
async def test_looped_reasoning_execution():
    context = MockWorkflowContext()

    # Node configuration
    node_config = context.workflow_definition["nodes"][0]

    # Mock secret_manager in the target module
    with patch("pipecatapp.workflow.nodes.llm_nodes.secret_manager") as mock_secrets:
        mock_secrets.get_secret.return_value = "fake_token"

        # Mock httpx.AsyncClient
        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = mock_client

            # Setup responses
            # 1. Discovery response (GET)
            discovery_resp = MagicMock()
            discovery_resp.status_code = 200
            discovery_resp.json.return_value = [{
                "Service": {"Address": "127.0.0.1", "Port": 8080}
            }]

            # 2. Chat completion responses (POST)
            # We expect 1 initial call + 2 iteration calls = 3 calls

            # Response 1: Initial
            chat_resp1 = MagicMock()
            chat_resp1.status_code = 200
            chat_resp1.json.return_value = {
                "choices": [{"message": {"content": "Initial answer"}}]
            }

            # Response 2: Iteration 1
            chat_resp2 = MagicMock()
            chat_resp2.status_code = 200
            chat_resp2.json.return_value = {
                "choices": [{"message": {"content": "Refined answer 1"}}]
            }

            # Response 3: Iteration 2 (Final)
            chat_resp3 = MagicMock()
            chat_resp3.status_code = 200
            chat_resp3.json.return_value = {
                "choices": [{"message": {"content": "Final Answer"}}]
            }

            mock_client.get.return_value = discovery_resp
            mock_client.post.side_effect = [chat_resp1, chat_resp2, chat_resp3]

            # Instantiate Node
            # The Node class inherits from Node, which likely takes config in __init__
            # Let's check Node.__init__ signature if possible, but assuming standard:
            # class Node: def __init__(self, config): self.config = config; self.id = config["id"]

            # Re-read Node class to be sure about init
            # But based on usage in other files, it seems correct.

            node = LoopedReasoningNode(node_config)

            # Execute
            await node.execute(context)

            # Assertions
            # Verify outputs were set
            assert "test_node" in context.node_outputs
            outputs = context.node_outputs["test_node"]

            assert outputs["response"] == "Final Answer"
            assert "trace" in outputs
            assert "Iteration 0: Initial answer" in outputs["trace"]
            assert "Iteration 1: Refined answer 1" in outputs["trace"]
            assert "Iteration 2: Final Answer" in outputs["trace"]

            # Verify API calls
            mock_client.get.assert_called_once() # Discovery
            assert mock_client.post.call_count == 3 # 1 initial + 2 loops
