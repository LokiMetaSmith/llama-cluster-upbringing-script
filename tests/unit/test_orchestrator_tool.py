import pytest
import sys
import os
import httpx
from unittest.mock import MagicMock, patch

# Add the tools directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from orchestrator_tool import OrchestratorTool

def test_orchestrator_tool_instantiation():
    """Tests that the OrchestratorTool class can be instantiated."""
    # Test default URL
    tool = OrchestratorTool()
    assert tool.world_model_url == "http://localhost:8000"

    # Test with environment variable
    os.environ["WORLD_MODEL_URL"] = "http://test:8000"
    try:
        tool = OrchestratorTool()
        assert tool.world_model_url == "http://test:8000"
    finally:
        if "WORLD_MODEL_URL" in os.environ:
            del os.environ["WORLD_MODEL_URL"]

@patch('httpx.Client')
def test_dispatch_job_success(mock_client_cls):
    """Tests successful job dispatch."""
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_client

    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "dispatched", "job_id": "123"}
    mock_client.post.return_value = mock_response

    tool = OrchestratorTool()
    result = tool.dispatch_job(model_name="test-model", prompt="hello")

    assert result == {"status": "dispatched", "job_id": "123"}

    mock_client.post.assert_called_once_with(
        "http://localhost:8000/dispatch-job",
        json={
            "model_name": "test-model",
            "prompt": "hello",
            "cpu": 1000,
            "memory": 4096,
            "gpu_count": 1,
            "context": "",
        },
    )
    mock_response.raise_for_status.assert_called_once()

@patch('httpx.Client')
def test_dispatch_job_failure(mock_client_cls):
    """Tests failed job dispatch."""
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_client

    mock_response = MagicMock()
    mock_response.text = "Internal Server Error"

    # Simulate HTTPStatusError
    error = httpx.HTTPStatusError("Error", request=MagicMock(), response=mock_response)
    mock_response.raise_for_status.side_effect = error
    mock_client.post.return_value = mock_response

    tool = OrchestratorTool()
    result = tool.dispatch_job(model_name="test-model", prompt="hello")

    assert "Error dispatching job: Internal Server Error" in result
