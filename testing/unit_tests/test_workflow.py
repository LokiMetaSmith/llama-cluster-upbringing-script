import pytest
import os
import sys
from unittest.mock import MagicMock, AsyncMock

# Add the necessary path to import the workflow modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files')))

from workflow.runner import WorkflowRunner
from workflow.context import WorkflowContext
from workflow.nodes.base_nodes import InputNode, OutputNode
from workflow.nodes.tool_nodes import ToolParserNode

@pytest.fixture
def mock_registry(mocker):
    # Mock the global registry to control which nodes are available in tests
    mock = MagicMock()
    mocker.patch('workflow.runner.registry', mock)
    return mock

def test_topological_sort_linear(mocker):
    """Tests that a simple linear workflow is sorted correctly."""
    workflow_def = {
        "nodes": [
            # Intentionally out of order to test the sort
            {"id": "node3", "type": "OutputNode", "inputs": [{"name": "in1", "connection": {"from_node": "node2", "from_output": "out1"}}]},
            {"id": "node2", "type": "MiddleNode", "inputs": [{"name": "in1", "connection": {"from_node": "node1", "from_output": "out1"}}], "outputs": [{"name": "out1"}]},
            {"id": "node1", "type": "InputNode", "outputs": [{"name": "out1"}]},
        ]
    }
    mocker.patch('builtins.open', mocker.mock_open(read_data=str(workflow_def)))
    mocker.patch('yaml.safe_load', return_value=workflow_def)

    runner = WorkflowRunner("dummy/path.yaml")
    order = runner._get_execution_order()
    assert order == ["node1", "node2", "node3"]

def test_topological_sort_with_cycle(mocker):
    """Tests that the topological sort correctly identifies a cycle."""
    workflow_def = {
        "nodes": [
            {"id": "node1", "type": "NodeA", "inputs": [{"name": "in1", "connection": {"from_node": "node3", "from_output": "out1"}}], "outputs": [{"name": "out1"}]},
            {"id": "node2", "type": "NodeB", "inputs": [{"name": "in1", "connection": {"from_node": "node1", "from_output": "out1"}}], "outputs": [{"name": "out1"}]},
            {"id": "node3", "type": "NodeC", "inputs": [{"name": "in1", "connection": {"from_node": "node2", "from_output": "out1"}}], "outputs": [{"name": "out1"}]}
        ]
    }
    mocker.patch('builtins.open', mocker.mock_open(read_data=str(workflow_def)))
    mocker.patch('yaml.safe_load', return_value=workflow_def)

    runner = WorkflowRunner("dummy/path.yaml")
    with pytest.raises(ValueError, match="Workflow contains a cycle"):
        runner._get_execution_order()

@pytest.mark.asyncio
async def test_workflow_execution_data_flow(mock_registry):
    """Tests a simple workflow from end-to-end, verifying data is passed correctly."""

    # Define a simple workflow
    workflow_def = {
        "nodes": [
            {"id": "start", "type": "InputNode", "outputs": [{"name": "initial_data"}]},
            {"id": "end", "type": "OutputNode", "inputs": [{"name": "final_output", "connection": {"from_node": "start", "from_output": "initial_data"}}]}
        ]
    }

    # Mock node classes
    mock_registry.get_node_class.side_effect = lambda type: {
        "InputNode": InputNode,
        "OutputNode": OutputNode
    }.get(type)

    mocker.patch('builtins.open', mocker.mock_open(read_data=str(workflow_def)))
    mocker.patch('yaml.safe_load', return_value=workflow_def)

    runner = WorkflowRunner("dummy/path.yaml")

    # Run the workflow with a global input
    result = await runner.run(global_inputs={"initial_data": "hello world"})

    # Assert that the final output is what we expect
    assert result == "hello world"

@pytest.mark.asyncio
@pytest.mark.parametrize("response, expected_tool_call, expected_final_response", [
    ('{"tool": "test.do_thing", "args": {"arg1": "val1"}}', {"tool": "test.do_thing", "args": {"arg1": "val1"}}, None),
    ('This is a plain text response.', None, 'This is a plain text response.'),
    ('{"not_a_tool": "just_json"}', None, '{"not_a_tool": "just_json"}'),
    ('This is not json.', None, 'This is not json.')
])
async def test_tool_parser_node(response, expected_tool_call, expected_final_response):
    """Tests that the ToolParserNode correctly identifies tool calls and text responses."""
    node = ToolParserNode({"id": "parser"})
    context = MagicMock(spec=WorkflowContext)

    # Mock the get_input method
    def get_input_side_effect(node_id, input_name):
        if node_id == "parser" and input_name == "llm_response":
            return response
        return None
    context.get_input.side_effect = get_input_side_effect

    # Execute the node
    await node.execute(context)

    # Verify that set_output was called with the correct values
    # We create a dictionary of the calls to set_output for easier assertion
    outputs = {}
    for call in context.set_output.call_args_list:
        args = call.args
        outputs[args[1]] = args[2]

    assert outputs.get("tool_call_data") == expected_tool_call
    assert outputs.get("final_response") == expected_final_response
