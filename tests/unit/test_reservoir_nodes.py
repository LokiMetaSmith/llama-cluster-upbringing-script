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


from pipecatapp.workflow.nodes.reservoir_nodes import ReservoirBenchmarkNode

@pytest.mark.asyncio
async def test_reservoir_benchmark_node_passing():
    # Setup test matrix that should pass
    activation_matrix = {
        "dimensions": [128, 128],
        "correlation_length": 0.9,
        "branches": 5,
        "substrate_state": "focused"
    }

    node_config = {
        "id": "benchmark_test",
        "type": "ReservoirBenchmarkNode",
        "inputs": [
            {"name": "activation_matrix", "global_input": "matrix"}
        ]
    }

    workflow_def = {"nodes": [node_config]}
    context = WorkflowContext(workflow_def)
    context.set_global_input("matrix", activation_matrix)

    node = ReservoirBenchmarkNode(node_config)
    await node.execute(context)

    results = context.node_outputs["benchmark_test"]["benchmark_results"]

    assert results["collimation_efficiency_snr"] > 80
    assert results["branch_reduction_rate"] == 75.0 # (20-5)/20 * 100
    assert results["passed"] is True

@pytest.mark.asyncio
async def test_reservoir_benchmark_node_failing():
    # Setup test matrix that should fail
    activation_matrix = {
        "dimensions": [128, 128],
        "correlation_length": 0.2,
        "branches": 18,
        "substrate_state": "scattered"
    }

    node_config = {
        "id": "benchmark_test_fail",
        "type": "ReservoirBenchmarkNode",
        "inputs": [
            {"name": "activation_matrix", "global_input": "matrix"}
        ]
    }

    workflow_def = {"nodes": [node_config]}
    context = WorkflowContext(workflow_def)
    context.set_global_input("matrix", activation_matrix)

    node = ReservoirBenchmarkNode(node_config)
    await node.execute(context)

    results = context.node_outputs["benchmark_test_fail"]["benchmark_results"]

    assert results["collimation_efficiency_snr"] == 0 # 0.2 * 100 - 30 penalty = < 0
    assert results["branch_reduction_rate"] == 10.0 # (20-18)/20 * 100
    assert results["passed"] is False
