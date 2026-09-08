import asyncio
import logging
import os
import struct

import httpx
import numpy as np

from faster_whisper import WhisperModel
from pipecat.frames.frames import (
    AudioRawFrame,
    TranscriptionFrame,
    UserStartedSpeakingFrame,
    UserStoppedSpeakingFrame,
)
from pipecat.processors.frame_processor import FrameProcessor
from wyoming.asr import Transcribe
from wyoming.audio import AudioChunk, AudioStart, AudioStop
from wyoming.client import AsyncTcpClient

from pipecatapp.pipeline.processors import AudioFileFrame


class WyomingSTTService(FrameProcessor):
    """A Pipecat processor for Speech-to-Text using a Wyoming protocol server.

    This service connects to a Wyoming server (e.g., Wyoming ONNX ASR), sends audio
    frames, and waits for transcriptions.
    """
    def __init__(self, host: str, port: int, sample_rate: int = 16000):
        super().__init__()
        self.host = host
        self.port = port
        self.sample_rate = sample_rate
        self.audio_buffer = bytearray()

    async def process_frame(self, frame, direction):
        if isinstance(frame, UserStartedSpeakingFrame):
            self.audio_buffer.clear()
        elif isinstance(frame, AudioRawFrame):
            self.audio_buffer.extend(frame.audio)
        elif isinstance(frame, UserStoppedSpeakingFrame):
            if not self.audio_buffer:
                return

            audio_bytes = bytes(self.audio_buffer)
            self.audio_buffer.clear()

            try:
                # Wyoming protocol interaction
                client = AsyncTcpClient(self.host, self.port)
                await client.connect()

                await client.write_event(Transcribe().event())
                await client.write_event(AudioStart(rate=self.sample_rate, width=2, channels=1).event())

                # Send audio in chunks
                chunk_size = 4096
                for i in range(0, len(audio_bytes), chunk_size):
                    chunk = audio_bytes[i:i + chunk_size]
                    await client.write_event(AudioChunk(rate=self.sample_rate, width=2, channels=1, audio=chunk).event())

                await client.write_event(AudioStop().event())

                # Wait for response
                while True:
                    event = await client.read_event()
                    if event is None:
                        break
                    if event.type == "transcript":
                        text = event.data.get("text", "").strip()
                        if text:
                            await self.push_frame(TranscriptionFrame(text))
                        break

                await client.disconnect()
            except Exception as e:
                logging.error(f"Error communicating with Wyoming STT server: {e}")

class FasterWhisperSTTService(FrameProcessor):
    """A Pipecat processor for Speech-to-Text using Faster-Whisper.

    This service buffers incoming audio frames and, upon detecting the end of
    speech, transcribes the audio using a CPU-optimized Whisper model.

    Attributes:
        model: The loaded Faster-Whisper model.
        audio_buffer (bytearray): A buffer to accumulate audio data.
        sample_rate (int): The audio sample rate required by the model.
    """
    def __init__(self, model_path: str, sample_rate: int = 16000):
        """Initializes the STT service.

        Args:
            model_path (str): The path to the Faster-Whisper model directory.
            sample_rate (int): The sample rate of the input audio.
        """
        super().__init__()
        # Use CPU int8 to reduce memory; adjust if you want GPU
        if not os.path.isdir(model_path):
            logging.error(f"Model directory not found at: {model_path}")
            # Fallback to model name if path doesn't exist
            model_identifier = os.path.basename(model_path)
            logging.info(f"Attempting to load model by name: {model_identifier}")
        else:
            model_identifier = model_path

        try:
            self.model = WhisperModel(
                model_identifier,
                device="cpu",
                compute_type="int8"
            )
        except Exception as e:
            logging.error(f"Fatal error loading WhisperModel with identifier '{model_identifier}': {e}")
            raise e

        self.audio_buffer = bytearray()
        self.sample_rate = sample_rate
        logging.info(f"FasterWhisperSTTService initialized with model identifier '{model_identifier}'")

    def _convert_audio_bytes_to_float_array(self, audio_bytes: bytes) -> np.ndarray:
        """Converts raw 16-bit PCM audio bytes to a 32-bit float NumPy array.

        Args:
            audio_bytes (bytes): The raw audio data.

        Returns:
            np.ndarray: The audio data as a normalized float array.
        """
        audio_s16 = np.frombuffer(audio_bytes, dtype=np.int16)
        # Bolt ⚡ Optimization: In-place multiplication to avoid extra allocation
        audio_f32 = audio_s16.astype(np.float32)
        audio_f32 *= (1.0 / 32768.0)
        return audio_f32

    def _transcribe_sync(self, audio_bytes: bytes) -> str:
        """Synchronous helper for transcription to run in a thread."""
        # Bolt ⚡ Optimization: Perform CPU-heavy numpy conversion in the thread
        audio_data = self._convert_audio_bytes_to_float_array(audio_bytes)
        segments, _ = self.model.transcribe(audio_data, language="en")
        return "".join(segment.text for segment in segments).strip()

    def _transcribe_file_sync(self, file_path: str) -> str:
        """Synchronous helper for file transcription."""
        segments, _ = self.model.transcribe(file_path, language="en")
        return "".join(segment.text for segment in segments).strip()

    async def process_frame(self, frame, direction):
        """Processes audio frames, buffering and transcribing them.

        Args:
            frame: The frame to process.
            direction: The direction of the frame in the pipeline.
        """
        if isinstance(frame, UserStartedSpeakingFrame):
            self.audio_buffer.clear()
        elif isinstance(frame, AudioRawFrame):
            # append incoming audio bytes (signed int16)
            self.audio_buffer.extend(frame.audio)
        elif isinstance(frame, UserStoppedSpeakingFrame):
            if not self.audio_buffer:
                return
            # Bolt ⚡ Optimization: Avoid bytes() copy by swapping buffer
            audio_bytes = self.audio_buffer
            self.audio_buffer = bytearray()

            # Bolt ⚡ Optimization: Run blocking inference in a thread
            loop = asyncio.get_running_loop()
            full_text = await loop.run_in_executor(None, self._transcribe_sync, audio_bytes)

            if full_text:
                await self.push_frame(TranscriptionFrame(full_text))
        elif isinstance(frame, AudioFileFrame):
            logging.info(f"Processing AudioFileFrame: {frame.file_path}")
            loop = asyncio.get_running_loop()
            try:
                full_text = await loop.run_in_executor(None, self._transcribe_file_sync, frame.file_path)
                if full_text:
                    await self.push_frame(TranscriptionFrame(full_text, meta=frame.meta))
            except Exception as e:
                logging.error(f"Error transcribing audio file: {e}")
            finally:
                # Cleanup temp file
                if os.path.exists(frame.file_path):
                    os.remove(frame.file_path)
        else:
            await self.push_frame(frame, direction)

class GroqSTTService(FrameProcessor):
    """A Pipecat processor for Speech-to-Text using Groq's fast Whisper API.

    Attributes:
        api_key: The Groq API key.
        model: The Whisper model to use (default: whisper-large-v3).
    """
    def __init__(self, api_key: str, model: str = "whisper-large-v3"):
        super().__init__()
        self.api_key = api_key
        self.model = model
        self.audio_buffer = bytearray()
        self.client = httpx.AsyncClient(headers={"Authorization": f"Bearer {api_key}"}, timeout=10.0)

    async def _transcribe(self, audio_bytes):
        try:
            # Prepare WAV header (16kHz, 16-bit, Mono)
            header = struct.pack(
                '<4sI4s4sIHHIIHH4sI',
                b'RIFF', 36 + len(audio_bytes), b'WAVE', b'fmt ', 16, 1, 1,
                16000, 32000, 2, 16, b'data', len(audio_bytes)
            )
            wav_data = header + audio_bytes

            files = {'file': ('audio.wav', wav_data, 'audio/wav')}
            data = {'model': self.model, 'response_format': 'json'}

            response = await self.client.post(
                "https://api.groq.com/openai/v1/audio/transcriptions",
                files=files,
                data=data
            )
            response.raise_for_status()
            return response.json().get("text", "").strip()
        except Exception as e:
            logging.error(f"Groq STT error: {e}")
            return ""

    def _read_file_sync(self, file_path: str):
        with open(file_path, "rb") as f:
            return f.read()

    async def _transcribe_file(self, file_path: str):
        try:
            loop = asyncio.get_running_loop()
            file_content = await loop.run_in_executor(None, self._read_file_sync, file_path)

            filename = os.path.basename(file_path)
            # Basic mime type guess or fallback
            mime_type = "audio/mpeg"
            if filename.endswith(".wav"):
                mime_type = "audio/wav"
            elif filename.endswith(".ogg"):
                mime_type = "audio/ogg"
            elif filename.endswith(".m4a"):
                mime_type = "audio/m4a"

            files = {'file': (filename, file_content, mime_type)}
            data = {'model': self.model, 'response_format': 'json'}

            response = await self.client.post(
                "https://api.groq.com/openai/v1/audio/transcriptions",
                files=files,
                data=data
            )
            response.raise_for_status()
            return response.json().get("text", "").strip()
        except Exception as e:
            logging.error(f"Groq STT file error: {e}")
            return ""

    async def process_frame(self, frame, direction):
        if isinstance(frame, UserStartedSpeakingFrame):
            self.audio_buffer.clear()
        elif isinstance(frame, AudioRawFrame):
            self.audio_buffer.extend(frame.audio)
        elif isinstance(frame, UserStoppedSpeakingFrame):
            if not self.audio_buffer:
                return

            audio_bytes = self.audio_buffer
            self.audio_buffer = bytearray()

            text = await self._transcribe(audio_bytes)
            if text:
                await self.push_frame(TranscriptionFrame(text))
        elif isinstance(frame, AudioFileFrame):
            logging.info(f"GroqSTT processing file: {frame.file_path}")
            text = await self._transcribe_file(frame.file_path)
            if text:
                await self.push_frame(TranscriptionFrame(text, meta=frame.meta))
            if os.path.exists(frame.file_path):
                os.remove(frame.file_path)
        else:
            await self.push_frame(frame, direction)
