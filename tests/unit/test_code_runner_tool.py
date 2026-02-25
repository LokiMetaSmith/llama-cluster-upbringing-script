import pytest
import sys
import os
import docker
import tempfile
from unittest.mock import MagicMock, patch

# Add repo root to path to allow importing pipecatapp as a package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pipecatapp.tools.code_runner_tool import CodeRunnerTool, DockerSandboxExecutor

@pytest.fixture
def code_runner():
    with patch('docker.from_env') as mock_from_env:
        # Create a fresh tool instance for each test to ensure clean state
        runner = CodeRunnerTool()
        # Mock the client on the executor
        if isinstance(runner.executor, DockerSandboxExecutor):
            # Use the mock from from_env
            runner.executor.client = mock_from_env.return_value
            # Alias for tests expecting runner.client
            runner.client = runner.executor.client
        yield runner

@patch('pipecatapp.tools.code_runner_tool.SandboxSession')
def test_run_code_in_sandbox_success(mock_sandbox_session, code_runner):
    """
    Test that run_code_in_sandbox successfully executes Python code via llm-sandbox.
    """
    # ... (rest of test remains same, code_runner fixture handles setup)
    code_to_run = "print('hello sandbox')"
    expected_output = "hello sandbox\n"

    mock_result = MagicMock()
    mock_result.stdout = expected_output
    mock_result.stderr = ""
    mock_result.exit_code = 0
    mock_result.plots = []

    mock_session_instance = mock_sandbox_session.return_value.__enter__.return_value
    mock_session_instance.run.return_value = mock_result

    result = code_runner.run_code_in_sandbox(code=code_to_run, language="python")

    assert result == expected_output
    # Fix: verify method call on instance
    mock_session_instance.run.assert_called_with(code_to_run, libraries=[])

def test_run_python_code_success(code_runner):
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

            result = code_runner.run_python_code(code_to_run)

            mock_file.write.assert_called_with(code_to_run)

    assert result == expected_output
    code_runner.client.containers.run.assert_called_once()
    args, kwargs = code_runner.client.containers.run.call_args
    assert args[0] == "python:3.9-slim"
    assert kwargs["command"] == ["python", "/code/script.py"]
    assert kwargs["network_mode"] == "none"
    # Fix: check for detach=True
    assert kwargs.get("detach") is True

def test_run_python_code_no_docker_client(code_runner):
    """
    Test that run_python_code returns an error message when Docker client is not available.
    """
    # Simulate failed docker client init
    code_runner.executor.client = None
    code_runner.client = None # Sync alias if used in test (though tool logic uses executor.client)

    result = code_runner.run_python_code("print('hello')")
    assert "Error: Docker execution is not available" in result
