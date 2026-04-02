import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Adjust path to import pipecatapp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from pipecatapp.tools.polyphony_tool import PolyphonyTool

class TestPolyphonyTool(unittest.TestCase):
    @patch('pipecatapp.tools.polyphony_tool.os.path.exists')
    @patch('pipecatapp.tools.polyphony_tool.subprocess.run')
    def test_share_action(self, mock_run, mock_exists):
        mock_exists.return_value = True
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Thought shared"
        mock_run.return_value = mock_result

        tool = PolyphonyTool()
        result = tool.execute(action="share", thought="Hello Swarm")

        self.assertEqual(result, "Thought shared")
        mock_run.assert_called_once()
        cmd_args = mock_run.call_args[0][0]
        self.assertEqual(cmd_args[1], "share")
        self.assertEqual(cmd_args[2], "Hello Swarm")

    @patch('pipecatapp.tools.polyphony_tool.os.path.exists')
    @patch('pipecatapp.tools.polyphony_tool.subprocess.run')
    def test_ping_action(self, mock_run, mock_exists):
        mock_exists.return_value = True
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Ping sent"
        mock_run.return_value = mock_result

        tool = PolyphonyTool()
        result = tool.execute(action="ping", node_id="agent-1", message="Are you there?")

        self.assertEqual(result, "Ping sent")
        mock_run.assert_called_once()
        cmd_args = mock_run.call_args[0][0]
        self.assertEqual(cmd_args[1], "ping")
        self.assertEqual(cmd_args[2], "agent-1")
        self.assertEqual(cmd_args[3], "Are you there?")

    @patch('pipecatapp.tools.polyphony_tool.os.path.exists')
    @patch('pipecatapp.tools.polyphony_tool.subprocess.run')
    def test_task_list(self, mock_run, mock_exists):
        mock_exists.return_value = True
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Tasks:\n1. Fix bug"
        mock_run.return_value = mock_result

        tool = PolyphonyTool()
        result = tool.execute(action="task_list")

        self.assertEqual(result, "Tasks:\n1. Fix bug")
        cmd_args = mock_run.call_args[0][0]
        self.assertEqual(cmd_args[1], "task")
        self.assertEqual(cmd_args[2], "list")

    @patch('pipecatapp.tools.polyphony_tool.os.path.exists')
    def test_missing_cli(self, mock_exists):
        mock_exists.return_value = False

        tool = PolyphonyTool(cli_path="/fake/path")
        result = tool.execute(action="status")

        self.assertIn("Error: Polyphony CLI not found", result)

if __name__ == '__main__':
    unittest.main()
