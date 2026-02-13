import pytest
import sys
import os
from unittest.mock import MagicMock, patch
import json

# Add repo root to path to allow importing pipecatapp as a package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pipecatapp.tools.code_runner_tool import NomadSandboxExecutor, DockerSandboxExecutor, CodeRunnerTool

@pytest.fixture
def nomad_executor():
    with patch.dict('os.environ', {'NOMAD_ADDR': 'http://nomad.test:4646'}):
        return NomadSandboxExecutor()

@patch('requests.post')
@patch('requests.get')
@patch('requests.delete')
@patch('uuid.uuid4')
def test_nomad_execution_success(mock_uuid, mock_delete, mock_get, mock_post, nomad_executor):
    # Setup
    mock_uuid.return_value = "test-job-id"
    code = "print('hello')"

    # Mock Job Registration
    mock_post.return_value.status_code = 200

    # Mock Allocation Polling (First pending, then complete)
    mock_alloc_pending = MagicMock()
    mock_alloc_pending.json.return_value = []

    mock_alloc_complete = MagicMock()
    mock_alloc_complete.json.return_value = [{
        "ID": "alloc-123",
        "ClientStatus": "complete",
        "CreateTime": 1000,
        "NodeID": "node-1"
    }]

    # Mock Allocation Detail
    mock_alloc_detail = MagicMock()
    mock_alloc_detail.json.return_value = {
        "ID": "alloc-123",
        "ClientStatus": "complete",
        "CreateTime": 1000,
        "NodeID": "node-1"
    }

    # Mock Node Info
    mock_node_info = MagicMock()
    mock_node_info.json.return_value = {"HTTPAddr": "10.0.0.5:4646"}

    # Mock Logs
    mock_stdout = MagicMock()
    mock_stdout.status_code = 200
    mock_stdout.text = "hello\n"

    mock_stderr = MagicMock()
    mock_stderr.status_code = 200
    mock_stderr.text = ""

    # Sequence of GET calls:
    # 1. allocations (empty/pending)
    # 2. allocations (complete)
    # 3. allocation detail (for NodeID)
    # 4. node detail (for HTTPAddr)
    # 5. stdout
    # 6. stderr
    mock_get.side_effect = [
        mock_alloc_pending,
        mock_alloc_complete,
        mock_alloc_detail,
        mock_node_info,
        mock_stdout,
        mock_stderr
    ]

    # Execute
    result = nomad_executor.execute(code)

    # Verify
    assert "---STDOUT---\nhello" in result

    # Verify Job Registration Payload
    args, kwargs = mock_post.call_args
    assert args[0] == "http://nomad.test:4646/v1/jobs"
    payload = kwargs['json']
    assert payload['Job']['ID'] == "sandbox-test-job-id"
    template = payload['Job']['TaskGroups'][0]['Tasks'][0]['Templates'][0]
    assert template['EmbeddedTmpl'] == "print('hello')"
    assert template['LeftDelim'] == "[["
    assert template['RightDelim'] == "]]"

    # Verify Cleanup
    mock_delete.assert_called_with("http://nomad.test:4646/v1/job/sandbox-test-job-id?purge=true", headers={}, timeout=10)

def test_hybrid_mode_logic():
    with patch.dict('os.environ', {'SANDBOX_EXECUTOR': 'hybrid'}):
        tool = CodeRunnerTool()
        assert isinstance(tool.executor, NomadSandboxExecutor)
        assert hasattr(tool, 'fast_executor')
        assert isinstance(tool.fast_executor, DockerSandboxExecutor)

        # Test routing - Fast path
        tool.fast_executor.client = MagicMock()
        with patch.object(tool.fast_executor, 'execute_simple_python', return_value="fast") as mock_fast:
            res = tool.run_python_code("print('hi')")
            assert res == "fast"
            mock_fast.assert_called_once()

        # Test fallback
        tool.fast_executor.client = None
        with patch.object(tool.executor, 'execute', return_value="fallback") as mock_fallback:
             res = tool.run_python_code("print('hi')")
             assert res == "fallback"
             mock_fallback.assert_called_once()

        # Test slow path
        with patch.object(tool.executor, 'execute', return_value="slow") as mock_slow:
            res = tool.run_code_in_sandbox("print('hi')")
            assert res == "slow"
            mock_slow.assert_called_once()

def test_docker_mode_logic():
    with patch.dict('os.environ', {'SANDBOX_EXECUTOR': 'docker'}):
        tool = CodeRunnerTool()
        assert isinstance(tool.executor, DockerSandboxExecutor)
        assert not hasattr(tool, 'fast_executor')
