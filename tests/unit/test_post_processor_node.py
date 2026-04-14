import pytest
from pipecatapp.workflow.nodes.base_nodes import PostProcessorNode
from pipecatapp.workflow.context import WorkflowContext

@pytest.mark.asyncio
async def test_post_processor_node_evaluate_data():
    config = {
        "id": "test_post_processor",
        "inputs": [
            {"name": "data"},
            {"name": "expression"}
        ]
    }
    node = PostProcessorNode(config)
    context = WorkflowContext({"nodes": []})

    def mock_get_input(ctx, name):
        if name == "data": return {"key": "value"}
        if name == "expression": return "data['key'] + '_modified'"
        raise ValueError()

    node.get_input = mock_get_input

    await node.execute(context)

    assert context.node_outputs[node.id]["processed_data"] == "value_modified"

@pytest.mark.asyncio
async def test_post_processor_node_evaluate_list_comp():
    config = {
        "id": "test_post_processor",
        "inputs": [
            {"name": "data"},
            {"name": "expression"}
        ]
    }
    node = PostProcessorNode(config)
    context = WorkflowContext({"nodes": []})

    def mock_get_input(ctx, name):
        if name == "data": return [{"a": 1}, {"a": 2}, {"a": 3}]
        if name == "expression": return "[x['a'] * 2 for x in data]"
        raise ValueError()

    node.get_input = mock_get_input

    await node.execute(context)

    assert context.node_outputs[node.id]["processed_data"] == [2, 4, 6]
