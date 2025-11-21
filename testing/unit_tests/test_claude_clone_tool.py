import pytest
import sys
import os
from unittest.mock import patch, AsyncMock

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from claude_clone_tool import ClaudeCloneTool

@pytest.mark.asyncio
@patch('asyncio.create_subprocess_exec')
@patch('os.path.isdir')
@patch('os.path.isfile')
async def test_explain_success(mock_isfile, mock_isdir, mock_create_subprocess_exec):
    # Arrange
    mock_isdir.return_value = True
    mock_isfile.return_value = True

    mock_process = AsyncMock()
    mock_process.communicate.return_value = (b"Explanation of code.", b"")
    mock_process.returncode = 0
    mock_create_subprocess_exec.return_value = mock_process

    tool = ClaudeCloneTool()

    # Act
    result = await tool._run_command("explain", "file1.py", "file2.py")

    # Assert
    assert result == "Explanation of code."
    mock_create_subprocess_exec.assert_called_once()

@pytest.mark.asyncio
@patch('asyncio.create_subprocess_exec')
@patch('os.path.isdir')
@patch('os.path.isfile')
async def test_command_failure(mock_isfile, mock_isdir, mock_create_subprocess_exec):
    # Arrange
    mock_isdir.return_value = True
    mock_isfile.return_value = True

    mock_process = AsyncMock()
    mock_process.communicate.return_value = (b"", b"Error message")
    mock_process.returncode = 1
    mock_create_subprocess_exec.return_value = mock_process

    tool = ClaudeCloneTool()

    # Act
    result = await tool._run_command("report")

    # Assert
    assert "Error executing Claude_Clone command 'report': Error message" in result

@pytest.mark.asyncio
async def test_directory_not_found():
    # Arrange
    with patch('os.path.isdir', return_value=False):
        tool = ClaudeCloneTool()

        # Act
        result = await tool._run_command("explain", "file.py")

        # Assert
        assert "Error: Claude_Clone directory not found" in result

@pytest.mark.asyncio
async def test_cli_not_found():
    # Arrange
    with patch('os.path.isdir', return_value=True), \
         patch('os.path.isfile', return_value=False):
        tool = ClaudeCloneTool()

        # Act
        result = await tool._run_command("explain", "file.py")

        # Assert
        assert "Error: Claude_Clone CLI not found" in result
