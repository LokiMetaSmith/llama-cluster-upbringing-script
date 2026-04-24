import threading
import json
import logging
import os
import httpx
from typing import Dict, Any

try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None

logger = logging.getLogger(__name__)

class LocalWorldModel:
    """
    A singleton class representing the local world model state.
    It provides methods to get the state and dispatch jobs, matching
    the API of the MQTT-based world model service.
    When WORLD_MODEL_MODE is local, this class is used to store state
    in-memory and optionally fire-and-forget MQTT updates to keep
    external observers (like Home Assistant) in sync.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LocalWorldModel, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.world_state: Dict[str, Any] = {}
        self.state_lock = threading.Lock()

        self.mqtt_host = os.getenv("MQTT_HOST", "localhost")
        self.mqtt_port = int(os.getenv("MQTT_PORT", "1883"))

        self.mqtt_client = None
        if mqtt is not None:
            try:
                self.mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
            except AttributeError:
                self.mqtt_client = mqtt.Client()

            try:
                # We connect but do not loop_forever or subscribe
                # This is just for fire-and-forget publishing.
                self.mqtt_client.connect(self.mqtt_host, self.mqtt_port, 60)
                self.mqtt_client.loop_start()
            except Exception as e:
                logger.warning(f"LocalWorldModel could not connect to MQTT broker at {self.mqtt_host}:{self.mqtt_port} for publishing: {e}")
                self.mqtt_client = None

        self._initialized = True

    def get_state(self) -> Dict[str, Any]:
        """Returns the current world state."""
        with self.state_lock:
            return self.world_state.copy()

    def update_state(self, topic: str, payload: Any):
        """
        Updates the local state and fires an MQTT message.
        """
        with self.state_lock:
            keys = topic.split('/')
            current_level = self.world_state
            for key in keys[:-1]:
                current_level = current_level.setdefault(key, {})
            current_level[keys[-1]] = payload

        if self.mqtt_client:
            try:
                payload_str = json.dumps(payload) if not isinstance(payload, str) else payload
                self.mqtt_client.publish(topic, payload_str)
            except Exception as e:
                logger.error(f"Failed to publish MQTT message on topic {topic}: {e}")

    async def dispatch_job(self, model_name: str, prompt: str, cpu: int = 1000, memory: int = 4096, gpu_count: int = 1, context: str = "") -> Any:
        """
        Dispatches a Nomad batch job directly.
        """
        nomad_addr = os.getenv("NOMAD_ADDR", "http://localhost:4646")
        job_id = "llamacpp-batch"
        url = f"{nomad_addr}/v1/job/{job_id}/dispatch"

        payload = {
            "Meta": {
                "model_name": model_name,
                "prompt": prompt,
                "cpu": str(cpu),
                "memory": str(memory),
                "gpu_count": str(gpu_count),
                "context": context,
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
