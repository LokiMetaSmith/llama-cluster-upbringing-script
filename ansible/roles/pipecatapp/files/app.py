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
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from memory import MemoryStore
from tools.ssh_tool import SSH_Tool
from tools.mcp_tool import MCP_Tool
import inspect

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

import json

class TwinService(FrameProcessor):
    def __init__(self, llm, yolo_detector):
        super().__init__()
        self.llm = llm
        self.yolo_detector = yolo_detector
        self.short_term_memory = []
        self.long_term_memory = MemoryStore()
        self.tools = {
            "ssh": SSH_Tool(),
            "mcp": MCP_Tool(self),
            "vision": self.yolo_detector,
        }

    def get_tools_prompt(self):
        prompt = "You have access to the following tools:\n"
        for tool_name, tool in self.tools.items():
            if tool_name == "vision":
                prompt += f'- {{"tool": "vision.get_observation"}}: {tool.get_observation.__doc__}\n'
            else:
                for method_name, method in inspect.getmembers(tool, predicate=inspect.ismethod):
                    if not method_name.startswith('_'):
                        prompt += f'- {{"tool": "{tool.name}.{method_name}", "args": {{...}}}}: {method.__doc__}\n'
        prompt += "\nTo use a tool, respond with a JSON object with the 'tool' and 'args' keys."
        return prompt

    async def process_frame(self, frame, direction):
        if not isinstance(frame, TranscriptionFrame):
            await self.push_frame(frame, direction)
            return

        user_text = frame.text
        logging.info(f"TwinService received: {user_text}")

        retrieved_memories = self.long_term_memory.search(user_text)
        short_term_context = "\n".join(self.short_term_memory)
        tools_prompt = self.get_tools_prompt()

        prompt = f"""
        {tools_prompt}
        Short-term conversation history:
        {short_term_context}
        Relevant long-term memories:
        {retrieved_memories}
        Current user query: {user_text}
        """

        logging.info(f"Constructed prompt for LLM: {prompt}")

        llm_response_text = await self.llm.process_text(prompt)

        try:
            tool_call = json.loads(llm_response_text)
            tool_name, method_name = tool_call.get("tool", "").split('.')
            args = tool_call.get("args", {})

            if tool_name in self.tools:
                tool = self.tools[tool_name]
                method = getattr(tool, method_name)
                logging.info(f"LLM requested to use tool: {tool_name}.{method_name} with args: {args}")
                result = method(**args)

                final_prompt = f"The result of using the tool {tool_name}.{method_name} is: {result}. Now, answer the user's original question based on this."
                final_response = await self.llm.process_text(final_prompt)
                await self.push_frame(TextFrame(final_response))
                self.short_term_memory.append(f"Assistant: {final_response}")
            else:
                await self.push_frame(TextFrame(llm_response_text))
                self.short_term_memory.append(f"Assistant: {llm_response_text}")
        except Exception:
            await self.push_frame(TextFrame(llm_response_text))
            self.short_term_memory.append(f"Assistant: {llm_response_text}")

        self.short_term_memory.append(f"User: {user_text}")
        if len(self.short_term_memory) > 10:
            self.short_term_memory.pop(0)

class YOLOv8Detector(FrameProcessor):
    def __init__(self, model_name="yolov8n.pt"):
        super().__init__()
        self.model = YOLO(model_name)
        self.latest_observation = "I don't see anything."
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
                self.latest_observation = f"I see {', '.join(detected_objects)}."
            else:
                self.latest_observation = "I don't see anything."
            logging.info(f"YOLOv8Detector updated observation: {self.latest_observation}")

    def get_observation(self):
        return self.latest_observation

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
    twin = TwinService(llm=llm, yolo_detector=yolo)

    # Main conversational pipeline
    pipeline_steps = [
        transport.input(),
        stt,
        twin,
        tts,
        transport.output()
    ]

    if os.getenv("BENCHMARK_MODE", "false").lower() == "true":
        pipeline_steps.insert(1, BenchmarkCollector())

    main_pipeline = Pipeline(pipeline_steps)

    # Vision pipeline (runs in parallel to update the detector's state)
    vision_pipeline = Pipeline([yolo])

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
