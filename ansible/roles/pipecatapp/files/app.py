import asyncio
import logging
import cv2
import torch
from ultralytics import YOLO
import time
import json
import io
import wave
import os
import shutil
import inspect
import threading

from pipecat.frames.frames import (
    AudioRawFrame,
    EndFrame,
    TextFrame,
    UserImageRawFrame as VisionImageRawFrame,
    UserStartedSpeakingFrame,
    UserStoppedSpeakingFrame,
    TranscriptionFrame,
)
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat_whisker import WhiskerObserver
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transports.local.audio import LocalAudioTransport, LocalAudioTransportParams
from faster_whisper import WhisperModel
from piper.voice import PiperVoice
import soundfile as sf
import requests
import consul.aio
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from memory import MemoryStore
import web_server
from web_server import approval_queue, text_message_queue
from tools.ssh_tool import SSH_Tool
from tools.mcp_tool import MCP_Tool
from tools.code_runner_tool import CodeRunnerTool
from tools.web_browser_tool import WebBrowserTool
from tools.ansible_tool import Ansible_Tool
from tools.power_tool import Power_Tool
from tools.summarizer_tool import SummarizerTool
from moondream_detector import MoondreamDetector

import uvicorn

# Custom logging handler to broadcast logs to the web UI
class WebSocketLogHandler(logging.Handler):
    """A custom logging handler that broadcasts log records to the web UI.

    This handler integrates with the application's WebSocket manager to send
    formatted log messages to all connected web clients, enabling real-time
    log monitoring from the browser.
    """
    def emit(self, record):
        """Formats and broadcasts a log record.

        Args:
            record: The log record to be emitted.
        """
        log_entry = self.format(record)
        try:
            # Get the currently running event loop
            loop = asyncio.get_running_loop()
            # Schedule the broadcast coroutine to run on the existing loop
            loop.create_task(web_server.manager.broadcast(json.dumps({"type": "log", "data": log_entry})))
        except RuntimeError:
            # This can happen if a log is emitted when no event loop is running (e.g., at shutdown)
            # In this case, we can just ignore the log message for the UI.
            pass

logger = logging.getLogger()
logger.addHandler(WebSocketLogHandler())

# Custom frame processor to broadcast conversation to the web UI
class UILogger(FrameProcessor):
    """A Pipecat frame processor to broadcast conversation text to the web UI.

    This processor intercepts transcription and text frames to send their
    contents to the web UI, allowing real-time display of the conversation.

    Attributes:
        sender (str): A label to identify the origin of the message (e.g., "user" or "agent").
    """
    def __init__(self, sender: str):
        """Initializes the UILogger.

        Args:
            sender (str): The identifier for the message sender (e.g., "user", "agent").
        """
        super().__init__()
        self.sender = sender

    async def process_frame(self, frame, direction):
        """Processes incoming frames and broadcasts text-based ones to the UI.

        Args:
            frame: The frame to process.
            direction: The direction of the frame in the pipeline.
        """
        if isinstance(frame, (TranscriptionFrame, TextFrame)):
            await web_server.manager.broadcast(json.dumps({"type": self.sender, "data": frame.text}))
        await self.push_frame(frame, direction)

class BenchmarkCollector(FrameProcessor):
    """A Pipecat frame processor for measuring and logging pipeline latency.

    This processor captures timestamps at key stages of the conversational AI
    pipeline (user speech end, STT transcription, LLM first token, TTS first

    audio) to calculate and log performance metrics.

    Attributes:
        start_time (float): Timestamp when the user stops speaking.
        stt_end_time (float): Timestamp when transcription is received.
        llm_first_token_time (float): Timestamp of the first LLM text token.
        tts_first_audio_time (float): Timestamp of the first TTS audio frame.
    """
    def __init__(self):
        """Initializes the BenchmarkCollector."""
        super().__init__()
        self.reset()

    async def process_frame(self, frame, direction):
        """Captures timestamps as specific frames pass through the pipeline.

        Args:
            frame: The frame being processed.
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

        logging.info("--- BENCHMARK RESULTS ---")
        logging.info(f"STT Latency: {stt_latency:.4f}s")
        logging.info(f"LLM Time to First Token: {llm_ttft:.4f}s")
        logging.info(f"TTS Time to First Audio: {tts_ttfa:.4f}s")
        logging.info(f"Total Pipeline Latency: {total_latency:.4f}s")
        logging.info("-------------------------")

    def reset(self):
        """Resets all timestamps to zero for the next measurement."""
        self.start_time = 0
        self.stt_end_time = 0
        self.llm_first_token_time = 0
        self.tts_first_audio_time = 0

class FasterWhisperSTTService(FrameProcessor):
    """A Pipecat FrameProcessor for Speech-to-Text using a local FasterWhisper model.

    This service buffers audio frames and transcribes them into text when the user
    stops speaking. This implementation avoids using external recorders and relies
    solely on the audio stream provided by the Pipecat pipeline.

    Attributes:
        model: The loaded `faster_whisper` model.
        audio_buffer (bytearray): A buffer to accumulate raw audio data.
        sample_rate (int): The sample rate of the audio stream.
    """
    def __init__(self, model_path: str, sample_rate: int = 16000):
        """Initializes the FasterWhisperSTTService.

        Args:
            model_path (str): The path to the FasterWhisper model directory.
            sample_rate (int, optional): The sample rate of the incoming audio.
                                         Defaults to 16000.
        """
        super().__init__()
        # Using "cpu" and "int8" for broad compatibility.
        # For better performance on compatible hardware, consider "cuda" and "float16".
        self.model = WhisperModel(model_path, device="cpu", compute_type="int8")
        self.audio_buffer = bytearray()
        self.sample_rate = sample_rate
        logging.info(f"FasterWhisperSTTService initialized with model '{model_path}'")

    def _convert_audio_bytes_to_float_array(self, audio_bytes: bytes) -> np.ndarray:
        """Converts raw s16le audio bytes to a NumPy array of f32 samples."""
        audio_s16 = np.frombuffer(audio_bytes, dtype=np.int16)
        audio_f32 = audio_s16.astype(np.float32) / 32768.0
        return audio_f32

    async def process_frame(self, frame, direction):
        """Processes audio and user speaking status frames.

        This method buffers audio frames when the user is speaking and triggers
        transcription when the user stops.

        Args:
            frame: The frame to process.
            direction: The direction of the frame in the pipeline.
        """
        if isinstance(frame, UserStartedSpeakingFrame):
            logging.debug("User started speaking, clearing audio buffer.")
            self.audio_buffer.clear()
        elif isinstance(frame, AudioRawFrame):
            self.audio_buffer.extend(frame.audio)
        elif isinstance(frame, UserStoppedSpeakingFrame):
            logging.debug("User stopped speaking, transcribing buffered audio.")
            if not self.audio_buffer:
                logging.warning("User stopped speaking but audio buffer is empty.")
                return

            audio_f32 = self._convert_audio_bytes_to_float_array(self.audio_buffer)
            self.audio_buffer.clear()

            segments, _ = self.model.transcribe(audio_f32, language="en")

            full_text = "".join(segment.text for segment in segments).strip()

            if full_text:
                logging.info(f"Transcription result: {full_text}")
                await self.push_frame(TranscriptionFrame(full_text))
            else:
                logging.info("Transcription resulted in empty text.")
        else:
            await self.push_frame(frame, direction)

class PiperTTSService(FrameProcessor):
    """A FrameProcessor that uses a local Piper model for Text-to-Speech.

    This service converts TextFrames into AudioRawFrames by synthesizing speech
    using a Piper TTS model.

    Attributes:
        voice (PiperVoice): The loaded Piper voice model for synthesis.
        sample_rate (int): The sample rate of the synthesized audio.
    """

    def __init__(self, model_path: str, config_path: str):
        """Initializes the PiperTTSService.

        Args:
            model_path (str): The file path to the Piper .onnx model.
            config_path (str): The file path to the Piper .json config.
        """
        super().__init__()
        self.voice = PiperVoice.from_files(model_path, config_path)
        self.sample_rate = self.voice.config.sample_rate

    async def process_frame(self, frame, direction):
        """Processes TextFrames to synthesize audio and pushes AudioRawFrames.

        Args:
            frame: The frame to process.
            direction: The direction of the frame in the pipeline.
        """
        if not isinstance(frame, TextFrame):
            await self.push_frame(frame, direction)
            return

        logging.info(f"PiperTTS synthesizing audio for: '{frame.text}'")

        # Synthesize audio to an in-memory WAV stream
        audio_stream = io.BytesIO()
        self.voice.synthesize(frame.text, audio_stream)
        audio_stream.seek(0)

        # Read the raw audio bytes from the WAV stream
        with wave.open(audio_stream, "rb") as wf:
            audio_bytes = wf.readframes(wf.getnframes())

        await self.push_frame(AudioRawFrame(audio_bytes))

async def load_config_from_consul(consul_host, consul_port):
    """Fetches application configuration from the Consul KV store."""
    logging.info("Loading configuration from Consul KV store...")
    config = {}
    c = consul.aio.Consul(host=consul_host, port=consul_port)
    try:
        index, data = await c.kv.get('config/app/settings')
        if data:
            app_settings = json.loads(data['Value'].decode('utf-8'))
            config.update(app_settings)
            logging.info("Successfully loaded application settings from Consul.")
        else:
            logging.error("Could not find 'config/app/settings' in Consul KV.")

        # Also load tts_voices, which are stored separately
        index, data = await c.kv.get('config/models/tts_voices')
        if data:
            config['tts_voices'] = json.loads(data['Value'].decode('utf-8'))
            logging.info("Successfully loaded TTS voices from Consul.")
        else:
            logging.warning("Could not find 'config/models/tts_voices' in Consul KV.")

    except Exception as e:
        logging.error(f"Error loading configuration from Consul: {e}")
    return config

class TwinService(FrameProcessor):
    """The core logic unit ("brain") of the conversational AI agent.

    This service orchestrates the agent's behavior by processing user input,
    managing memory, using tools, routing to specialized experts, and generating
    responses. It acts as a central hub in the Pipecat pipeline.

    Attributes:
        router_llm: The primary LLM service used for routing and general conversation.
        vision_detector: The service responsible for visual perception.
        runner: The PipelineRunner instance, used for managing pipeline tasks.
        app_config (dict): A dictionary containing the application's configuration.
        approval_queue: A queue for receiving approval status from the UI.
        short_term_memory (list): A list storing the recent conversation history.
        long_term_memory (MemoryStore): A vector store for long-term knowledge.
        consul_http_addr (str): The address of the Consul agent for service discovery.
        experts (dict): A dictionary to cache discovered expert services.
        tools (dict): A dictionary of available tools for the agent.
    """
    def __init__(self, llm, vision_detector, runner, app_config: dict, approval_queue=None):
        """Initializes the TwinService.

        Args:
            llm: The primary LLM service.
            vision_detector: The vision processing service.
            runner: The Pipecat PipelineRunner.
            app_config (dict): The application's configuration loaded from Consul.
            approval_queue: The queue for UI approval messages.
        """
        super().__init__()
        self.router_llm = llm # The main LLM acts as a router
        self.vision_detector = vision_detector
        self.runner = runner
        self.app_config = app_config
        self.approval_queue = approval_queue
        self.short_term_memory = []
        self.long_term_memory = MemoryStore()

        self.debug_mode = self.app_config.get("debug_mode", False)
        self.approval_mode = self.app_config.get("approval_mode", False)
        self.consul_http_addr = f"http://{self.app_config.get('consul_host', '127.0.0.1')}:{self.app_config.get('consul_port', 8500)}"

        # External experts config is now part of the main app_config
        self.experts = self.app_config.get("external_experts_config", {})
        
        self.tools = {
            "ssh": SSH_Tool(),
            "mcp": MCP_Tool(self, self.runner),
            "vision": self.vision_detector,
            "code_runner": CodeRunnerTool(),
            "web_browser": WebBrowserTool(),
            "ansible": Ansible_Tool(),
            "power": Power_Tool(),
        }

        if self.app_config.get("use_summarizer", False):
            self.tools["summarizer"] = SummarizerTool(self)
            logging.info("Summarizer tool enabled.")

    def get_discovered_experts(self) -> list[str]:
        """Discovers available 'expert' services registered in Consul.

        It queries the Consul catalog for services with the 'expert' tag or
        with names following the 'llamacpp-rpc-<name>' convention.

        Returns:
            list[str]: A list of discovered expert names (e.g., "main", "coding").
        """
        # Start with externally configured experts
        expert_names = set(self.experts.keys())
        try:
            response = requests.get(f"{self.consul_http_addr}/v1/catalog/services")
            response.raise_for_status()
            services = response.json()

            # Discover local experts from Consul by service name and tags
            for name, service_info in services.items():
                # Method 1: Discover from service name convention (e.g., "llamacpp-rpc-coding")
                if name.startswith("llamacpp-rpc-"):
                    expert_names.add(name.replace("llamacpp-rpc-", ""))

                # Method 2: Discover from "expert" tag
                tags = service_info.get("Tags", [])
                if "expert" in tags:
                    # The expert name is also a tag. Ignore common tags like "llm".
                    for tag in tags:
                        if tag not in ["expert", "llm"]:
                            expert_names.add(tag)
                            break  # Assume only one expert name tag per service
        except requests.exceptions.RequestException as e:
            logging.error(f"Could not connect to Consul for expert discovery: {e}")

        return sorted(list(expert_names))

    def get_system_prompt(self, expert_name: str = "router") -> str:
        """Constructs the system prompt for a given agent or expert.

        The prompt is assembled from a base prompt file and a dynamically
        generated list of available tools and experts.

        Args:
            expert_name (str, optional): The name of the expert to get the
                prompt for. Defaults to "router".

        Returns:
            str: The fully constructed system prompt.
        """
        prompt_file = f"prompts/{expert_name}.txt"
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

        for expert in self.get_discovered_experts():
            tools_prompt += f'- {{"tool": "route_to_expert", "args": {{"expert": "{expert}", "query": "<user_query>"}}}}: Use this for queries related to {expert}.\n'

        return f"{base_prompt}\n\n{tools_prompt}\n\nIf the query doesn't fit a specific expert or tool, handle it yourself. Otherwise, respond with a JSON object with the 'tool' and 'args' keys."

    async def get_expert_service(self, expert_name: str):
        """Retrieves a healthy instance of an expert LLM service."""
        # Check if it's an external expert first
        if expert_name in self.experts:
            config = self.experts[expert_name]
            api_key = os.getenv(config["api_key_env"])
            if not api_key:
                logging.error(f"API key environment variable '{config['api_key_env']}' not set for expert '{expert_name}'.")
                return None
            return OpenAILLMService(
                base_url=config["base_url"],
                api_key=api_key,
                model=config.get("model", expert_name) # Use specific model if provided
            )
    
        # Otherwise, assume it's a local expert and discover via Consul
        service_name = f"llamacpp-rpc-{expert_name}"
        try:
            response = requests.get(f"{self.consul_http_addr}/v1/health/service/{service_name}?passing")
            response.raise_for_status()
            services = response.json()
            if not services:
                return None
    
            address = services[0]['Service']['Address']
            port = services[0]['Service']['Port']
            base_url = f"http://{address}:{port}/v1"
    
            return OpenAILLMService(base_url=base_url, api_key="dummy", model=expert_name)
        except requests.exceptions.RequestException as e:
            logging.error(f"Could not get address for local expert {expert_name}: {e}")
            return None

    async def _request_approval(self, tool_call_info: dict) -> bool:
        """Sends a tool use request to the UI for approval and waits for a response.

        Args:
            tool_call_info (dict): A dictionary describing the tool call.

        Returns:
            bool: True if the action is approved, False otherwise.
        """
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
        """Saves the current agent state to a named snapshot.

        This includes the short-term and long-term memory.

        Args:
            save_name (str): The name for the saved state snapshot.

        Returns:
            str: A message indicating success or failure.
        """
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
        """Loads agent state from a named snapshot.

        This restores the short-term and long-term memory from a saved state.

        Args:
            save_name (str): The name of the state snapshot to load.

        Returns:
            str: A message indicating success or failure.
        """
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
        """The main processing loop for the agent's logic.

        This method is called for each frame in the pipeline. It handles
        TranscriptionFrames by generating a response, which may involve
        memory retrieval, tool use, or routing to an expert.

        Args:
            frame: The frame to process.
            direction: The direction of the frame in the pipeline.
        """
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
    """A Pipecat FrameProcessor for real-time object detection using YOLOv8.

    This class processes VisionImageRawFrames, runs object detection on them
    using a YOLOv8 model, and maintains the latest observation as a text
    description.

    Attributes:
        model: The loaded YOLO model object.
        latest_observation (str): A human-readable string of the latest detected objects.
        last_detected_objects (set): A set of object names from the last frame to
            avoid redundant logging.
    """
    def __init__(self):
        """Initializes the YOLOv8Detector and loads the model."""
        super().__init__()
        # The model is now managed by Ansible and placed in a predictable location.
        model_path = "/opt/nomad/models/vision/yolov8n.pt"
        self.model = YOLO(model_path)
        self.latest_observation = "I don't see anything."
        self.last_detected_objects = set()

    async def process_frame(self, frame, direction):
        """Processes a vision frame to detect objects.

        Args:
            frame: The frame to process.
            direction: The direction of the frame in the pipeline.
        """
        if not isinstance(frame, VisionImageRawFrame):
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

    def get_observation(self) -> str:
        """Returns the latest observation from the vision detector.

        This method is intended to be called by other services (like the
        TwinService's vision tool) to get the current state of what the
        agent "sees."

        Returns:
            str: A text description of the detected objects.
        """
        return self.latest_observation

class TextMessageInjector(FrameProcessor):
    """A custom FrameProcessor to inject text messages from the web UI into the pipeline.

    This processor listens to a queue for incoming text messages and pushes them
    downstream as TranscriptionFrames, allowing the agent to process text input.
    """
    def __init__(self, queue: asyncio.Queue):
        super().__init__()
        self.queue = queue
        self._task = None

    def start_listening(self):
        """Starts the background task to listen for messages from the queue."""
        if not self._task:
            self._task = asyncio.create_task(self._run())

    async def _run(self):
        """The main loop that waits for messages and pushes them as frames."""
        while True:
            try:
                message = await self.queue.get()
                text = message.get("data")
                if text:
                    logging.info(f"Injecting text message from UI: {text}")
                    await self.push_frame(TranscriptionFrame(text))
            except Exception as e:
                logging.error(f"Error in TextMessageInjector: {e}")

    async def process_frame(self, frame, direction):
        """Processes frames from upstream (i.e., the audio STT).

        This method simply passes through any frames it receives from the
        previous step in the pipeline.
        """
        await self.push_frame(frame, direction)

    def stop_listening(self):
        """Stops the listening task."""
        if self._task:
            self._task.cancel()
            self._task = None

def find_workable_audio_config():
    """
    Iterates through all available audio devices and common sample rates to
    find a working configuration for audio input.

    Returns:
        tuple[int, int]: A tuple containing the device index and a supported
                         sample rate. Returns (None, 16000) if no workable
                         combination is found.
    """
    try:
        import pyaudio
    except ImportError:
        logging.error("PyAudio is not installed. Please install it to enable dynamic audio configuration.")
        return None, 16000  # Default fallback

    p = pyaudio.PyAudio()
    common_rates = [16000, 48000, 44100, 32000, 8000]

    try:
        device_count = p.get_device_count()
        logging.info(f"Found {device_count} audio devices.")

        for i in range(device_count):
            device_info = p.get_device_info_by_index(i)
            if device_info.get('maxInputChannels', 0) > 0:
                logging.info(f"Checking device {i}: {device_info.get('name')}")
                for rate in common_rates:
                    try:
                        if p.is_format_supported(
                            rate,
                            input_device=device_info['index'],
                            input_channels=1,
                            input_format=pyaudio.paInt16
                        ):
                            logging.info(f"Found workable config: Device Index {device_info['index']}, Sample Rate {rate}Hz")
                            return device_info['index'], rate
                    except ValueError:
                        continue # This combination is not supported

        logging.warning("Could not find a workable audio input configuration. Falling back to defaults.")
        return None, 16000

    except Exception as e:
        logging.error(f"An error occurred during audio device discovery: {e}. Falling back to defaults.")
        return None, 16000
    finally:
        p.terminate()


#async def discover_main_llm_service(consul_http_addr="http://localhost:8500", delay=10):
#    """Discovers the main LLM service from Consul, retrying indefinitely."""
#    service_name = os.getenv("LLAMA_API_SERVICE_NAME", "llamacpp-rpc-api")
#    logging.info(f"Attempting to discover main LLM service: {service_name}")
async def discover_service(service_name: str, consul_http_addr: str, delay=10):
    """Discovers a healthy service from Consul, retrying indefinitely."""
    logging.info(f"Attempting to discover service: {service_name}")
    while True:
        try:
            response = requests.get(f"{consul_http_addr}/v1/health/service/{service_name}?passing")
            response.raise_for_status()
            services = response.json()
            if services:
                address = services[0]['Service']['Address']
                port = services[0]['Service']['Port']
                base_url = f"http://{address}:{port}/v1"
                logging.info(f"Successfully discovered {service_name} at {base_url}")
                return base_url
        except requests.exceptions.RequestException as e:
            logging.warning(f"Could not connect to Consul or find service {service_name}: {e}")

        logging.info(f"Service {service_name} not found, retrying in {delay} seconds...")
        await asyncio.sleep(delay)

async def main():
    """The main entry point for the conversational AI application.

    This function initializes all components, including the web server,
    transport layers, and Pipecat pipelines (main, vision, and interrupt).
    It then starts the PipelineRunner to run all pipelines concurrently.
    """
    # Dynamically find a workable audio configuration to avoid hardware issues
    device_index, sample_rate = find_workable_audio_config()

    transport_params = LocalAudioTransportParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
        audio_in_device_index=device_index,
        audio_in_sample_rate=sample_rate,
        audio_out_sample_rate=sample_rate,
    )
    transport = LocalAudioTransport(transport_params)

    # Start the web server in a separate thread
    config = uvicorn.Config(web_server.app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    threading.Thread(target=server.run).start()

    # Load configuration from Consul
    consul_host = os.getenv("CONSUL_HOST", "127.0.0.1")
    consul_port = int(os.getenv("CONSUL_PORT", "8500"))
    app_config = await load_config_from_consul(consul_host, consul_port)

    # Add consul host and port to config for other components to use
    app_config['consul_host'] = consul_host
    app_config['consul_port'] = consul_port

    tts_voices = app_config.get("tts_voices", [])
    stt_service_name = app_config.get("stt_service")
    if stt_service_name == "faster-whisper":
        stt_provider = app_config.get("active_stt_provider", "faster-whisper")
        stt_model_name = app_config.get("active_stt_model_name", "tiny.en")
        model_path = f"/opt/nomad/models/stt/{stt_provider}/{stt_model_name}"
        stt = FasterWhisperSTTService(model_path=model_path, sample_rate=sample_rate)
        logging.info(f"Configured FasterWhisper for STT with model '{model_path}' and sample rate {sample_rate}Hz.")
    else:
        raise RuntimeError(f"STT_SERVICE not configured correctly in Consul. Got '{stt_service_name}'")

    # Discover the main LLM service from Consul
    main_llm_service_name = app_config.get("llama_api_service_name", "llamacpp-rpc-api")
    consul_http_addr = f"http://{consul_host}:{consul_port}"
    llm_base_url = await discover_service(main_llm_service_name, consul_http_addr)

    llm = OpenAILLMService(
        base_url=llm_base_url,
        api_key="dummy",
        model="dummy" # The model is selected by the prima-expert job, not here.
    )

    # Use the local Piper TTS service with the configured voices
    if not tts_voices:
        raise RuntimeError("TTS voices not configured in Consul.")
    model_path = f"/opt/nomad/models/tts/{tts_voices[0]['model']}"
    config_path = f"/opt/nomad/models/tts/{tts_voices[0]['config']}"
    tts = PiperTTSService(model_path=model_path, config_path=config_path)
    runner = PipelineRunner()

    vision_detector = YOLOv8Detector()
    logging.info("Using YOLOv8 for vision.")

    # Set logging level and approval mode from config
    if app_config.get("debug_mode", False):
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug mode enabled.")

    if app_config.get("approval_mode", False):
        logging.info("Approval mode enabled. Sensitive actions will require user confirmation.")

    twin = TwinService(
        llm=llm,
        vision_detector=vision_detector,
        runner=runner,
        app_config=app_config,
        approval_queue=approval_queue
    )
    web_server.twin_service_instance = twin

    text_injector = TextMessageInjector(text_message_queue)

    pipeline_steps = [
        transport.input(),
        stt,
        text_injector,
        UILogger(sender="user"),
        twin,
        UILogger(sender="agent"),
        tts,
        transport.output()
    ]

    # Add benchmark collector if enabled in config
    if app_config.get("benchmark_mode", False):
        pipeline_steps.insert(1, BenchmarkCollector())

    main_pipeline = Pipeline(pipeline_steps)

    whisker = WhiskerObserver(main_pipeline)

    # Vision pipeline (runs in parallel to update the detector's state)
    vision_pipeline = Pipeline([vision_detector])

    main_task = PipelineTask(main_pipeline, observers=[whisker])

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

    text_injector.start_listening()

    await runner.run(
        [main_task, PipelineTask(vision_pipeline), PipelineTask(interrupt_pipeline)]
    )

if __name__ == "__main__":
    asyncio.run(main())