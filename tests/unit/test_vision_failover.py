import sys
from unittest.mock import MagicMock, patch

# ----------------------------------------------------------------------
# 1. Pre-Mock Heavy Dependencies
# ----------------------------------------------------------------------
mock_modules = [
    "ultralytics",
    "pipecat",
    "pipecat.frames",
    "pipecat.frames.frames",
    "pipecat.pipeline",
    "pipecat.pipeline.pipeline",
    "pipecat.pipeline.runner",
    "pipecat.pipeline.task",
    "pipecat.processors",
    "pipecat.processors.frame_processor",
    "pipecat.services",
    "pipecat.services.openai",
    "pipecat.services.openai.llm",
    "pipecat.transports",
    "pipecat.transports.local",
    "pipecat.transports.local.audio",
    "faster_whisper",
    "piper",
    "piper.voice",
    "consul",
    "consul.aio",
    "numpy",
    "pmm_memory",
    "pmm_memory_client",
    "quality_control",
    "web_server",
    "tools",
    "tools.ssh_tool",
    "tools.mcp_tool",
    "tools.desktop_control_tool",
    "tools.code_runner_tool",
    "tools.web_browser_tool",
    "tools.ansible_tool",
    "tools.power_tool",
    "tools.summarizer_tool",
    "tools.term_everything_tool",
    "tools.rag_tool",
    "tools.ha_tool",
    "tools.git_tool",
    "tools.orchestrator_tool",
    "tools.llxprt_code_tool",
    "tools.claude_clone_tool",
    "tools.smol_agent_tool",
    "tools.final_answer_tool",
    "tools.shell_tool",
    "tools.prompt_improver_tool",
    "tools.council_tool",
    "tools.swarm_tool",
    "tools.project_mapper_tool",
    "tools.planner_tool",
    "agent_factory",
    "task_supervisor",
    "durable_execution",
    "workflow",
    "workflow.runner",
    "workflow.nodes",
    "workflow.nodes.base_nodes",
    "workflow.nodes.llm_nodes",
    "workflow.nodes.tool_nodes",
    "workflow.nodes.system_nodes",
    "uvicorn"
]

for mod_name in mock_modules:
    sys.modules[mod_name] = MagicMock()

# ----------------------------------------------------------------------
# 2. Specific Mocks
# ----------------------------------------------------------------------
class MockFrameProcessor:
    def __init__(self):
        pass
    async def push_frame(self, frame, direction):
        pass

# Fix: Create a real class for isinstance checks
class MockVisionImageRawFrame:
    pass

sys.modules["pipecat.processors.frame_processor"].FrameProcessor = MockFrameProcessor
sys.modules["pipecat.frames.frames"].VisionImageRawFrame = MockVisionImageRawFrame
sys.modules["pipecat.frames.frames"].UserImageRawFrame = MockVisionImageRawFrame # Alias used in app.py

import os
sys.path.append(os.getcwd())
import importlib.util

spec = importlib.util.spec_from_file_location("app", "ansible/roles/pipecatapp/files/app.py")
app_module = importlib.util.module_from_spec(spec)
sys.modules["app"] = app_module
spec.loader.exec_module(app_module)

YOLOv8Detector = app_module.YOLOv8Detector

import pytest

def test_yolo_initialization_failover():
    """
    Test that YOLOv8Detector handles failure gracefully by not crashing
    and providing a fallback observation.
    """
    with patch("app.YOLO", side_effect=Exception("Model file not found")):
        # AFTER FIX: This should NOT raise an exception
        detector = YOLOv8Detector()

        # Check that it initialized in a 'disabled' or safe state
        assert detector.get_observation() == "Vision system unavailable."

def test_yolo_process_frame_failover():
    """Test that process_frame does not crash when model is missing."""
    with patch("app.YOLO", side_effect=Exception("Model file not found")):
        detector = YOLOv8Detector()

        # Create an instance of our mock class
        frame = MockVisionImageRawFrame()

        # This should execute without error (mocking push_frame is already done via MockFrameProcessor)
        import asyncio
        asyncio.run(detector.process_frame(frame, "downstream"))
