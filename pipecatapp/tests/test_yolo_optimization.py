
import sys
import os
import asyncio
import base64
import numpy as np
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

# Add pipecatapp to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 1. Mock dependencies that are not relevant to YOLOv8Detector or are heavy
sys.modules["faster_whisper"] = MagicMock()
sys.modules["piper"] = MagicMock()
sys.modules["piper.voice"] = MagicMock()
sys.modules["consul"] = MagicMock()
sys.modules["consul.aio"] = MagicMock()
sys.modules["requests"] = MagicMock()
sys.modules["httpx"] = MagicMock()
sys.modules["paramiko"] = MagicMock()
sys.modules["fastapi"] = MagicMock()
sys.modules["fastapi.security"] = MagicMock()
sys.modules["uvicorn"] = MagicMock()

# Mock internal modules
sys.modules["pmm_memory"] = MagicMock()
sys.modules["pmm_memory_client"] = MagicMock()
sys.modules["quality_control"] = MagicMock()
sys.modules["agent_factory"] = MagicMock()
sys.modules["task_supervisor"] = MagicMock()
sys.modules["durable_execution"] = MagicMock()
sys.modules["moondream_detector"] = MagicMock()
sys.modules["workflow"] = MagicMock()
sys.modules["workflow.runner"] = MagicMock()
sys.modules["workflow.nodes"] = MagicMock()
sys.modules["workflow.nodes.base_nodes"] = MagicMock()
sys.modules["workflow.nodes.llm_nodes"] = MagicMock()
sys.modules["workflow.nodes.tool_nodes"] = MagicMock()
sys.modules["workflow.nodes.system_nodes"] = MagicMock()

# Mock tools package
mock_tools = MagicMock()
sys.modules["tools"] = mock_tools
sys.modules["tools.ssh_tool"] = MagicMock()
sys.modules["tools.mcp_tool"] = MagicMock()
sys.modules["tools.desktop_control_tool"] = MagicMock()
sys.modules["tools.code_runner_tool"] = MagicMock()
sys.modules["tools.web_browser_tool"] = MagicMock()
sys.modules["tools.ansible_tool"] = MagicMock()
sys.modules["tools.power_tool"] = MagicMock()
sys.modules["tools.summarizer_tool"] = MagicMock()
sys.modules["tools.term_everything_tool"] = MagicMock()
sys.modules["tools.rag_tool"] = MagicMock()
sys.modules["tools.ha_tool"] = MagicMock()
sys.modules["tools.git_tool"] = MagicMock()
sys.modules["tools.orchestrator_tool"] = MagicMock()
sys.modules["tools.llxprt_code_tool"] = MagicMock()
sys.modules["tools.claude_clone_tool"] = MagicMock()
sys.modules["tools.smol_agent_tool"] = MagicMock()
sys.modules["tools.final_answer_tool"] = MagicMock()
sys.modules["tools.shell_tool"] = MagicMock()
sys.modules["tools.prompt_improver_tool"] = MagicMock()
sys.modules["tools.council_tool"] = MagicMock()
sys.modules["tools.swarm_tool"] = MagicMock()
sys.modules["tools.project_mapper_tool"] = MagicMock()
sys.modules["tools.planner_tool"] = MagicMock()

# Mock pipecat
mock_pipecat = MagicMock()
sys.modules["pipecat"] = mock_pipecat
sys.modules["pipecat.frames"] = MagicMock()
sys.modules["pipecat.frames.frames"] = MagicMock()
sys.modules["pipecat.pipeline"] = MagicMock()
sys.modules["pipecat.pipeline.pipeline"] = MagicMock()
sys.modules["pipecat.pipeline.runner"] = MagicMock()
sys.modules["pipecat.pipeline.task"] = MagicMock()
sys.modules["pipecat.processors"] = MagicMock()
sys.modules["pipecat.processors.frame_processor"] = MagicMock()
sys.modules["pipecat.services"] = MagicMock()
sys.modules["pipecat.services.openai"] = MagicMock()
sys.modules["pipecat.services.openai.llm"] = MagicMock()
sys.modules["pipecat.transports"] = MagicMock()
sys.modules["pipecat.transports.local"] = MagicMock()
sys.modules["pipecat.transports.local.audio"] = MagicMock()

# Mock FrameProcessor
class MockFrameProcessor:
    def __init__(self):
        pass
    async def push_frame(self, frame, direction):
        pass
sys.modules["pipecat.processors.frame_processor"].FrameProcessor = MockFrameProcessor

# Mock VisionImageRawFrame
class MockVisionImageRawFrame:
    def __init__(self, image):
        self.image = image
sys.modules["pipecat.frames.frames"].UserImageRawFrame = MockVisionImageRawFrame
# Also mock other frames to avoid AttributeErrors during import or execution
sys.modules["pipecat.frames.frames"].TextFrame = MagicMock()
sys.modules["pipecat.frames.frames"].TranscriptionFrame = MagicMock()
sys.modules["pipecat.frames.frames"].AudioRawFrame = MagicMock()
sys.modules["pipecat.frames.frames"].UserStartedSpeakingFrame = MagicMock()
sys.modules["pipecat.frames.frames"].UserStoppedSpeakingFrame = MagicMock()

# Mock web_server
mock_web_server = MagicMock()
mock_web_server.manager = MagicMock()
mock_web_server.manager.broadcast = AsyncMock()
mock_web_server.manager.active_connections = [1] # Simulate active connection
sys.modules["web_server"] = mock_web_server

# Mock Ultralytics YOLO
mock_yolo_class = MagicMock()
sys.modules["ultralytics"] = MagicMock()
sys.modules["ultralytics"].YOLO = mock_yolo_class

# Mock PIL Image because it's imported in app.py (even if we plan to remove it, currently it is there)
# But wait, if we are testing the NEW code, we might have removed it.
# If we test before modification, we need it.
# We will run this test AFTER modification.
# However, for now, let's just allow it to be imported if needed, or mock it if we remove the import.
# Using MagicMock for PIL is safe if we don't use it in our new code path.
sys.modules["PIL"] = MagicMock()
sys.modules["PIL.Image"] = MagicMock()

# Import the class to test
# We need to use 'from app import ...' but app.py is in pipecatapp/
# sys.path is already set.
from app import YOLOv8Detector

@pytest.mark.asyncio
async def test_yolo_inference_optimization():
    # Arrange
    detector = YOLOv8Detector()

    # Mock the model instance and its return value
    mock_model_instance = mock_yolo_class.return_value
    mock_result = MagicMock()
    # Create a dummy BGR image (numpy array)
    dummy_frame = np.zeros((100, 100, 3), dtype=np.uint8)
    dummy_frame[:] = [0, 0, 255] # Red

    # plot() returns the annotated frame
    mock_result.plot.return_value = dummy_frame

    # The model call returns a list of results
    mock_model_instance.return_value = [mock_result]

    # Mock result boxes cls for object detection logic
    # In Ultralytics, result.boxes is an object with a .cls attribute (Tensor)
    mock_boxes_obj = MagicMock()
    mock_boxes_obj.cls = [0.0] # Class 0
    mock_result.boxes = mock_boxes_obj
    mock_model_instance.names = {0: "person"}

    # Mock connection check callback to ensure debug image is generated
    detector.set_connection_check_callback(lambda: True)

    # Create a dummy input frame
    # content doesn't matter much as we mock the model response
    input_frame = MockVisionImageRawFrame(image=b"dummy_bytes")

    # Act
    # We call _run_inference directly or process_frame.
    # process_frame is async and calls run_in_executor.
    # For unit testing, calling process_frame is better integration test.

    await detector.process_frame(input_frame, direction=None)

    # Assert
    # Verify that web_server.manager.broadcast was called with a vision_debug message
    assert mock_web_server.manager.broadcast.called
    args, _ = mock_web_server.manager.broadcast.call_args
    message = args[0]

    import json
    data = json.loads(message)
    assert data["type"] == "vision_debug"
    assert "data" in data

    # Verify the data is valid base64
    img_data = base64.b64decode(data["data"])
    assert len(img_data) > 0
    assert img_data.startswith(b'\xff\xd8') # JPEG header

    # Verify we didn't use PIL (if we can)
    # Since we mocked PIL, if the code used PIL.Image.fromarray, it would have called the mock.
    # We can assert that the mock was NOT called.
    from PIL import Image
    # Image.fromarray.assert_not_called()
    # Note: If app.py imports Image, it uses the mocked Image.
    # If we remove the import in app.py, this check is irrelevant/impossible via mock.
