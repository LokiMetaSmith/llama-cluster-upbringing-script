import pytest
import asyncio
import os
import sys
from unittest.mock import MagicMock, patch

# Add the docker/pipecatapp directory to the Python path to allow for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'docker', 'pipecatapp')))

# Mock modules that are not part of the test and may have heavy dependencies
MOCK_MODULES = [
    'ultralytics', 'pyaudio', 'piper.voice', 'uvicorn', 'web_server', 'memory',
    'api_keys', 'tools.ssh_tool', 'tools.mcp_tool', 'tools.code_runner_tool',
    'tools.web_browser_tool', 'tools.ansible_tool', 'tools.power_tool',
    'tools.summarizer_tool', 'llm_clients', 'expert_tracker',
    'pipecat.transports.local.audio', 'pipecat.services.openai.llm'
]
for module in MOCK_MODULES:
    sys.modules[module] = MagicMock()

# Now it should be safe to import from app and other local files
from app import FasterWhisperSTTService
from stub_services import StubOutputService
from pipecat.frames.frames import AudioRawFrame, EndFrame, StartFrame, TranscriptionFrame, UserStartedSpeakingFrame, UserStoppedSpeakingFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.processors.frame_processor import FrameProcessor


class MockListAudioSource(FrameProcessor):
    """A mock source that pushes a given list of frames when the pipeline starts."""
    def __init__(self, frames: list):
        super().__init__()
        self._frames = frames

    async def start(self):
        """Overrides the default start behavior to push frames directly."""
        for frame in self._frames:
            await self.push_frame(frame)
        # Signal completion to downstream processors
        await self.push_frame(EndFrame())

@pytest.mark.asyncio
@patch('app.WhisperModel')  # Patch the WhisperModel where it's used in the 'app' module
async def test_stt_mini_pipeline(mock_whisper_model):
    """
    Tests the FasterWhisperSTTService in a minimal, isolated pipeline
    by using a local mock audio source.
    """
    # Configure the mock WhisperModel
    mock_model_instance = mock_whisper_model.return_value
    mock_segment = MagicMock()
    mock_segment.text = "Hello world"
    mock_model_instance.transcribe.return_value = ([mock_segment], None)

    # The pipeline will consist of our mock source, the STT service, and a stub output.
    source = MockListAudioSource([
        UserStartedSpeakingFrame(),
        AudioRawFrame(b'\\x00\\x00', 16000, 1),  # Dummy audio data
        UserStoppedSpeakingFrame(),
    ])

    stt = FasterWhisperSTTService(model_path="dummy_model", sample_rate=16000)
    stub_output = StubOutputService()

    pipeline = Pipeline([
        source,
        stt,
        stub_output,
    ])

    runner = PipelineRunner()

    task = PipelineTask(pipeline)

    await runner.run(task)

    # Check the frames collected by the stub output service
    transcription_frames = [f for f in stub_output.frames if isinstance(f, TranscriptionFrame)]

    assert len(transcription_frames) == 1
    assert transcription_frames[0].text == "Hello world"

    mock_model_instance.transcribe.assert_called_once()
