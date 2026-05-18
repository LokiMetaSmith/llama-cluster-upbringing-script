import asyncio
import io
import logging
import os
import re
from contextlib import asynccontextmanager

import numpy as np

try:
    from PIL import Image
except ImportError:
    Image = None

from pipecat.frames.frames import (
    AudioRawFrame,
    TextFrame,
    Frame,
    CancelFrame,
    UserImageRawFrame,
    UserImageRawFrame as VisionImageRawFrame,
    StartFrame,
    EndFrame,
    UserStoppedSpeakingFrame
)
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor

try:
    import litert_lm
except ImportError:
    litert_lm = None


HF_REPO = "litert-community/gemma-4-E2B-it-litert-lm"
HF_FILENAME = "gemma-4-E2B-it.litertlm"

logger = logging.getLogger("pipecat")


def _resolve_model_path() -> str:
    path = os.environ.get("MODEL_PATH", "")
    if path:
        return path
    from huggingface_hub import hf_hub_download
    logger.info(f"Downloading {HF_REPO}/{HF_FILENAME} (first run only)...")
    return hf_hub_download(repo_id=HF_REPO, filename=HF_FILENAME)


class GemmaE2BService(FrameProcessor):
    """
    A custom Pipecat processor that uses litert_lm (Gemma 4 E2B) to natively process
    raw audio and images, bypassing the need for separate STT or VLM steps.
    """

    def __init__(self, system_prompt: str = None, **kwargs):
        super().__init__(**kwargs)
        if litert_lm is None:
            raise ImportError("litert-lm is not installed. Please install it to use GemmaE2BService.")

        self.system_prompt = system_prompt or (
            "You are a friendly, conversational AI assistant. The user is talking to you "
            "through a microphone and showing you their camera. "
            "First transcribe exactly what the user said, then write your response."
        )

        self._engine = None
        self._current_audio = bytearray()
        self._current_image = None
        self._is_processing = False

        self._sentence_split_re = re.compile(r'(?<=[.!?])\s+')
        self.model_path = _resolve_model_path()

    def _load_model(self):
        if self._engine is None:
            logger.info(f"Loading Gemma 4 E2B model from {self.model_path}")
            self._engine = litert_lm.Engine(self.model_path)
            self._engine.init(
                max_prefill_length=10000,
                max_decode_length=1024,
                num_threads=4,
                weight_type=litert_lm.WeightType.WQ4
            )
            logger.info("Gemma 4 E2B engine initialized.")

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        if isinstance(frame, StartFrame):
            self._load_model()
            await self.push_frame(frame, direction)

        elif isinstance(frame, EndFrame):
            await self.push_frame(frame, direction)

        elif isinstance(frame, CancelFrame):
            self._current_audio = bytearray()
            self._current_image = None
            self._is_processing = False
            await self.push_frame(frame, direction)

        elif isinstance(frame, AudioRawFrame):
            if not self._is_processing:
                # Accumulate raw PCM 16kHz audio
                # Gemma E2B expects 16kHz float32. We assume incoming is int16.
                # If incoming is 16kHz we just keep it, we'll convert it when executing.
                self._current_audio.extend(frame.audio)

            # Pass through the audio frame untouched (unless we want to consume it)
            # Typically, we'd wait for a VAD frame or a prompt to process.

        elif isinstance(frame, (UserImageRawFrame, VisionImageRawFrame)):
            if not self._is_processing and Image is not None:
                # Store the latest image frame
                try:
                    img = Image.open(io.BytesIO(frame.image))
                    self._current_image = img.copy()
                except Exception as e:
                    logger.error(f"GemmaE2BService failed to read image: {e}")

        elif isinstance(frame, UserStoppedSpeakingFrame):
            await self.push_frame(frame, direction)
            if not self._is_processing:
                # Use create_task to avoid blocking the pipeline while generating
                asyncio.create_task(self._generate_response(direction))
        else:
            await self.push_frame(frame, direction)

    async def _generate_response(self, direction: FrameDirection):
        if not self._current_audio:
            logger.warning("No audio accumulated for Gemma 4 E2B processing.")
            return

        self._is_processing = True

        try:
            audio_array = np.frombuffer(self._current_audio, dtype=np.int16)
            audio_f32 = audio_array.astype(np.float32) / 32768.0

            prompts = []
            if self._current_image:
                rgb_img = self._current_image.convert("RGB")
                img_array = np.array(rgb_img)
                prompts.append(litert_lm.Image(img_array))
                logger.debug("Image added to Gemma prompt.")

            prompts.append(litert_lm.Audio(audio_f32))
            logger.debug(f"Audio added to Gemma prompt (length: {len(audio_f32)}).")

            builder = self._engine.build_prompt()
            builder.add_text(f"System: {self.system_prompt}\nUser: ")

            for p in prompts:
                builder.add(p)

            loop = asyncio.get_event_loop()
            queue = asyncio.Queue()

            def run_inference():
                current_sentence = []
                try:
                    for output in self._engine.generate(builder):
                        # If canceled during thought process, break early
                        if not self._is_processing:
                            break

                        token = output
                        current_sentence.append(token)
                        text_so_far = "".join(current_sentence)

                        if self._sentence_split_re.search(text_so_far):
                            loop.call_soon_threadsafe(queue.put_nowait, text_so_far)
                            current_sentence = []

                    if current_sentence and self._is_processing:
                        loop.call_soon_threadsafe(queue.put_nowait, "".join(current_sentence))
                finally:
                    loop.call_soon_threadsafe(queue.put_nowait, None) # EOF marker

            thread_task = loop.run_in_executor(None, run_inference)

            while True:
                sentence = await queue.get()
                if sentence is None:
                    break

                if not self._is_processing:
                    break # Abort if canceled

                sentence = sentence.strip()
                if sentence:
                    logger.debug(f"Gemma 4 generated: {sentence}")
                    await self.push_frame(TextFrame(text=sentence), direction)

            await thread_task

        except Exception as e:
            logger.error(f"Gemma 4 E2B inference error: {e}")
        finally:
            self._current_audio = bytearray()
            self._current_image = None
            self._is_processing = False
