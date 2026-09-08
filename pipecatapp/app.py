import asyncio
import json
import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transports.local.audio import LocalAudioTransport, LocalAudioTransportParams

# Import components from newly refactored modules to maintain backward compatibility and for use in this file
from pipecatapp.core.audio_setup import find_workable_audio_input_device
from pipecatapp.core.config import load_config_from_consul
from pipecatapp.core.service_discovery import discover_main_llm_service, discover_services
from pipecatapp.core.twin import TwinService, session_locks
from pipecatapp.pipeline.processors import (
    AudioFileFrame,
    BenchmarkCollector,
    TextMessageInjector,
    UILogger,
    WebsocketAudioStreamer,
)
from pipecatapp.services.stt import FasterWhisperSTTService, GroqSTTService, WyomingSTTService
from pipecatapp.services.tts import KokoroTTSService, PiperTTSService, DummyTTSService
from pipecatapp.services.vision import YOLOv8Detector, initialize_vision_detector

from pipecatapp.api_keys import initialize_api_keys
from pipecatapp.gossip_discovery import gossip_registry
from pipecatapp.local_world_model import LocalWorldModel
from pipecatapp.mqtt_world_model_client import MQTTWorldModelClient
from pipecatapp.secret_manager import secret_manager
from pipecatapp.security import redact_sensitive_data
from pipecatapp.services.obsidian_gardener import ObsidianGardener
from pipecatapp.task_supervisor import TaskSupervisor
import pipecatapp.web_server
from pipecatapp.web_server import approval_queue, text_message_queue
from pipecatapp.workflow.runner import WorkflowRunner


# -----------------------
# Logging -> web UI bridge
# -----------------------
class WebSocketLogHandler(logging.Handler):
    """A logging handler that forwards records to a WebSocket connection.

    This class allows the application's logs to be streamed in real-time
    to a web-based user interface.
    """
    def emit(self, record):
        """Formats the log record and broadcasts it to WebSocket clients."""
        log_entry = self.format(record)
        log_entry = redact_sensitive_data(log_entry)
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(pipecatapp.web_server.manager.broadcast(json.dumps({"type": "log", "data": log_entry})))
        except RuntimeError:
            pass

logger = logging.getLogger()
logger.addHandler(WebSocketLogHandler())

# Global variable to hold the background task
agent_task = None

async def run_agent():
    """The main entry point for the conversational AI application logic."""
    logging.info("Starting agent background task...")

    # Security: Initialize SecretManager and scrub environment
    sensitive_keys = {
        "OPENAI_API_KEY",
        "OPENROUTER_API_KEY",
        "DEEPSEEK_API_KEY",
        "GROQ_API_KEY",
        "PIPECAT_API_KEYS",
        "PIECAT_API_KEYS",
        "CONSUL_HTTP_TOKEN"
    }
    secret_manager.initialize_from_env(sensitive_keys)

    api_keys_str = secret_manager.get_secret("PIPECAT_API_KEYS") or secret_manager.get_secret("PIECAT_API_KEYS")
    if api_keys_str:
        hashed_keys = [key.strip() for key in api_keys_str.split(',')]
        initialize_api_keys(hashed_keys)
        logging.info(f"Initialized with {len(hashed_keys)} API key(s).")
    else:
        logging.warning("No API keys found in PIPECAT_API_KEYS.")

    pipecatapp.web_server.app.state.is_ready = False
    pipecatapp.web_server.app.state.twin_service_instance = None

    world_model_mode = os.getenv("WORLD_MODEL_MODE", "distributed")
    if world_model_mode == "local":
        world_model = LocalWorldModel()
    else:
        world_model = MQTTWorldModelClient()
    pipecatapp.web_server.app.state.world_model = world_model

    consul_host = os.getenv("CONSUL_HOST", os.getenv("CLUSTER_IP", "127.0.0.1"))
    consul_port = int(os.getenv("CONSUL_PORT", 8500))

    try:
        app_config = await load_config_from_consul(consul_host, consul_port)
    except Exception as e:
        logging.critical(f"Failed to load config from Consul: {e}")
        return

    app_config['consul_host'] = consul_host
    app_config['consul_port'] = consul_port

    audio_device_index = find_workable_audio_input_device()

    env_service_names = os.getenv("LLAMA_API_SERVICE_NAME")
    if env_service_names:
        main_llm_service_names = [s.strip() for s in env_service_names.split(",") if s.strip()]
    else:
        main_llm_service_names = [app_config.get("llama_api_service_name", "llamacpp-rpc-api")]

    from pipecatapp.net_utils import format_url
    consul_http_addr = format_url("http", consul_host, consul_port)
    run_local_llm = os.getenv("RUN_LOCAL_LLM", "false").lower() == "true"
    llm_provider = os.getenv("LLM_PROVIDER", "local")
    llm_api_key = "dummy"
    llm_model = "dummy"
    llm_base_url = ""

    if run_local_llm:
        from pipecatapp.local_llm import LocalLLMService
        model_path = os.getenv("LOCAL_LLM_MODEL_PATH", "/opt/nomad/models/llama-2-7b-chat.gguf")
        llm = LocalLLMService(model_path=model_path)
        llm_base_url = "local"
    else:
        if llm_provider == "groq":
            llm_base_url = "https://api.groq.com/openai/v1"
            llm_api_key = secret_manager.get_secret("GROQ_API_KEY", "")
            llm_model = os.getenv("LLM_MODEL", "llama3-70b-8192")
        elif llm_provider == "deepseek":
            llm_base_url = "https://api.deepseek.com"
            llm_api_key = secret_manager.get_secret("DEEPSEEK_API_KEY", "")
            llm_model = os.getenv("LLM_MODEL", "deepseek-chat")
        elif llm_provider == "openai":
            llm_base_url = "https://api.openai.com/v1"
            llm_api_key = secret_manager.get_secret("OPENAI_API_KEY", "")
            llm_model = os.getenv("LLM_MODEL", "gpt-4o")
        else:
            explicit_llm_url = os.getenv("LLAMA_API_BASE_URL")
            if explicit_llm_url and "localhost" in explicit_llm_url:
                 llm_base_url = explicit_llm_url
            else:
                 llm_base_url = await discover_services(main_llm_service_names, consul_http_addr)

        llm = OpenAILLMService(base_url=llm_base_url, api_key=llm_api_key, model=llm_model)

    runner = PipelineRunner()
    vision_detector = initialize_vision_detector(app_config)

    if isinstance(vision_detector, YOLOv8Detector):
        vision_detector.set_connection_check_callback(lambda: len(pipecatapp.web_server.manager.active_connections) > 0)

    if app_config.get("debug_mode", False):
        logging.getLogger().setLevel(logging.DEBUG)
    if app_config.get("approval_mode", False):
        logging.info("Approval mode enabled.")

    tts = None
    websocket_streamer = None

    try:
        tts_voices = app_config.get("tts_voices", [])
        if tts_voices:
            first_voice = tts_voices[0]
            if first_voice["name"].startswith("kokoro"):
                tts = KokoroTTSService(model_path="")
            else:
                model_path = f"/opt/nomad/models/tts/{first_voice['model']}"
                tts = PiperTTSService(model_path=model_path)
            websocket_streamer = WebsocketAudioStreamer(sample_rate=tts.sample_rate)
        else:
            logging.warning("TTS voices not configured in Consul. Audio output will be disabled.")
    except Exception as e:
        logging.error(f"Failed to initialize TTS services: {e}")

    twin = TwinService(
        llm=llm,
        vision_detector=vision_detector,
        runner=runner,
        app_config=app_config,
        approval_queue=approval_queue,
        llm_base_url=llm_base_url,
        tts_service=tts
    )
    pipecatapp.web_server.app.state.twin_service_instance = twin

    task_supervisor = TaskSupervisor(twin)
    twin.task_supervisor = task_supervisor
    asyncio.create_task(task_supervisor.start())

    pipecatapp.web_server.app.state.is_ready = True
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
            if stt_provider == "wyoming":
                host = app_config.get("wyoming_host", "localhost")
                port = int(app_config.get("wyoming_port", 10300))
                stt = WyomingSTTService(host=host, port=port)
            else:
                stt_model_name = app_config.get("active_stt_model_name", "tiny.en")
                if stt_model_name.startswith(f"{stt_provider}-"):
                    stt_model_name = stt_model_name[len(stt_provider) + 1:]
                model_path = f"/opt/nomad/models/stt/{stt_provider}/{stt_model_name}"
                stt = FasterWhisperSTTService(model_path=model_path, sample_rate=16000)
        elif stt_service_name == "groq":
            groq_key = secret_manager.get_secret("GROQ_API_KEY")
            stt = GroqSTTService(api_key=groq_key)
        else:
            raise RuntimeError(f"STT_SERVICE not configured correctly in Consul. Got '{stt_service_name}'")

        pipeline_steps.extend([
            transport.input(),
            stt,
            UILogger(sender="user"),
            twin,
            UILogger(sender="agent")
        ])

        if tts:
             pipeline_steps.append(tts)
             if websocket_streamer:
                 pipeline_steps.append(websocket_streamer)

        pipeline_steps.append(transport.output())
    else:
        logging.warning("No audio device found. Starting in headless mode.")
        pipeline_steps.extend([twin, UILogger(sender="agent")])
        if tts:
             pipeline_steps.append(tts)
             if websocket_streamer:
                 pipeline_steps.append(websocket_streamer)

    pipeline_steps.insert(0, text_injector)
    if app_config.get("benchmark_mode", False):
        pipeline_steps.insert(1, BenchmarkCollector())

    main_pipeline = Pipeline(pipeline_steps)
    main_task = PipelineTask(main_pipeline)
    vision_pipeline = Pipeline([vision_detector])
    text_injector.start_listening()

    await asyncio.gather(
        runner.run(main_task),
        runner.run(PipelineTask(vision_pipeline))
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent_task
    await gossip_registry.start()

    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    gardener = None
    if vault_path:
        gardener = ObsidianGardener(vault_path=vault_path, workflow_runner_class=WorkflowRunner)
        gardener.start()

    agent_task = asyncio.create_task(run_agent(), name="pipecat_agent_loop")
    asyncio.create_task(pipecatapp.web_server.discover_ouroboros_members(), name="ouroboros_discovery")

    yield

    await gossip_registry.stop()
    if gardener:
        gardener.stop()
    if agent_task:
        agent_task.cancel()
        try:
            await agent_task
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    web_port = int(os.getenv("WEB_PORT", os.getenv("PORT", os.getenv("NOMAD_PORT_http", 8000))))
    gossip_registry.register_service("pipecatapp", web_port)
    pipecatapp.web_server.app.router.lifespan_context = lifespan

    ssl_keyfile = os.getenv("SSL_KEYFILE")
    ssl_certfile = os.getenv("SSL_CERTFILE")

    if ssl_keyfile and ssl_certfile:
        uvicorn.run(pipecatapp.web_server.app, host="0.0.0.0", port=web_port, log_level="info", ssl_keyfile=ssl_keyfile, ssl_certfile=ssl_certfile)
    else:
        uvicorn.run(pipecatapp.web_server.app, host="0.0.0.0", port=web_port, log_level="info")
