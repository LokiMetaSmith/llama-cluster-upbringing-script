import pytest
import sys
import os
from unittest.mock import MagicMock, AsyncMock, patch

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

# Mock dependencies
mock_pipecat = MagicMock()
mock_frames = MagicMock()

sys.modules['pipecat'] = mock_pipecat
sys.modules['pipecat.frames'] = mock_frames
sys.modules['pipecat.frames.frames'] = mock_frames

# FrameProcessor is a class, so we mock it as a class
class MockFrameProcessor:
    def __init__(self):
        pass
    async def push_frame(self, frame, direction):
        pass

mock_frames.FrameProcessor = MockFrameProcessor
mock_frames.Frame = MagicMock()

from tap_service import TapService

@pytest.mark.asyncio
async def test_process_frame():
    service = TapService("test_tap")
    # Mock push_frame on the instance because inheritance might not link it perfectly with our Mock class structure if we didn't patch fully right,
    # but since TapService inherits from MockFrameProcessor, it has push_frame. We replace it to verify call.
    service.push_frame = AsyncMock()

    mock_frame_inst = MagicMock()
    mock_frame_inst.__str__.return_value = "FrameData"

    with patch('tap_service.logger') as mock_logger:
        await service.process_frame(mock_frame_inst, "UPSTREAM")

        mock_logger.info.assert_called_with("TAP SERVICE 'test_tap': FrameData")
        service.push_frame.assert_called_once_with(mock_frame_inst, "UPSTREAM")
