import pytest
import sys
from unittest.mock import MagicMock, AsyncMock

# Mock langchain dependencies
sys.modules["langchain_core"] = MagicMock()
sys.modules["langchain_core.runnables"] = MagicMock()

from pipecatapp.workflow.nodes.langchain_nodes import LangGraphNode
from pipecatapp.workflow.context import WorkflowContext

@pytest.fixture
def mock_context():
    context = MagicMock(spec=WorkflowContext)
    context.global_inputs = {}
    context.runner_id = "test_runner"
    return context

@pytest.mark.asyncio
async def test_langgraph_node_execute_no_graph(mock_context):
    node = LangGraphNode({"id": "test_langgraph"})

    # Mock set_output
    node.set_output = MagicMock()

    await node.execute(mock_context)

    node.set_output.assert_called_once_with(mock_context, "error", "No compiled_langgraph provided in global inputs.")

@pytest.mark.asyncio
async def test_langgraph_node_execute_ainvoke(mock_context):
    node = LangGraphNode({"id": "test_langgraph", "inputs": [{"name": "input_var"}]})
    node.set_output = MagicMock()
    node.get_input = MagicMock(return_value="test_value")

    # Mock compiled graph with ainvoke
    mock_graph = MagicMock()
    mock_graph.ainvoke = AsyncMock(return_value={"messages": [MagicMock(content="async response")]})
    mock_context.global_inputs["compiled_langgraph"] = mock_graph

    await node.execute(mock_context)

    # Check ainvoke is called
    mock_graph.ainvoke.assert_called_once()
    assert not mock_graph.invoke.called

    # Check outputs are set correctly
    node.set_output.assert_any_call(mock_context, "response", "async response")
    node.set_output.assert_any_call(mock_context, "full_state", {"messages": [mock_graph.ainvoke.return_value["messages"][0]]})

@pytest.mark.asyncio
async def test_langgraph_node_execute_invoke_fallback(mock_context):
    node = LangGraphNode({"id": "test_langgraph"})
    node.set_output = MagicMock()

    # Mock compiled graph without ainvoke, only invoke
    mock_graph = MagicMock()
    del mock_graph.ainvoke
    mock_graph.invoke = MagicMock(return_value={"messages": [MagicMock(content="sync response")]})

    mock_context.global_inputs["compiled_langgraph"] = mock_graph
    mock_context.global_inputs["user_text"] = "hello"
    mock_context.global_inputs["tools_dict"] = {}

    await node.execute(mock_context)

    # Check invoke is called
    mock_graph.invoke.assert_called_once()

    # Check outputs are set correctly
    node.set_output.assert_any_call(mock_context, "response", "sync response")

@pytest.mark.asyncio
async def test_langgraph_node_execute_error(mock_context):
    node = LangGraphNode({"id": "test_langgraph"})
    node.set_output = MagicMock()

    mock_graph = MagicMock()
    mock_graph.ainvoke = AsyncMock(side_effect=Exception("Test Error"))
    mock_context.global_inputs["compiled_langgraph"] = mock_graph

    await node.execute(mock_context)

    # Check error is handled and output is set
    node.set_output.assert_any_call(mock_context, "error", "LangGraph execution failed: Test Error")
