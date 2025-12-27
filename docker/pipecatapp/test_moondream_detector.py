import pytest
from unittest.mock import MagicMock, patch
import torch
from pipecat.frames.frames import UserImageRawFrame as VisionImageRawFrame
from PIL import Image
import numpy as np

from moondream_detector import MoondreamDetector

@pytest.fixture
def mock_torch():
    """Fixture to mock the torch library."""
    with patch('moondream_detector.torch') as mock:
        mock.cuda.is_available.return_value = False
        # Mock torch.compile to behave like identity or return a mock that passes calls through
        def mock_compile(model, **kwargs):
            return model
        mock.compile.side_effect = mock_compile
        yield mock

@pytest.fixture
def mock_auto_model():
    """Fixture to mock the AutoModelForCausalLM."""
    with patch('moondream_detector.AutoModelForCausalLM') as mock:
        mock_instance = mock.from_pretrained.return_value
        # Ensure the model mock behaves well when "compiled" (which is now identity)
        mock_instance.caption.return_value = {"caption": "a cat"}
        yield mock

@pytest.mark.asyncio
async def test_initialization(mock_torch, mock_auto_model):
    """Tests that the MoondreamDetector initializes correctly."""
    detector = MoondreamDetector()
    assert detector.latest_observation == "I don't see anything."
    mock_auto_model.from_pretrained.assert_called_once()

@pytest.mark.asyncio
async def test_process_frame(mock_torch, mock_auto_model):
    """Tests the process_frame method."""
    detector = MoondreamDetector()
    image = Image.fromarray(np.uint8(np.random.rand(100, 100, 3) * 255))
    frame = VisionImageRawFrame(image=image, size=(100, 100), format="RGB")
    await detector.process_frame(frame, None)
    assert detector.latest_observation == "a cat"

@pytest.mark.asyncio
async def test_process_frame_error(mock_torch, mock_auto_model):
    """Tests the process_frame method with an error."""
    mock_auto_model.from_pretrained.return_value.caption.side_effect = Exception("test error")
    detector = MoondreamDetector()
    image = Image.fromarray(np.uint8(np.random.rand(100, 100, 3) * 255))
    frame = VisionImageRawFrame(image=image, size=(100, 100), format="RGB")
    await detector.process_frame(frame, None)
    assert detector.latest_observation == "I am having trouble seeing."

@pytest.mark.asyncio
async def test_get_observation(mock_torch, mock_auto_model):
    """Tests the get_observation method."""
    detector = MoondreamDetector()
    assert detector.get_observation() == "I don't see anything."
    image = Image.fromarray(np.uint8(np.random.rand(100, 100, 3) * 255))
    frame = VisionImageRawFrame(image=image, size=(100, 100), format="RGB")
    await detector.process_frame(frame, None)
    assert detector.get_observation() == "a cat"
