import os
import json
import threading
from fastapi import FastAPI
import paho.mqtt.client as mqtt
import requests

# --- Configuration ---
MQTT_HOST = os.getenv("MQTT_HOST", "mqtt.service.consul")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "#")
CONSUL_HOST = os.getenv("CONSUL_HOST", "localhost")
CONSUL_PORT = int(os.getenv("CONSUL_PORT", 8500))

# --- In-Memory State ---
world_state = {}
state_lock = threading.Lock()

# --- FastAPI App ---
app = FastAPI()

# --- MQTT Client ---
def on_connect(client, userdata, flags, rc, properties=None):
    """Callback for when the client connects to the MQTT broker."""
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}\n")

def on_message(client, userdata, msg):
    """Callback for when a PUBLISH message is received from the server."""
    global world_state
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
    try:
        # Assume payload is JSON, otherwise store as raw string
        payload = json.loads(msg.payload.decode())
    except (json.JSONDecodeError, UnicodeDecodeError):
        payload = msg.payload.decode()

    with state_lock:
        # Use a nested structure for topics, e.g., "home/livingroom/light" -> {"home": {"livingroom": {"light": payload}}}
        keys = msg.topic.split('/')
        current_level = world_state
        for key in keys[:-1]:
            current_level = current_level.setdefault(key, {})
        current_level[keys[-1]] = payload

def run_mqtt_client():
    """Sets up and runs the MQTT client loop."""
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_forever()

def get_consul_services():
    """Fetch all services from Consul."""
    try:
        url = f"http://{CONSUL_HOST}:{CONSUL_PORT}/v1/catalog/services"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching services from Consul: {e}")
        return {}

def update_state_from_consul():
    """Periodically update the world state with Consul service information."""
    while True:
        services = get_consul_services()
        with state_lock:
            world_state['consul'] = {'services': services}
        threading.Event().wait(60) # Update every 60 seconds

# --- API Endpoints ---
@app.get("/state")
async def get_state():
    """Returns the current world state."""
    with state_lock:
        return world_state

@app.on_event("startup")
async def startup_event():
    """Start background threads on app startup."""
    mqtt_thread = threading.Thread(target=run_mqtt_client, daemon=True)
    mqtt_thread.start()
    consul_thread = threading.Thread(target=update_state_from_consul, daemon=True)
    consul_thread.start()