import sys
import os
from unittest.mock import MagicMock, patch, AsyncMock
import pytest

# Add the app's directory to the Python path to ensure correct module resolution
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ansible/roles/pipecatapp/files'))
sys.path.insert(0, app_path)

# Mock heavy dependencies before they are imported by the app
# This prevents them from being loaded and causing side effects during tests.
mock_modules = [
    "ultralytics", "pipecat", "pipecat.frames", "pipecat.frames.frames",
    "pipecat.pipeline", "pipecat.pipeline.pipeline", "pipecat.pipeline.runner",
    "pipecat.pipeline.task", "pipecat.processors", "pipecat.processors.frame_processor",
    "pipecat.services", "pipecat.services.openai", "pipecat.services.openai.llm",
    "pipecat.transports", "pipecat.transports.local", "pipecat.transports.local.audio",
    "faster_whisper", "piper", "piper.voice", "consul", "consul.aio", "numpy",
    "pmm_memory", "pmm_memory_client", "quality_control", "web_server", "tools",
    "tools.ssh_tool", "tools.mcp_tool", "tools.desktop_control_tool",
    "tools.code_runner_tool", "tools.web_browser_tool", "tools.ansible_tool",
    "tools.power_tool", "tools.summarizer_tool", "tools.term_everything_tool",
    "tools.rag_tool", "tools.ha_tool", "tools.git_tool", "tools.orchestrator_tool",
    "tools.llxprt_code_tool", "tools.claude_clone_tool", "tools.smol_agent_tool",
    "tools.final_answer_tool", "tools.shell_tool", "tools.prompt_improver_tool",
    "tools.council_tool", "tools.swarm_tool", "tools.project_mapper_tool",
    "tools.planner_tool", "agent_factory", "task_supervisor", "durable_execution",
    "workflow", "workflow.runner", "workflow.nodes", "workflow.nodes.base_nodes",
    "workflow.nodes.llm_nodes", "workflow.nodes.tool_nodes", "workflow.nodes.system_nodes",
    "uvicorn", "transformers", "torch"
]
for mod_name in mock_modules:
    sys.modules[mod_name] = MagicMock()

# Configure the web_server mock to have an awaitable broadcast method
sys.modules['web_server'].manager.broadcast = AsyncMock()

# Define mock base classes for isinstance checks and method existence
class MockFrameProcessor:
    def get_observation(self) -> str: return "Not implemented"
    async def process_frame(self, frame, direction): pass
    async def push_frame(self, frame, direction): pass  # Add missing async method

class MockVisionImageRawFrame: pass

sys.modules["pipecat.processors.frame_processor"].FrameProcessor = MockFrameProcessor
sys.modules["pipecat.frames.frames"].UserImageRawFrame = MockVisionImageRawFrame

# Import the module under test AFTER mocks are set up
from app import initialize_vision_detector, YOLOv8Detector

# Correct patch target is where the object is looked up
@patch('app.MoondreamDetector')
@patch('app.YOLOv8Detector')
def test_vision_selection_primary_succeeds(mock_yolo, mock_moondream):
    """Test that the correct primary model is chosen and initialized."""
    mock_yolo.__name__ = "YOLOv8Detector"
    mock_moondream.__name__ = "MoondreamDetector"
    # Case 1: Select yolov8
    detector = initialize_vision_detector({"vision_model": "yolov8"})
    mock_yolo.assert_called_once()
    mock_moondream.assert_not_called()
    assert detector == mock_yolo.return_value

    mock_yolo.reset_mock(); mock_moondream.reset_mock()
    mock_yolo.__name__ = "YOLOv8Detector"
    mock_moondream.__name__ = "MoondreamDetector"

    # Case 2: Select moondream
    detector = initialize_vision_detector({"vision_model": "moondream"})
    mock_yolo.assert_not_called()
    mock_moondream.assert_called_once()
    assert detector == mock_moondream.return_value

@patch('app.MoondreamDetector')
@patch('app.YOLOv8Detector', side_effect=Exception("YOLO failed"))
def test_vision_selection_fallback_succeeds(mock_yolo, mock_moondream):
    """Test that the fallback model is used when the primary one fails."""
    mock_yolo.__name__ = "YOLOv8Detector"
    mock_moondream.__name__ = "MoondreamDetector"
    detector = initialize_vision_detector({"vision_model": "yolov8"})
    mock_yolo.assert_called_once()
    mock_moondream.assert_called_once()
    assert detector == mock_moondream.return_value

@patch('app.MoondreamDetector', side_effect=Exception("Moondream failed"))
@patch('app.YOLOv8Detector', side_effect=Exception("YOLO failed"))
def test_vision_selection_both_fail(mock_yolo, mock_moondream):
    """Test that a dummy detector is returned when both models fail."""
    mock_yolo.__name__ = "YOLOv8Detector"
    mock_moondream.__name__ = "MoondreamDetector"
    detector = initialize_vision_detector({"vision_model": "yolov8"})
    mock_yolo.assert_called_once()
    mock_moondream.assert_called_once()
    assert detector.get_observation() == "Vision system is completely unavailable."

def test_yolo_internal_initialization_failover():
    """Test that YOLOv8Detector's internal try/except to load the model works."""
    with patch("app.YOLO", side_effect=Exception("Model file not found")):
        detector = YOLOv8Detector()
        assert detector.model is None
        assert detector.get_observation() == "Vision system unavailable."

@pytest.mark.asyncio
async def test_yolo_internal_process_frame_failover():
    """Test that process_frame doesn't crash if the model failed to load."""
    with patch("app.YOLO", side_effect=Exception("Model file not found")):
        detector = YOLOv8Detector()
        frame = MockVisionImageRawFrame()
        # This should now pass as the base class has the required method
        await detector.process_frame(frame, "downstream")
