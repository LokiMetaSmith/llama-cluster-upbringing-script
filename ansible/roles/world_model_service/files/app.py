import os
import json
import threading
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import paho.mqtt.client as mqtt

# --- Configuration ---
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "#")

NOMAD_ADDR = os.getenv("NOMAD_ADDR", "http://localhost:4646")


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

# --- API Endpoints ---
@app.get("/state")
async def get_state():
    """Returns the current world state."""
    with state_lock:
        return world_state

@app.on_event("startup")
async def startup_event():
    """Start the MQTT client in a background thread on app startup."""
    mqtt_thread = threading.Thread(target=run_mqtt_client, daemon=True)
    mqtt_thread.start()

class DispatchJobRequest(BaseModel):
    model_name: str
    prompt: str
    cpu: int = 1000
    memory: int = 4096
    gpu_count: int = 1

@app.post("/dispatch-job")
async def dispatch_job(job_request: DispatchJobRequest):
    """Receives a request to dispatch a Nomad batch job."""
    job_id = "llamacpp-batch"
    url = f"{NOMAD_ADDR}/v1/job/{job_id}/dispatch"

    payload = {
        "Meta": {
            "model_name": job_request.model_name,
            "prompt": job_request.prompt,
            "cpu": str(job_request.cpu),
            "memory": str(job_request.memory),
            "gpu_count": str(job_request.gpu_count),
        }
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e.response.text))
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
