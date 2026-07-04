import pytest
import sys
import os
from unittest.mock import MagicMock, patch
import json
import base64
import asyncio
import aiohttp

# Add repo root to path to allow importing pipecatapp as a package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pipecatapp.tools.code_runner_tool import NomadSandboxExecutor, DockerSandboxExecutor, CodeRunnerTool

@pytest.fixture
def nomad_executor():
    with patch.dict('os.environ', {'NOMAD_ADDR': 'http://nomad.test:4646'}):
        return NomadSandboxExecutor()

class MockAsyncResponse:
    def __init__(self, json_data=None, text_data=None, status=200):
        self.json_data = json_data
        self.text_data = text_data
        self.status = status
    async def __aenter__(self): return self
    async def __aexit__(self, *args): pass
    def raise_for_status(self): pass
    async def json(self): return self.json_data
    async def text(self): return self.text_data

@pytest.mark.asyncio
async def test_nomad_execution_success(nomad_executor):
    # Setup
    code = "print('hello success')"
    code_b64 = base64.b64encode(code.encode('utf-8')).decode('utf-8')

    with patch('aiohttp.ClientSession.post') as mock_post, \
         patch('aiohttp.ClientSession.get') as mock_get, \
         patch('aiohttp.ClientSession.delete') as mock_delete, \
         patch('uuid.uuid4', return_value="test-job-id"):

        mock_post.return_value = MockAsyncResponse({"EvalID": "eval-123"})

        mock_get.side_effect = [
            MockAsyncResponse([{
                "ID": "alloc-123",
                "ClientStatus": "complete",
                "CreateTime": 1000,
                "NodeID": "node-1"
            }]), # allocations
            MockAsyncResponse({
                "NodeID": "node-1"
            }), # allocation detail
            MockAsyncResponse({"HTTPAddr": "10.0.0.5:4646"}), # node detail
            MockAsyncResponse({}, text_data="hello success\n"), # stdout
            MockAsyncResponse({}, text_data="") # stderr
        ]
        mock_delete.return_value = MockAsyncResponse({})

        result = await nomad_executor.execute(code)
        assert "---STDOUT---\nhello success" in result

@pytest.mark.asyncio
async def test_nomad_template_injection_prevention(nomad_executor):
    """
    Tests that code containing Nomad template syntax is safely encoded
    and does not leak into the template definition as raw text.
    """
    # Setup
    malicious_code = "print('[[ .Secrets ]]') or {{ env \"NOMAD_TOKEN\" }}"
    expected_b64 = base64.b64encode(malicious_code.encode('utf-8')).decode('utf-8')

    with patch('aiohttp.ClientSession.post') as mock_post, \
         patch('aiohttp.ClientSession.get') as mock_get, \
         patch('aiohttp.ClientSession.delete') as mock_delete, \
         patch('uuid.uuid4', return_value="injection-test-id"):

        mock_post.return_value = MockAsyncResponse({"EvalID": "eval-123"})

        # Return a failed status immediately to break the wait loop
        mock_get.return_value = MockAsyncResponse([{
            "ID": "alloc-123",
            "ClientStatus": "failed",
            "CreateTime": 1000
        }])
        mock_delete.return_value = MockAsyncResponse({})

        # We don't care about the final logs, just the payload sent in post
        await nomad_executor.execute(malicious_code)

        # Verify Payload
        args, kwargs = mock_post.call_args
        payload = kwargs['json']
        template = payload['Job']['TaskGroups'][0]['Tasks'][0]['Templates'][0]

        # CRITICAL SECURITY ASSERTION:
        assert template['EmbeddedTmpl'] == expected_b64
        assert "[[" not in template['EmbeddedTmpl']
        assert "}}" not in template['EmbeddedTmpl']

@pytest.mark.asyncio
async def test_hybrid_mode_logic():
    with patch.dict('os.environ', {'SANDBOX_EXECUTOR': 'hybrid'}):
        tool = CodeRunnerTool()
        assert isinstance(tool.executor, NomadSandboxExecutor)

        # Test routing - Fast path
        tool.fast_executor = MagicMock()
        tool.fast_executor.client = True
        tool.fast_executor.execute_simple_python.return_value = "fast"

        res = await tool.run_python_code("print('hi fast')")
        assert res == "fast"

        # Test fallback
        tool.fast_executor.client = None

        # Mock executor.execute since it's async
        async def mock_exec(*args, **kwargs): return "fallback"
        with patch.object(tool.executor, 'execute', side_effect=mock_exec):
            res = await tool.run_python_code("print('hi fallback')")
            assert res == "fallback"

def test_docker_mode_logic():
    with patch.dict('os.environ', {'SANDBOX_EXECUTOR': 'docker'}):
        tool = CodeRunnerTool()
        assert isinstance(tool.executor, DockerSandboxExecutor)
