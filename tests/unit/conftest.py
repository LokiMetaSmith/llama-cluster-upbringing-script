import sys
from unittest.mock import MagicMock
import pytest

# List of modules to mock if they are missing in the test environment
modules_to_mock = [
    'torch',
    'sentence_transformers',
    'pipecat',
    'pipecat.frames',
    'pipecat.frames.frames',
    'pipecat.pipeline',
    'pipecat.pipeline.pipeline',
    'pipecat.pipeline.runner',
    'pipecat.pipeline.task',
    'pipecat.processors',
    'pipecat.processors.frame_processor',
    'pipecat.processors.aggregators',
    'pipecat.processors.aggregators.llm_response',
    'pipecat.services',
    'pipecat.services.ai_services',
    'pipecat.services.openai',
    'pipecat.services.openai.llm',
    'pipecat.transports',
    'pipecat.transports.services',
    'pipecat.transports.services.daily',
    'pipecat.transports.local',
    'pipecat.transports.local.audio',
    'pipecat.vad',
    'pipecat.vad.silero',
    'pipecat.vad.vad_analyzer',
    'ultralytics',
    'faiss',
    'numpy',
    'paho',
    'paho.mqtt',
    'paho.mqtt.client',
    'openevolve',
    'llm_sandbox',
    'dotenv',
    'pyautogui',
    'pyaudio',
    'faster_whisper',
    'piper',
    'piper.voice',
    'daily'
]

def mock_module_if_missing(module_name):
    if module_name in sys.modules:
        return

    try:
        __import__(module_name)
    except (ImportError, Exception):
        sys.modules[module_name] = MagicMock()
        if module_name == 'numpy':
             # Ensure array creation returns a Mock that behaves like a list/array
             sys.modules[module_name].array.side_effect = lambda x, **kwargs: MagicMock(tolist=lambda: x)

# Execute mocking at the top level to ensure it runs before test collection
for m in modules_to_mock:
    mock_module_if_missing(m)
