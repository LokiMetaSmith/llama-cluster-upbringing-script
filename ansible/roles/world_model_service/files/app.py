import os
import json
import threading
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import paho.mqtt.client as mqtt
import sys
import logging
import time

# Set up basic logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "#")

NOMAD_ADDR = os.getenv("NOMAD_ADDR", "http://localhost:4646")
PORT = int(os.getenv("PORT", 5678))

# --- In-Memory State ---
world_state = {}
state_lock = threading.Lock()

# --- FastAPI App ---
app = FastAPI()

# --- MQTT Client ---
def on_connect(client, userdata, flags, rc, properties=None):
    """Callback for when the client connects to the MQTT broker."""
    if rc == 0:
        logger.info("Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
    else:
        logger.error(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    """Callback for when a PUBLISH message is received from the server."""
    global world_state
    logger.debug(f"Received message on topic {msg.topic}")
    try:
        # Assume payload is JSON, otherwise store as raw string
        payload = json.loads(msg.payload.decode())
    except (json.JSONDecodeError, UnicodeDecodeError):
        # If decoding as JSON or UTF-8 fails, store a safe representation
        try:
             payload = msg.payload.decode(errors='replace')
        except Exception:
             payload = str(msg.payload)

    with state_lock:
        # Use a nested structure for topics, e.g., "home/livingroom/light" -> {"home": {"livingroom": {"light": payload}}}
        keys = msg.topic.split('/')
        current_level = world_state
        for key in keys[:-1]:
            current_level = current_level.setdefault(key, {})
        current_level[keys[-1]] = payload


def run_mqtt_client():
    """Sets up and runs the MQTT client loop with connection retries."""
    # Fix: Explicitly name the argument to avoid it being interpreted as client_id
    try:
        client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        # Fallback for older paho-mqtt versions if needed, though requirements install latest
        logger.warning("CallbackAPIVersion not found, assuming older paho-mqtt version.")
        client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    max_retries = 5
    retry_delay = 10  # seconds
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to connect to MQTT broker at {MQTT_HOST}:{MQTT_PORT}... (Attempt {attempt + 1}/{max_retries})")
            client.connect(MQTT_HOST, MQTT_PORT, 60)
            client.loop_forever()
            # If loop_forever() returns, it means the connection was lost.
            # We break the loop to allow the process to exit and be restarted by Nomad.
            logger.info("MQTT client loop exited. The service might need to restart.")
            break
        except ConnectionRefusedError:
            logger.error(f"Connection refused. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        except OSError as e:
            logger.error(f"Connection failed with OSError: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}. Not retrying.")
            break
    else:
        logger.critical(f"Failed to connect to MQTT broker after {max_retries} attempts. Exiting.")
        # We don't exit the main process here because uvicorn is running in main thread,
        # but this thread dies. Health check currently only checks /state which is served by uvicorn.
        # Ideally we should mark the service as unhealthy if MQTT is down.

# --- API Endpoints ---
@app.get("/")
async def root():
    return {"status": "ok", "service": "world-model-service"}

@app.get("/state")
async def get_state():
    """Returns the current world state."""
    with state_lock:
        return world_state

@app.on_event("startup")
async def startup_event():
    """Start the MQTT client in a background thread on app startup."""
    logger.info("Starting up World Model Service...")
    mqtt_thread = threading.Thread(target=run_mqtt_client, daemon=True)
    mqtt_thread.start()

class DispatchJobRequest(BaseModel):
    model_name: str
    prompt: str
    cpu: int = 1000
    memory: int = 4096
    gpu_count: int = 1

async def dispatch_job_func(job_request: DispatchJobRequest):
    """Dispatches a Nomad batch job."""
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

@app.post("/dispatch-job")
async def dispatch_job_endpoint(job_request: DispatchJobRequest):
    """Endpoint to dispatch a Nomad batch job."""
    return await dispatch_job_func(job_request)

if __name__ == "__main__":
    logger.info(f"Starting Uvicorn server on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
