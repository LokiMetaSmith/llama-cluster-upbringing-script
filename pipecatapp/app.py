import asyncio
import logging
import os
# Set config dir before importing ultralytics to avoid permission errors
os.environ["YOLO_CONFIG_DIR"] = "/tmp/Ultralytics"
from ultralytics import YOLO
import time
import json
import io
import wave
import inspect
import threading

from pipecat.frames.frames import (
    AudioRawFrame,
    TextFrame,
    UserImageRawFrame as VisionImageRawFrame,
    UserStartedSpeakingFrame,
    UserStoppedSpeakingFrame,
    TranscriptionFrame,
)
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.processors.frame_processor import FrameProcessor
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transports.local.audio import LocalAudioTransport, LocalAudioTransportParams
from faster_whisper import WhisperModel
from piper.voice import PiperVoice
import requests
import httpx
import consul.aio
import numpy as np
from pmm_memory import PMMMemory
from pmm_memory_client import PMMMemoryClient
from quality_control import CodeQualityAnalyzer
import web_server
from web_server import approval_queue, text_message_queue
from tools.ssh_tool import SSH_Tool
from tools.mcp_tool import MCP_Tool
from tools.desktop_control_tool import DesktopControlTool
from tools.code_runner_tool import CodeRunnerTool
from tools.web_browser_tool import WebBrowserTool
from tools.ansible_tool import Ansible_Tool
from tools.power_tool import Power_Tool
from tools.summarizer_tool import SummarizerTool
from tools.term_everything_tool import TermEverythingTool
from tools.rag_tool import RAG_Tool
from tools.ha_tool import HA_Tool
from tools.git_tool import Git_Tool
from tools.orchestrator_tool import OrchestratorTool
from tools.llxprt_code_tool import LLxprt_Code_Tool
from tools.claude_clone_tool import ClaudeCloneTool
from tools.smol_agent_tool import SmolAgentTool
from tools.final_answer_tool import FinalAnswerTool
from tools.shell_tool import ShellTool
from tools.prompt_improver_tool import PromptImproverTool
from tools.council_tool import CouncilTool
from tools.swarm_tool import SwarmTool
from tools.project_mapper_tool import ProjectMapperTool
from tools.planner_tool import PlannerTool
from agent_factory import create_tools
from task_supervisor import TaskSupervisor
from durable_execution import DurableExecutionEngine, durable_step
from moondream_detector import MoondreamDetector
from workflow.runner import WorkflowRunner, ActiveWorkflows
# Import all node classes to ensure they are registered
from workflow.nodes.base_nodes import *
from workflow.nodes.llm_nodes import *
from workflow.nodes.tool_nodes import *
from workflow.nodes.system_nodes import *
from api_keys import initialize_api_keys


import uvicorn

# -----------------------
# Logging -> web UI bridge
# -----------------------
class WebSocketLogHandler(logging.Handler):
    """A logging handler that forwards records to a WebSocket connection.

    This class allows the application's logs to be streamed in real-time
    to a web-based user interface.
    """

    def emit(self, record):
        """Formats the log record and broadcasts it to WebSocket clients.

        Args:
            record: The log record to be emitted.
        """
        log_entry = self.format(record)
        try:
            # Get the running asyncio loop to safely schedule the broadcast.
            loop = asyncio.get_running_loop()
            loop.create_task(web_server.manager.broadcast(json.dumps({"type": "log", "data": log_entry})))
        except RuntimeError:
            # If no event loop is running (e.g., during shutdown), do nothing.
            pass

logger = logging.getLogger()
logger.addHandler(WebSocketLogHandler())

# -----------------------
# Frame processors
# -----------------------
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
            await web_server.manager.broadcast(json.dumps({"type": self.sender, "data": frame.text}))
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
        return audio_s16.astype(np.float32) / 32768.0

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
            audio_f32 = self._convert_audio_bytes_to_float_array(self.audio_buffer)
            self.audio_buffer.clear()
            segments, _ = self.model.transcribe(audio_f32, language="en")
            full_text = "".join(segment.text for segment in segments).strip()
            if full_text:
                await self.push_frame(TranscriptionFrame(full_text))
        else:
            await self.push_frame(frame, direction)

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

    async def process_frame(self, frame, direction):
        """Processes text frames to synthesize audio.

        Args:
            frame: The frame to process.
            direction: The direction of the frame in the pipeline.
        """
        if not isinstance(frame, TextFrame):
            await self.push_frame(frame, direction)
            return
        audio_stream = io.BytesIO()
        self.voice.synthesize(frame.text, audio_stream)
        audio_stream.seek(0)
        with wave.open(audio_stream, "rb") as wf:
            audio_bytes = wf.readframes(wf.getnframes())
        await self.push_frame(AudioRawFrame(audio_bytes))

# -----------------------
# YOLO Vision Detector
# -----------------------
class YOLOv8Detector(FrameProcessor):
    """A Pipecat processor for real-time object detection using YOLOv8.

    This processor analyzes incoming video frames to detect objects and maintains
    a textual description of the current scene.

    Attributes:
        model: The loaded YOLOv8 model.
        latest_observation (str): A human-readable string of detected objects.
        last_detected_objects (set): The set of objects detected in the last frame.
    """
    def __init__(self):
        """Initializes the YOLOv8 detector."""
        super().__init__()
        model_path = os.getenv("YOLO_MODEL_PATH")
        if not model_path:
             logging.error("YOLO_MODEL_PATH environment variable not set.")
             model_path = "/opt/nomad/models/vision/yolov8n.pt" # Last resort fallback
        self.latest_observation = "I don't see anything."
        self.last_detected_objects = set()
        try:
            self.model = YOLO(model_path)
        except Exception as e:
            logging.error(f"Failed to load YOLOv8 model from {model_path}: {e}")
            self.model = None
            self.latest_observation = "Vision system unavailable."

    async def process_frame(self, frame, direction):
        """Processes an image frame to detect objects.

        Args:
            frame: The image frame to process.
            direction: The direction of the frame in the pipeline.
        """
        if not isinstance(frame, VisionImageRawFrame):
            await self.push_frame(frame, direction)
            return

        if self.model is None:
            # Pass frame through without processing if vision is unavailable
            await self.push_frame(frame, direction)
            return

        try:
            # run model; returns list of results; boxes.cls may be torch tensors or arrays
            detected_objects = {self.model.names[int(c)] for r in self.model(frame.image) for c in r.boxes.cls}
        except Exception as e:
            logging.error(f"YOLOv8 detection error: {e}")
            detected_objects = set()
        if detected_objects != self.last_detected_objects:
            self.last_detected_objects = detected_objects
            self.latest_observation = f"I see {', '.join(detected_objects)}." if detected_objects else "I don't see anything."
            logging.info(f"YOLOv8Detector updated observation: {self.latest_observation}")

    def get_observation(self) -> str:
        """Returns the latest observation of detected objects.

        Returns:
            A string describing the objects currently visible.
        """
        return self.latest_observation

# -----------------------
# Text message injector (UI -> pipeline)
# -----------------------
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
                    text = message.get("text")
                    is_system_alert = message.get("is_system_alert", False)

                    if is_system_alert:
                        prefix = "SYSTEM ALERT: "
                        logging.warning(f"Injecting system alert: {text}")
                        # Prepend alert tag to text to ensure the agent takes it seriously
                        text = f"{prefix}{text}"

                    # Pass the whole dict along in the frame's meta attribute
                    if text:
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

# -----------------------
# Helper: find workable audio config
# -----------------------
import contextlib
import sys

@contextlib.contextmanager
def suppress_stderr():
    """A context manager to temporarily redirect stderr to /dev/null."""
    stderr = sys.stderr
    devnull = open(os.devnull, 'w')
    sys.stderr = devnull
    try:
        yield
    finally:
        sys.stderr = stderr  # Restore stderr
        devnull.close()

def find_workable_audio_input_device():
    """
    Silently scans for a workable PyAudio input device.

    Returns:
        An integer (device_index) if a workable device is found.
        None if no workable device is found.
    """
    logging.info("Starting silent audio device scan...")
    pa = None
    try:
        import pyaudio
        # 1. Suppress C-level spam during init
        with suppress_stderr():
            pa = pyaudio.PyAudio()

        # 2. Scan devices for a workable input
        for i in range(pa.get_device_count()):
            device_info = pa.get_device_info_by_index(i)
            # This is a basic check. You can make this more robust
            # (e.g., check for sample rate, "USB", "Analog", etc.)
            if device_info.get('maxInputChannels') > 0:
                logging.info(f"Found workable audio device: [Index {i}] {device_info.get('name')}")
                return i  # Return the first workable device index

        logging.warning("No workable audio input device found after full scan.")
        return None

    except (ImportError, Exception) as e:
        # This catches errors like "No Default Input Device" on truly headless systems
        logging.warning(f"Audio subsystem scan failed (this is OK for headless): {e}")
        return None

    finally:
        # 3. Always terminate PyAudio to release resources
        if pa:
            pa.terminate()

# -----------------------
# Service discovery helpers
# -----------------------
async def discover_services(service_names: list, consul_http_addr: str, delay=10):
    """Periodically queries Consul to find a healthy instance of a service, with failover support.

    Args:
        service_names (list): A list of service names to discover, in order of preference.
        consul_http_addr (str): The HTTP address of the Consul agent.
        delay (int): The number of seconds to wait between retries.

    Returns:
        The base URL (e.g., "http://1.2.3.4:5678/v1") of the first discovered service.
    """
    logging.info(f"Attempting to discover services: {service_names}")
    token = os.getenv("CONSUL_HTTP_TOKEN", "").strip()
    headers = {"X-Consul-Token": token} if token else {}

    async with httpx.AsyncClient() as client:
        while True:
            for service_name in service_names:
                try:
                    logging.debug(f"Checking status of service: {service_name}")
                    url = f"{consul_http_addr}/v1/health/service/{service_name}?passing"
                    response = await client.get(url, headers=headers, timeout=5)

                    if response.status_code != 200:
                        logging.warning(f"Consul returned {response.status_code} for {service_name} at {url}: {response.text}")
                        continue

                    services = response.json()
                    if services:
                        address, port = services[0]['Service']['Address'], services[0]['Service']['Port']
                        base_url = f"http://{address}:{port}/v1"
                        logging.info(f"Successfully discovered {service_name} at {base_url}")
                        return base_url
                    else:
                        logging.info(f"Consul returned empty list for {service_name} at {url}")
                except Exception as e:
                    logging.error(f"Unexpected error discovering {service_name}: {e}")

            logging.info(f"No healthy services found in list {service_names}, retrying in {delay} seconds...")
            await asyncio.sleep(delay)

async def discover_main_llm_service(consul_http_addr="http://localhost:8500", delay=10):
    """Discovers the main LLM service used for vision-related tasks.

    This is a specialized wrapper around `discover_service` for the primary
    vision-capable LLM.

    Args:
        consul_http_addr (str): The HTTP address of the Consul agent.
        delay (int): The number of seconds to wait between retries.

    Returns:
        The base URL of the discovered LLM service.
    """
    # This is useful for vision-specific LLM calls (used by TwinService._call_vision_llm)
    service_name = os.getenv("PRIMA_API_SERVICE_NAME")
    if not service_name:
         logging.warning("PRIMA_API_SERVICE_NAME not set, defaulting to llama-api-main")
         service_name = "llama-api-main"

    token = os.getenv("CONSUL_HTTP_TOKEN", "").strip()
    headers = {"X-Consul-Token": token} if token else {}

    async with httpx.AsyncClient() as client:
        while True:
            try:
                url = f"{consul_http_addr}/v1/health/service/{service_name}?passing"
                response = await client.get(url, headers=headers, timeout=5)

                if response.status_code != 200:
                    logging.warning(f"Consul returned {response.status_code} for {service_name} at {url}: {response.text}")
                else:
                    services = response.json()
                    if services:
                        address, port = services[0]['Service']['Address'], services[0]['Service']['Port']
                        base_url = f"http://{address}:{port}/v1"
                        logging.info(f"Discovered main LLM service at {base_url}")
                        return base_url
                    else:
                        logging.info(f"Consul returned empty list for {service_name} at {url}")
            except Exception as e:
                logging.warning(f"Could not find service {service_name}: {e}")
            await asyncio.sleep(delay)

# -----------------------
# TwinService (keeps the richer app_config-aware version)
# -----------------------
class TwinService(FrameProcessor):
    """Core conversational agent orchestrator.

    This class is the "brain" of the agent. It receives user input,
    initializes the workflow engine, and sends the final response.
    The core logic is now managed by the declarative workflow system.
    """
    def __init__(self, llm, vision_detector, runner, app_config: dict, approval_queue=None, llm_base_url=None):
        """Initializes the TwinService.

        Args:
            llm: The primary LLM service client.
            vision_detector: An instance of YOLOv8Detector for scene analysis.
            runner: The Pipecat PipelineRunner instance.
            app_config (dict): The application's configuration loaded from Consul.
            approval_queue: The queue for handling tool use approval requests.
            llm_base_url (str, optional): The base URL of the LLM service.
        """
        super().__init__()
        self.router_llm = llm
        self.llm_base_url = llm_base_url
        self.vision_detector = vision_detector
        self.runner = runner
        self.app_config = app_config or {}
        self.approval_queue = approval_queue
        self.short_term_memory = []

        # Optimization: Pre-load external experts config to avoid json.loads in process_frame loop
        external_experts_config_str = os.getenv("EXTERNAL_EXPERTS_CONFIG", "{}")
        try:
            self.external_experts_config = json.loads(external_experts_config_str)
        except json.JSONDecodeError:
            self.external_experts_config = {}
            logging.warning("Failed to parse EXTERNAL_EXPERTS_CONFIG JSON.")

        # Use Remote Memory if available (via Consul discovery or env var), otherwise fallback to local
        memory_service_url = os.getenv("MEMORY_SERVICE_URL")
        if memory_service_url:
             logging.info(f"Using Remote Memory Service at {memory_service_url}")
             self.long_term_memory = PMMMemoryClient(base_url=memory_service_url)
        else:
             logging.info("Using Local PMMMemory (SQLite)")
             self.long_term_memory = PMMMemory(db_path="~/.config/pipecat/pypicat_memory.db")

        self.quality_analyzer = CodeQualityAnalyzer()

        # This will hold metadata from incoming requests (e.g., from the gateway)
        self.current_request_meta = None

        # Optimization: Reusable HTTP client for gateway responses
        self.http_client = httpx.AsyncClient(timeout=30.0)

        self.debug_mode = self.app_config.get("debug_mode", False)
        self.approval_mode = self.app_config.get("approval_mode", False)
        self.consul_http_addr = f"http://{self.app_config.get('consul_host', '127.0.0.1')}:{self.app_config.get('consul_port', 8500)}"

        # Initialize tools via factory
        self.tools = create_tools(self.app_config, twin_service=self, runner=self.runner)
        # Add vision detector explicitly as it is a special case (frame processor)
        self.tools["vision"] = self.vision_detector
       # self.tools = {
       #     "ssh": SSH_Tool(),
       #     "mcp": MCP_Tool(self, self.runner),
       #     "vision": self.vision_detector,
       #     "desktop_control": DesktopControlTool(),
       #     "code_runner": CodeRunnerTool(),
       #     "smol_agent_computer": SmolAgentTool(),
       #     "web_browser": WebBrowserTool(),
       #     "ansible": Ansible_Tool(),
       #    "power": Power_Tool(),
       #    "term_everything": TermEverythingTool(app_image_path="/opt/mcp/termeverything.AppImage"),
       #    "rag": RAG_Tool(pmm_memory=self.long_term_memory, base_dir="/"),
       #    "ha": HA_Tool(
       #        ha_url=self.app_config.get("ha_url"),
       #        ha_token=self.app_config.get("ha_token")
       #   ),
       #   "git": Git_Tool(),
       #    "orchestrator": OrchestratorTool(),
       #    "llxprt_code": LLxprt_Code_Tool(),
       #    "claude_clone": ClaudeCloneTool(),
       #    "final_answer": FinalAnswerTool(),
       #    "shell": ShellTool(),
       #    "prompt_improver": PromptImproverTool(self),
       #    "council": CouncilTool(self),
       #    "swarm": SwarmTool(),
       #    "project_mapper": ProjectMapperTool(),
       #    "planner": PlannerTool(self),
       #}

        #if self.app_config.get("use_summarizer", False):
       #     self.tools["summarizer"] = SummarizerTool(self)

    async def process_frame(self, frame, direction):
        """Entry point for the agent's logic, triggered by a transcription frame.
        This now uses the new workflow engine.
        Args:
            frame: The incoming frame from the pipeline.
            direction: The direction of the frame in the pipeline.
        """
        if not isinstance(frame, TranscriptionFrame):
            await self.push_frame(frame, direction)
            return

        # Store meta for this request
        self.current_request_meta = frame.meta if hasattr(frame, 'meta') else None

        logging.info(f"Starting workflow for user query: {frame.text}")

        active_workflows = ActiveWorkflows()
        request_id = self.current_request_meta.get("request_id", str(time.time()))

        try:
            workflow_runner = WorkflowRunner("workflows/default_agent_loop.yaml", runner_id=request_id)
            active_workflows.add_runner(request_id, workflow_runner)

            global_inputs = {
                "user_text": frame.text,
                "tools_dict": self.tools,
                "tool_result": None, # Start with no tool result
                "consul_http_addr": self.consul_http_addr,
                "twin_service": self,
                "external_experts_config": self.external_experts_config
            }

            previous_tool_calls = []

            for _ in range(10): # Allow up to 10 steps in the thought process
                workflow_result = await workflow_runner.run(global_inputs)

                final_response = workflow_result.get("final_response")
                tool_call = workflow_result.get("tool_call")

                if final_response:
                    logging.info(f"Workflow produced final response: {final_response}")
                    await self._send_response(final_response)
                    await self.long_term_memory.add_event(kind="assistant_message", content=final_response)
                    self.short_term_memory.append(f"Assistant: {final_response}")
                    return # End the loop

                if tool_call:
                    logging.info(f"Workflow produced tool call: {tool_call}")

                    # Detect Loops
                    tool_name = tool_call.get("name")
                    tool_args = tool_call.get("arguments", {})
                    # Normalize args to ensure consistent string representation
                    try:
                        tool_args_str = json.dumps(tool_args, sort_keys=True)
                    except Exception:
                        tool_args_str = str(tool_args)

                    current_signature = (tool_name, tool_args_str)
                    previous_tool_calls.append(current_signature)

                    # Check if the last 3 calls are identical
                    if len(previous_tool_calls) >= 3 and all(c == current_signature for c in previous_tool_calls[-3:]):
                        logging.warning("Loop detected in tool calls. Injecting system alert.")
                        global_inputs["tool_result"] = "SYSTEM ALERT: You have called this tool with these exact arguments 3 times in a row. Please change your strategy or ask the user for help."
                    else:
                        # The tool is executed within the workflow, so we just need to
                        # grab the result and feed it back into the next iteration.
                        global_inputs["tool_result"] = workflow_result.get("tool_result")

                    # Continue the loop
                else:
                    # This case should not be reached if the workflow is designed correctly
                    logging.error("Workflow ended without a final response or a tool call.")
                    await self._send_response("I'm sorry, my thought process ended unexpectedly.")
                    return

            # If the loop completes without a final answer
            await self._send_response("I seem to be stuck in a thought loop. Could you please clarify your request?")

        except Exception as e:
            logging.error(f"An error occurred during workflow execution: {e}", exc_info=True)
            await self._send_response("I'm sorry, an internal error occurred while processing your request with the new workflow engine.")
        finally:
            active_workflows.remove_runner(request_id)

    async def _send_response(self, text: str):
        """Sends a response back to the appropriate channel (TTS or Gateway)."""
        if self.current_request_meta and "response_url" in self.current_request_meta:
            response_url = self.current_request_meta["response_url"]
            request_id = self.current_request_meta["request_id"]
            try:
                # Bolt ⚡ Optimization: Use reused client instead of creating new one
                await self.http_client.post(response_url, json={"request_id": request_id, "content": text})
                logging.info(f"Sent response for request {request_id} to gateway.")
            except Exception as e:
                logging.error(f"Failed to send response to gateway: {e}")
        else:
            # Default to pushing to the audio pipeline
            await self.push_frame(TextFrame(text))

    async def _request_approval(self, tool_call_info: dict) -> bool:
        """Sends a tool call to the web UI for user approval.

        Args:
            tool_call_info (dict): A dictionary describing the tool call.

        Returns:
            True if the user approved the action, False otherwise.
        """
        request_id = str(time.time())
        await web_server.manager.broadcast(json.dumps({"type": "approval_request", "data": {"request_id": request_id, "tool_call": tool_call_info}}))
        while True:
            response = await self.approval_queue.get()
            if response.get("data", {}).get("request_id") == request_id:
                return response.get("data", {}).get("approved", False)

# -----------------------
# Main entrypoint
# -----------------------
def initialize_vision_detector(app_config: dict) -> FrameProcessor:
    """Initializes the vision detector based on configuration with failover.

    This function selects a primary vision model (e.g., YOLOv8, Moondream)
    based on the `app_config`. If the primary model fails to initialize,
    it attempts to load a fallback model. If both fail, it returns a dummy
    processor that indicates the vision system is unavailable.

    Args:
        app_config (dict): The application configuration dictionary.

    Returns:
        An instance of a vision detector (e.g., YOLOv8Detector, MoondreamDetector)
        or a dummy FrameProcessor if initialization fails.
    """
    vision_model_name = app_config.get("vision_model", "yolov8")
    primary_model, fallback_model = (YOLOv8Detector, MoondreamDetector) if vision_model_name == "yolov8" else (MoondreamDetector, YOLOv8Detector)

    try:
        logging.info(f"Attempting to initialize primary vision model: {primary_model.__name__}")
        detector = primary_model()
        logging.info(f"Successfully initialized {primary_model.__name__}")
        return detector
    except Exception as e:
        logging.warning(f"Failed to initialize {primary_model.__name__}: {e}. Attempting fallback.")
        try:
            logging.info(f"Attempting to initialize fallback vision model: {fallback_model.__name__}")
            detector = fallback_model()
            logging.info(f"Successfully initialized {fallback_model.__name__}")
            return detector
        except Exception as e_fallback:
            logging.error(f"Failed to initialize fallback vision model {fallback_model.__name__}: {e_fallback}")
            class VisionUnavailable(FrameProcessor):
                def get_observation(self) -> str:
                    return "Vision system is completely unavailable."
            detector = VisionUnavailable()
            logging.info("Initialized with a dummy vision processor.")
            return detector

async def load_config_from_consul(consul_host, consul_port):
    """Loads application and model configuration from the Consul KV store.

    Args:
        consul_host (str): The hostname or IP address of the Consul agent.
        consul_port (int): The port of the Consul agent.

    Returns:
        A dictionary containing the loaded configuration.
    """
    logging.info("Loading configuration from Consul KV store...")
    config = {}
    token = os.getenv("CONSUL_HTTP_TOKEN", "").strip()
    c = consul.aio.Consul(host=consul_host, port=consul_port, token=token)
    try:
        index, data = await c.kv.get('config/app/settings')
        if data:
            app_settings = json.loads(data['Value'].decode('utf-8'))
            config.update(app_settings)
            logging.info("Successfully loaded application settings from Consul.")
        else:
            logging.error("Could not find 'config/app/settings' in Consul KV.")

        index, data = await c.kv.get('config/models/tts_voices')
        if data:
            config['tts_voices'] = json.loads(data['Value'].decode('utf-8'))
            logging.info("Successfully loaded TTS voices from Consul.")
        else:
            logging.warning("Could not find 'config/models/tts_voices' in Consul KV.")

    except Exception as e:
        logging.error(f"Error loading configuration from Consul: {e}")
    return config

async def main():
    """The main entry point for the conversational AI application."""
    # Initialize API Keys
    api_keys_str = os.getenv("PIPECAT_API_KEYS") or os.getenv("PIECAT_API_KEYS", "")
    if api_keys_str:
        hashed_keys = [key.strip() for key in api_keys_str.split(',')]
        initialize_api_keys(hashed_keys)
        logging.info(f"Initialized with {len(hashed_keys)} API key(s).")
    else:
        logging.warning("No API keys found in PIPECAT_API_KEYS (or PIECAT_API_KEYS). Sensitive endpoints will be insecure if not protected elsewhere.")

    # Load configuration from Consul
    consul_host = os.getenv("CONSUL_HOST")
    if not consul_host:
         raise RuntimeError("CONSUL_HOST environment variable not set")

    consul_port_str = os.getenv("CONSUL_PORT")
    if not consul_port_str:
         raise RuntimeError("CONSUL_PORT environment variable not set")
    consul_port = int(consul_port_str)

    app_config = await load_config_from_consul(consul_host, consul_port)

    # Add consul host/port to app_config
    app_config['consul_host'] = consul_host
    app_config['consul_port'] = consul_port

    # Run the robust, silent pre-flight check
    audio_device_index = find_workable_audio_input_device()

    # Discover main LLM from Consul or Environment
    # We prefer environment variables which can contain a comma-separated list of services for failover
    env_service_names = os.getenv("LLAMA_API_SERVICE_NAME")
    if env_service_names:
        # Split by comma and strip whitespace
        main_llm_service_names = [s.strip() for s in env_service_names.split(",") if s.strip()]
    else:
        # Fallback to single service from Consul config or default
        logging.warning("LLAMA_API_SERVICE_NAME not set, falling back to Consul config or default.")
        main_llm_service_names = [app_config.get("llama_api_service_name", "llamacpp-rpc-api")]

    consul_http_addr = f"http://{consul_host}:{consul_port}"

    # Set initial state for web server
    web_server.app.state.is_ready = False
    web_server.app.state.twin_service_instance = None

    # Start web server (uvicorn) in its own thread immediately so /health checks pass
    # even while we are waiting for discovery
    web_port_str = os.getenv("WEB_PORT")
    if not web_port_str:
        logging.warning("WEB_PORT not set, defaulting to 8000")
        web_port = 8000
    else:
        web_port = int(web_port_str)

    config = uvicorn.Config(
        web_server.app,
        host="0.0.0.0",
        port=web_port,
        log_level="info"
    )
    server = uvicorn.Server(config)
    threading.Thread(target=server.run, daemon=True).start()

    llm_base_url = await discover_services(main_llm_service_names, consul_http_addr)

    llm = OpenAILLMService(
        base_url=llm_base_url,
        api_key="dummy",
        model="dummy"
    )

    runner = PipelineRunner()

    vision_detector = initialize_vision_detector(app_config)


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
        approval_queue=approval_queue,
        llm_base_url=llm_base_url
    )
    web_server.app.state.twin_service_instance = twin

    # Start Task Supervisor
    task_supervisor = TaskSupervisor(twin)
    asyncio.create_task(task_supervisor.start())

    # Now that the twin service is initialized and the web server is starting,
    # we can mark the application as ready.
    web_server.app.state.is_ready = True
    logging.info("Application is fully initialized and ready.")

    text_injector = TextMessageInjector(text_message_queue)

    pipeline_steps = []

    if audio_device_index is not None:
        logging.info("Audio device detected. Starting audio pipeline.")
        transport_params = LocalAudioTransportParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            audio_in_device_index=audio_device_index,
            audio_in_sample_rate=16000,
            audio_out_sample_rate=16000,
        )
        transport = LocalAudioTransport(transport_params)

        stt_service_name = app_config.get("stt_service") or os.getenv("STT_SERVICE")
        if stt_service_name == "faster-whisper":
            stt_provider = app_config.get("active_stt_provider", "faster-whisper")
            stt_model_name = app_config.get("active_stt_model_name", "tiny.en")
            # Sanitize the model name if it contains the provider name as a prefix
            if stt_model_name.startswith(f"{stt_provider}-"):
                stt_model_name = stt_model_name[len(stt_provider) + 1:]
            model_path = f"/opt/nomad/models/stt/{stt_provider}/{stt_model_name}"
            stt = FasterWhisperSTTService(model_path=model_path, sample_rate=16000)
            logging.info(f"Configured FasterWhisper for STT with model '{model_path}' and sample rate 16000Hz.")
        else:
            raise RuntimeError(f"STT_SERVICE not configured correctly in Consul. Got '{stt_service_name}'")

        tts_voices = app_config.get("tts_voices", [])
        if not tts_voices:
            raise RuntimeError("TTS voices not configured in Consul.")
        model_path = f"/opt/nomad/models/tts/{tts_voices[0]['model']}"
        tts = PiperTTSService(model_path=model_path)

        pipeline_steps.extend([
            transport.input(),
            stt,
            UILogger(sender="user"),
            twin,
            UILogger(sender="agent"),
            tts,
            transport.output()
        ])
    else:
        logging.warning("No audio device found. Starting in headless mode (no audio source, no STT).")
        pipeline_steps.append(twin)

    pipeline_steps.insert(0, text_injector)

    # Optionally insert benchmark collector
    if app_config.get("benchmark_mode", False):
        pipeline_steps.insert(1, BenchmarkCollector())

    main_pipeline = Pipeline(pipeline_steps)
    main_task = PipelineTask(main_pipeline)

    # Vision pipeline (parallel)
    vision_pipeline = Pipeline([vision_detector])

    text_injector.start_listening()

    await runner.run(
        main_task, PipelineTask(vision_pipeline)
    )

if __name__ == "__main__":
    asyncio.run(main())
