import pytest
from pipecatapp.workflow.context import WorkflowContext
from pipecatapp.workflow.nodes.llm_nodes import SimpleLLMNode
from pipecatapp.workflow.nodes.research_nodes import FindNode, ValidateNode

@pytest.mark.asyncio
async def test_simple_llm_node(mocker):
    mock_health = mocker.MagicMock()
    mock_health.status_code = 200
    mock_health.json = lambda: [{"Service": {"Address": "127.0.0.1", "Port": 8081}}]

    mock_chat = mocker.MagicMock()
    mock_chat.status_code = 200
    mock_chat.json = lambda: {"choices": [{"message": {"content": "Mocked LLM Response"}}]}

    mock_client = mocker.MagicMock()
    mock_client.get = mocker.AsyncMock(return_value=mock_health)
    mock_client.post = mocker.AsyncMock(return_value=mock_chat)
    mock_client.__aenter__ = mocker.AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = mocker.AsyncMock()

    mocker.patch("httpx.AsyncClient", return_value=mock_client)

    node = SimpleLLMNode(config={"id": "llm_1", "inputs": [{"name": "prompt", "value": "Explain quantum computing"}]})
    context = WorkflowContext(
        workflow_definition={"name": "test_wf", "nodes": [{"id": "llm_1", "inputs": [{"name": "prompt", "value": "Explain quantum computing"}]}]}
    )
    context.set_global_input("consul_http_addr", "http://127.0.0.1:8500")

    await node.execute(context)

    response = context.node_outputs["llm_1"]["response"]
    assert response == "Mocked LLM Response"

@pytest.mark.asyncio
async def test_find_node(mocker):
    async def mock_perform_step(step, client):
        return ("completed", '[{"claim": "Claim 1", "source_url": "http://example.com"}]')

    mocker.patch("pipecatapp.worker_agent.WorkerAgent.perform_step", side_effect=mock_perform_step)

    node = FindNode(config={"id": "find_1", "inputs": [{"name": "research_topic", "value": "quantum computing"}]})
    context = WorkflowContext(
        workflow_definition={"name": "test_wf", "nodes": [{"id": "find_1", "inputs": [{"name": "research_topic", "value": "quantum computing"}]}]}
    )

    await node.execute(context)

    claims = context.node_outputs["find_1"]["claims"]
    assert len(claims) >= 1

@pytest.mark.asyncio
async def test_validate_node():
    node = ValidateNode(config={"id": "val_1", "inputs": [{"name": "judged_claims", "value": [{"claim": "Claim A", "source_url": "http://a.com"}]}]})
    context = WorkflowContext(
        workflow_definition={"name": "test_wf", "nodes": [{"id": "val_1", "inputs": [{"name": "judged_claims", "value": [{"claim": "Claim A", "source_url": "http://a.com"}]}]}]}
    )

    await node.execute(context)

    report = context.node_outputs["val_1"]["final_report"]
    assert "Claim A" in report
    assert "http://a.com" in report
