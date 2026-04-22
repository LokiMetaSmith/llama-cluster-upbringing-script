import pytest
import asyncio
from pipecatapp.workflow.nodes.tasky_nodes import TaskyAuditNode
from pipecatapp.workflow.context import WorkflowContext

@pytest.mark.asyncio
async def test_tasky_audit_node_no_markdown():
    node = TaskyAuditNode({"id": "test_node", "config": {}, "inputs": [{"name": "task_markdown", "value": ""}, {"name": "execution_result", "value": "done"}]})
    context = WorkflowContext({"nodes": [{"id": "test_node", "inputs": [{"name": "task_markdown", "value": ""}, {"name": "execution_result", "value": "done"}]}]})

    await node.execute(context)

    # We shouldn't use `get_input` to fetch outputs, outputs are stored in `context.node_outputs`
    assert context.node_outputs.get("test_node", {}).get("all_completed") is False
    assert "Error: No task_markdown provided" in context.node_outputs.get("test_node", {}).get("audit_report")

@pytest.mark.asyncio
async def test_tasky_audit_node_no_execution_result():
    node = TaskyAuditNode({"id": "test_node", "config": {}, "inputs": [{"name": "task_markdown", "value": "# Todo"}, {"name": "execution_result", "value": ""}]})
    context = WorkflowContext({"nodes": [{"id": "test_node", "inputs": [{"name": "task_markdown", "value": "# Todo"}, {"name": "execution_result", "value": ""}]}]})

    await node.execute(context)

    assert context.node_outputs.get("test_node", {}).get("all_completed") is False
    assert "Error: No execution_result provided" in context.node_outputs.get("test_node", {}).get("audit_report")
