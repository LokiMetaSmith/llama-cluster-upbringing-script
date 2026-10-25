import pytest
import asyncio
from pipecatapp.workflow.context import WorkflowContext
from pipecatapp.workflow.nodes.tool_nodes import ToolExecutorNode
from pipecatapp.tools.frugal_sandbox_tool import FrugalSandboxTool
from pipecatapp.agent_factory import _safe_create

@pytest.mark.asyncio
async def test_tool_executor_resolves_from_tools_dict_in_global_inputs():
    """Verify ToolExecutorNode resolves tools when provided via tools_dict in global_inputs."""
    node_config = {
        "id": "test_executor",
        "type": "ToolExecutorNode",
        "inputs": [
            {
                "name": "tool_call_data",
                "value": {
                    "tool": "frugal_sandbox.run",
                    "args": {
                        "task_query": "Calculate sum 2+2",
                        "proposed_code": "print(2 + 2)"
                    }
                }
            }
        ]
    }
    wf_def = {"nodes": [node_config]}
    context = WorkflowContext(wf_def)
    
    sandbox_tool = FrugalSandboxTool()
    context.global_inputs["tools_dict"] = {"frugal_sandbox": sandbox_tool}
    
    node = ToolExecutorNode(node_config)
    await node.execute(context)
    result = context.node_outputs.get("test_executor", {}).get("tool_result")
    assert result is not None
    assert "4" in str(result)

@pytest.mark.asyncio
async def test_tool_executor_resolves_without_method_dot():
    """Verify ToolExecutorNode resolves default run method when tool string lacks dot."""
    node_config = {
        "id": "test_executor_nodot",
        "type": "ToolExecutorNode",
        "inputs": [
            {
                "name": "tool_call_data",
                "value": {
                    "tool": "frugal_sandbox",
                    "args": {
                        "task_query": "Calculate 3*3",
                        "proposed_code": "print(3 * 3)"
                    }
                }
            }
        ]
    }
    wf_def = {"nodes": [node_config]}
    context = WorkflowContext(wf_def)
    
    sandbox_tool = FrugalSandboxTool()
    context.global_inputs["tools"] = {"frugal_sandbox": sandbox_tool}
    
    node = ToolExecutorNode(node_config)
    await node.execute(context)
    result = context.node_outputs.get("test_executor_nodot", {}).get("tool_result")
    assert result is not None
    assert "9" in str(result)

@pytest.mark.asyncio
async def test_tool_executor_graceful_missing_tool():
    """Verify ToolExecutorNode handles missing tools gracefully without raising uncaught exception."""
    node_config = {
        "id": "test_executor_missing",
        "type": "ToolExecutorNode",
        "inputs": [
            {
                "name": "tool_call_data",
                "value": {
                    "tool": "non_existent_tool.run",
                    "args": {}
                }
            }
        ]
    }
    wf_def = {"nodes": [node_config]}
    context = WorkflowContext(wf_def)
    context.global_inputs["tools_dict"] = {}
    
    node = ToolExecutorNode(node_config)
    # Should not raise exception
    await node.execute(context)
    result = context.node_outputs.get("test_executor_missing", {}).get("tool_result")
    assert result is not None
    assert "Tool 'non_existent_tool' not found" in result

def test_agent_factory_safe_create():
    """Verify _safe_create catches errors without crashing."""
    def broken_factory():
        raise RuntimeError("simulated factory failure")
    
    res = _safe_create("broken_tool", broken_factory)
    assert res is None
