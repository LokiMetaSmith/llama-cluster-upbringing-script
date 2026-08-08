import pytest
from pipecatapp.workflow.nodes.reservoir_nodes import ReservoirSubstrateNode
from pipecatapp.workflow.context import WorkflowContext

@pytest.mark.asyncio
async def test_reservoir_substrate_node_without_hdl():
    # Setup test node
    node_config = {
        "id": "reservoir_test",
        "type": "ReservoirSubstrateNode",
        "inputs": [
            {"name": "input_signal", "global_input": "signal"},
            {"name": "hdl_modulation", "global_input": "modulation"}
        ]
    }

    workflow_def = {
        "nodes": [node_config]
    }

    context = WorkflowContext(workflow_def)
    context.set_global_input("signal", "Test Signal")
    context.set_global_input("modulation", None) # No modulation

    node = ReservoirSubstrateNode(node_config)
    await node.execute(context)

    activation_matrix = context.node_outputs["reservoir_test"]["activation_matrix"]
    assert activation_matrix["correlation_length"] == 0.5
    assert activation_matrix["substrate_state"] == "scattered"

@pytest.mark.asyncio
async def test_reservoir_substrate_node_with_hdl():
    # Setup test node
    node_config = {
        "id": "reservoir_test",
        "type": "ReservoirSubstrateNode",
        "inputs": [
            {"name": "input_signal", "global_input": "signal"},
            {"name": "hdl_modulation", "global_input": "modulation"}
        ]
    }

    workflow_def = {
        "nodes": [node_config]
    }

    context = WorkflowContext(workflow_def)
    context.set_global_input("signal", "Test Signal")
    context.set_global_input("modulation", "tune correlation length") # With modulation

    node = ReservoirSubstrateNode(node_config)
    await node.execute(context)

    activation_matrix = context.node_outputs["reservoir_test"]["activation_matrix"]
    assert activation_matrix["correlation_length"] == 0.8
    assert activation_matrix["substrate_state"] == "focused"
