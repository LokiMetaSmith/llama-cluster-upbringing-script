import pytest
from pipecatapp.workflow.context import WorkflowContext
from pipecatapp.workflow.nodes.emperor_nodes import EmperorAgentNode
from pipecatapp.workflow.nodes.tasky_nodes import TaskyAuditNode
from pipecatapp.workflow.nodes.consolidation_nodes import ContinuousConsolidationNode
from pipecatapp.workflow.nodes.schema_nodes import HypothesizeNode
from pipecatapp.tools.ssd_streaming_tool import SSDStreamingTool

def test_ssd_streaming_tool(tmp_path):
    tool = SSDStreamingTool()

    # Test stream status
    status = tool.execute("stream_status")
    assert "Colibri NVMe io_uring" in status
    assert "ACTIVE" in status

    # Test weight prefetching
    model_file = str(tmp_path / "model.gguf")
    with open(model_file, "w") as f:
        f.write("mock gguf weights")

    prefetch = tool.execute("prefetch_weights", model_path=model_file, chunk_size_mb=32)
    assert "io_uring" in prefetch or "completed" in prefetch

@pytest.mark.asyncio
async def test_emperor_agent_node(mocker):
    mock_resp = mocker.MagicMock()
    mock_resp.status_code = 200
    mock_resp.json = lambda: {"choices": [{"message": {"content": "Emperor Decision: Proceed."}}]}

    mock_client = mocker.MagicMock()
    mock_client.post = mocker.AsyncMock(return_value=mock_resp)
    mock_client.get = mocker.AsyncMock(return_value=mocker.MagicMock(status_code=200, json=lambda: [{"Service": {"Address": "127.0.0.1", "Port": 8081}}]))
    mock_client.__aenter__ = mocker.AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = mocker.AsyncMock()

    mocker.patch("httpx.AsyncClient", return_value=mock_client)

    node = EmperorAgentNode(config={"id": "emp_1", "inputs": [{"name": "task", "value": "Orchestrate cluster upgrade"}]})
    context = WorkflowContext(
        workflow_definition={"name": "test_wf", "nodes": [{"id": "emp_1", "inputs": [{"name": "task", "value": "Orchestrate cluster upgrade"}]}]}
    )

    await node.execute(context)

    response = context.node_outputs["emp_1"]["response"]
    assert response is not None

@pytest.mark.asyncio
async def test_tasky_audit_node():
    node = TaskyAuditNode(config={"id": "task_1", "inputs": [{"name": "task_markdown", "value": "- [ ] Step 1"}, {"name": "execution_result", "value": "Step 1 complete"}]})
    context = WorkflowContext(
        workflow_definition={"name": "test_wf", "nodes": [{"id": "task_1", "inputs": [{"name": "task_markdown", "value": "- [ ] Step 1"}, {"name": "execution_result", "value": "Step 1 complete"}]}]}
    )

    await node.execute(context)

    report = context.node_outputs["task_1"]["audit_report"]
    assert report is not None

@pytest.mark.asyncio
async def test_consolidation_node(mocker):
    mock_memory = mocker.MagicMock()
    mock_memory.get_unconsolidated_memories.return_value = []

    node = ContinuousConsolidationNode(config={"id": "cons_1"})
    context = WorkflowContext(
        workflow_definition={"name": "test_wf", "nodes": [{"id": "cons_1"}]}
    )
    context.set_global_input("memory_store", mock_memory)

    await node.execute(context)

    count = context.node_outputs["cons_1"]["consolidated_count"]
    assert count == 0

@pytest.mark.asyncio
async def test_hypothesize_node():
    node = HypothesizeNode(config={"id": "hypo_1"})
    context = WorkflowContext(
        workflow_definition={"name": "test_wf", "nodes": [{"id": "hypo_1"}]}
    )

    await node.execute(context)

    code = context.node_outputs["hypo_1"]["world_model_code"]
    assert "def step" in code
