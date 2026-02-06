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
from workflow.node import Node

@pytest.fixture
def mock_registry(mocker):
    # Mock the global registry to control which nodes are available in tests
    mock = MagicMock()
    mocker.patch('workflow.runner.registry', mock)
    return mock

@pytest.fixture(autouse=True)
def clear_workflow_cache():
    """Clears the workflow definition cache before each test."""
    WorkflowRunner._workflow_cache.clear()
    yield
    WorkflowRunner._workflow_cache.clear()

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
async def test_workflow_execution_data_flow(mock_registry, mocker):
    """Tests a simple workflow from end-to-end, verifying data is passed correctly."""

    # Define a simple workflow
    workflow_def = {
        "nodes": [
            {"id": "start", "type": "InputNode", "config": {"outputs": [{"name": "initial_data"}]}},
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

@pytest.mark.asyncio
async def test_tool_executor_node():
    """Tests that the ToolExecutorNode correctly calls a mocked tool."""
    from workflow.nodes.tool_nodes import ToolExecutorNode

    # Create a mock tool
    mock_tool = MagicMock()
    mock_tool.do_something = MagicMock(return_value="it worked")

    tools = {"my_tool": mock_tool}
    tool_call = {"tool": "my_tool.do_something", "args": {"foo": "bar"}}

    node = ToolExecutorNode({"id": "executor"})
    context = MagicMock(spec=WorkflowContext)
    context.global_inputs = {"tools": tools}

    def get_input_side_effect(node_id, input_name):
        if node_id == "executor" and input_name == "tool_call_data":
            return tool_call
        return None
    context.get_input.side_effect = get_input_side_effect

    await node.execute(context)

    # Verify the tool was called correctly
    mock_tool.do_something.assert_called_once_with(foo="bar")

    # Verify the output was set
    context.set_output.assert_called_with("executor", "tool_result", "it worked")

@pytest.mark.asyncio
async def test_workflow_tool_loop(mock_registry, mocker):
    """Tests a workflow with a tool call and verifies the result is fed back."""
    from workflow.nodes.base_nodes import MergeNode
    from workflow.nodes.tool_nodes import ToolExecutorNode

    class PromptBuilderNode(Node):
        """A simple mock PromptBuilderNode."""
        async def execute(self, context: WorkflowContext):
            tool_result = self.get_input(context, "tool_result")
            message = [{"text": tool_result}] if tool_result else []
            if not "messages" in context.node_outputs.get(self.id, {}):
                self.set_output(context, "messages", [])

            current_messages = context.node_outputs.get(self.id, {}).get("messages", [])
            current_messages.append({"role": "user", "content": message})
            self.set_output(context, "messages", current_messages)

    workflow_def = {
        "nodes": [
            {"id": "input", "type": "InputNode", "outputs": ["tool_result"]},
            {"id": "executor", "type": "ToolExecutorNode", "inputs": [{"name": "tool_call_data", "value": {"tool": "dummy.run", "args": {}}}]},
            {"id": "merger", "type": "MergeNode", "inputs": [{"name": "in1", "connection": {"from_node": "executor", "from_output": "tool_result"}}, {"name": "in2", "connection": {"from_node": "input", "from_output": "tool_result"}}]},
            {"id": "prompter", "type": "PromptBuilderNode", "inputs": [{"name": "tool_result", "connection": {"from_node": "merger", "from_output": "merged_output"}}]}
        ]
    }

    # Mock node classes
    mock_registry.get_node_class.side_effect = lambda type: {
        "InputNode": InputNode,
        "ToolExecutorNode": ToolExecutorNode,
        "MergeNode": MergeNode,
        "PromptBuilderNode": PromptBuilderNode,
    }.get(type)

    mocker.patch('builtins.open', mocker.mock_open(read_data=str(workflow_def)))
    mocker.patch('yaml.safe_load', return_value=workflow_def)

    runner = WorkflowRunner("dummy/path.yaml")

    # Mock the tool
    mock_dummy_tool = MagicMock()
    mock_dummy_tool.run = MagicMock(return_value="tool_output")

    # Run with no initial tool result
    await runner.run(global_inputs={"tool_result": None, "tools": {"dummy": mock_dummy_tool}})

    # Verify that the prompter received the tool's output
    assert runner.context.node_outputs["prompter"]["messages"][-1]["content"][0]["text"] == "tool_output"

@pytest.mark.asyncio
@pytest.mark.parametrize("tool_name_to_check, input_tool_call, expected_branch", [
    ("route_to_expert", {"tool": "route_to_expert"}, "output_true"),
    ("route_to_expert", {"tool": "other_tool"}, "output_false"),
    ("some_tool", {"tool": "some_other_tool"}, "output_false"),
    ("my_tool", None, "output_false"),
])
async def test_conditional_branch_node_tool_check(tool_name_to_check, input_tool_call, expected_branch):
    """Tests the ConditionalBranchNode's tool checking functionality."""
    from workflow.nodes.base_nodes import ConditionalBranchNode

    config = {"id": "branch", "check_if_tool_is": tool_name_to_check}
    node = ConditionalBranchNode(config)
    context = MagicMock(spec=WorkflowContext)
    context.get_input.return_value = input_tool_call

    await node.execute(context)

    outputs = {}
    for call in context.set_output.call_args_list:
        args = call.args
        outputs[args[1]] = args[2]

    if expected_branch == "output_true":
        assert outputs.get("output_true") == input_tool_call
        assert outputs.get("output_false") is None
    else:
        assert outputs.get("output_true") is None
        assert outputs.get("output_false") == input_tool_call

@pytest.mark.asyncio
async def test_nested_output_resolution(mock_registry, mocker):
    """Tests that a workflow with nested connections in the output resolves correctly."""
    workflow_def = {
        "nodes": [
            {"id": "source1", "type": "InputNode", "config": {"outputs": ["out1"]}},
            {"id": "source2", "type": "InputNode", "config": {"outputs": ["out2"]}},
            {"id": "output", "type": "OutputNode", "inputs": [{
                "name": "final_output",
                "value": {
                    "key1": {"connection": {"from_node": "source1", "from_output": "out1"}},
                    "key2": {"connection": {"from_node": "source2", "from_output": "out2"}}
                }
            }]}
        ]
    }

    mock_registry.get_node_class.side_effect = lambda type: {"InputNode": InputNode, "OutputNode": OutputNode}.get(type)
    mocker.patch('builtins.open', mocker.mock_open(read_data=str(workflow_def)))
    mocker.patch('yaml.safe_load', return_value=workflow_def)

    runner = WorkflowRunner("dummy/path.yaml")

    result = await runner.run(global_inputs={"out1": "hello", "out2": "world"})

    assert result == {"key1": "hello", "key2": "world"}
