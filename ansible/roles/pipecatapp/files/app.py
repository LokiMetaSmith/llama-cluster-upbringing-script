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
from RealtimeSTT import AudioToText
from kittentts import KittenTTS as KittenTTSModel
import soundfile as sf
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from memory import MemoryStore
import requests
from tools.ssh_tool import SSH_Tool
from tools.mcp_tool import MCP_Tool
from tools.code_runner_tool import CodeRunnerTool
from tools.web_browser_tool import WebBrowserTool
from tools.ansible_tool import Ansible_Tool
from tools.power_tool import Power_Tool
from tools.summarizer_tool import SummarizerTool
from moondream_detector import MoondreamDetector
import inspect
import web_server
from web_server import approval_queue
import uvicorn
import threading
import shutil

# Custom logging handler to broadcast logs to the web UI
class WebSocketLogHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        asyncio.run(web_server.manager.broadcast(json.dumps({"type": "log", "data": log_entry})))

logger = logging.getLogger()
logger.addHandler(WebSocketLogHandler())

# Custom frame processor to broadcast conversation to the web UI
class UILogger(FrameProcessor):
    def __init__(self, sender: str):
        super().__init__()
        self.sender = sender

    async def process_frame(self, frame, direction):
        if isinstance(frame, (TranscriptionFrame, TextFrame)):
            await web_server.manager.broadcast(json.dumps({"type": self.sender, "data": frame.text}))
        await self.push_frame(frame, direction)

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

from piper.voice import Piper
import io
import wave

class FasterWhisperSTTService(FrameProcessor):
    def __init__(self, model="tiny.en"):
        super().__init__()
        self.model = model
        self.audio_to_text = AudioToText(model=self.model, language="en")

    async def process_frame(self, frame, direction):
        if not isinstance(frame, AudioFrame):
            await self.push_frame(frame, direction)
            return

        text = self.audio_to_text.transcribe(frame.audio)
        if text:
            await self.push_frame(TranscriptionFrame(text))

class PiperTTSService(FrameProcessor):
    """A FrameProcessor that uses a local Piper model for Text-to-Speech."""
    def __init__(self, voices=None):
        super().__init__()
        self.voice = None

        if not voices:
            logging.error("PiperTTSService: No voices configured.")
            return

        for voice_config in voices:
            try:
                model_path = f"/opt/nomad/models/tts/{voice_config['model']}"
                config_path = f"/opt/nomad/models/tts/{voice_config['config']}"

                logging.info(f"Attempting to load Piper TTS model: {voice_config['name']}")

                loaded_voice = Piper.load(model_path, config_path=config_path)
                self.voice = loaded_voice
                self.sample_rate = self.voice.config.sample_rate

                logging.info(f"Successfully loaded Piper TTS model '{voice_config['name']}' with sample rate: {self.sample_rate}")
                break # Stop on first successful load
            except Exception as e:
                logging.warning(f"Failed to load Piper TTS model '{voice_config['name']}': {e}")

        if not self.voice:
            logging.error("Failed to load any Piper TTS models. TTS will be silent.")

    async def process_frame(self, frame, direction):
        if not isinstance(frame, TextFrame):
            await self.push_frame(frame, direction)
            return

        if not self.voice:
            logging.warning("PiperTTSService: No voice loaded, cannot synthesize audio.")
            return

        logging.info(f"PiperTTS synthesizing audio for: '{frame.text}'")

        # Synthesize audio to an in-memory WAV stream
        audio_stream = io.BytesIO()
        self.voice.synthesize(frame.text, audio_stream)
        audio_stream.seek(0)

        # Read the raw audio bytes from the WAV stream
        with wave.open(audio_stream, 'rb') as wf:
            # Ensure the WAV file has the correct sample rate, etc.
            # For now, we assume it matches what pipecat expects.
            audio_bytes = wf.readframes(wf.getnframes())

        await self.push_frame(AudioFrame(audio_bytes))

import json

class TwinService(FrameProcessor):
    def __init__(self, llm, vision_detector, runner, debug_mode=False, approval_mode=False, approval_queue=None):
        super().__init__()
        self.router_llm = llm # The main LLM acts as a router
        self.vision_detector = vision_detector
        self.runner = runner
        self.debug_mode = debug_mode
        self.approval_mode = approval_mode
        self.approval_queue = approval_queue
        self.short_term_memory = []
        self.long_term_memory = MemoryStore()

        self.consul_http_addr = os.getenv("CONSUL_HTTP_ADDR", "http://localhost:8500")
        self.experts = {} # Experts will be discovered dynamically

        self.tools = {
            "ssh": SSH_Tool(),
            "mcp": MCP_Tool(self, self.runner),
            "vision": self.vision_detector,
            "code_runner": CodeRunnerTool(),
            "web_browser": WebBrowserTool(),
            "ansible": Ansible_Tool(),
            "power": Power_Tool(),
        }

        if os.getenv("USE_SUMMARIZER", "false").lower() == "true":
            self.tools["summarizer"] = SummarizerTool(self)
            logging.info("Summarizer tool enabled.")

    def get_discovered_experts(self):
        try:
            response = requests.get(f"{self.consul_http_addr}/v1/catalog/services")
            response.raise_for_status()
            services = response.json()
            # Filter for services that match our expert pattern, e.g., "llama-api-"
            expert_names = [name for name in services.keys() if name.startswith("llama-api-")]
            return expert_names
        except requests.exceptions.RequestException as e:
            logging.error(f"Could not connect to Consul: {e}")
            return []

    def get_system_prompt(self, expert_name="router"):
        prompt_file = f"ansible/roles/pipecatapp/files/prompts/{expert_name}.txt"
        try:
            with open(prompt_file, "r") as f:
                base_prompt = f.read()
        except FileNotFoundError:
            base_prompt = "You are a helpful AI assistant."

        tools_prompt = "You have access to the following tools:\n"
        for tool_name, tool in self.tools.items():
            if tool_name == "vision":
                tools_prompt += f'- {{"tool": "vision.get_observation"}}: Get a real-time description of what is visible in the webcam.\n'
            else:
                for method_name, method in inspect.getmembers(tool, predicate=inspect.ismethod):
                    if not method_name.startswith('_'):
                        tools_prompt += f'- {{"tool": "{tool_name}.{method_name}", "args": {{...}}}}: {method.__doc__}\n'

        for service_name in self.get_discovered_experts():
            expert_name = service_name.replace("llama-api-", "")
            tools_prompt += f'- {{"tool": "route_to_expert", "args": {{"expert": "{expert_name}", "query": "<user_query>"}}}}: Use this for queries related to {expert_name}.\n'

        return f"{base_prompt}\n\n{tools_prompt}\n\nIf the query doesn't fit a specific expert or tool, handle it yourself. Otherwise, respond with a JSON object with the 'tool' and 'args' keys."

    async def get_expert_service(self, expert_name):
        service_name = f"llama-api-{expert_name}"
        try:
            response = requests.get(f"{self.consul_http_addr}/v1/health/service/{service_name}")
            response.raise_for_status()
            services = response.json()
            if not services:
                return None

            # Get the first healthy service instance
            address = services[0]['Service']['Address']
            port = services[0]['Service']['Port']
            base_url = f"http://{address}:{port}/v1"

            return OpenAILLMService(base_url=base_url, api_key="dummy", model=expert_name)
        except requests.exceptions.RequestException as e:
            logging.error(f"Could not get address for expert {expert_name}: {e}")
            return None

    async def _request_approval(self, tool_call_info: dict) -> bool:
        """Send a request for approval to the UI and wait for a response."""
        request_id = str(time.time())
        approval_request = {
            "type": "approval_request",
            "data": {
                "request_id": request_id,
                "tool_call": tool_call_info
            }
        }
        await web_server.manager.broadcast(json.dumps(approval_request))

        # Wait for a response from the queue
        while True:
            response = await self.approval_queue.get()
            if response.get("data", {}).get("request_id") == request_id:
                approved = response.get("data", {}).get("approved", False)
                logging.info(f"Received approval response: {'Approved' if approved else 'Denied'}")
                return approved

    def save_state(self, save_name: str) -> str:
        """Saves the current agent state to a named snapshot."""
        try:
            state_dir = os.path.join("saved_states", save_name)
            os.makedirs(state_dir, exist_ok=True)

            # Save long-term memory files
            shutil.copy("long_term_memory.faiss", os.path.join(state_dir, "long_term_memory.faiss"))
            shutil.copy("long_term_memory.json", os.path.join(state_dir, "long_term_memory.json"))

            # Save short-term memory
            with open(os.path.join(state_dir, "short_term_memory.json"), "w") as f:
                json.dump(self.short_term_memory, f)

            logging.info(f"Successfully saved state to '{save_name}'")
            return f"Successfully saved state to '{save_name}'"
        except Exception as e:
            logging.error(f"Failed to save state '{save_name}': {e}")
            return f"Error saving state: {e}"

    def load_state(self, save_name: str) -> str:
        """Loads agent state from a named snapshot."""
        try:
            state_dir = os.path.join("saved_states", save_name)
            if not os.path.isdir(state_dir):
                return f"Error: Save state '{save_name}' not found."

            # Load long-term memory files
            shutil.copy(os.path.join(state_dir, "long_term_memory.faiss"), "long_term_memory.faiss")
            shutil.copy(os.path.join(state_dir, "long_term_memory.json"), "long_term_memory.json")

            # Load short-term memory
            with open(os.path.join(state_dir, "short_term_memory.json"), "r") as f:
                self.short_term_memory = json.load(f)

            # Re-initialize the memory store to load the new files
            self.long_term_memory = MemoryStore()

            logging.info(f"Successfully loaded state from '{save_name}'")
            return f"Successfully loaded state from '{save_name}'"
        except Exception as e:
            logging.error(f"Failed to load state '{save_name}': {e}")
            return f"Error loading state: {e}"

    async def process_frame(self, frame, direction):
        if not isinstance(frame, TranscriptionFrame):
            await self.push_frame(frame, direction)
            return

        user_text = frame.text
        logging.info(f"TwinService received: {user_text}")

        retrieved_memories = self.long_term_memory.search(user_text)
        short_term_context = "\n".join(self.short_term_memory)
        system_prompt = self.get_system_prompt("router")

        prompt = f"""
        {system_prompt}
        Short-term conversation history:
        {short_term_context}
        Relevant long-term memories:
        {retrieved_memories}
        Current user query: {user_text}
        """

        llm_response_text = await self.router_llm.process_text(prompt)

        try:
            tool_call = json.loads(llm_response_text)
            tool_parts = tool_call.get("tool", "").split('.')

            if tool_parts[0] == "route_to_expert":
                expert_name = tool_call["args"]["expert"]
                query = tool_call["args"]["query"]
                expert_llm = await self.get_expert_service(expert_name)
                if expert_llm:
                    logging.info(f"Routing to {expert_name} with query: {query}")
                    expert_prompt = self.get_system_prompt(expert_name)
                    final_expert_prompt = f"{expert_prompt}\n\nUser query: {query}"
                    expert_response = await expert_llm.process_text(final_expert_prompt)
                    await self.push_frame(TextFrame(expert_response))
                    self.short_term_memory.append(f"Assistant ({expert_name}): {expert_response}")
                else:
                    final_response = await self.router_llm.process_text(f"I could not find the {expert_name} expert. Please try again later.")
                    await self.push_frame(TextFrame(final_response))
            elif tool_parts[0] in self.tools:
                tool_name = tool_parts[0]
                method_name = tool_parts[1]
                args = tool_call.get("args", {})
                tool = self.tools[tool_name]
                method = getattr(tool, method_name)

                sensitive_tools = ["ssh", "code_runner", "ansible"]
                if self.approval_mode and tool_name in sensitive_tools:
                    logging.info(f"Requesting approval for sensitive tool: {tool_name}")
                    approved = await self._request_approval(tool_call)
                    if not approved:
                        logging.warning(f"Execution of tool {tool_name} denied by user.")
                        await self.push_frame(TextFrame(f"Action denied. I cannot use the {tool_name} tool."))
                        # We need to make sure the user's text is re-added to memory to avoid losing context
                        self.short_term_memory.append(f"User: {user_text}")
                        if len(self.short_term_memory) > 10:
                            self.short_term_memory.pop(0)
                        return

                logging.info(f"LLM requested to use tool: {tool_name}.{method_name} with args: {args}")
                result = method(**args)

                if self.debug_mode:
                    logging.debug(f"Tool {tool_name}.{method_name} returned: {result}")

                final_prompt = f"The result of using the tool {tool_name}.{method_name} is: {result}. Now, answer the user's original question based on this."
                final_response = await self.router_llm.process_text(final_prompt)
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
    def __init__(self):
        super().__init__()
        # The model is now managed by Ansible and placed in a predictable location.
        model_path = "/opt/nomad/models/vision/yolov8n.pt"
        self.model = YOLO(model_path)
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

    # Start the web server in a separate thread
    config = uvicorn.Config(web_server.app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    threading.Thread(target=server.run).start()

    # Load configuration from the JSON file created by Ansible
    pipecat_config = {}
    try:
        with open("/opt/pipecatapp/pipecat_config.json", "r") as f:
            pipecat_config = json.load(f)
    except FileNotFoundError:
        logging.warning("pipecat_config.json not found, using defaults.")

    tts_voices = pipecat_config.get("tts_voices", [])

    stt_service_name = os.getenv("STT_SERVICE", "deepgram")
    if stt_service_name == "faster-whisper":
        stt = FasterWhisperSTTService()
    else:
        stt = DeepgramSTTService()

    llm = OpenAILLMService(
        base_url="http://localhost:8080/v1", # This should point to the prima.cpp service
        api_key="dummy",
        model="dummy"
    )
    # Use the local Piper TTS service with the configured voices
    tts = PiperTTSService(voices=tts_voices)
    runner = PipelineRunner()

    # TODO: Implement failover or selection logic for vision models
    vision_detector = YOLOv8Detector()
    logging.info("Using YOLOv8 for vision.")

    debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
    if debug_mode:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug mode enabled.")

    approval_mode = os.getenv("APPROVAL_MODE", "false").lower() == "true"
    if approval_mode:
        logging.info("Approval mode enabled. Sensitive actions will require user confirmation.")

    twin = TwinService(
        llm=llm,
        vision_detector=vision_detector,
        runner=runner,
        debug_mode=debug_mode,
        approval_mode=approval_mode,
        approval_queue=approval_queue
    )
    web_server.twin_service_instance = twin

    # Main conversational pipeline
    pipeline_steps = [
        transport.input(),
        stt,
        UILogger(sender="user"),
        twin,
        UILogger(sender="agent"),
        tts,
        transport.output()
    ]
    # Set Debug  mode for troubleshooting and examining state
    debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
    if debug_mode:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug mode enabled.")

    approval_mode = os.getenv("APPROVAL_MODE", "false").lower() == "true"
    if approval_mode:
        logging.info("Approval mode enabled. Sensitive actions will require user confirmation.")
    if os.getenv("BENCHMARK_MODE", "false").lower() == "true":
        pipeline_steps.insert(1, BenchmarkCollector())

    main_pipeline = Pipeline(pipeline_steps)

    # Vision pipeline (runs in parallel to update the detector's state)
    vision_pipeline = Pipeline([vision_detector])

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

    await runner.run(
        [main_task, PipelineTask(vision_pipeline), PipelineTask(interrupt_pipeline)]
    )

if __name__ == "__main__":
    asyncio.run(main())
