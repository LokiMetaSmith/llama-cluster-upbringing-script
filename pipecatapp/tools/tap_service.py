
from pipecat.frames.frames import Frame, FrameProcessor

import logging

logger = logging.getLogger("pipecat")

class TapService(FrameProcessor):
    def __init__(self, name: str):
        super().__init__()
        self._name = name

    async def process_frame(self, frame: Frame, direction):
        logger.info(f"TAP SERVICE '{self._name}': {frame}")
        await self.push_frame(frame, direction)
