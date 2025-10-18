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
import numpy as np
from memory import MemoryStore
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
from moondream_detector import MoondreamDetector

import uvicorn

# -----------------------
# Logging -> web UI bridge
# -----------------------
class WebSocketLogHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(web_server.manager.broadcast(json.dumps({"type": "log", "data": log_entry})))
        except RuntimeError:
            # If no running loop, just drop (or fallback to normal logging)
            pass

logger = logging.getLogger()
logger.addHandler(WebSocketLogHandler())

# -----------------------
# Frame processors
# -----------------------
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
        self.reset()

    async def process_frame(self, frame, direction):
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
        self.start_time = 0
        self.stt_end_time = 0
        self.llm_first_token_time = 0
        self.tts_first_audio_time = 0

class FasterWhisperSTTService(FrameProcessor):
    def __init__(self, model_path: str, sample_rate: int = 16000):
        super().__init__()
        # Use CPU int8 to reduce memory; adjust if you want GPU
        self.model = WhisperModel(model_path, device="cpu", compute_type="int8")
        self.audio_buffer = bytearray()
        self.sample_rate = sample_rate
        logging.info(f"FasterWhisperSTTService initialized with model '{model_path}'")

    def _convert_audio_bytes_to_float_array(self, audio_bytes: bytes) -> np.ndarray:
        audio_s16 = np.frombuffer(audio_bytes, dtype=np.int16)
        return audio_s16.astype(np.float32) / 32768.0

    async def process_frame(self, frame, direction):
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
    def __init__(self, model_path: str, config_path: str):
        super().__init__()
        self.voice = PiperVoice.from_files(model_path, config_path)
        self.sample_rate = self.voice.config.sample_rate

    async def process_frame(self, frame, direction):
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
    def __init__(self):
        super().__init__()
        model_path = os.getenv("YOLO_MODEL_PATH", "/opt/nomad/models/vision/yolov8n.pt")
        self.model = YOLO(model_path)
        self.latest_observation = "I don't see anything."
        self.last_detected_objects = set()

    async def process_frame(self, frame, direction):
        if not isinstance(frame, VisionImageRawFrame):
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
        return self.latest_observation

# -----------------------
# Text message injector (UI -> pipeline)
# -----------------------
class TextMessageInjector(FrameProcessor):
    def __init__(self, queue: asyncio.Queue):
        super().__init__()
        self.queue = queue
        self._task = None

    def start_listening(self):
        if not self._task:
            self._task = asyncio.create_task(self._run())

    async def _run(self):
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
        await self.push_frame(frame, direction)

    def stop_listening(self):
        if self._task:
            self._task.cancel()
            self._task = None

# -----------------------
# Helper: find workable audio config
# -----------------------
def find_workable_audio_config():
    try:
        import pyaudio
    except ImportError:
        logging.error("PyAudio is not installed. Using default audio config.")
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
                        continue
        logging.warning("Could not find a workable audio input configuration. Falling back to defaults.")
        return None, 16000

    except Exception as e:
        logging.error(f"An error occurred during audio device discovery: {e}. Falling back to defaults.")
        return None, 16000
    finally:
        p.terminate()

# -----------------------
# Service discovery helpers
# -----------------------
async def discover_service(service_name: str, consul_http_addr: str, delay=10):
    logging.info(f"Attempting to discover service: {service_name}")
    while True:
        try:
            response = requests.get(f"{consul_http_addr}/v1/health/service/{service_name}?passing")
            response.raise_for_status()
            services = response.json()
            if services:
                address, port = services[0]['Service']['Address'], services[0]['Service']['Port']
                base_url = f"http://{address}:{port}/v1"
                logging.info(f"Successfully discovered {service_name} at {base_url}")
                return base_url
        except requests.exceptions.RequestException as e:
            logging.warning(f"Could not connect to Consul or find service {service_name}: {e}")
        logging.info(f"Service {service_name} not found, retrying in {delay} seconds...")
        await asyncio.sleep(delay)

async def discover_main_llm_service(consul_http_addr="http://localhost:8500", delay=10):
    # This is useful for vision-specific LLM calls (used by TwinService._call_vision_llm)
    service_name = os.getenv("PRIMA_API_SERVICE_NAME", "llama-api-main")
    while True:
        try:
            response = requests.get(f"{consul_http_addr}/v1/health/service/{service_name}?passing")
            response.raise_for_status()
            services = response.json()
            if services:
                address, port = services[0]['Service']['Address'], services[0]['Service']['Port']
                base_url = f"http://{address}:{port}/v1"
                logging.info(f"Discovered main LLM service at {base_url}")
                return base_url
        except requests.exceptions.RequestException as e:
            logging.warning(f"Could not find service {service_name}: {e}")
        await asyncio.sleep(delay)

# -----------------------
# TwinService (keeps the richer app_config-aware version)
# -----------------------
class TwinService(FrameProcessor):
    """Core conversational agent orchestrator (kept from the first file)."""
    def __init__(self, llm, vision_detector, runner, app_config: dict, approval_queue=None):
        super().__init__()
        self.router_llm = llm
        self.vision_detector = vision_detector
        self.runner = runner
        self.app_config = app_config or {}
        self.approval_queue = approval_queue
        self.short_term_memory = []
        chroma_host = self.app_config.get("chroma_host", "chromadb-api.service.consul")
        chroma_port = self.app_config.get("chroma_port", 8000)
        self.long_term_memory = MemoryStore(host=chroma_host, port=chroma_port)

        self.debug_mode = self.app_config.get("debug_mode", False)
        self.approval_mode = self.app_config.get("approval_mode", False)
        self.consul_http_addr = f"http://{self.app_config.get('consul_host', '127.0.0.1')}:{self.app_config.get('consul_port', 8500)}"

        # External experts config can be provided via app_config
        self.experts = self.app_config.get("external_experts_config", {})

        self.tools = {
            "ssh": SSH_Tool(),
            "mcp": MCP_Tool(self, self.runner),
            "vision": self.vision_detector,
            "desktop_control": DesktopControlTool(),
            "code_runner": CodeRunnerTool(),
            "web_browser": WebBrowserTool(),
            "ansible": Ansible_Tool(),
            "power": Power_Tool(),
            "term_everything": TermEverythingTool(app_image_path="/opt/mcp/termeverything.AppImage"),
            "rag": RAG_Tool(base_dir="/", chroma_host=chroma_host, chroma_port=chroma_port),
        }

        if self.app_config.get("use_summarizer", False):
            self.tools["summarizer"] = SummarizerTool(self)

        self._contents = []
        self.vision_model_name = os.getenv("VISION_MODEL_NAME", "llava-llama-3")

    def get_discovered_experts(self) -> list[str]:
        """Discover expert services from Consul, merging external config and discovered services."""
        expert_names = set(self.experts.keys())
        try:
            response = requests.get(f"{self.consul_http_addr}/v1/catalog/services")
            response.raise_for_status()
            services = response.json()

            for name, service_info in services.items():
                if name.startswith("llamacpp-rpc-"):
                    expert_names.add(name.replace("llamacpp-rpc-", ""))

                tags = service_info.get("Tags", [])
                if "expert" in tags:
                    for tag in tags:
                        if tag not in ["expert", "llm"]:
                            expert_names.add(tag)
                            break
        except requests.exceptions.RequestException as e:
            logging.error(f"Could not connect to Consul for expert discovery: {e}")

        return sorted(list(expert_names))

    def get_system_prompt(self, expert_name: str = "router") -> str:
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

        return f"{base_prompt}\n\n{tools_prompt}\n\nIf the query doesn't fit a specific expert or tool, handle it yourself. Otherwise, respond with a JSON object with the \'tool\' and \'args\' keys."

    async def get_expert_service(self, expert_name: str):
        if expert_name in self.experts:
            config = self.experts[expert_name]
            api_key = os.getenv(config["api_key_env"])
            if not api_key:
                logging.error(f"API key not set for expert '{expert_name}'.")
                return None
            return OpenAILLMService(
                base_url=config["base_url"],
                api_key=api_key,
                model=config.get("model", expert_name)
            )

        service_name = f"llamacpp-rpc-{expert_name}"
        try:
            response = requests.get(f"{self.consul_http_addr}/v1/health/service/{service_name}?passing")
            response.raise_for_status()
            services = response.json()
            if not services:
                return None
            address, port = services[0]['Service']['Address'], services[0]['Service']['Port']
            return OpenAILLMService(base_url=f"http://{address}:{port}/v1", api_key="dummy", model=expert_name)
        except requests.exceptions.RequestException as e:
            logging.error(f"Could not get address for local expert {expert_name}: {e}")
            return None

    async def _request_approval(self, tool_call_info: dict) -> bool:
        request_id = str(time.time())
        await web_server.manager.broadcast(json.dumps({"type": "approval_request", "data": {"request_id": request_id, "tool_call": tool_call_info}}))
        while True:
            response = await self.approval_queue.get()
            if response.get("data", {}).get("request_id") == request_id:
                return response.get("data", {}).get("approved", False)

    async def process_frame(self, frame, direction):
        if not isinstance(frame, TranscriptionFrame):
            await self.push_frame(frame, direction)
            return
        await self.run_agent_loop(frame.text)

    async def run_agent_loop(self, user_text: str):
        logging.info(f"Starting agent loop for user query: {user_text}")
        screenshot = self.tools["desktop_control"].get_desktop_screenshot()
        self._contents = [
            {"role": "system", "content": [{"type": "text", "text": self.get_system_prompt("router")}]},
            {"role": "user", "content": [{"type": "text", "text": user_text}, {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot}"}}]}
        ]
        self.short_term_memory.append(f"User: {user_text}")

        for _ in range(10):  # Max 10 turns
            llm_response_text = await self._call_vision_llm()
            self._contents.append({"role": "assistant", "content": [{"type": "text", "text": llm_response_text}]})
            try:
                tool_call = json.loads(llm_response_text)
                if tool_call.get("tool") == "task_complete":
                    final_response = await self.router_llm.process_text("Summarize what you did and why.")
                    await self.push_frame(TextFrame(final_response))
                    self.short_term_memory.append(f"Assistant: {final_response}")
                    return

                tool_name, method_name = tool_call.get("tool", "").split('.')
                args = tool_call.get("args", {})

                if tool_name == "route_to_expert":
                    expert_name = args["expert"]
                    query = args["query"]
                    expert_llm = await self.get_expert_service(expert_name)
                    if expert_llm:
                        expert_prompt = self.get_system_prompt(expert_name)
                        expert_response = await expert_llm.process_text(f"{expert_prompt}\n\nUser query: {query}")
                        await self.push_frame(TextFrame(expert_response))
                        self.short_term_memory.append(f"Assistant ({expert_name}): {expert_response}")
                    else:
                        await self.push_frame(TextFrame(f"Could not find expert {expert_name}."))
                    return

                tool = self.tools[tool_name]
                method = getattr(tool, method_name)

                if self.approval_mode and tool_name in ["ssh", "code_runner", "ansible"]:
                    if not await self._request_approval(tool_call):
                        await self.push_frame(TextFrame(f"Action denied. I cannot use the {tool_name} tool."))
                        return

                # Synchronous tool call (tools were synchronous in your code)
                result = method(**args)
                new_screenshot = self.tools["desktop_control"].get_desktop_screenshot()
                self._contents.append({"role": "tool", "content": [{"type": "text", "text": result}, {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{new_screenshot}"}}]})
                continue

            except (json.JSONDecodeError, ValueError, KeyError) as e:
                logging.info(f"No tool call detected or error processing: {e}")
                await self.push_frame(TextFrame(llm_response_text))
                self.short_term_memory.append(f"Assistant: {llm_response_text}")
                break

        if len(self.short_term_memory) > 10:
            self.short_term_memory.pop(0)

    async def _call_vision_llm(self) -> str:
        base_url = await discover_main_llm_service(self.consul_http_addr)
        chat_url = f"{base_url}/chat/completions"
        headers = {"Content-Type": "application/json"}
        payload = {"model": self.vision_model_name, "messages": self._contents, "max_tokens": 1024, "temperature": 0.7}
        try:
            response = requests.post(chat_url, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except (requests.exceptions.RequestException, KeyError, IndexError) as e:
            logging.error(f"Error calling/parsing vision LLM: {e}")
            return "Error interacting with vision model."

# -----------------------
# Main entrypoint
# -----------------------
async def load_config_from_consul(consul_host, consul_port):
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
    # Find workable audio device/sample rate
    device_index, sample_rate = find_workable_audio_config()

    transport_params = LocalAudioTransportParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
        audio_in_device_index=device_index,
        audio_in_sample_rate=sample_rate,
        audio_out_sample_rate=sample_rate,
    )
    transport = LocalAudioTransport(transport_params)

    # Start web server (uvicorn) in its own thread
    config = uvicorn.Config(web_server.app, host="0.0.0.0", port=int(os.getenv("WEB_PORT", "8000")), log_level="info")
    server = uvicorn.Server(config)
    threading.Thread(target=server.run, daemon=True).start()

    # Load configuration from Consul
    consul_host = os.getenv("CONSUL_HOST", "127.0.0.1")
    consul_port = int(os.getenv("CONSUL_PORT", "8500"))
    app_config = await load_config_from_consul(consul_host, consul_port)

    # Add consul host/port to app_config
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

    # Discover main LLM from Consul
    main_llm_service_name = app_config.get("llama_api_service_name", "llamacpp-rpc-api")
    consul_http_addr = f"http://{consul_host}:{consul_port}"
    llm_base_url = await discover_service(main_llm_service_name, consul_http_addr)

    llm = OpenAILLMService(
        base_url=llm_base_url,
        api_key="dummy",
        model="dummy"
    )

    # TTS setup
    if not tts_voices:
        raise RuntimeError("TTS voices not configured in Consul.")
    model_path = f"/opt/nomad/models/tts/{tts_voices[0]['model']}"
    config_path = f"/opt/nomad/models/tts/{tts_voices[0]['config']}"
    tts = PiperTTSService(model_path=model_path, config_path=config_path)

    runner = PipelineRunner()
    vision_detector = YOLOv8Detector()
    logging.info("Using YOLOv8 for vision.")

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

    # Optionally insert benchmark collector
    if app_config.get("benchmark_mode", False):
        pipeline_steps.insert(1, BenchmarkCollector())

    main_pipeline = Pipeline(pipeline_steps)
    whisker = WhiskerObserver(main_pipeline)
    main_task = PipelineTask(main_pipeline, observers=[whisker])

    # Vision pipeline (parallel)
    vision_pipeline = Pipeline([vision_detector])

    # Interruption handler pipeline (best-effort)
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
