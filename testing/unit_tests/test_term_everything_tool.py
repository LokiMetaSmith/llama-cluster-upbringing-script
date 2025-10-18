import pytest
import sys
import os
import subprocess
from unittest.mock import patch, AsyncMock

# Ensure the tool's path is in the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ansible/roles/pipecatapp/files')))

from tools.term_everything_tool import TermEverythingTool

# Mock path for the AppImage
MOCK_APPIMAGE_PATH = "/opt/mcp/termeverything.AppImage"

@pytest.fixture
def tool():
    """Provides a reusable instance of the TermEverythingTool."""
    return TermEverythingTool(app_image_path=MOCK_APPIMAGE_PATH)

@pytest.mark.asyncio
async def test_execute_command_success(tool):
    """
    Tests the happy path where the command executes successfully.
    """
    # 1. ARRANGE
    command = "search --path /home"
    expected_stdout = "Command executed successfully."

    # Mock the asyncio subprocess
    mock_process = AsyncMock()
    mock_process.communicate.return_value = (expected_stdout.encode(), b"")
    mock_process.returncode = 0

    # 2. ACT
    with patch('asyncio.create_subprocess_exec', return_value=mock_process) as mock_create_subprocess:
        result = await tool.execute(command)

        # 3. ASSERT
        mock_create_subprocess.assert_called_once_with(
            MOCK_APPIMAGE_PATH,
            *command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        assert result == expected_stdout

@pytest.mark.asyncio
async def test_execute_command_failure(tool):
    """
    Tests the failure path where the command returns a non-zero exit code.
    """
    # 1. ARRANGE
    command = "search --invalid"
    expected_stderr = "Error: Invalid argument."

    # Mock the asyncio subprocess to simulate a failure
    mock_process = AsyncMock()
    mock_process.communicate.return_value = (b"", expected_stderr.encode())
    mock_process.returncode = 1

    # 2. ACT
    with patch('asyncio.create_subprocess_exec', return_value=mock_process) as mock_create_subprocess:
        result = await tool.execute(command)

        # 3. ASSERT
        mock_create_subprocess.assert_called_once_with(
            MOCK_APPIMAGE_PATH,
            *command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        assert result == f"Error: {expected_stderr}"

@pytest.mark.asyncio
async def test_execute_exception(tool):
    """
    Tests the tool's behavior when an exception occurs during subprocess execution.
    """
    # 1. ARRANGE
    command = "search --path /home"
    error_message = "A critical error occurred."

    # 2. ACT
    with patch('asyncio.create_subprocess_exec', side_effect=Exception(error_message)) as mock_create_subprocess:
        result = await tool.execute(command)

        # 3. ASSERT
        mock_create_subprocess.assert_called_once_with(
            MOCK_APPIMAGE_PATH,
            *command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        assert result == f"Error: {error_message}"