import sys
from unittest.mock import MagicMock, AsyncMock
import pytest

# List of modules to mock if they are missing in the test environment
modules_to_mock = [
    'llm_sandbox',
    'opentelemetry.exporter',
    'kokoro',
    'numpy',
    'soundfile',
    'opentelemetry.sdk.trace',
    'apscheduler.triggers.date',
    'pipecat',
    'pipecat.vad.silero',
    'aiohttp',
    'pipecat.vad.vad_analyzer',
    'pyaudio',
    'pipecat.services.openai.llm',
    'apscheduler',
    'daily',
    'paho',
    'consul',
    'pipecat.transports',
    'wyoming',
    'pipecat.transports.local',
    'wyoming.wake',
    'chromadb',
    'opentelemetry.instrumentation.requests',
    'opentelemetry.sdk.trace.export',
    'pipecat.pipeline',
    'pipecat.processors',
    'piper',
    'pipecat.vad',
    'opencode_ai',
    'opentelemetry.instrumentation.httpx',
    'torch',
    'opentelemetry.exporter.otlp',
    'cv2',
    'paho.mqtt',
    'pipecat.transports.services',
    'pipecat.processors.aggregators',
    'paho.mqtt.client',
    'pipecat.services',
    'websockets',
    'pipecat.pipeline.runner',
    'ultralytics',
    'cryptography.fernet',
    'wyoming.audio',
    'openevolve',
    'opentelemetry.exporter.otlp.proto.grpc.trace_exporter',
    'opentelemetry',
    'cryptography',
    'pipecat.frames',
    'pipecat.pipeline.pipeline',
    'pipecat.processors.frame_processor',
    'faiss',
    'pipecat.transports.local.audio',
    'pyautogui',
    'opentelemetry.exporter.otlp.proto.grpc',
    'opentelemetry.sdk',
    'pipecat.processors.aggregators.llm_response',
    'apscheduler.triggers',
    'pipecat.transports.services.daily',
    'apscheduler.schedulers',
    'pipecat.pipeline.task',
    'pipecat.frames.frames',
    'opentelemetry.instrumentation',
    'transformers',
    'pipecat.services.ai_services',
    'dotenv',
    'apscheduler.triggers.cron',
    'pipecat.services.openai',
    'opentelemetry.exporter.otlp.proto',
    'wyoming.asr',
    'sentence_transformers',
    'apscheduler.schedulers.asyncio',
    'websockets.exceptions',
    'wyoming.client',
    'opentelemetry.sdk.resources',
    'wyoming.vad',
    'paramiko',
    'requests',
    'apscheduler.triggers.interval',
    'yaml',
    'jinja2',
    'fastapi',
    'fastapi.responses',
    'openai',
    'supervisor',
    'starlette',
    'fastapi.testclient',
    'wyoming.event',
    'chromadb.config',
    'consul.aio',
    'faster_whisper',
    'opentelemetry.instrumentation.fastapi',
    'piper.voice',
    'graphviz',
    'pmm_memory'
]

def mock_module_if_missing(module_name):
    if module_name in sys.modules:
        return

    try:
        __import__(module_name)
    except (ImportError, Exception):
        if module_name == 'pipecat.pipeline.runner' or any(p in module_name for p in ['pipecat', 'frame_processor', 'pipeline', 'services', 'transports']):
            m = AsyncMock()
        else:
            m = MagicMock()

        if module_name == 'numpy':
             m.array.side_effect = lambda x, **kwargs: MagicMock(tolist=lambda: x)
        if module_name == 'opentelemetry' or module_name == 'opentelemetry.trace':
            class DummySpan:
                def __enter__(self): return self
                def __exit__(self, exc_type, exc_val, exc_tb): pass
                def set_attribute(self, k, v): pass
                def __call__(self, func): return func

            m.trace.get_tracer.return_value.start_as_current_span.return_value = DummySpan()
            m.get_tracer.return_value.start_as_current_span.return_value = DummySpan()
        if module_name == 'pipecat.processors.frame_processor':
            m.FrameProcessor.push_frame = AsyncMock()
            m.FrameProcessor.process_frame = AsyncMock()
        if module_name == 'graphviz':
            m.Digraph = MagicMock()
        sys.modules[module_name] = m

# Execute mocking at the top level to ensure it runs before test collection
for m in modules_to_mock:
    mock_module_if_missing(m)
