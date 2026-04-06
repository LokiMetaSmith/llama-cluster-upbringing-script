import asyncio
import io
import pytest
import sys
from unittest.mock import MagicMock, patch

# Mock pipecat module hierarchy
mock_pipecat = MagicMock()
sys.modules["pipecat"] = mock_pipecat
sys.modules["pipecat.frames"] = MagicMock()
sys.modules["pipecat.frames.frames"] = MagicMock()
sys.modules["pipecat.processors"] = MagicMock()
sys.modules["pipecat.processors.frame_processor"] = MagicMock()

# Define mock classes
class MockFrame: pass
class MockAudioRawFrame(MockFrame):
    def __init__(self, audio, sample_rate, num_channels):
        self.audio = audio
        self.sample_rate = sample_rate
        self.num_channels = num_channels
class MockTextFrame(MockFrame):
    def __init__(self, text):
        self.text = text
class MockStartFrame(MockFrame): pass
class MockEndFrame(MockFrame): pass
class MockUserImageRawFrame(MockFrame):
    def __init__(self, image):
        self.image = image
class MockCancelFrame(MockFrame): pass
class MockUserStoppedSpeakingFrame(MockFrame): pass

class MockFrameDirection:
    DOWNSTREAM = "DOWNSTREAM"
    UPSTREAM = "UPSTREAM"

class MockFrameProcessor:
    def __init__(self, **kwargs):
        pass
    async def process_frame(self, frame, direction):
        pass
    async def push_frame(self, frame, direction):
        pass

# Assign mocks
sys.modules["pipecat.frames.frames"].Frame = MockFrame
sys.modules["pipecat.frames.frames"].AudioRawFrame = MockAudioRawFrame
sys.modules["pipecat.frames.frames"].TextFrame = MockTextFrame
sys.modules["pipecat.frames.frames"].StartFrame = MockStartFrame
sys.modules["pipecat.frames.frames"].EndFrame = MockEndFrame
sys.modules["pipecat.frames.frames"].UserImageRawFrame = MockUserImageRawFrame
sys.modules["pipecat.frames.frames"].CancelFrame = MockCancelFrame
sys.modules["pipecat.frames.frames"].VisionImageRawFrame = MockUserImageRawFrame
sys.modules["pipecat.frames.frames"].UserStoppedSpeakingFrame = MockUserStoppedSpeakingFrame

sys.modules["pipecat.processors.frame_processor"].FrameDirection = MockFrameDirection
sys.modules["pipecat.processors.frame_processor"].FrameProcessor = MockFrameProcessor

# Mock litert_lm
mock_litert = MagicMock()
sys.modules['litert_lm'] = mock_litert

from pipecatapp.services.gemma_e2b_service import GemmaE2BService

@pytest.fixture
def mock_engine():
    engine = MagicMock()
    mock_litert.Engine.return_value = engine
    mock_litert.WeightType = MagicMock()
    mock_litert.WeightType.WQ4 = "WQ4"

    builder = MagicMock()
    engine.build_prompt.return_value = builder
    engine.generate.return_value = ["Hello", " world.", " How", " are", " you?"]
    return engine

@pytest.mark.asyncio
async def test_gemma_service_initialization():
    service = GemmaE2BService()
    assert service.system_prompt is not None
    assert service._engine is None

@pytest.mark.asyncio
@patch('pipecatapp.services.gemma_e2b_service._resolve_model_path')
async def test_gemma_service_start_frame(mock_resolve, mock_engine):
    mock_resolve.return_value = "/fake/path.litertlm"
    service = GemmaE2BService()
    frame = MockStartFrame()
    await service.process_frame(frame, MockFrameDirection.DOWNSTREAM)
    assert service._engine is not None
    mock_litert.Engine.assert_called_once()
    mock_engine.init.assert_called_once()

@pytest.mark.asyncio
@patch('pipecatapp.services.gemma_e2b_service._resolve_model_path')
async def test_gemma_service_audio_accumulation(mock_resolve, mock_engine):
    mock_resolve.return_value = "/fake/path.litertlm"
    service = GemmaE2BService()
    audio_frame1 = MockAudioRawFrame(audio=b"\x00\x01\x02\x03", sample_rate=16000, num_channels=1)
    audio_frame2 = MockAudioRawFrame(audio=b"\x04\x05", sample_rate=16000, num_channels=1)
    await service.process_frame(audio_frame1, MockFrameDirection.DOWNSTREAM)
    await service.process_frame(audio_frame2, MockFrameDirection.DOWNSTREAM)
    assert len(service._current_audio) == 6
    assert service._current_audio == b"\x00\x01\x02\x03\x04\x05"

@pytest.mark.asyncio
@patch('pipecatapp.services.gemma_e2b_service._resolve_model_path')
async def test_gemma_service_processing(mock_resolve, mock_engine):
    mock_resolve.return_value = "/fake/path.litertlm"
    service = GemmaE2BService()
    output_frames = []
    async def mock_push_frame(frame, direction):
        if isinstance(frame, MockTextFrame):
            output_frames.append(frame)
    service.push_frame = mock_push_frame

    await service.process_frame(MockStartFrame(), MockFrameDirection.DOWNSTREAM)
    audio_frame = MockAudioRawFrame(audio=b"\x00\x01\x02\x03", sample_rate=16000, num_channels=1)
    await service.process_frame(audio_frame, MockFrameDirection.DOWNSTREAM)

    # Process trigger is now UserStoppedSpeakingFrame
    process_frame = MockUserStoppedSpeakingFrame()
    await service.process_frame(process_frame, MockFrameDirection.DOWNSTREAM)

    # Let the async tasks run
    await asyncio.sleep(0.1)

    mock_engine.generate.assert_called_once()
    assert len(output_frames) == 2
    assert output_frames[0].text == "Hello world. How"
    assert output_frames[1].text == "are you?"
    assert len(service._current_audio) == 0
    assert service._is_processing is False

@pytest.mark.asyncio
@patch('pipecatapp.services.gemma_e2b_service._resolve_model_path')
async def test_gemma_service_barge_in_cancellation(mock_resolve, mock_engine):
    mock_resolve.return_value = "/fake/path.litertlm"
    service = GemmaE2BService()

    output_frames = []
    async def mock_push_frame(frame, direction):
        if isinstance(frame, MockTextFrame):
            output_frames.append(frame)
    service.push_frame = mock_push_frame

    # Configure mock engine to be slow to simulate background processing
    def slow_generate(builder):
        import time
        for token in ["Hello", " world.", " How"]:
            time.sleep(0.05)
            yield token

    mock_engine.generate.side_effect = slow_generate

    await service.process_frame(MockStartFrame(), MockFrameDirection.DOWNSTREAM)
    await service.process_frame(MockAudioRawFrame(audio=b"\x00\x01", sample_rate=16000, num_channels=1), MockFrameDirection.DOWNSTREAM)

    # Trigger generation
    process_task = asyncio.create_task(service.process_frame(MockUserStoppedSpeakingFrame(), MockFrameDirection.DOWNSTREAM))

    # Wait a tiny bit then cancel (barge-in)
    await asyncio.sleep(0.01)
    await service.process_frame(MockCancelFrame(), MockFrameDirection.DOWNSTREAM)

    await process_task
    # Wait for any dangling background threads
    await asyncio.sleep(0.2)

    # Generate might have been called, but no frames should be pushed!
    assert len(output_frames) == 0
    assert service._is_processing is False
