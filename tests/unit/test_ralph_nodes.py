import pytest
import os
import sys
from unittest.mock import MagicMock, AsyncMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pipecatapp')))

from pipecatapp.workflow.nodes.ralph_nodes import RalphLoopNode
from pipecatapp.workflow.context import WorkflowContext
import pipecatapp.tools.code_runner_tool # Import to make it mockable

@pytest.mark.asyncio
async def test_ralph_loop_success(mocker):
    config = {"id": "test_ralph", "type": "RalphLoopNode", "config": {"max_iterations": 2, "model_service": "rpc-test"}}
    node = RalphLoopNode(config)
    context = WorkflowContext(workflow_definition={})
    # Add mock input resolver
    context.get_input = MagicMock(return_value="write a python function")
    context.node_outputs["test_ralph"] = {}

    mock_client_instance = AsyncMock()
    mock_post_resp = MagicMock()
    mock_post_resp.json.return_value = {"choices": [{"message": {"content": "print('hello')"}}]}
    mock_client_instance.post.return_value = mock_post_resp

    mocker.patch('httpx.AsyncClient.__aenter__', return_value=mock_client_instance)

    mock_runner = MagicMock()
    mock_runner.run_code_in_sandbox.return_value = "hello\n"

    mocker.patch('pipecatapp.tools.code_runner_tool.CodeRunnerTool', return_value=mock_runner)

    await node.execute(context)

    assert "final_response" in context.node_outputs.get("test_ralph", {})
    assert "Success" in context.node_outputs["test_ralph"]["final_response"]

@pytest.mark.asyncio
async def test_ralph_loop_failure_then_success(mocker):
    config = {"id": "test_ralph", "type": "RalphLoopNode", "config": {"max_iterations": 2, "model_service": "rpc-test"}}
    node = RalphLoopNode(config)
    context = WorkflowContext(workflow_definition={})
    context.get_input = MagicMock(return_value="write a python function")
    context.node_outputs["test_ralph"] = {}

    mock_client_instance = AsyncMock()

    # First attempt: code fails
    mock_post_resp_1 = MagicMock()
    mock_post_resp_1.json.return_value = {"choices": [{"message": {"content": "print(a)"}}]}

    # Second attempt: code succeeds
    mock_post_resp_2 = MagicMock()
    mock_post_resp_2.json.return_value = {"choices": [{"message": {"content": "print('hello')"}}]}

    mock_client_instance.post.side_effect = [mock_post_resp_1, mock_post_resp_2]
    mocker.patch('httpx.AsyncClient.__aenter__', return_value=mock_client_instance)

    mock_runner = MagicMock()
    # First execution fails, second succeeds
    mock_runner.run_code_in_sandbox.side_effect = ["Error: name 'a' is not defined", "hello\n"]
    mocker.patch('pipecatapp.tools.code_runner_tool.CodeRunnerTool', return_value=mock_runner)

    await node.execute(context)

    assert "final_response" in context.node_outputs.get("test_ralph", {})
    assert "Success" in context.node_outputs["test_ralph"]["final_response"]
