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

# Enforce strict SSL/TLS verification using system CA or Consul CA
verify_param = True
if CONSUL_HTTP_ADDR.startswith("https://"):
    for ca_path in ["/etc/consul.d/ca.pem", "/etc/ssl/certs/ca-certificates.crt"]:
        if os.path.exists(ca_path):
            verify_param = ca_path
            break

# Use a writable directory for the DB, defaulting to /tmp/gateway_data
DB_DIR = os.getenv("GATEWAY_DB_DIR", "/tmp/gateway_data")
DB_PATH = os.path.join(DB_DIR, "gateway_metrics.db")

import math
import random
import re

# --- Prompt Compass Router ---
class PromptCompassRouter:
    """
    A lightweight, content-aware pre-flight router to classify intent (trivial vs complex)
    and detect PII or Jailbreaks natively in Python.
    """
    def __init__(self):
        # Extremely lightweight heuristics for jailbreaks and complexity
        self.jailbreak_patterns = [
            re.compile(r"\bignore all previous instructions\b", re.IGNORECASE),
            re.compile(r"\bact as\b", re.IGNORECASE),
            re.compile(r"\bsystem prompt\b", re.IGNORECASE),
            re.compile(r"\bbypass\b", re.IGNORECASE),
            re.compile(r"\bdeveloper mode\b", re.IGNORECASE),
            re.compile(r"\bdan\b.*\bdo anything now\b", re.IGNORECASE)
        ]
        self.pii_patterns = [
            re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), # SSN
            re.compile(r"\b(?:\d[ -]*?){13,16}\b") # Credit Card roughly
        ]
        self.complex_patterns = [
            re.compile(r"\bwrite.*code\b", re.IGNORECASE),
            re.compile(r"\banalyze\b", re.IGNORECASE),
            re.compile(r"\barchitect\b", re.IGNORECASE),
            re.compile(r"\bpython\b", re.IGNORECASE),
            re.compile(r"\bjavascript\b", re.IGNORECASE),
            re.compile(r"\bexplain\b.*\btheorem\b", re.IGNORECASE),
            re.compile(r"\boptimize\b", re.IGNORECASE)
        ]

    def analyze(self, text: str) -> dict:
        result = {
            "tier": "trivial",
            "is_jailbreak": False,
            "has_pii": False
        }

        for p in self.jailbreak_patterns:
            if p.search(text):
                result["is_jailbreak"] = True
                break

        for p in self.pii_patterns:
            if p.search(text):
                result["has_pii"] = True
                break

        if len(text) > 500: # Length heuristic
            result["tier"] = "complex"
        else:
            for p in self.complex_patterns:
                if p.search(text):
                    result["tier"] = "complex"
                    break

        return result

prompt_compass = PromptCompassRouter()

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
        # Idempotent migration to add expert_name column
        c.execute("PRAGMA table_info(requests)")
        columns = [row[1] for row in c.fetchall()]
        if "expert_name" not in columns:
            c.execute("ALTER TABLE requests ADD COLUMN expert_name TEXT DEFAULT 'default'")
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to initialize database at {DB_PATH}: {e}")

# Initialize DB synchronously on startup (safe as it's once)
init_db()

def _log_request_sync(request_id: str, timestamp: float, user_input: str, response: str, status_code: int, latency: float, expert_name: str = 'default'):
    """Synchronous DB write."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO requests (request_id, timestamp, user_input, response, status_code, latency, expert_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (request_id, timestamp, user_input, response, status_code, latency, expert_name))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to log request to DB: {e}")

async def log_request(request_id: str, timestamp: float, user_input: str, response: str, status_code: int, latency: float, expert_name: str = 'default'):
    """Async wrapper for DB write."""
    await asyncio.to_thread(_log_request_sync, request_id, timestamp, user_input, response, status_code, latency, expert_name)

# --- Thompson Sampling Scorer (Marsaglia-Tsang) ---
def random_normal() -> float:
    u1 = random.random() or 1e-15
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * random.random())

def sample_gamma(shape: float) -> float:
    if shape < 1.0:
        return sample_gamma(shape + 1.0) * math.pow(random.random() or 1e-15, 1.0 / shape)
    d = shape - 1.0 / 3.0
    c = 1.0 / math.sqrt(9.0 * d)
    while True:
        x = random_normal()
        v = 1.0 + c * x
        while v <= 0.0:
            x = random_normal()
            v = 1.0 + c * x
        v = v ** 3
        u = random.random()
        if u < 1.0 - 0.0331 * x ** 4:
            return d * v
        if math.log(u) < 0.5 * x * x + d * (1.0 - v + math.log(v)):
            return d * v

def sample_beta(alpha: float, beta: float) -> float:
    x = sample_gamma(alpha)
    y = sample_gamma(beta)
    sum_xy = x + y
    return x / sum_xy if sum_xy > 0.0 else 0.5

# --- External Experts Configuration ---
EXTERNAL_EXPERTS_CONFIG_STR = os.getenv("EXTERNAL_EXPERTS_CONFIG", "{}")
try:
    EXTERNAL_EXPERTS = json.loads(EXTERNAL_EXPERTS_CONFIG_STR)
except Exception:
    EXTERNAL_EXPERTS = {}

if not EXTERNAL_EXPERTS:
    EXTERNAL_EXPERTS = {
        "openai_gpt4": {"model": "gpt-4-turbo", "tier": "complex"},
        "openrouter_claude_sonnet": {"model": "anthropic/claude-3.5-sonnet", "tier": "complex"},
        "openrouter_gemini_flash": {"model": "google/gemini-2.0-flash-001", "tier": "complex"},
        "together_ternary_bonsai_27b": {"model": "prism-ml/ternary-bonsai-27b", "tier": "trivial"},
        "together_1bit_bonsai_27b": {"model": "prism-ml/1bit-bonsai-27b", "tier": "trivial"}
    }

def get_expert_scores(db_path: str, external_experts: dict) -> dict:
    """
    Calculates decay-weighted successes and failures for each expert,
    and draws a Thompson Sample for reliability.
    """
    now = time.time()
    # Decay parameters: half-life of 2 days (172800 seconds)
    HALF_LIFE = 2.0 * 24.0 * 60.0 * 60.0

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute('''
            SELECT expert_name, status_code, timestamp, latency
            FROM requests
            WHERE timestamp >= ?
        ''', (now - 7 * 24 * 3600,))
        rows = c.fetchall()
    except Exception as e:
        logger.error(f"Failed to query requests history: {e}")
        rows = []
    finally:
        conn.close()

    counts = {name: {"successes": 0.0, "failures": 0.0, "latencies": []} for name in external_experts}
    if 'default' not in counts:
        counts['default'] = {"successes": 0.0, "failures": 0.0, "latencies": []}

    for row in rows:
        expert_name = row[0]
        status = row[1]
        ts = row[2]
        lat = row[3] or 0.0

        if expert_name not in counts:
            counts[expert_name] = {"successes": 0.0, "failures": 0.0, "latencies": []}

        age = max(0, now - ts)
        weight = 0.5 ** (age / HALF_LIFE)

        if status == 200:
            counts[expert_name]["successes"] += weight
            counts[expert_name]["latencies"].append(lat)
        else:
            counts[expert_name]["failures"] += weight

    scores = {}
    for name, metric in counts.items():
        alpha = metric["successes"] + 1.0 # PRIOR_SUCCESS
        beta = metric["failures"] + 1.0 # PRIOR_FAILURE

        # Thompson Sample Reliability
        reliability = sample_beta(alpha, beta)

        # Speed score from average latency
        avg_lat = sum(metric["latencies"]) / len(metric["latencies"]) if metric["latencies"] else 1.0
        speed = 1.0 - min(1.0, max(0.0, (avg_lat - 0.1) / (5.0 - 0.1)))

        # Intelligence score normalized
        intel = 0.5
        if name == "openai_gpt4":
            intel = 0.9
        elif "claude" in name or "r1" in name or "o1" in name or "gpt-5" in name:
            intel = 0.95
        elif "qwen_72b" in name:
            intel = 0.8
        elif "ternary_bonsai_27b" in name:
            intel = 0.8
        elif "1bit_bonsai_27b" in name:
            intel = 0.75
        elif "flash" in name or "mini" in name:
            intel = 0.4

        score = 0.5 * reliability + 0.25 * speed + 0.25 * intel
        scores[name] = score

    return scores

def select_best_expert(tier_filter: str = None) -> str:
    """Selects the highest scoring expert based on Thompson Sampling scores, optionally filtered by tier."""
    try:
        scores = get_expert_scores(DB_PATH, EXTERNAL_EXPERTS)

        candidate_scores = {}
        for k, v in scores.items():
            if k == 'default':
                continue

            # If a tier filter is provided, skip experts that don't match
            if tier_filter and k in EXTERNAL_EXPERTS:
                expert_tier = EXTERNAL_EXPERTS[k].get("tier")
                if expert_tier and expert_tier != tier_filter:
                    continue

            candidate_scores[k] = v

        if not candidate_scores:
            candidate_scores = scores

        best_expert = max(candidate_scores, key=candidate_scores.get)
        logger.info(f"Thompson-sampling bandit chose expert: {best_expert} (score={candidate_scores[best_expert]:.4f}, tier_filter={tier_filter})")
        return best_expert
    except Exception as e:
        logger.error(f"Error selecting best expert: {e}")
        return "default"

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

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup, discover the pipecat service in the background so it doesn't block startup
    asyncio.create_task(discover_pipecat_service())
    yield

# --- FastAPI App ---
app = FastAPI(
    title="Mixture of Experts (MoE) Gateway",
    description="An OpenAI-compatible API gateway for the distributed agent cluster.",
    version="1.0.0",
    lifespan=lifespan,
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

    headers = {}
    token = os.getenv("CONSUL_HTTP_TOKEN")
    if token:
        headers["X-Consul-Token"] = token

    try:
        async with httpx.AsyncClient(verify=verify_param) as client:
            response = await client.get(consul_url, headers=headers, timeout=5.0)
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

async def apply_personality_steering(name: str, strength: float):
    """Dynamically steers the local model using the PersonalityTool mechanism."""
    try:
        api_url = f"http://{os.getenv('CLUSTER_IP', '127.0.0.1')}:8080"
        payload = [{"fname": f"/opt/nomad/models/vectors/{name}.gguf", "strength": strength}]
        # Fire and forget steering, timeouts short to avoid blocking
        async with httpx.AsyncClient(timeout=2.0) as client:
            await client.post(f"{api_url}/control-vectors", json=payload)
        logger.warning(f"Applied steering vector '{name}' (strength: {strength}) due to trigger.")
    except Exception as e:
        logger.error(f"Failed to apply personality steering: {e}")

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

    # Extract user input for pre-flight routing and logging
    messages = payload.get("messages", [])
    last_user_message = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")

    # Pre-flight content-aware routing
    analysis = prompt_compass.analyze(last_user_message)
    tier = analysis.get("tier", "trivial")

    if analysis.get("is_jailbreak") or analysis.get("has_pii"):
        # Teachable Moment: Instead of blocking, engage the steering mechanism
        logger.warning(f"PromptCompass detected flags (Jailbreak: {analysis.get('is_jailbreak')}, PII: {analysis.get('has_pii')}). Engaging steering mechanism.")
        # Apply a strict or aligned vector to handle the request safely without blocking
        asyncio.create_task(apply_personality_steering("system_alignment", 1.5))
        # Force routing to a local/trivial model to prevent expensive frontier model jailbreaks
        tier = "trivial"

    # Dynamic expert selection using Thompson-sampling convex combination filtered by tier
    selected_expert = select_best_expert(tier_filter=tier)

    request_id = str(uuid.uuid4())
    event = asyncio.Event()
    pending_requests[request_id] = {"event": event, "response": None}

    # Store initial log entry (status 0 = pending)
    await log_request(request_id, start_time, last_user_message, "", 0, 0, selected_expert)

    try:
        if not last_user_message:
            return JSONResponse(status_code=400, content={"error": "No user message found"})

        forward_payload = {
            "type": "user_message",
            "text": last_user_message,
            "request_id": request_id,
            "response_url": f"{GATEWAY_URL}/internal/response",
            "expert_name": selected_expert
        }

        async with httpx.AsyncClient(verify=verify_param) as client:
            response = await client.post(f"{PIPECAT_SERVICE_URL}/internal/chat", json=forward_payload, timeout=5.0)
            response.raise_for_status()

    except Exception as e:
        del pending_requests[request_id]
        error_msg = f"Failed to forward request to pipecat-app: {e}"
        await log_request(request_id, start_time, last_user_message, error_msg, 500, time.time() - start_time, selected_expert)
        return JSONResponse(status_code=500, content={"error": error_msg})

    # Wait for the response to come back
    try:
        await asyncio.wait_for(event.wait(), timeout=60.0)
    except asyncio.TimeoutError:
        await log_request(request_id, start_time, last_user_message, "Timeout", 504, time.time() - start_time, selected_expert)
        return JSONResponse(status_code=504, content={"error": "Request timed out"})
    finally:
        response_data = pending_requests.pop(request_id, None)

    if response_data and response_data["response"]:
        # Log success
        latency = time.time() - start_time
        await log_request(request_id, start_time, last_user_message, response_data["response"], 200, latency, selected_expert)

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
        await log_request(request_id, start_time, last_user_message, "No response content", 500, time.time() - start_time, selected_expert)
        return JSONResponse(status_code=500, content={"error": "Failed to get a response from the agent"})

if __name__ == "__main__":
    import uvicorn
    # Configure the port from Nomad environment variables, defaulting to 8001 for local dev
    port = int(os.getenv("NOMAD_PORT_http", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
