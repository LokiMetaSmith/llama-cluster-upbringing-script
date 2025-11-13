import asyncio
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from .claude_clone_tool import ClaudeCloneTool

class TestClaudeCloneTool(unittest.IsolatedAsyncioTestCase):

    @patch('asyncio.create_subprocess_exec')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    async def test_explain_success(self, mock_isfile, mock_isdir, mock_create_subprocess_exec):
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
        self.assertEqual(result, "Explanation of code.")
        mock_create_subprocess_exec.assert_called_once_with(
            'node', '/opt/claude_clone/dist/cli.js', 'explain', 'file1.py', 'file2.py',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd='/opt/claude_clone'
        )

    @patch('asyncio.create_subprocess_exec')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    async def test_command_failure(self, mock_isfile, mock_isdir, mock_create_subprocess_exec):
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
        self.assertIn("Error executing Claude_Clone command 'report': Error message", result)

    async def test_directory_not_found(self):
        # Arrange
        with patch('os.path.isdir', return_value=False):
            tool = ClaudeCloneTool()

            # Act
            result = await tool._run_command("explain", "file.py")

            # Assert
            self.assertIn("Error: Claude_Clone directory not found", result)

    async def test_cli_not_found(self):
        # Arrange
        with patch('os.path.isdir', return_value=True), \
             patch('os.path.isfile', return_value=False):
            tool = ClaudeCloneTool()

            # Act
            result = await tool._run_command("explain", "file.py")

            # Assert
            self.assertIn("Error: Claude_Clone CLI not found", result)

if __name__ == '__main__':
    unittest.main()
