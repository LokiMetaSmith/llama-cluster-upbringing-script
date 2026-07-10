import os
import unittest
from unittest.mock import patch, MagicMock, AsyncMock

from pipecatapp.janitor_agent import JanitorAgent

class TestJanitorAgent(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.agent = JanitorAgent()
        self.agent.memory_client = MagicMock()
        self.agent.memory_client.update_dlq_item = AsyncMock()

    @patch("pipecatapp.janitor_agent.JulesTool")
    async def test_process_item_triggers_jules_on_test_failure(self, mock_jules_class):
        # Setup mock JulesTool
        mock_jules_instance = MagicMock()
        mock_jules_instance.api_key = "fake_key"
        mock_jules_instance.run = AsyncMock(return_value="Jules session created successfully. Session ID: 12345.")
        mock_jules_class.return_value = mock_jules_instance

        # Setup critical DLQ item
        item = {
            "id": "item-123",
            "event_type": "test_failure",
            "error_reason": "AssertionError: 1 != 2",
            "payload": {
                "source_path": "pipecatapp/app.py",
                "foo": "bar"
            }
        }

        # Run process_item
        await self.agent.process_item(item)

        # Assert JulesTool was instantiated and called
        mock_jules_class.assert_called_once()
        mock_jules_instance.run.assert_called_once_with(
            prompt=(
                "Crash/Fault Detected!\n"
                "Event Type: test_failure\n"
                "Error Reason: AssertionError: 1 != 2\n"
                "Payload Context: {'source_path': 'pipecatapp/app.py', 'foo': 'bar'}\n"
                "Please investigate the codebase and autonomously implement a fix."
            ),
            source="pipecatapp/app.py",
            title="Fix DLQ Event item-123: test_failure",
            automation_mode="AUTO_CREATE_PR"
        )

        # Assert memory_client.update_dlq_item was called with SUCCEEDED and trigger info
        self.agent.memory_client.update_dlq_item.assert_called_once_with(
            item_id="item-123",
            status="SUCCEEDED",
            result="Triggered autonomous Jules session: Jules session created successfully. Session ID: 12345."
        )

    @patch("pipecatapp.janitor_agent.JulesTool")
    async def test_process_item_skips_jules_on_other_failures(self, mock_jules_class):
        # Setup non-critical DLQ item
        item = {
            "id": "item-456",
            "event_type": "llm_failure",
            "error_reason": "Rate limit exceeded",
            "payload": {
                "foo": "bar"
            }
        }

        # Run process_item
        await self.agent.process_item(item)

        # Assert JulesTool was NOT instantiated
        mock_jules_class.assert_not_called()

        # Assert standard processing succeeded
        self.agent.memory_client.update_dlq_item.assert_called_once_with(
            item_id="item-456",
            status="SUCCEEDED",
            result="Janitor cleaned up the mess."
        )

if __name__ == "__main__":
    unittest.main()
