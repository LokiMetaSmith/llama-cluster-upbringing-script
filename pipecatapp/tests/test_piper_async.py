import sys
import os
import asyncio
import threading
import pytest
from unittest.mock import MagicMock, patch

@pytest.mark.asyncio
async def test_piper_tts_async_execution():
    # Setup path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    # Context manager for mocking sys.modules ensures we don't pollute global state for other tests
    with patch.dict(sys.modules):
        MOCK_MODULES = [
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
            "PIL",
            "PIL.Image",
            "requests",
            "httpx",
            "dotenv",
            "pydantic",
            "uvicorn",
            "agent_factory",
            "task_supervisor",
            "durable_execution",
            "moondream_detector",
            "workflow",
            "workflow.runner",
            "workflow.nodes",
            "workflow.nodes.base_nodes",
            "workflow.nodes.llm_nodes",
            "workflow.nodes.tool_nodes",
            "workflow.nodes.system_nodes",
            "api_keys",
            "web_server",
        ]

        for mod in MOCK_MODULES:
            sys.modules[mod] = MagicMock()

        # Mock specific classes used in inheritance or typing
        # We need to recreate these structure inside the loop because sys.modules is fresh (mostly)

        # Ensure 'pipecat.processors.frame_processor' is a module
        sys.modules["pipecat.processors.frame_processor"] = MagicMock()

        class MockFrameProcessor:
            def __init__(self):
                pass
            async def push_frame(self, frame, direction=None):
                pass
        sys.modules["pipecat.processors.frame_processor"].FrameProcessor = MockFrameProcessor

        # Mock Frames
        class MockTextFrame:
            def __init__(self, text):
                self.text = text

        sys.modules["pipecat.frames.frames"].TextFrame = MockTextFrame
        sys.modules["pipecat.frames.frames"].AudioRawFrame = MagicMock()

        # Mock tools package
        tools_mock = MagicMock()
        sys.modules["tools"] = tools_mock
        tool_names = [
            "ssh_tool", "mcp_tool", "desktop_control_tool", "code_runner_tool", "web_browser_tool",
            "ansible_tool", "power_tool", "summarizer_tool", "term_everything_tool", "rag_tool",
            "ha_tool", "git_tool", "orchestrator_tool", "llxprt_code_tool", "claude_clone_tool",
            "smol_agent_tool", "final_answer_tool", "shell_tool", "prompt_improver_tool",
            "council_tool", "swarm_tool", "project_mapper_tool", "planner_tool"
        ]
        for t in tool_names:
            sys.modules[f"tools.{t}"] = MagicMock()

        # Import app
        # Force reload or clean import
        if 'app' in sys.modules:
            del sys.modules['app']

        from app import PiperTTSService

        # Setup Test Mocks
        mock_voice = MagicMock()
        mock_voice.config.sample_rate = 16000

        execution_thread_id = None

        def side_effect_synthesize(text, stream):
            nonlocal execution_thread_id
            execution_thread_id = threading.get_ident()
            # Write dummy wav
            import wave
            with wave.open(stream, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes(b'\x00' * 100)

        mock_voice.synthesize.side_effect = side_effect_synthesize

        # Patch PiperVoice.load to return our mock
        with patch("piper.voice.PiperVoice.load", return_value=mock_voice):
            service = PiperTTSService(model_path="dummy")

            main_thread_id = threading.get_ident()
            frame = MockTextFrame("test")

            await service.process_frame(frame, direction=None)

            print(f"Main thread: {main_thread_id}")
            print(f"Exec thread: {execution_thread_id}")

            # Verify
            assert execution_thread_id is not None
            assert execution_thread_id != main_thread_id, "Piper TTS synthesis blocked the main event loop!"
