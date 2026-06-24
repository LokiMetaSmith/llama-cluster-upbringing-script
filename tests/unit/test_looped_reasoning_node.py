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


def test_looped_reasoning_execution():
    import asyncio
    async def run_test():
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
                mock_client.get.return_value = discovery_resp

                chat_resp1 = MagicMock()
                chat_resp1.status_code = 200
                chat_resp1.json.return_value = {
                    "choices": [{"message": {"content": "Initial answer"}}]
                }

                judge_resp1 = MagicMock()
                judge_resp1.status_code = 200
                judge_resp1.json.return_value = {
                    "choices": [{"message": {"content": '{"status": "FAIL", "critique": "Needs more detail"}'}}]
                }

                chat_resp2 = MagicMock()
                chat_resp2.status_code = 200
                chat_resp2.json.return_value = {
                    "choices": [{"message": {"content": "Refined answer 1"}}]
                }

                judge_resp2 = MagicMock()
                judge_resp2.status_code = 200
                judge_resp2.json.return_value = {
                    "choices": [{"message": {"content": '{"status": "PASS", "critique": ""}'}}]
                }

                mock_client.post.side_effect = [chat_resp1, judge_resp1, chat_resp2, judge_resp2]

                node = LoopedReasoningNode(node_config)
                await node.execute(context)

                assert "test_node" in context.node_outputs
                outputs = context.node_outputs["test_node"]

                assert outputs["response"] == "Refined answer 1"
                assert "trace" in outputs
                assert "Iteration 0: Initial answer" in outputs["trace"]
                assert "Judge Evaluation 1: Status=FAIL" in outputs["trace"]
                assert "Iteration 1: Refined answer 1" in outputs["trace"]
                assert "Judge Evaluation 2: Status=PASS" in outputs["trace"]

                assert mock_client.post.call_count == 4

    asyncio.run(run_test())