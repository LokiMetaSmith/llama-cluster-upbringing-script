import asyncio
import logging
import os
import uuid
import sqlite3
import time
import json
from typing import Dict, Any, List

import httpx
from fastapi import FastAPI, Request, Response, Body, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from pydantic import BaseModel

# --- Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---
PIPECAT_SERVICE_URL = ""
GATEWAY_URL = f"http://{os.getenv('NOMAD_IP_http')}:{os.getenv('NOMAD_PORT_http')}" if os.getenv('NOMAD_IP_http') and os.getenv('NOMAD_PORT_http') else "http://127.0.0.1:8001"
CONSUL_HTTP_ADDR = os.getenv("CONSUL_HTTP_ADDR", "http://127.0.0.1:8500")
# Use a writable directory for the DB, defaulting to /tmp/gateway_data
DB_DIR = os.getenv("GATEWAY_DB_DIR", "/tmp/gateway_data")
DB_PATH = os.path.join(DB_DIR, "gateway_metrics.db")

# --- Database Setup ---
def init_db():
    try:
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                request_id TEXT PRIMARY KEY,
                timestamp REAL,
                user_input TEXT,
                response TEXT,
                status_code INTEGER,
                latency REAL
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to initialize database at {DB_PATH}: {e}")

# Initialize DB synchronously on startup (safe as it's once)
init_db()

def _log_request_sync(request_id: str, timestamp: float, user_input: str, response: str, status_code: int, latency: float):
    """Synchronous DB write."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO requests (request_id, timestamp, user_input, response, status_code, latency)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (request_id, timestamp, user_input, response, status_code, latency))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to log request to DB: {e}")

async def log_request(request_id: str, timestamp: float, user_input: str, response: str, status_code: int, latency: float):
    """Async wrapper for DB write."""
    await asyncio.to_thread(_log_request_sync, request_id, timestamp, user_input, response, status_code, latency)

def _get_recent_requests_sync(limit: int) -> List[Dict]:
    """Synchronous DB read."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM requests ORDER BY timestamp DESC LIMIT ?', (limit,))
        rows = c.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"Failed to fetch requests: {e}")
        return []

async def get_recent_requests(limit: int = 50) -> List[Dict]:
    """Async wrapper for fetching requests."""
    return await asyncio.to_thread(_get_recent_requests_sync, limit)

def _get_metrics_sync() -> Dict:
    """Synchronous DB read."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT COUNT(*), AVG(latency) FROM requests')
        total, avg_latency = c.fetchone()
        conn.close()
        return {
            "total_requests": total or 0,
            "avg_latency": (avg_latency or 0) * 1000  # Convert to ms
        }
    except Exception as e:
        logger.error(f"Failed to fetch metrics: {e}")
        return {"total_requests": 0, "avg_latency": 0}

async def get_metrics() -> Dict:
    """Async wrapper for fetching metrics."""
    return await asyncio.to_thread(_get_metrics_sync)

# --- FastAPI App ---
app = FastAPI(
    title="Mixture of Experts (MoE) Gateway",
    description="An OpenAI-compatible API gateway for the distributed agent cluster.",
    version="1.0.0",
)

# Serve Static Files (Dashboard)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def read_root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Dashboard static files not found."}

# --- API Endpoints for Dashboard ---
@app.get("/api/logs")
async def api_logs(limit: int = 50):
    return await get_recent_requests(limit)

@app.get("/api/metrics")
async def api_metrics():
    return await get_metrics()


# --- In-memory store for pending requests ---
# In a production system, you might use Redis or another store for this.
pending_requests: Dict[str, Dict[str, Any]] = {}

# --- Service Discovery ---
class ServiceNotFound(Exception):
    pass

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((httpx.RequestError, ServiceNotFound)),
    before_sleep=lambda retry_state: logger.info(f"Retrying service discovery, attempt {retry_state.attempt_number}...")
)
async def discover_pipecat_service():
    """
    Discovers the pipecat-app service URL from Consul with retry logic.
    """
    global PIPECAT_SERVICE_URL
    consul_url = f"{CONSUL_HTTP_ADDR}/v1/health/service/pipecat-app?passing"
    logger.info(f"Attempting to discover 'pipecat-app' service from Consul at {consul_url}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(consul_url, timeout=5.0)
            response.raise_for_status()
            services = response.json()
            if services:
                service = services[0]["Service"]
                address = service["Address"]
                port = service["Port"]
                PIPECAT_SERVICE_URL = f"http://{address}:{port}"
                logger.info(f"Successfully discovered 'pipecat-app' service at: {PIPECAT_SERVICE_URL}")
            else:
                raise ServiceNotFound("Could not find a healthy 'pipecat-app' service instance in Consul.")
    except httpx.RequestError as e:
        logger.error(f"A network error occurred while trying to connect to Consul: {e}")
        raise
    except ServiceNotFound as e:
        logger.warning(str(e))
        raise
    except Exception as e:
        logger.exception(f"An unexpected error occurred during service discovery: {e}")
        raise

@app.on_event("startup")
async def startup_event():
    """On startup, discover the pipecat service."""
    await discover_pipecat_service()

# --- Health Check Endpoint ---
@app.get("/health", status_code=200)
async def health_check():
    """A simple health check endpoint."""
    return {"status": "ok"}


# --- Internal Endpoint for Responses ---
@app.post("/internal/response")
async def receive_response(payload: Dict = Body(...)):
    """
    Receives the final response from the pipecat-app service.
    """
    request_id = payload.get("request_id")
    content = payload.get("content")

    if request_id in pending_requests:
        pending_requests[request_id]["response"] = content
        pending_requests[request_id]["event"].set()
        return Response(status_code=200)
    else:
        return Response(status_code=404, content="Request ID not found")


# --- OpenAI-Compatible Endpoint ---
@app.post("/v1/chat/completions")
async def chat_completions(request: Request, payload: Dict = Body(...)):
    """
    The main OpenAI-compatible chat completions endpoint.
    """
    start_time = time.time()

    if not PIPECAT_SERVICE_URL:
        await discover_pipecat_service()
        if not PIPECAT_SERVICE_URL:
            return JSONResponse(status_code=503, content={"error": "pipecat-app service not available"})

    request_id = str(uuid.uuid4())
    event = asyncio.Event()
    pending_requests[request_id] = {"event": event, "response": None}

    # Extract user input for logging
    messages = payload.get("messages", [])
    last_user_message = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")

    # Store initial log entry (status 0 = pending)
    await log_request(request_id, start_time, last_user_message, "", 0, 0)

    try:
        if not last_user_message:
            return JSONResponse(status_code=400, content={"error": "No user message found"})

        forward_payload = {
            "type": "user_message",
            "text": last_user_message,
            "request_id": request_id,
            "response_url": f"{GATEWAY_URL}/internal/response"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{PIPECAT_SERVICE_URL}/internal/chat", json=forward_payload, timeout=5.0)
            response.raise_for_status()

    except Exception as e:
        del pending_requests[request_id]
        error_msg = f"Failed to forward request to pipecat-app: {e}"
        await log_request(request_id, start_time, last_user_message, error_msg, 500, time.time() - start_time)
        return JSONResponse(status_code=500, content={"error": error_msg})

    # Wait for the response to come back
    try:
        await asyncio.wait_for(event.wait(), timeout=60.0)
    except asyncio.TimeoutError:
        await log_request(request_id, start_time, last_user_message, "Timeout", 504, time.time() - start_time)
        return JSONResponse(status_code=504, content={"error": "Request timed out"})
    finally:
        response_data = pending_requests.pop(request_id, None)

    if response_data and response_data["response"]:
        # Log success
        latency = time.time() - start_time
        await log_request(request_id, start_time, last_user_message, response_data["response"], 200, latency)

        # Format the response to be OpenAI-compatible
        final_response = {
            "id": f"chatcmpl-{request_id}",
            "object": "chat.completion",
            "created": int(asyncio.get_event_loop().time()),
            "model": "moe-cluster",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_data["response"],
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 0,  # We don't have token counts, so we'll use 0
                "completion_tokens": 0,
                "total_tokens": 0,
            },
        }
        return JSONResponse(content=final_response)
    else:
        await log_request(request_id, start_time, last_user_message, "No response content", 500, time.time() - start_time)
        return JSONResponse(status_code=500, content={"error": "Failed to get a response from the agent"})

if __name__ == "__main__":
    import uvicorn
    # The port should be configured via environment variables in a real deployment
    uvicorn.run(app, host="0.0.0.0", port=8001)
