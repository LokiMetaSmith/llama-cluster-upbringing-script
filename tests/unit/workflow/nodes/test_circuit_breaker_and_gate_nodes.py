import pytest
from pipecatapp.workflow.context import WorkflowContext
from pipecatapp.workflow.nodes.system_nodes import CircuitBreakerNode, HITLGateNode

@pytest.mark.asyncio
async def test_circuit_breaker_node_normal():
    wf_def = {
        "name": "cb_test",
        "nodes": [
            {
                "id": "cb1",
                "type": "CircuitBreakerNode",
                "inputs": [
                    {"name": "identifier", "value": "agent_alpha"},
                    {"name": "limit", "value": "10"},
                    {"name": "window", "value": "60"}
                ]
            }
        ]
    }
    context = WorkflowContext(workflow_definition=wf_def)
    node = CircuitBreakerNode(config=wf_def["nodes"][0])
    await node.execute(context)

    status = context.node_outputs["cb1"]["status"]
    is_tripped = context.node_outputs["cb1"]["is_tripped"]
    assert status == "Normal"
    assert is_tripped is False

@pytest.mark.asyncio
async def test_circuit_breaker_node_tripped_halt():
    wf_def = {
        "name": "cb_tripped_test",
        "nodes": [
            {
                "id": "cb2",
                "type": "CircuitBreakerNode",
                "inputs": [
                    {"name": "identifier", "value": "agent_beta"},
                    {"name": "limit", "value": "5"},
                    {"name": "window", "value": "60"},
                    {"name": "current_count", "value": "5"}
                ],
                "config": {"halt_on_stopped": True}
            }
        ]
    }
    context = WorkflowContext(workflow_definition=wf_def)
    node = CircuitBreakerNode(config=wf_def["nodes"][0])

    with pytest.raises(ValueError, match="Circuit Breaker TRIPPED"):
        await node.execute(context)

    status = context.node_outputs["cb2"]["status"]
    is_tripped = context.node_outputs["cb2"]["is_tripped"]
    assert status == "Stopped"
    assert is_tripped is True

@pytest.mark.asyncio
async def test_hitl_gate_node_auto_approved():
    wf_def = {
        "name": "hitl_test",
        "nodes": [
            {
                "id": "hitl1",
                "type": "HITLGateNode",
                "inputs": [
                    {"name": "prompt", "value": "Approve production deploy?"},
                    {"name": "action_details", "value": "Deploy v2.0.0"}
                ]
            }
        ]
    }
    context = WorkflowContext(workflow_definition=wf_def)
    context.set_global_input("human_approval_granted", True)
    node = HITLGateNode(config=wf_def["nodes"][0])
    await node.execute(context)

    approval_status = context.node_outputs["hitl1"]["approval_status"]
    assert approval_status == "approved"

@pytest.mark.asyncio
async def test_hitl_gate_node_auto_rejected():
    wf_def = {
        "name": "hitl_test_reject",
        "nodes": [
            {
                "id": "hitl2",
                "type": "HITLGateNode",
                "inputs": [
                    {"name": "prompt", "value": "Purge database?"},
                    {"name": "action_details", "value": "Drop table users"}
                ]
            }
        ]
    }
    context = WorkflowContext(workflow_definition=wf_def)
    context.set_global_input("human_approval_granted", False)
    node = HITLGateNode(config=wf_def["nodes"][0])

    with pytest.raises(ValueError, match="HITL Gate HALT"):
        await node.execute(context)

    approval_status = context.node_outputs["hitl2"]["approval_status"]
    assert approval_status == "rejected"
