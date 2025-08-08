import asyncio
import logging
import cv2
import torch
from ultralytics import YOLO
import time

from pipecat.frames.frames import AudioFrame, EndFrame, TextFrame, VisionImageFrame, UserStartedSpeakingFrame, UserStoppedSpeakingFrame, TranscriptionFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.elevenlabs import ElevenLabsTTSService
from pipecat.services.openai import OpenAILLMService
from pipecat.transports.local.local import LocalTransport
from kittentts import KittenTTS as KittenTTSModel
import soundfile as sf
import os

logging.basicConfig(level=logging.DEBUG)

class BenchmarkCollector(FrameProcessor):
    def __init__(self):
        super().__init__()
        self.start_time = 0
        self.stt_end_time = 0
        self.llm_first_token_time = 0
        self.tts_first_audio_time = 0

    async def process_frame(self, frame, direction):
        if isinstance(frame, UserStoppedSpeakingFrame):
            self.start_time = time.time()
        elif isinstance(frame, TranscriptionFrame):
            self.stt_end_time = time.time()
        elif isinstance(frame, TextFrame) and self.llm_first_token_time == 0:
            self.llm_first_token_time = time.time()
        elif isinstance(frame, AudioFrame) and self.tts_first_audio_time == 0:
            self.tts_first_audio_time = time.time()
            self.log_benchmarks()
            self.reset()

        await self.push_frame(frame, direction)

    def log_benchmarks(self):
        stt_latency = self.stt_end_time - self.start_time
        llm_ttft = self.llm_first_token_time - self.stt_end_time
        tts_ttfa = self.tts_first_audio_time - self.llm_first_token_time
        total_latency = self.tts_first_audio_time - self.start_time

        logging.info("--- BENCHMARK RESULTS ---")
        logging.info(f"STT Latency: {stt_latency:.4f}s")
        logging.info(f"LLM Time to First Token: {llm_ttft:.4f}s")
        logging.info(f"TTS Time to First Audio: {tts_ttfa:.4f}s")
        logging.info(f"Total Pipeline Latency: {total_latency:.4f}s")
        logging.info("-------------------------")

    def reset(self):
        self.start_time = 0
        self.stt_end_time = 0
        self.llm_first_token_time = 0
        self.tts_first_audio_time = 0

class KittenTTSService(FrameProcessor):
    def __init__(self, model_name="KittenML/kitten-tts-nano-0.1"):
        super().__init__()
        self.model = KittenTTSModel(model_name)

    async def process_frame(self, frame, direction):
        if not isinstance(frame, TextFrame):
            await self.push_frame(frame, direction)
            return

        audio = self.model.generate(frame.text, voice='expr-voice-2-f')
        await self.push_frame(AudioFrame(audio.tobytes(), 24000, 1))

class TwinService(FrameProcessor):
    def __init__(self):
        super().__init__()
        # In the future, we will initialize memory and tools here.

    async def process_frame(self, frame, direction):
        if not isinstance(frame, TranscriptionFrame):
            await self.push_frame(frame, direction)
            return

        # For now, just pass the transcription through.
        # In the future, we will do memory retrieval and tool use here.
        logging.info(f"TwinService received transcription: {frame.text}")
        await self.push_frame(TextFrame(frame.text))

class YOLOv8Detector(FrameProcessor):
    def __init__(self, model_name="yolov8n.pt"):
        super().__init__()
        self.model = YOLO(model_name)
        self.last_detected_objects = set()

    async def process_frame(self, frame, direction):
        if not isinstance(frame, VisionImageFrame):
            await self.push_frame(frame, direction)
            return

        img = frame.image
        results = self.model(img)

        detected_objects = set()
        for r in results:
            for c in r.boxes.cls:
                detected_objects.add(self.model.names[int(c)])

        if detected_objects != self.last_detected_objects:
            self.last_detected_objects = detected_objects
            if detected_objects:
                observation = f"Observation: I see {', '.join(detected_objects)}."
                await self.push_frame(TextFrame(observation))

async def main():
    transport = LocalTransport()

    stt = DeepgramSTTService()
    llm = OpenAILLMService(
        base_url="http://localhost:8080/v1", # This should point to the prima.cpp service
        api_key="dummy",
        model="dummy"
    )
    tts_service_name = os.getenv("TTS_SERVICE", "elevenlabs")
    if tts_service_name == "kittentts":
        tts = KittenTTSService()
    else:
        tts = ElevenLabsTTSService(
            voice_id="21m00Tcm4TlvDq8ikWAM" # A default voice
        )
    yolo = YOLOv8Detector()
    twin = TwinService()

    # Main conversational pipeline
    pipeline_steps = [
        transport.input(),
        stt,
        twin,
        llm,
        tts,
        transport.output()
    ]

    if os.getenv("BENCHMARK_MODE", "false").lower() == "true":
        pipeline_steps.insert(1, BenchmarkCollector())

    main_pipeline = Pipeline(pipeline_steps)

    # Vision pipeline
    vision_pipeline = Pipeline([
        yolo,
        llm
    ])

    main_task = PipelineTask(main_pipeline)

    # Interruption handling
    async def handle_interrupt(frame):
        if isinstance(frame, TextFrame) and frame.text.strip():
            logging.info(f"User interrupted with: {frame.text}")
            await main_task.cancel()

    interrupt_pipeline = Pipeline([
        transport.input(),
        stt,
        PipelineTask(handle_interrupt)
    ])

    runner = PipelineRunner()

    await runner.run(
        [main_task, PipelineTask(vision_pipeline), PipelineTask(interrupt_pipeline)]
    )

if __name__ == "__main__":
    asyncio.run(main())
