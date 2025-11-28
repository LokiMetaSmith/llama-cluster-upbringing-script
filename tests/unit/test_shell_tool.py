import pytest
import sys
import os
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from shell_tool import ShellTool

@pytest.mark.asyncio
async def test_shell_tool_initialization():
    tool = ShellTool()
    assert tool.name == "shell"

@pytest.mark.asyncio
@patch('asyncio.create_subprocess_exec')
@patch('uuid.uuid4')
async def test_execute_command_success(mock_uuid, mock_subprocess):
    mock_uuid.return_value.hex = "FIXED_UUID"
    sentinel = "END_FIXED_UUID"

    # Mock process objects
    mock_proc_check = AsyncMock()
    mock_proc_check.wait.return_value = None
    mock_proc_check.returncode = 0 # Session exists

    mock_proc_send = AsyncMock()
    mock_proc_send.wait.return_value = None

    mock_proc_capture = AsyncMock()
    # Return output containing sentinel
    mock_proc_capture.communicate.return_value = (f"some output\n{sentinel}".encode('utf-8'), b"")

    # define side effects based on args could be better, but list is easier if order is deterministic
    # Order: has-session, send-keys, capture-pane
    mock_subprocess.side_effect = [mock_proc_check, mock_proc_send, mock_proc_capture]

    tool = ShellTool()
    result = await tool.execute_command("echo hello")

    assert "some output" in result
    # The tool strips the sentinel
    assert sentinel not in result

@pytest.mark.asyncio
@patch('asyncio.create_subprocess_exec')
async def test_execute_command_timeout(mock_subprocess):
    # Mock process objects
    mock_proc_check = AsyncMock()
    mock_proc_check.wait.return_value = None
    mock_proc_check.returncode = 0

    mock_proc_send = AsyncMock()
    mock_proc_send.wait.return_value = None

    mock_proc_capture = AsyncMock()
    # No sentinel
    mock_proc_capture.communicate.return_value = (b"some output", b"")

    # Order: has-session, send-keys, capture-pane (repeatedly)
    mock_subprocess.side_effect = [mock_proc_check, mock_proc_send] + [mock_proc_capture] * 20

    tool = ShellTool()
    result = await tool.execute_command("echo hello", timeout=0.1)

    assert "Command timed out" in result
