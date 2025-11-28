import pytest
import sys
import os
from unittest.mock import MagicMock

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from mcp_tool import MCP_Tool

@pytest.fixture
def mcp_tool():
    mock_twin_service = MagicMock()
    mock_runner = MagicMock()
    return MCP_Tool(mock_twin_service, mock_runner)

def test_get_status_with_running_pipelines(mcp_tool):
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

    mcp_tool.runner.get_tasks.return_value = [mock_task1, mock_task2]

    expected_report = "Current pipeline status:\n- Task pipeline_1: running\n- Task pipeline_2: completed\n"
    assert mcp_tool.get_status() == expected_report

def test_get_status_with_no_pipelines(mcp_tool):
    """Test get_status when there are no active pipelines."""
    mcp_tool.runner.get_tasks.return_value = []
    assert mcp_tool.get_status() == "No active pipelines."

def test_get_status_with_no_runner(mcp_tool):
    """Test get_status when the runner is not available."""
    mcp_tool.runner = None
    assert mcp_tool.get_status() == "Error: PipelineRunner not available."

def test_get_memory_summary(mcp_tool):
    """Test the memory summary functionality."""
    # Mocking memory attributes
    mcp_tool.twin_service.short_term_memory = ["turn1", "turn2"]
    mcp_tool.twin_service.long_term_memory.index.ntotal = 5

    expected_summary = "Short-term memory contains 2 turns. Long-term memory contains 5 entries."
    assert mcp_tool.get_memory_summary() == expected_summary

def test_clear_short_term_memory(mcp_tool):
    """Test clearing the short-term memory."""
    # Mocking the clear method on a list
    mock_short_term_memory = MagicMock()
    mcp_tool.twin_service.short_term_memory = mock_short_term_memory

    assert mcp_tool.clear_short_term_memory() == "Short-term memory cleared."
    mock_short_term_memory.clear.assert_called_once()
