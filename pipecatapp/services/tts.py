import asyncio
import io
import wave

from kokoro import KPipeline
from pipecat.frames.frames import AudioRawFrame, TextFrame
from pipecat.processors.frame_processor import FrameProcessor
from piper.voice import PiperVoice


class KokoroTTSService(FrameProcessor):
    """A Pipecat processor for Text-to-Speech using Kokoro.

    This service synthesizes speech from text frames using the Kokoro TTS engine
    and pushes the resulting raw audio frames back into the pipeline.
    """
    def __init__(self, model_path: str, lang_code: str = 'a', voice_name: str = 'af_heart'):
        super().__init__()
        self.pipeline = KPipeline(lang_code=lang_code)
        self.voice_name = voice_name
        self.sample_rate = 24000

    def _synthesize_sync(self, text: str) -> bytes:
        """Helper to run synthesis in a separate thread."""
        audio_stream = io.BytesIO()
        # Generate audio using Kokoro
        # KPipeline returns an iterator of (graphemes, phonemes, audio)
        result = list(self.pipeline(text, voice=self.voice_name, speed=1, split_pattern=r'\n+'))
        if not result:
             return b""

        # Concatenate audio chunks if multiple
        import numpy as np
        audio_chunks = [chunk[2] for chunk in result if chunk[2] is not None]
        if not audio_chunks:
            return b""

        full_audio = np.concatenate(audio_chunks)

        # Convert to 16-bit PCM
        import soundfile as sf
        sf.write(audio_stream, full_audio, self.sample_rate, format='WAV', subtype='PCM_16')

        audio_stream.seek(0)
        with wave.open(audio_stream, "rb") as wf:
            return wf.readframes(wf.getnframes())

    async def process_frame(self, frame, direction):
        if not isinstance(frame, TextFrame):
            await self.push_frame(frame, direction)
            return

        loop = asyncio.get_running_loop()
        audio_bytes = await loop.run_in_executor(None, self._synthesize_sync, frame.text)
        await self.push_frame(AudioRawFrame(audio_bytes))

class PiperTTSService(FrameProcessor):
    """A Pipecat processor for Text-to-Speech using Piper.

    This service synthesizes speech from text frames and pushes the resulting
    raw audio frames back into the pipeline.

    Attributes:
        voice: The loaded Piper voice model.
        sample_rate (int): The sample rate of the synthesized audio.
    """
    def __init__(self, model_path: str):
        """Initializes the TTS service.

        Args:
            model_path (str): The path to the Piper TTS model file.
        """
        super().__init__()
        self.voice = PiperVoice.load(model_path)
        self.sample_rate = self.voice.config.sample_rate

    def _synthesize_sync(self, text: str) -> bytes:
        """Helper to run synthesis in a separate thread."""
        audio_stream = io.BytesIO()
        self.voice.synthesize(text, audio_stream)
        audio_stream.seek(0)
        with wave.open(audio_stream, "rb") as wf:
            return wf.readframes(wf.getnframes())

    async def process_frame(self, frame, direction):
        """Processes text frames to synthesize audio.

        Args:
            frame: The frame to process.
            direction: The direction of the frame in the pipeline.
        """
        if not isinstance(frame, TextFrame):
            await self.push_frame(frame, direction)
            return

        loop = asyncio.get_running_loop()
        # Bolt ⚡ Optimization: Run blocking synthesis in a thread
        audio_bytes = await loop.run_in_executor(None, self._synthesize_sync, frame.text)
        await self.push_frame(AudioRawFrame(audio_bytes))

class DummyTTSService(FrameProcessor):
    """A placeholder TTS service that generates no audio but fulfills the pipeline requirement."""
    def __init__(self, sample_rate: int = 16000):
        super().__init__()
        self.sample_rate = sample_rate

    def _synthesize_sync(self, text: str) -> bytes:
        """Returns empty audio."""
        return b""

    async def process_frame(self, frame, direction):
        """Passes text frames through, generating an empty audio frame."""
        if not isinstance(frame, TextFrame):
            await self.push_frame(frame, direction)
            return

        await self.push_frame(AudioRawFrame(b""))
