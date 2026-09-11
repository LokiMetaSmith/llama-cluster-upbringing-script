"""
Unit tests for mini-swe-agent integration in pipecatapp.
"""

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from pipecatapp.services.mini_swe_service import MiniSWEService
from pipecatapp.tools.mini_swe_tool import MiniSWEAgentTool
from pipecatapp.workflow.nodes.tool_nodes import MiniSWEAgentNode
from pipecatapp.workflow.context import WorkflowContext
from pipecatapp.agent_factory import create_tools
from pipecatapp.api_keys import get_api_key
from pipecatapp.web_server import app


def test_mini_swe_service_init():
    service = MiniSWEService(
        model_name="openai/gpt-4o-mini",
        api_base="http://127.0.0.1:8081/v1",
        environment_type="docker",
        container_image="python:3.12-slim"
    )
    assert service.model_name == "openai/gpt-4o-mini"
    assert service.api_base == "http://127.0.0.1:8081/v1"
    assert service.environment_type == "docker"
    assert service.container_image == "python:3.12-slim"


@patch("pipecatapp.services.mini_swe_service.DefaultAgent")
@patch("pipecatapp.services.mini_swe_service.LitellmModel")
@patch("pipecatapp.services.mini_swe_service.DockerEnvironment")
def test_mini_swe_service_run_task_docker(mock_docker_env, mock_model, mock_agent):
    mock_agent_instance = MagicMock()
    mock_agent_instance.run.return_value = [{"step": 1, "action": "ls"}]
    mock_agent.return_value = mock_agent_instance

    service = MiniSWEService(environment_type="docker")
    res = service.run_task(task="Fix issue in main.py")

    assert res["status"] == "success"
    assert res["environment_type"] == "docker"
    assert res["trajectory"] == [{"step": 1, "action": "ls"}]
    mock_docker_env.assert_called_once()
    mock_agent_instance.run.assert_called_once_with("Fix issue in main.py")


@patch("pipecatapp.services.mini_swe_service.DefaultAgent")
@patch("pipecatapp.services.mini_swe_service.LitellmModel")
@patch("pipecatapp.services.mini_swe_service.LocalEnvironment")
def test_mini_swe_service_run_task_local(mock_local_env, mock_model, mock_agent):
    mock_agent_instance = MagicMock()
    mock_agent_instance.run.return_value = [{"step": 1, "action": "echo test"}]
    mock_agent.return_value = mock_agent_instance

    service = MiniSWEService(environment_type="local")
    res = service.run_task(task="Run local diagnostic script", environment_type="local")

    assert res["status"] == "success"
    assert res["environment_type"] == "local"
    assert res["trajectory"] == [{"step": 1, "action": "echo test"}]
    mock_local_env.assert_called_once()


def test_mini_swe_tool():
    mock_service = MagicMock()
    mock_service.run_task.return_value = {"status": "success", "trajectory": []}

    tool = MiniSWEAgentTool(service=mock_service)
    assert tool.name == "mini_swe_agent"
    schema = tool.get_schema()
    assert schema["function"]["name"] == "mini_swe_agent"

    res = tool.execute(task="Test task", environment_type="docker")
    assert res["status"] == "success"
    mock_service.run_task.assert_called_once_with(task="Test task", cwd=None, environment_type="docker")


@patch("sentence_transformers.SentenceTransformer")
def test_agent_factory_includes_mini_swe(mock_st):
    mock_instance = MagicMock()
    mock_instance.get_sentence_embedding_dimension.return_value = 384
    mock_st.return_value = mock_instance
    with patch("pipecatapp.tools.rag_tool.RAG_Tool", MagicMock()):
        with patch("pipecatapp.agent_factory.RAG_Tool", MagicMock()):
            with patch("pipecatapp.agent_factory.HA_Tool", MagicMock()):
                tools = create_tools(config={"tool_execution_mode": "local"})
                assert "mini_swe_agent" in tools
                assert isinstance(tools["mini_swe_agent"], MiniSWEAgentTool)


@pytest.mark.asyncio
async def test_mini_swe_agent_workflow_node():
    mock_service = MagicMock()
    mock_service.run_task.return_value = {"status": "success", "trajectory": [{"action": "pytest"}]}

    with patch("pipecatapp.tools.mini_swe_tool.MiniSWEService", return_value=mock_service):
        node = MiniSWEAgentNode(config={"id": "TestNode", "task": "Run tests"})
        context = WorkflowContext(workflow_definition={"id": "wf_test", "nodes": []})
        await node.execute(context)

        output = context.node_outputs.get("TestNode", {}).get("output")
        assert "success" in output
        assert "pytest" in output


def test_mini_swe_rest_api_endpoint():
    mock_service = MagicMock()
    mock_service.run_task.return_value = {"status": "success", "trajectory": []}

    app.dependency_overrides[get_api_key] = lambda: "ok"
    try:
        with patch("pipecatapp.services.mini_swe_service.MiniSWEService", return_value=mock_service):
            client = TestClient(app)
            response = client.post(
                "/api/agents/mini-swe/run",
                json={"task": "Refactor router.py", "environment_type": "docker"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
    finally:
        app.dependency_overrides.clear()
