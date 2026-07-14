import pytest
import os
import sys
from unittest.mock import MagicMock, AsyncMock, patch
import yaml

# Add correct Python paths
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pipecatapp')))

# Mock modules
sys.modules["pyaudio"] = MagicMock()
sys.modules["faster_whisper"] = MagicMock()
sys.modules["piper"] = MagicMock()
sys.modules["piper.voice"] = MagicMock()
sys.modules["pipecat.transports.local.audio"] = MagicMock()

mock_pipecat = MagicMock()
sys.modules["pipecat"] = mock_pipecat
sys.modules["pipecat.frames"] = mock_pipecat.frames
sys.modules["pipecat.frames.frames"] = mock_pipecat.frames.frames
sys.modules["pipecat.pipeline"] = mock_pipecat.pipeline
sys.modules["pipecat.pipeline.pipeline"] = mock_pipecat.pipeline.pipeline
sys.modules["pipecat.pipeline.runner"] = mock_pipecat.pipeline.runner
sys.modules["pipecat.pipeline.task"] = mock_pipecat.pipeline.task
sys.modules["pipecat.processors"] = mock_pipecat.processors
sys.modules["pipecat.processors.frame_processor"] = mock_pipecat.processors.frame_processor
sys.modules["pipecat.services"] = mock_pipecat.services
sys.modules["pipecat.services.openai"] = mock_pipecat.services.openai
sys.modules["pipecat.services.openai.llm"] = mock_pipecat.services.openai.llm

from workflow.runner import WorkflowRunner

def test_last30days_workflow_loading():
    """
    Verifies that workflows/last30days_research.yaml can be successfully loaded and parses cleanly.
    """
    workflow_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', '..', 'workflows', 'last30days_research.yaml'
    ))

    assert os.path.exists(workflow_path)

    runner = WorkflowRunner(workflow_path)
    assert runner.workflow_definition["name"] == "Last30Days Research Workflow"
    assert len(runner.workflow_definition["nodes"]) == 6

    # Check execution order topological sort
    execution_order = runner._get_execution_order()
    assert "Input" in execution_order
    assert "Output" in execution_order
    # Verify topological order makes sense (Input runs before SystemPrompt and ResearchReasoning)
    assert execution_order.index("Input") < execution_order.index("SystemPrompt")
    assert execution_order.index("Input") < execution_order.index("ResearchReasoning")
    assert execution_order.index("ToolParser") < execution_order.index("ToolExecutor")
