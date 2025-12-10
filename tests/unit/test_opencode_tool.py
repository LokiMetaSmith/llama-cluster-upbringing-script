import unittest
from unittest.mock import AsyncMock, patch, MagicMock
import sys
import os

# Ensure the tool module can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ansible/roles/pipecatapp/files')))

from tools.opencode_tool import OpencodeTool

class TestOpencodeTool(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.tool = OpencodeTool(base_url="http://test-url", provider_id="test-provider", model_id="test-model")

    @patch('tools.opencode_tool.AsyncOpencode')
    async def test_run_success(self, mock_async_opencode):
        # Mock the client and session
        mock_client = AsyncMock()
        mock_session_resource = MagicMock()
        mock_session = MagicMock()
        mock_session.id = "test-session-id"

        mock_client.session = mock_session_resource
        mock_session_resource.create = AsyncMock(return_value=mock_session)
        mock_session_resource.chat = AsyncMock(return_value="Task completed")

        mock_async_opencode.return_value = mock_client

        result = await self.tool.run("Test task")

        self.assertIn("Task completed", result)
        self.assertIn("test-session-id", result)
        mock_session_resource.create.assert_called_once()
        # Verify call args match new implementation
        mock_session_resource.chat.assert_called_once()
        call_args = mock_session_resource.chat.call_args
        self.assertEqual(call_args.kwargs['id'], "test-session-id")
        self.assertEqual(call_args.kwargs['parts'], [{"type": "text", "text": "Test task"}])
        self.assertEqual(call_args.kwargs['provider_id'], "test-provider")
        self.assertEqual(call_args.kwargs['model_id'], "test-model")

    @patch('tools.opencode_tool.AsyncOpencode')
    async def test_run_error(self, mock_async_opencode):
        mock_client = AsyncMock()
        mock_client.session.create.side_effect = Exception("Connection error")
        mock_async_opencode.return_value = mock_client

        result = await self.tool.run("Test task")

        self.assertIn("Error executing OpenCode task", result)

if __name__ == '__main__':
    unittest.main()
