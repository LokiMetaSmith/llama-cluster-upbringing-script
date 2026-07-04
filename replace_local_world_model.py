import base64

content = """import threading
import json
import logging
import os
import httpx
import yaml
import re
from typing import Dict, Any, List, Optional
from pipecatapp.ontology import WorldOntology, Device, Agent, Node, Cluster

try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None

logger = logging.getLogger(__name__)

class LocalWorldModel:
    \"\"\"
    A singleton class representing the local world model state.
    It provides methods to get the state and dispatch jobs, matching
    the API of the MQTT-based world model service.
    When WORLD_MODEL_MODE is local, this class is used to store state
    in-memory and optionally fire-and-forget MQTT updates to keep
    external observers (like Home Assistant) in sync.
    \"\"\"
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

        self.ontology = WorldOntology()
        self.state_lock = threading.Lock()

        self.load_static_definitions()

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

    def load_static_definitions(self):
        \"\"\"Loads static definitions from ontology.yaml if it exists.\"\"\"
        ontology_path = os.getenv("ONTOLOGY_PATH", "ontology.yaml")
        if os.path.exists(ontology_path):
            try:
                with open(ontology_path, 'r') as f:
                    data = yaml.safe_load(f)
                    if data:
                        self.ontology = WorldOntology.model_validate(data)
                        logger.info(f"Loaded ontology from {ontology_path}")

                        # Populate global devices list from locations if not already present
                        for loc in self.ontology.locations:
                            for device in loc.infrastructure:
                                if not any(d.id == device.id for d in self.ontology.devices):
                                    self.ontology.devices.append(device)
            except Exception as e:
                logger.error(f"Failed to load ontology from {ontology_path}: {e}")
        else:
            logger.info(f"No static ontology definitions found at {ontology_path}")

    def refresh_state(self):
        \"\"\"Pulls state from Nomad API for cluster and node info, and Consul API for agents.\"\"\"
        nomad_addr = os.getenv("NOMAD_ADDR", "http://localhost:4646")
        consul_addr = os.getenv("CONSUL_ADDR", "http://localhost:8500")

        try:
            with httpx.Client() as client:
                # Refresh Nodes from Nomad
                try:
                    nodes_resp = client.get(f"{nomad_addr}/v1/nodes")
                    nodes_resp.raise_for_status()
                    nomad_nodes = nodes_resp.json()

                    with self.state_lock:
                        if not self.ontology.cluster:
                            self.ontology.cluster = Cluster(id="local_cluster", name="Local Nomad Cluster")

                        for n_data in nomad_nodes:
                            node_id = n_data.get("ID")
                            node_name = n_data.get("Name")
                            status = n_data.get("Status")
                            address = n_data.get("Address")

                            existing_node = next((n for n in self.ontology.cluster.nodes if n.id == node_id), None)
                            if existing_node:
                                existing_node.status = status
                                existing_node.address = address
                            else:
                                self.ontology.cluster.nodes.append(Node(id=node_id, name=node_name, status=status, address=address))
                except Exception as e:
                    logger.error(f"Error refreshing nodes from Nomad: {e}")

                # Refresh Agents from Consul
                try:
                    services_resp = client.get(f"{consul_addr}/v1/agent/services")
                    services_resp.raise_for_status()
                    services = services_resp.json()

                    with self.state_lock:
                        for s_id, s_data in services.items():
                            if "agent" in s_id.lower() or "agent" in s_data.get("Service", "").lower():
                                agent_id = s_id
                                agent_name = s_data.get("Service")

                                existing_agent = next((a for a in self.ontology.agents if a.id == agent_id), None)
                                if existing_agent:
                                    existing_agent.state = s_data
                                else:
                                    self.ontology.agents.append(Agent(id=agent_id, name=agent_name, state=s_data))
                except Exception as e:
                    logger.error(f"Error refreshing agents from Consul: {e}")

        except Exception as e:
            logger.error(f"Error in refresh_state: {e}")

    def get_state(self) -> Dict[str, Any]:
        \"\"\"Returns the current world state as a dictionary.\"\"\"
        with self.state_lock:
            return self.ontology.model_dump()

    def get_device(self, device_id: str) -> Optional[Device]:
        \"\"\"Retrieves a device from the ontology by ID.\"\"\"
        with self.state_lock:
            for device in self.ontology.devices:
                if device.id == device_id:
                    return device
        return None

    def get_available_compute(self) -> List[Node]:
        \"\"\"Returns a list of nodes that are ready.\"\"\"
        with self.state_lock:
            if not self.ontology.cluster:
                return []
            return [node for node in self.ontology.cluster.nodes if node.status == "ready"]

    def get_contextual_relationships(self, device_id: str) -> Dict[str, Any]:
        \"\"\"Returns contextual relationship data for a specific device.\"\"\"
        with self.state_lock:
            device = next((d for d in self.ontology.devices if d.id == device_id), None)
            if not device:
                return {"error": "Device not found"}

            location = None
            if device.location_id:
                location = next((l for l in self.ontology.locations if l.id == device.location_id), None)

            available_compute = [node.model_dump() for node in self.ontology.cluster.nodes if node.status == "ready"] if self.ontology.cluster else []

            return {
                "device": device.model_dump(),
                "location": location.model_dump() if location else None,
                "available_compute": available_compute
            }

    def update_state(self, topic: str, payload: Any):
        \"\"\"
        Updates the local state via topic routing and fires an MQTT message.
        Topic examples: telemetry/biochar/temp -> updates device 'biochar' with {'temp': payload}
        \"\"\"
        with self.state_lock:
            # Topic routing
            match = re.match(r"^telemetry/([^/]+)/(.*)$", topic)
            if match:
                device_id = match.group(1)
                subtopic = match.group(2)

                device = next((d for d in self.ontology.devices if d.id == device_id), None)

                if device:
                    keys = subtopic.split('/')
                    current_level = device.state
                    for key in keys[:-1]:
                        current_level = current_level.setdefault(key, {})
                    current_level[keys[-1]] = payload
                else:
                    # If device doesn't exist, we could create it or just log.
                    logger.debug(f"Received telemetry for unknown device {device_id} on topic {topic}. Ignoring.")
            else:
                logger.debug(f"Unmatched MQTT topic {topic}. Ignoring.")

        if self.mqtt_client:
            try:
                payload_str = json.dumps(payload) if not isinstance(payload, str) else payload
                self.mqtt_client.publish(topic, payload_str)
            except Exception as e:
                logger.error(f"Failed to publish MQTT message on topic {topic}: {e}")

    async def dispatch_job(self, model_name: str, prompt: str, cpu: int = 1000, memory: int = 4096, gpu_count: int = 1, context: str = "") -> Any:
        \"\"\"
        Dispatches a Nomad batch job directly.
        \"\"\"
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
"""

with open("pipecatapp/local_world_model.py", "w") as f:
    f.write(content)
