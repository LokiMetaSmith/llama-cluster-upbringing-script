import pytest
import sys
import os
from unittest.mock import MagicMock, patch
import json
import base64

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
    code_b64 = base64.b64encode(code.encode('utf-8')).decode('utf-8')

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

    # Check Template
    template = payload['Job']['TaskGroups'][0]['Tasks'][0]['Templates'][0]
    assert template['EmbeddedTmpl'] == code_b64
    assert template['DestPath'] == "local/script.b64"
    # Ensure delimiters are NOT set (using defaults)
    assert 'LeftDelim' not in template
    assert 'RightDelim' not in template

    # Check Command
    config = payload['Job']['TaskGroups'][0]['Tasks'][0]['Config']
    assert config['command'] == "/bin/sh"
    assert config['args'][0] == "-c"
    assert "base64.b64decode" in config['args'][1]
    assert "/local/script.b64" in config['args'][1]
    assert "/local/script.py" in config['args'][1]


    # Verify Cleanup
    mock_delete.assert_called_with("http://nomad.test:4646/v1/job/sandbox-test-job-id?purge=true", headers={}, timeout=10)

@patch('requests.post')
@patch('requests.get')
@patch('requests.delete')
@patch('uuid.uuid4')
def test_nomad_template_injection_prevention(mock_uuid, mock_delete, mock_get, mock_post, nomad_executor):
    """
    Tests that code containing Nomad template syntax is safely encoded
    and does not leak into the template definition as raw text.
    """
    # Setup
    mock_uuid.return_value = "injection-test-id"
    # Malicious code trying to access secrets via template injection
    malicious_code = "print('[[ .Secrets ]]') or {{ env \"NOMAD_TOKEN\" }}"

    # We expect the payload to contain the base64 version of this,
    # NOT the raw string which would trigger template rendering.
    expected_b64 = base64.b64encode(malicious_code.encode('utf-8')).decode('utf-8')

    mock_post.return_value.status_code = 200

    # Mock minimal success path for execution to avoid errors
    mock_get.return_value.json.return_value = [] # Just returns empty to break loop eventually or mock side effect

    # We just want to check the POST payload, so we can let it fail later or mock enough to pass
    # For this test, verifying the POST call is enough.
    # Let's mock a quick failure in allocation wait to exit early
    mock_get.side_effect = Exception("Stop execution after post")

    # Reduce timeout to fail fast
    nomad_executor.timeout = 0.1

    try:
        with patch('time.sleep'):
            nomad_executor.execute(malicious_code)
    except Exception:
        pass # Expected due to our mock side effect

    # Verify Payload
    args, kwargs = mock_post.call_args
    payload = kwargs['json']
    template = payload['Job']['TaskGroups'][0]['Tasks'][0]['Templates'][0]

    # CRITICAL SECURITY ASSERTION:
    # The EmbeddedTmpl must match the Base64 string.
    assert template['EmbeddedTmpl'] == expected_b64

    # The raw malicious code MUST NOT appear in the template body
    # (Checking if the template string itself contains the delimiters)
    # Since it is base64, it won't contain {{ or [[ unless by extreme chance in b64 alphabet (which doesn't have them)
    assert "[[" not in template['EmbeddedTmpl']
    assert "}}" not in template['EmbeddedTmpl']

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
