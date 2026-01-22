import sys
from unittest.mock import MagicMock, patch
import numpy as np
import pytest

# Mock dependencies before importing app
sys.modules["faster_whisper"] = MagicMock()
sys.modules["pipecat"] = MagicMock()
sys.modules["pipecat.frames.frames"] = MagicMock()
sys.modules["pipecat.pipeline.pipeline"] = MagicMock()
sys.modules["pipecat.pipeline.runner"] = MagicMock()
sys.modules["pipecat.pipeline.task"] = MagicMock()

# Define a real class for FrameProcessor instead of MagicMock
class MockFrameProcessor:
    def __init__(self):
        pass
    async def push_frame(self, frame, direction):
        pass

mock_fp_module = MagicMock()
mock_fp_module.FrameProcessor = MockFrameProcessor
sys.modules["pipecat.processors.frame_processor"] = mock_fp_module

sys.modules["pipecat.services.openai.llm"] = MagicMock()
sys.modules["pipecat.transports.local.audio"] = MagicMock()
sys.modules["piper.voice"] = MagicMock()
sys.modules["ultralytics"] = MagicMock()
sys.modules["consul"] = MagicMock()
sys.modules["consul.aio"] = MagicMock()
sys.modules["uvicorn"] = MagicMock()

# Mock internal modules
sys.modules["pmm_memory"] = MagicMock()
sys.modules["pmm_memory_client"] = MagicMock()
sys.modules["quality_control"] = MagicMock()
sys.modules["web_server"] = MagicMock()
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
sys.modules["agent_factory"] = MagicMock()
sys.modules["task_supervisor"] = MagicMock()
sys.modules["durable_execution"] = MagicMock()
sys.modules["moondream_detector"] = MagicMock()
sys.modules["workflow.runner"] = MagicMock()
sys.modules["workflow.nodes.base_nodes"] = MagicMock()
sys.modules["workflow.nodes.llm_nodes"] = MagicMock()
sys.modules["workflow.nodes.tool_nodes"] = MagicMock()
sys.modules["workflow.nodes.system_nodes"] = MagicMock()
sys.modules["api_keys"] = MagicMock()
sys.modules["PIL"] = MagicMock()
sys.modules["requests"] = MagicMock()
sys.modules["httpx"] = MagicMock()
sys.modules["torch"] = MagicMock()

# Now we can import the class we want to test
# We need to use patch because FrameProcessor is imported from pipecat
from pipecatapp.app import FasterWhisperSTTService

class TestFasterWhisperSTTService:
    def test_convert_audio_bytes_to_float_array(self):
        # Create a mock instance
        # We mock __init__ to avoid model loading
        with patch.object(FasterWhisperSTTService, "__init__", return_value=None):
            service = FasterWhisperSTTService("dummy_path")

            # Generate some dummy audio data (int16)
            # 3 values: 0, 32767, -32768
            audio_int16 = np.array([0, 32767, -32768], dtype=np.int16)
            audio_bytes = audio_int16.tobytes()

            # Helper function (which we want to preserve logic of)
            def original_logic(audio_bytes):
                audio_s16 = np.frombuffer(audio_bytes, dtype=np.int16)
                return audio_s16.astype(np.float32) / 32768.0

            result = original_logic(audio_bytes)

            # Verification
            assert len(result) == 3
            assert result.dtype == np.float32
            assert result[0] == 0.0
            assert np.isclose(result[1], 32767.0 / 32768.0)
            assert result[2] == -1.0

    def test_transcribe_sync_refactoring(self):
        """
        Verify that we can pass bytes to _transcribe_sync and it handles conversion.
        This uses the actual implemented method in app.py.
        """
        with patch.object(FasterWhisperSTTService, "__init__", return_value=None):
            service = FasterWhisperSTTService("dummy_path")
            service.model = MagicMock()

            # Mock the transcribe method of the model
            mock_segment = MagicMock()
            mock_segment.text = "Hello world"
            service.model.transcribe.return_value = ([mock_segment], None)

            # Test with dummy data
            audio_int16 = np.array([0, 100, -100], dtype=np.int16)
            audio_bytes = audio_int16.tobytes()

            # Call the actual method
            transcript = service._transcribe_sync(audio_bytes)

            assert transcript == "Hello world"
            # Verify transcribe was called with float array
            assert service.model.transcribe.called
            args, _ = service.model.transcribe.call_args
            passed_audio = args[0]
            assert passed_audio.dtype == np.float32
