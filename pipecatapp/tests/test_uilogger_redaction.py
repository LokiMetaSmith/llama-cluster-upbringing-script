import sys
import os
import json
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
import pytest

# Add pipecatapp to sys.path so we can import app and its dependencies
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Mock heavy dependencies BEFORE importing app
# These modules are imported by app.py but are not needed for UILogger logic
sys.modules["ultralytics"] = MagicMock()
sys.modules["faster_whisper"] = MagicMock()
sys.modules["piper"] = MagicMock()
sys.modules["piper.voice"] = MagicMock()
sys.modules["consul"] = MagicMock()
sys.modules["consul.aio"] = MagicMock()
sys.modules["PIL"] = MagicMock() # Mock Pillow
sys.modules["requests"] = MagicMock() # Mock requests
sys.modules["httpx"] = MagicMock() # Mock httpx
sys.modules["numpy"] = MagicMock() # Mock numpy
sys.modules["paramiko"] = MagicMock() # Mock paramiko (used by ssh_tool)
sys.modules["fastapi"] = MagicMock() # Mock fastapi
sys.modules["fastapi.security"] = MagicMock()
sys.modules["uvicorn"] = MagicMock() # Mock uvicorn

# Mock internal modules that might not be importable or have side effects
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

# Mock pipecat structure
mock_pipecat = MagicMock()
sys.modules["pipecat"] = mock_pipecat

# Mock submodules
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

# Define MockTextFrame
class MockTextFrame:
    def __init__(self, text):
        self.text = text
sys.modules["pipecat.frames.frames"].TextFrame = MockTextFrame
sys.modules["pipecat.frames.frames"].TranscriptionFrame = MockTextFrame
sys.modules["pipecat.frames.frames"].AudioRawFrame = MagicMock()
sys.modules["pipecat.frames.frames"].UserImageRawFrame = MagicMock()
sys.modules["pipecat.frames.frames"].UserStartedSpeakingFrame = MagicMock()
sys.modules["pipecat.frames.frames"].UserStoppedSpeakingFrame = MagicMock()

# Mock FrameProcessor base class
class MockFrameProcessor:
    def __init__(self):
        pass
    async def push_frame(self, frame, direction):
        pass
sys.modules["pipecat.processors.frame_processor"].FrameProcessor = MockFrameProcessor

# Mock web_server since it's used in UILogger
mock_web_server = MagicMock()
mock_web_server.manager = MagicMock()
mock_web_server.manager.broadcast = AsyncMock()
sys.modules["web_server"] = mock_web_server

# Now import the class we want to test
from app import UILogger

def test_uilogger_redaction_verification():
    """
    Test that UILogger redacts secrets.
    """
    async def run_test():
        # Arrange
        logger = UILogger(sender="agent")
        secret_text = "Here is my key: sk-abcdef1234567890abcdef123456"
        frame = MockTextFrame(text=secret_text)

        # Reset mock to clear previous calls
        mock_web_server.manager.broadcast.reset_mock()

        # Act
        await logger.process_frame(frame, direction=None)

        # Assert
        args, _ = mock_web_server.manager.broadcast.call_args
        message = json.loads(args[0])

        assert "[REDACTED]" in message["data"]
        assert "sk-abcdef1234567890abcdef123456" not in message["data"]

    asyncio.run(run_test())
