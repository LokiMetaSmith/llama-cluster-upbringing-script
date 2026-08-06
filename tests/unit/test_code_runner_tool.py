import pytest
from unittest.mock import MagicMock, patch
import asyncio
import os
import sys
import json
import base64
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pipecatapp.tools.code_runner_tool import CodeRunnerTool, DockerSandboxExecutor

import tempfile

# Add repo root to path to allow importing pipecatapp as a package

from pipecatapp.tools.code_runner_tool import CodeRunnerTool, DockerSandboxExecutor

@pytest.fixture
def code_runner():
    with patch('pipecatapp.tools.code_runner_tool.docker') as mock_docker:
        mock_from_env = mock_docker.from_env
        # Create a fresh tool instance for each test to ensure clean state
        runner = CodeRunnerTool()
        runner.history.db_path = ':memory:'
        runner.history._init_db()
        # Mock the client on the executor
        if isinstance(runner.executor, DockerSandboxExecutor):
            # Use the mock from from_env
            runner.executor.client = mock_from_env.return_value
            # Alias for tests expecting runner.client
            runner.client = runner.executor.client
        yield runner

@patch('pipecatapp.tools.code_runner_tool.multiprocessing.Process')
@patch('pipecatapp.tools.code_runner_tool.multiprocessing.Queue')
@patch('pipecatapp.tools.code_runner_tool.SandboxSession')
@pytest.mark.asyncio
async def test_run_code_in_sandbox_success(mock_sandbox_session, mock_queue, mock_process, code_runner):
    """
    Test that run_code_in_sandbox successfully executes Python code via llm-sandbox.
    """
    code_to_run = "print('hello sandbox')"
    expected_output = "hello sandbox\n"

    # Mock the Queue so q.get() returns our expected result
    mock_q = MagicMock()
    mock_q.empty.return_value = False
    mock_q.get.return_value = (0, expected_output, "", [])
    mock_queue.return_value = mock_q

    mock_p = MagicMock()
    mock_p.is_alive.return_value = False
    mock_process.return_value = mock_p

    result = await code_runner.run_code_in_sandbox(code=code_to_run, language="python")

    assert result == expected_output
    mock_p.start.assert_called_once()
    mock_p.join.assert_called_with(30) # default timeout

@pytest.mark.asyncio
async def test_run_python_code_success(code_runner):
    """
    Test that run_python_code successfully executes code using TemporaryDirectory and docker-py.
    """
    code_to_run = "print('hello world')"
    expected_output = "hello world\n"

    # Fix: run returns a container object now, not bytes
    mock_container = MagicMock()
    mock_container.logs.return_value = expected_output.encode('utf-8')
    mock_container.status = 'exited' # Simulate immediate finish

    code_runner.client.containers.run.return_value = mock_container

    with patch('tempfile.TemporaryDirectory') as mock_tempdir:
        mock_dir = MagicMock()
        mock_dir.__enter__.return_value = "/tmp/fake_dir"
        mock_tempdir.return_value = mock_dir

        with patch("builtins.open", new_callable=MagicMock) as mock_open:
            mock_file = MagicMock()
            mock_file.__enter__.return_value = mock_file
            mock_open.return_value = mock_file

            result = await code_runner.run_python_code(code_to_run)

            mock_file.write.assert_called_with(code_to_run)

    assert result == expected_output
    code_runner.client.containers.run.assert_called_once()
    args, kwargs = code_runner.client.containers.run.call_args
    assert args[0] == "python:3.9-slim"
    assert kwargs["command"] == ["python", "/code/script.py"]
    assert kwargs["network_mode"] == "none"
    # Fix: check for detach=True
    assert kwargs.get("detach") is True

@pytest.mark.asyncio
async def test_run_python_code_no_docker_client(code_runner):
    """
    Test that run_python_code returns an error message when Docker client is not available.
    """
    # Simulate failed docker client init
    code_runner.executor.client = None
    code_runner.client = None # Sync alias if used in test (though tool logic uses executor.client)

    result = await code_runner.run_python_code("print('hello')")
    assert "Error: Docker execution is not available" in result



@pytest.mark.asyncio
@patch('pipecatapp.tools.code_runner_tool.jupyter_client')
async def test_interactive_python_success(mock_jupyter_client):
    runner = CodeRunnerTool()
    runner.history.db_path = ':memory:'
    runner.history._init_db()

    mock_km = MagicMock()
    mock_kc = MagicMock()
    mock_jupyter_client.AsyncKernelManager.return_value = mock_km
    mock_km.client.return_value = mock_kc

    mock_kc.execute.return_value = 'test-msg-id'

    async def mock_get_iopub_msg(*args, **kwargs):
        if not hasattr(mock_get_iopub_msg, 'calls'):
            mock_get_iopub_msg.calls = 0
        mock_get_iopub_msg.calls += 1
        if mock_get_iopub_msg.calls == 1:
            return {'parent_header': {'msg_id': 'test-msg-id'}, 'header': {'msg_type': 'execute_result'}, 'content': {'data': {'text/plain': '42'}}}
        return {'parent_header': {'msg_id': 'test-msg-id'}, 'header': {'msg_type': 'status'}, 'content': {'execution_state': 'idle'}}
    mock_kc.get_iopub_msg.side_effect = mock_get_iopub_msg

    # Patch Docker out
    with patch('pipecatapp.tools.code_runner_tool.docker'):
        # Mock initialize so it uses our mock kc
        runner.jupyter_executor.kc = mock_kc
        result = await runner.run_interactive_python(code="x=42")

    assert "42" in result
    mock_kc.execute.assert_called_with("x=42")



@pytest.mark.asyncio
@patch('pipecatapp.tools.code_runner_tool.jupyter_client')
async def test_interactive_python_timeout(mock_jupyter_client):
    runner = CodeRunnerTool()
    runner.history.db_path = ':memory:'
    runner.history._init_db()

    mock_km = MagicMock()
    mock_kc = MagicMock()
    mock_jupyter_client.AsyncKernelManager.return_value = mock_km
    mock_km.client.return_value = mock_kc

    mock_kc.execute.return_value = 'test-msg-id'
    import asyncio
    async def mock_timeout(*args, **kwargs):
        raise asyncio.TimeoutError()
    mock_kc.get_iopub_msg.side_effect = mock_timeout

    with patch('pipecatapp.tools.code_runner_tool.docker'):
        runner.jupyter_executor.kc = mock_kc
        result = await runner.run_interactive_python(code="while True: pass", timeout=1)

    assert "Execution timed out" in result
