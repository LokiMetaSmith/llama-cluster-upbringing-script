import os
import json
import threading
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
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
def get_env_int(key, default):
    val = os.getenv(key, str(default))
    try:
        return int(val)
    except ValueError:
        logger.warning(f"Invalid integer for {key}: '{val}'. Using default: {default}")
        return default

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = get_env_int("MQTT_PORT", 1883)
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "#")

NOMAD_ADDR = os.getenv("NOMAD_ADDR", "http://localhost:4646")

# Robustly determine the port
nomad_port = os.getenv("NOMAD_PORT_http")
if nomad_port:
    logger.info(f"Found NOMAD_PORT_http: {nomad_port}")
    try:
        PORT = int(nomad_port)
    except ValueError:
        logger.error(f"Invalid NOMAD_PORT_http: {nomad_port}. Defaulting to 5678.")
        PORT = 5678
else:
    port_env = os.getenv("PORT", "5678")
    logger.info(f"NOMAD_PORT_http not found. Checking PORT: {port_env}")
    if port_env and port_env.isdigit():
        PORT = int(port_env)
    else:
        logger.warning(f"Invalid PORT environment variable '{port_env}'. Defaulting to 5678.")
        PORT = 5678

# --- In-Memory State ---
world_state = {}
state_lock = threading.Lock()
mqtt_connected = False

# --- FastAPI App ---
app = FastAPI()

# --- MQTT Client ---
def on_connect(client, userdata, flags, rc, properties=None):
    """Callback for when the client connects to the MQTT broker."""
    global mqtt_connected
    if rc == 0:
        logger.info("Connected to MQTT Broker!")
        mqtt_connected = True
        client.subscribe(MQTT_TOPIC)
    else:
        logger.error(f"Failed to connect, return code {rc}")
        mqtt_connected = False

def on_disconnect(client, userdata, rc):
    global mqtt_connected
    logger.warning(f"Disconnected from MQTT Broker with return code {rc}")
    mqtt_connected = False

def on_message(client, userdata, msg):
    """Callback for when a PUBLISH message is received from the server."""
    global world_state
    # logger.debug(f"Received message on topic {msg.topic}")
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
    try:
        client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        # Fallback for older paho-mqtt versions
        logger.warning("CallbackAPIVersion not found, assuming older paho-mqtt version.")
        client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    max_retries = 50
    retry_delay = 5  # seconds
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to connect to MQTT broker at {MQTT_HOST}:{MQTT_PORT}... (Attempt {attempt + 1}/{max_retries})")
            client.connect(MQTT_HOST, MQTT_PORT, 60)
            client.loop_forever()
            # If loop_forever returns, it might be a clean disconnect or error handled internally
            logger.warning("MQTT client loop exited.")
            break
        except ConnectionRefusedError:
            logger.error(f"Connection refused. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        except OSError as e:
            logger.error(f"Connection failed with OSError: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}. Retrying...")
            time.sleep(retry_delay)
    else:
        logger.critical(f"Failed to connect to MQTT broker after {max_retries} attempts. Exiting application to trigger restart.")
        os._exit(1) # Force exit to restart pod

# --- API Endpoints ---
@app.get("/")
async def root():
    return {"status": "ok", "service": "world-model-service", "mqtt_connected": mqtt_connected}

@app.get("/health")
async def health():
    """Health check endpoint."""
    if not mqtt_connected:
        return JSONResponse(status_code=503, content={"status": "unhealthy", "mqtt_connected": False})
    return {"status": "healthy", "mqtt_connected": True}

@app.get("/state")
async def get_state():
    """Returns the current world state."""
    with state_lock:
        return world_state

@app.on_event("startup")
async def startup_event():
    """Start the MQTT client in a background thread on app startup."""
    logger.info("Starting up World Model Service...")
    logger.info(f"Config: MQTT_HOST={MQTT_HOST}, MQTT_PORT={MQTT_PORT}, NOMAD_ADDR={NOMAD_ADDR}")
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
