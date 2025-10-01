import unittest
from unittest.mock import MagicMock, PropertyMock

# Assume mcp_tool is in the same directory or adjust path as needed
from mcp_tool import MCP_Tool

class TestMCPTool(unittest.TestCase):

    def setUp(self):
        """Set up mock objects before each test."""
        self.mock_twin_service = MagicMock()
        self.mock_runner = MagicMock()
        self.mcp_tool = MCP_Tool(self.mock_twin_service, self.mock_runner)

    def test_get_status_with_running_pipelines(self):
        """Test get_status when there are active pipelines."""
        # Mocking the runner and tasks
        mock_state1 = MagicMock()
        mock_state1.value = "running"
        mock_task1 = MagicMock()
        mock_task1.get_name.return_value = "pipeline_1"
        mock_task1.get_state.return_value = mock_state1

        mock_state2 = MagicMock()
        mock_state2.value = "completed"
        mock_task2 = MagicMock()
        mock_task2.get_name.return_value = "pipeline_2"
        mock_task2.get_state.return_value = mock_state2

        self.mock_runner.get_tasks.return_value = [mock_task1, mock_task2]

        expected_report = "Current pipeline status:\n- Task pipeline_1: running\n- Task pipeline_2: completed\n"
        self.assertEqual(self.mcp_tool.get_status(), expected_report)

    def test_get_status_with_no_pipelines(self):
        """Test get_status when there are no active pipelines."""
        self.mock_runner.get_tasks.return_value = []
        self.assertEqual(self.mcp_tool.get_status(), "No active pipelines.")

    def test_get_status_with_no_runner(self):
        """Test get_status when the runner is not available."""
        self.mcp_tool.runner = None
        self.assertEqual(self.mcp_tool.get_status(), "Error: PipelineRunner not available.")

    def test_get_memory_summary(self):
        """Test the memory summary functionality."""
        # Mocking memory attributes
        self.mock_twin_service.short_term_memory = ["turn1", "turn2"]
        self.mock_twin_service.long_term_memory.index.ntotal = 5

        expected_summary = "Short-term memory contains 2 turns. Long-term memory contains 5 entries."
        self.assertEqual(self.mcp_tool.get_memory_summary(), expected_summary)

    def test_clear_short_term_memory(self):
        """Test clearing the short-term memory."""
        # Mocking the clear method on a list
        mock_short_term_memory = MagicMock()
        self.mock_twin_service.short_term_memory = mock_short_term_memory

        self.assertEqual(self.mcp_tool.clear_short_term_memory(), "Short-term memory cleared.")
        mock_short_term_memory.clear.assert_called_once()

if __name__ == '__main__':
    unittest.main()