import pytest
import os
import asyncio
from pipecatapp.workflow.context import WorkflowContext
from pipecatapp.workflow.nodes.system_nodes import ComplexityEvaluatorNode
from pipecatapp.tools.vr_tool import VRTool

@pytest.mark.asyncio
async def test_complexity_evaluator_node(tmp_path):
    test_file = str(tmp_path / "sample.py")
    with open(test_file, "w") as f:
        f.write("def foo(x):\n    if x > 10:\n        for i in range(x):\n            if i % 2 == 0:\n                print(i)\n")

    node = ComplexityEvaluatorNode(config={"id": "comp_1", "inputs": [{"name": "filepath", "value": test_file}]})
    context = WorkflowContext(
        workflow_definition={"name": "test_wf", "nodes": [{"id": "comp_1", "inputs": [{"name": "filepath", "value": test_file}]}]}
    )

    await node.execute(context)

    score = context.node_outputs["comp_1"]["complexity_score"]
    sloc = context.node_outputs["comp_1"]["sloc"]
    report = context.node_outputs["comp_1"]["metrics_report"]

    assert score > 1
    assert sloc > 0
    assert report["cyclomatic_complexity"] == score
    assert "maintainability_index" in report

def test_vr_tool_steering_grid():
    vr = VRTool()
    nodes = ["node_a", "node_b", "node_c", "node_d"]
    grid = vr.compute_spatial_grid(nodes, use_procedural_steering=True)

    assert len(grid) == 4
    for node_id, pos in grid.items():
        assert "x" in pos
        assert "y" in pos
        assert "z" in pos
