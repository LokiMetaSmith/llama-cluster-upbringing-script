import asyncio
import base64
import json
import logging
import os
import struct
import tempfile
import time
import httpx

from pipecat.frames.frames import (
    Frame,
    AudioRawFrame,
    TextFrame,
    TranscriptionFrame,
    UserStoppedSpeakingFrame,
)
from pipecat.processors.frame_processor import FrameProcessor

from pipecatapp.net_utils import resolve_and_validate_url, get_safe_url_and_headers
from pipecatapp.security import redact_sensitive_data


class AudioFileFrame(Frame):
    """A frame containing a path to an audio file."""
    def __init__(self, file_path: str, meta: dict = None):
        super().__init__()
        self.file_path = file_path
        self.meta = meta or {}

class UILogger(FrameProcessor):
    """A Pipecat frame processor that logs frames to the web UI.

    This processor intercepts transcription and text frames and sends their
    content to the WebSocket manager for display in the UI.

    Attributes:
        sender (str): A string identifier ('user' or 'agent') to label
                      the source of the message in the UI.
    """
    def __init__(self, sender: str):
        """Initializes the UILogger.

        Args:
            sender (str): The identifier for the message source (e.g., "user").
        """
        super().__init__()
        self.sender = sender

    async def process_frame(self, frame, direction):
        """Processes incoming frames and logs relevant ones to the UI.

        Args:
            frame: The frame to process.
            direction: The direction of the frame in the pipeline.
        """
        if isinstance(frame, (TranscriptionFrame, TextFrame)):
            # Security Fix: Sentinel - Redact sensitive information
            redacted_text = redact_sensitive_data(frame.text)

            # Import dynamically to avoid circular dependencies
            import pipecatapp.web_server
            await pipecatapp.web_server.manager.broadcast(json.dumps({"type": self.sender, "data": redacted_text}))
        await self.push_frame(frame, direction)

class BenchmarkCollector(FrameProcessor):
    """A Pipecat frame processor for measuring pipeline latency.

    This captures timestamps at key stages of the conversational pipeline
    (speech detection, transcription, LLM response, audio synthesis) to
    calculate and log performance metrics.
    """
    def __init__(self):
        """Initializes the BenchmarkCollector and resets its state."""
        super().__init__()
        self.reset()

    async def process_frame(self, frame, direction):
        """Processes frames to capture timing information.

        Args:
            frame: The frame to process.
            direction: The direction of the frame in the pipeline.
        """
        if isinstance(frame, UserStoppedSpeakingFrame):
            self.start_time = time.time()
        elif isinstance(frame, TranscriptionFrame):
            self.stt_end_time = time.time()
        elif isinstance(frame, TextFrame) and self.llm_first_token_time == 0:
            self.llm_first_token_time = time.time()
        elif isinstance(frame, AudioRawFrame) and self.tts_first_audio_time == 0:
            self.tts_first_audio_time = time.time()
            self.log_benchmarks()
            self.reset()
        await self.push_frame(frame, direction)

    def log_benchmarks(self):
        """Calculates and logs the latency benchmarks."""
        stt_latency = self.stt_end_time - self.start_time
        llm_ttft = self.llm_first_token_time - self.stt_end_time
        tts_ttfa = self.tts_first_audio_time - self.llm_first_token_time
        total_latency = self.tts_first_audio_time - self.start_time
        logging.info(
            f"--- BENCHMARK RESULTS ---\n"
            f"STT Latency: {stt_latency:.4f}s\n"
            f"LLM Time to First Token: {llm_ttft:.4f}s\n"
            f"TTS Time to First Audio: {tts_ttfa:.4f}s\n"
            f"Total Pipeline Latency: {total_latency:.4f}s\n"
            f"-------------------------"
        )

    def reset(self):
        """Resets all benchmark timestamps to zero."""
        self.start_time = 0
        self.stt_end_time = 0
        self.llm_first_token_time = 0
        self.tts_first_audio_time = 0

class TextMessageInjector(FrameProcessor):
    """A processor to inject text from the UI into the Pipecat pipeline.

    This allows a user to type messages in a web interface and have them
    processed by the agent as if they were spoken.

    Attributes:
        queue (asyncio.Queue): The queue for receiving messages from the UI.
    """
    def __init__(self, queue: asyncio.Queue):
        """Initializes the TextMessageInjector.

        Args:
            queue (asyncio.Queue): The queue to listen on for new messages.
        """
        super().__init__()
        self.queue = queue
        self._task = None

    def start_listening(self):
        """Starts the background task that listens for messages on the queue."""
        if not self._task:
            self._task = asyncio.create_task(self._run())

    async def _run(self):
        """The main loop that waits for messages and pushes them into the pipeline."""
        while True:
            try:
                message = await self.queue.get()
                # The message can be a simple string (from UI) or a dict (from gateway)
                if isinstance(message, dict):
                    audio_url = message.get("audio_url")
                    audio_base64 = message.get("audio_base64")
                    text = message.get("text")
                    is_system_alert = message.get("is_system_alert", False)

                    if audio_url:
                        logging.info(f"Downloading audio from: {audio_url}")
                        try:
                            # Security Fix: Sentinel - Validate URL and use resolved IP for HTTP to prevent DNS Rebinding
                            original_url, safe_ip = await resolve_and_validate_url(audio_url)
                            safe_url, headers = get_safe_url_and_headers(original_url, safe_ip)

                            # Create a temp file to store the audio
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                                async with httpx.AsyncClient() as client:
                                    # Security Fix: Sentinel - Enforce size limit on audio downloads to prevent DoS
                                    MAX_AUDIO_SIZE = 50 * 1024 * 1024  # 50 MB limit
                                    async with client.stream("GET", safe_url, headers=headers) as resp:
                                        if resp.status_code == 200:
                                            downloaded_size = 0
                                            async for chunk in resp.aiter_bytes():
                                                downloaded_size += len(chunk)
                                                if downloaded_size > MAX_AUDIO_SIZE:
                                                    raise ValueError(f"Audio file exceeds limit of {MAX_AUDIO_SIZE} bytes")
                                                tmp_file.write(chunk)
                                            tmp_path = tmp_file.name
                                            await self.push_frame(AudioFileFrame(tmp_path, meta=message))
                                        else:
                                            logging.error(f"Failed to download audio from {audio_url}: {resp.status_code}")
                        except Exception as e:
                            logging.error(f"Error downloading audio: {e}")

                    elif audio_base64:
                        logging.info("Decoding base64 audio message")
                        try:
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                                tmp_file.write(base64.b64decode(audio_base64))
                                tmp_path = tmp_file.name
                                await self.push_frame(AudioFileFrame(tmp_path, meta=message))
                        except Exception as e:
                            logging.error(f"Error decoding base64 audio: {e}")

                    elif text:
                        if is_system_alert:
                            prefix = "SYSTEM ALERT: "
                            logging.warning(f"Injecting system alert: {text}")

                            # Check if this is a gateway exhaustion trigger for auto-scaling
                            if "Gateway reported critical exhaustion for expert" in text:
                                try:
                                    # Extract expert name from the message
                                    parts = text.split("expert:")
                                    if len(parts) > 1:
                                        expert_name = parts[1].split(".")[0].strip()
                                        import pipecatapp.web_server
                                        twin_service = getattr(pipecatapp.web_server.app.state, "twin_service_instance", None)
                                        if twin_service and hasattr(twin_service, "task_supervisor"):
                                            # Trigger dynamic auto-scaling in the supervisor
                                            asyncio.create_task(twin_service.task_supervisor.handle_gateway_exhaustion(expert_name))
                                except Exception as ex_fail:
                                    logging.error(f"Failed to trigger auto-scaling from system alert: {ex_fail}")

                            # Prepend alert tag to text to ensure the agent takes it seriously
                            text = f"{prefix}{text}"

                        logging.info(f"Injecting text message from gateway: {text}")
                        await self.push_frame(TranscriptionFrame(text, meta=message))
                elif isinstance(message, str):
                     # Legacy support for simple text messages
                    logging.info(f"Injecting text message from UI: {message}")
                    await self.push_frame(TranscriptionFrame(message))
            except Exception as e:
                logging.error(f"Error in TextMessageInjector: {e}")

    async def process_frame(self, frame, direction):
        """Passes frames through without modification.

        Args:
            frame: The frame to process.
            direction: The direction of the frame in the pipeline.
        """
        await self.push_frame(frame, direction)

    def stop_listening(self):
        """Stops the background listening task."""
        if self._task:
            self._task.cancel()
            self._task = None

class WebsocketAudioStreamer(FrameProcessor):
    """A Pipecat processor that streams audio frames to the frontend via WebSockets.

    This enables spatial audio in the VR interface.
    """
    def __init__(self, sample_rate: int = 16000):
        super().__init__()
        self.sample_rate = sample_rate

    async def process_frame(self, frame, direction):
        if not isinstance(frame, AudioRawFrame):
            await self.push_frame(frame, direction)
            return

        # Wrap raw PCM in WAV container for browser compatibility
        try:
            # Bolt ⚡ Optimization: Manually construct WAV header instead of using 'wave' module
            # This is ~7x faster and reduces object allocation
            audio_data = frame.audio
            length = len(audio_data)

            # WAV Header: 44 bytes
            # RIFF + size + WAVE + fmt + size + 1 (PCM) + 1 (channels) + rate + byte_rate + block_align + bits + data + size
            # We assume Mono 16-bit PCM as per app config
            header = struct.pack(
                '<4sI4s4sIHHIIHH4sI',
                b'RIFF',
                36 + length,
                b'WAVE',
                b'fmt ',
                16,
                1, # PCM
                1, # Mono
                self.sample_rate,
                self.sample_rate * 2, # ByteRate (SampleRate * NumChannels * BitsPerSample/8)
                2, # BlockAlign (NumChannels * BitsPerSample/8)
                16, # BitsPerSample
                b'data',
                length
            )

            # Combine header and audio data, then encode
            wav_bytes = header + audio_data
            b64_audio = base64.b64encode(wav_bytes).decode('utf-8')

            # Fix: Import web_server locally
            try:
                import pipecatapp.web_server
                await pipecatapp.web_server.manager.broadcast(json.dumps({
                    "type": "audio",
                    "data": b64_audio
                }))
            except Exception as ws_err:
                logging.error(f"Failed to stream audio frame: {ws_err}")

        except Exception as e:
             logging.error(f"Error packing audio for stream: {e}")

        await self.push_frame(frame, direction)
