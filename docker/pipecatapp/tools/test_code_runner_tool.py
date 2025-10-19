import pytest
from code_runner_tool import CodeRunnerTool
from unittest.mock import MagicMock, patch
import docker

@pytest.fixture
def code_runner():
    with patch('docker.from_env'):
        runner = CodeRunnerTool()
        # Mock the client that is created in the constructor
        runner.client = MagicMock()
        return runner

@patch('os.unlink')
@patch('os.path.exists', return_value=True)
def test_run_python_code_success(mock_path_exists, mock_unlink, code_runner, mocker):
    """
    Test that run_python_code successfully executes code.
    """
    code_to_run = "print('hello world')"
    expected_output = "hello world\n"

    # Mock the container run, which returns the output as bytes
    code_runner.client.containers.run.return_value = expected_output.encode('utf-8')

    # Mock tempfile creation to control the file path
    with patch('tempfile.NamedTemporaryFile') as mock_tempfile:
        mock_file = MagicMock()
        mock_file.name = "success.py"
        mock_file.__enter__.return_value = mock_file
        mock_tempfile.return_value = mock_file

        result = code_runner.run_python_code(code_to_run)

    assert result == expected_output
    # Check that run was called with the expected image and command
    code_runner.client.containers.run.assert_called_once()
    args, kwargs = code_runner.client.containers.run.call_args
    assert args[0] == "python:3.9-slim"
    assert "python" in kwargs["command"][0]
    assert "success.py" in kwargs["command"][1]
    mock_unlink.assert_called_with("success.py")

@patch('os.unlink')
@patch('os.path.exists', return_value=True)
def test_run_python_code_with_error(mock_path_exists, mock_unlink, code_runner, mocker):
    """
    Test that run_python_code returns stderr when the code fails.
    """
    code_to_run = "raise ValueError('test error')"
    # Docker's run command returns a single bytes string with both stdout and stderr
    error_output = "Traceback...\nValueError: test error\n"

    code_runner.client.containers.run.return_value = error_output.encode('utf-8')

    with patch('tempfile.NamedTemporaryFile') as mock_tempfile:
        mock_file = MagicMock()
        mock_file.name = "error.py"
        mock_file.__enter__.return_value = mock_file
        mock_tempfile.return_value = mock_file

        result = code_runner.run_python_code(code_to_run)

    assert result == error_output
    mock_unlink.assert_called_with("error.py")

@patch('os.unlink')
@patch('os.path.exists', return_value=True)
def test_image_not_found_error(mock_path_exists, mock_unlink, code_runner, mocker):
    """
    Test that a graceful error message is returned when the Docker image is not found.
    """
    code_to_run = "print('this will not run')"

    # Configure the mock to raise ImageNotFound
    code_runner.client.containers.run.side_effect = docker.errors.ImageNotFound("Image not found")

    with patch('tempfile.NamedTemporaryFile') as mock_tempfile:
        mock_file = MagicMock()
        mock_file.name = "not_found.py"
        mock_file.__enter__.return_value = mock_file
        mock_tempfile.return_value = mock_file

        result = code_runner.run_python_code(code_to_run)

    assert "Error: The Docker image 'python:3.9-slim' was not found" in result
    mock_unlink.assert_called_with("not_found.py")

@patch('os.unlink')
@patch('os.path.exists')
def test_temp_file_cleanup_on_success(mock_path_exists, mock_unlink, code_runner, mocker):
    """
    Test that the temporary file is cleaned up after a successful run.
    """
    mock_path_exists.return_value = True
    code_runner.client.containers.run.return_value = b"success"

    # We need to control the tempfile path to verify it's unlinked
    with patch('tempfile.NamedTemporaryFile') as mock_tempfile:
        # Simulate the context manager used in the tool
        mock_file = MagicMock()
        mock_file.name = "dummy_temp_file.py"
        mock_file.__enter__.return_value = mock_file
        mock_tempfile.return_value = mock_file

        code_runner.run_python_code("print('hello')")

        # Check that the file was written to
        mock_file.write.assert_called_with("print('hello')")
        # Assert that unlink was called on the correct file path
        mock_unlink.assert_called_with("dummy_temp_file.py")

@patch('os.unlink')
@patch('os.path.exists')
def test_temp_file_cleanup_on_error(mock_path_exists, mock_unlink, code_runner, mocker):
    """
    Test that the temporary file is cleaned up even when an exception occurs.
    """
    mock_path_exists.return_value = True
    # Simulate an error during container execution
    code_runner.client.containers.run.side_effect = Exception("Docker daemon is down")

    with patch('tempfile.NamedTemporaryFile') as mock_tempfile:
        mock_file = MagicMock()
        mock_file.name = "another_temp_file.py"
        mock_file.__enter__.return_value = mock_file
        mock_tempfile.return_value = mock_file

        result = code_runner.run_python_code("print('fail')")

        assert "An error occurred: Docker daemon is down" in result
        mock_unlink.assert_called_with("another_temp_file.py")