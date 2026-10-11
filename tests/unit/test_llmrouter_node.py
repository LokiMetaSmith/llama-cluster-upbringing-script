import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import sys

# Mock llmrouter to bypass the ImportError
sys.modules['llmrouter'] = MagicMock()
sys.modules['llmrouter.models'] = MagicMock()

from pipecatapp.workflow.nodes.llm_nodes import LLMRouterNode
from pipecatapp.workflow.context import WorkflowContext

@pytest.fixture
def mock_workflow_definition():
    return {
        "id": "wf1",
        "nodes": [
            {
                "id": "test_router",
                "type": "LLMRouterNode",
                "inputs": [{"name": "user_text", "value": "write me a python script"}],
                "outputs": [{"name": "response", "value": None}]
            }
        ]
    }

@pytest.mark.asyncio
async def test_llm_router_node_heuristic_fallback_coder(mock_workflow_definition):
    node = LLMRouterNode(config={"id": "test_router", "name": "Test Router"})
    context = WorkflowContext(workflow_definition=mock_workflow_definition)
    # node.set_input is handled by context.get_input looking at workflow_definition
    context.global_inputs["consul_http_addr"] = "http://localhost:8500"

    with patch("os.path.exists", return_value=False), \
         patch("httpx.AsyncClient") as mock_client_cls, \
         patch("pipecatapp.workflow.nodes.llm_nodes.secret_manager") as mock_secret_manager:

        mock_secret_manager.get_secret.return_value = "fake_token"

        mock_client = mock_client_cls.return_value
        mock_instance = AsyncMock()
        mock_client.__aenter__.return_value = mock_instance

        # We need 2 mock responses:
        # 1. Consul health check for "rpc-coding"
        consul_response = MagicMock()
        consul_response.json.return_value = [{"Service": {"Address": "127.0.0.1", "Port": 8000}}]
        consul_response.raise_for_status = MagicMock()

        # 2. Actual LLM call to rpc-coding
        llm_response = MagicMock()
        llm_response.json.return_value = {"choices": [{"message": {"content": "Here is your python script"}}]}
        llm_response.raise_for_status = MagicMock()

        async def mock_get(*args, **kwargs):
            return consul_response

        async def mock_post(*args, **kwargs):
            return llm_response

        mock_instance.get.side_effect = mock_get
        mock_instance.post.side_effect = mock_post

        await node.execute(context)

        # Verify output
        assert "Here is your python script" in context.node_outputs["test_router"]["response"]

@pytest.mark.asyncio
async def test_llm_router_node_with_trained_model():
    mock_def = {
        "id": "wf1",
        "nodes": [
            {
                "id": "test_router",
                "type": "LLMRouterNode",
                "inputs": [{"name": "user_text", "value": "Some query"}],
                "outputs": [{"name": "response", "value": None}]
            }
        ]
    }
    node = LLMRouterNode(config={"id": "test_router", "name": "Test Router"})
    context = WorkflowContext(workflow_definition=mock_def)
    context.global_inputs["consul_http_addr"] = "http://localhost:8500"

    with patch("os.path.exists", return_value=True), \
         patch("llmrouter.models.KNNRouter") as mock_router_cls, \
         patch("httpx.AsyncClient") as mock_client_cls, \
         patch("pipecatapp.workflow.nodes.llm_nodes.secret_manager") as mock_secret_manager:

        mock_secret_manager.get_secret.return_value = "fake_token"

        # Mock LLMRouter response
        mock_router = mock_router_cls.return_value
        mock_router.route_single.return_value = {"model_name": "phi-3"}

        mock_client = mock_client_cls.return_value
        mock_instance = AsyncMock()
        mock_client.__aenter__.return_value = mock_instance

        # 1. Consul health check for "rpc-router"
        consul_response = MagicMock()
        consul_response.json.return_value = [{"Service": {"Address": "127.0.0.1", "Port": 8001}}]
        consul_response.raise_for_status = MagicMock()

        # 2. Actual LLM call
        llm_response = MagicMock()
        llm_response.json.return_value = {"choices": [{"message": {"content": "Phi-3 response"}}]}
        llm_response.raise_for_status = MagicMock()

        async def mock_get(*args, **kwargs):
            return consul_response

        async def mock_post(*args, **kwargs):
            return llm_response

        mock_instance.get.side_effect = mock_get
        mock_instance.post.side_effect = mock_post

        # Execute
        await node.execute(context)

        assert "Phi-3 response" in context.node_outputs["test_router"]["response"]
