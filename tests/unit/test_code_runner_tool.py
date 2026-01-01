import pytest
import sys
import os
import docker
from unittest.mock import MagicMock, patch

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from code_runner_tool import CodeRunnerTool

@pytest.fixture
def code_runner():
    with patch('docker.from_env'):
        runner = CodeRunnerTool()
        # Mock the client that is created in the constructor
        runner.client = MagicMock()
        return runner

# We patch SandboxSession where it's used in the code_runner_tool module.
@patch('code_runner_tool.SandboxSession')
def test_run_code_in_sandbox_success(mock_sandbox_session, code_runner):
    """
    Test that run_code_in_sandbox successfully executes Python code.
    """
    code_to_run = "print('hello sandbox')"
    expected_output = "hello sandbox\n"

    # Configure the mock result from the sandbox run
    mock_result = MagicMock()
    mock_result.stdout = expected_output
    mock_result.stderr = ""
    mock_result.exit_code = 0
    mock_result.plots = []

    mock_session_instance = mock_sandbox_session.return_value.__enter__.return_value
    mock_session_instance.run.return_value = mock_result

    result = code_runner.run_code_in_sandbox(code=code_to_run, language="python")

    assert result == expected_output
    mock_sandbox_session.assert_called_once_with(lang="python")
    mock_session_instance.run.assert_called_once_with(code_to_run, libraries=[])

@patch('code_runner_tool.SandboxSession')
def test_run_code_in_sandbox_with_libraries(mock_sandbox_session, code_runner):
    """
    Test that run_code_in_sandbox correctly passes libraries.
    """
    code_to_run = "import pandas as pd; print(pd.DataFrame())"
    libraries = ["pandas"]
    expected_output = "Empty DataFrame\nColumns: []\nIndex: []\n"

    mock_result = MagicMock()
    mock_result.stdout = expected_output
    mock_result.stderr = ""
    mock_result.exit_code = 0
    mock_result.plots = []

    mock_session_instance = mock_sandbox_session.return_value.__enter__.return_value
    mock_session_instance.run.return_value = mock_result

    result = code_runner.run_code_in_sandbox(code=code_to_run, language="python", libraries=libraries)

    assert result == expected_output
    mock_session_instance.run.assert_called_once_with(code_to_run, libraries=libraries)

@patch('code_runner_tool.SandboxSession')
def test_run_code_in_sandbox_with_error(mock_sandbox_session, code_runner):
    """
    Test that run_code_in_sandbox returns a formatted error string.
    """
    code_to_run = "import non_existent_library"
    error_output = "ModuleNotFoundError: No module named 'non_existent_library'"

    mock_result = MagicMock()
    mock_result.stdout = ""
    mock_result.stderr = error_output
    mock_result.exit_code = 1
    mock_result.plots = []

    mock_session_instance = mock_sandbox_session.return_value.__enter__.return_value
    mock_session_instance.run.return_value = mock_result

    result = code_runner.run_code_in_sandbox(code=code_to_run, language="python")

    assert "Exit Code: 1" in result
    assert "---STDERR---" in result
    assert error_output in result

@patch('os.path.exists', return_value=True)
def test_run_python_code_success(mock_path_exists, code_runner, mocker):
    """
    Test that run_python_code successfully executes code using TemporaryDirectory.
    """
    code_to_run = "print('hello world')"
    expected_output = "hello world\n"

    # Mock the container run, which returns the output as bytes
    code_runner.client.containers.run.return_value = expected_output.encode('utf-8')

    # Mock tempfile.TemporaryDirectory
    with patch('tempfile.TemporaryDirectory') as mock_tempdir:
        mock_dir = MagicMock()
        mock_dir.__enter__.return_value = "/tmp/fake_dir"
        mock_tempdir.return_value = mock_dir

        # Mock open() to handle file writing
        with patch("builtins.open", mocker.mock_open()) as mock_file:
            result = code_runner.run_python_code(code_to_run)

            # Verify file write
            mock_file.assert_called_with("/tmp/fake_dir/script.py", "w")
            mock_file().write.assert_called_with(code_to_run)

    assert result == expected_output

    # Check that run was called with the expected parameters
    code_runner.client.containers.run.assert_called_once()
    _, kwargs = code_runner.client.containers.run.call_args
    assert kwargs["command"] == ["python", "/code/script.py"]
    assert kwargs["network_mode"] == "none"
    assert kwargs["mem_limit"] == "128m"
    assert kwargs["volumes"] == {"/tmp/fake_dir": {'bind': '/code', 'mode': 'ro'}}

@patch('os.path.exists', return_value=True)
def test_run_python_code_with_error(mock_path_exists, code_runner, mocker):
    """
    Test that run_python_code returns stderr when the code fails.
    """
    code_to_run = "raise ValueError('test error')"
    error_output = "Traceback...\nValueError: test error\n"

    code_runner.client.containers.run.return_value = error_output.encode('utf-8')

    with patch('tempfile.TemporaryDirectory') as mock_tempdir:
        mock_dir = MagicMock()
        mock_dir.__enter__.return_value = "/tmp/fake_dir"
        mock_tempdir.return_value = mock_dir

        with patch("builtins.open", mocker.mock_open()):
             result = code_runner.run_python_code(code_to_run)

    assert result == error_output

@patch('os.path.exists', return_value=True)
def test_image_not_found_error(mock_path_exists, code_runner, mocker):
    """
    Test that a graceful error message is returned when the Docker image is not found.
    """
    code_runner.client.containers.run.side_effect = docker.errors.ImageNotFound("Image not found")

    with patch('tempfile.TemporaryDirectory') as mock_tempdir:
        mock_dir = MagicMock()
        mock_dir.__enter__.return_value = "/tmp/fake_dir"
        mock_tempdir.return_value = mock_dir

        with patch("builtins.open", mocker.mock_open()):
             result = code_runner.run_python_code("foo")

    assert "Error: The Docker image 'python:3.9-slim' was not found" in result

def test_temp_file_cleanup_on_success(code_runner, mocker):
    """
    Test that TemporaryDirectory context manager is used, which implies cleanup.
    """
    code_runner.client.containers.run.return_value = b"success"

    with patch('tempfile.TemporaryDirectory') as mock_tempdir:
        mock_dir = MagicMock()
        mock_dir.__enter__.return_value = "/tmp/fake_dir"
        mock_tempdir.return_value = mock_dir

        with patch("builtins.open", mocker.mock_open()):
            code_runner.run_python_code("print('hello')")

        # Verify __exit__ was called
        mock_dir.__exit__.assert_called_once()
