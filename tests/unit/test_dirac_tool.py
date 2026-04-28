import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from tools.dirac_tool import DiracTool
import asyncio

def test_dirac_tool_success():
    tool = DiracTool(root_dir="/test/dir")

    with patch("asyncio.create_subprocess_exec", new_callable=AsyncMock) as mock_subprocess:
        mock_process = MagicMock()
        mock_process.communicate = AsyncMock(return_value=(b"success output", b""))
        mock_process.returncode = 0
        mock_subprocess.return_value = mock_process

        result = asyncio.run(tool.execute(prompt="test prompt"))

        mock_subprocess.assert_called_once_with(
            'dirac',
            '-y',
            'test prompt',
            cwd="/test/dir",
            stdout=-1, # asyncio.subprocess.PIPE
            stderr=-1
        )
        assert "Exit Code: 0" in result
        assert "success output" in result

def test_dirac_tool_failure():
    tool = DiracTool(root_dir="/test/dir")

    with patch("asyncio.create_subprocess_exec", new_callable=AsyncMock) as mock_subprocess:
        mock_process = MagicMock()
        mock_process.communicate = AsyncMock(return_value=(b"", b"error output"))
        mock_process.returncode = 1
        mock_subprocess.return_value = mock_process

        result = asyncio.run(tool.execute(prompt="test prompt"))

        assert "Exit Code: 1" in result
        assert "error output" in result

def test_dirac_tool_exception():
    tool = DiracTool()

    with patch("asyncio.create_subprocess_exec", side_effect=Exception("Test Error")):
        result = asyncio.run(tool.execute(prompt="test prompt"))

        assert "Failed to execute Dirac command: Test Error" in result
