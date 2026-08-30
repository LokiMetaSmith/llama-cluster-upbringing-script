import pytest
from pipecatapp.tools.unit_reasoning_tool import UnitReasoningTool
from pipecatapp.workflow.nodes.system_nodes import ComfyUIBridgeNode
from pipecatapp.workflow.context import WorkflowContext

def test_unit_reasoning_tool():
    tool = UnitReasoningTool()

    res_m = tool.execute("meters_to_feet", 10)
    assert "32.8084" in res_m

    res_temp = tool.execute("celsius_to_fahrenheit", 0)
    assert "32.0" in res_temp

    res_err = tool.execute("invalid_type", 100)
    assert "Error: Unknown conversion type" in res_err

@pytest.mark.asyncio
async def test_comfyui_bridge_node():
    node = ComfyUIBridgeNode(config={"id": "comfy_1", "inputs": [{"name": "prompt", "value": "A Cyberpunk City"}]})
    context = WorkflowContext(
        workflow_definition={"name": "test_wf", "nodes": [{"id": "comfy_1", "inputs": [{"name": "prompt", "value": "A Cyberpunk City"}]}]}
    )

    await node.execute(context)

    img_url = context.node_outputs["comfy_1"]["image_url"]
    status = context.node_outputs["comfy_1"]["status"]

    assert img_url is not None
    assert status is not None
