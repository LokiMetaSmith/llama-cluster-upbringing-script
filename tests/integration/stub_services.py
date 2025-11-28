import asyncio
from pipecat.processors.frame_processor import FrameProcessor

class StubOutputService(FrameProcessor):
    """A simple frame processor that collects all frames it receives into a list.

    This is useful for integration tests to verify the output of a pipeline.

    Attributes:
        frames (list): A list of all frames received by the service.
    """
    def __init__(self):
        super().__init__()
        self.frames = []
        self._future = None

    async def process_frame(self, frame, direction):
        """Adds the frame to the internal list."""
        self.frames.append(frame)
        await self.push_frame(frame, direction)

    def wait_for_frame(self):
        """Returns a future that resolves when a frame is received."""
        if not self._future:
            self._future = asyncio.Future()
        return self._future
