import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import httpx

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from orchestrator_tool import OrchestratorTool

@pytest.fixture
def orchestrator_tool():
    return OrchestratorTool()

@patch('httpx.Client')
def test_dispatch_job_success(mock_client_cls, orchestrator_tool):
    mock_client = mock_client_cls.return_value.__enter__.return_value
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"job_id": "123"}
    mock_client.post.return_value = mock_response

    result = orchestrator_tool.dispatch_job("llama3", "prompt")
    assert result == {"job_id": "123"}

    mock_client.post.assert_called_once()
    args, kwargs = mock_client.post.call_args
    assert kwargs['json']['model_name'] == "llama3"

@patch('httpx.Client')
def test_dispatch_job_failure(mock_client_cls, orchestrator_tool):
    mock_client = mock_client_cls.return_value.__enter__.return_value

    # Simulate raise_for_status raising an error
    def raise_error():
        mock_resp = MagicMock()
        mock_resp.text = "Server Error"
        raise httpx.HTTPStatusError("Error", request=MagicMock(), response=mock_resp)

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = raise_error
    mock_client.post.return_value = mock_response

    result = orchestrator_tool.dispatch_job("llama3", "prompt")
    assert "Error dispatching job: Server Error" in result
