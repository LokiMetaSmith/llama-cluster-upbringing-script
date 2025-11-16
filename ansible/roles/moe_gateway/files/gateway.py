import asyncio
import logging
import os
import uuid
from typing import Dict, Any

import httpx
from fastapi import FastAPI, Request, Response, Body
from fastapi.responses import JSONResponse
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# --- Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---
PIPECAT_SERVICE_URL = ""
GATEWAY_URL = f"http://{os.getenv('NOMAD_IP_http')}:{os.getenv('NOMAD_PORT_http')}" if os.getenv('NOMAD_IP_http') and os.getenv('NOMAD_PORT_http') else "http://127.0.0.1:8001"
CONSUL_HTTP_ADDR = os.getenv("CONSUL_HTTP_ADDR", "http://127.0.0.1:8500")


# --- FastAPI App ---
app = FastAPI(
    title="Mixture of Experts (MoE) Gateway",
    description="An OpenAI-compatible API gateway for the distributed agent cluster.",
    version="1.0.0",
)

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
    if not PIPECAT_SERVICE_URL:
        await discover_pipecat_service()
        if not PIPECAT_SERVICE_URL:
            return JSONResponse(status_code=503, content={"error": "pipecat-app service not available"})

    request_id = str(uuid.uuid4())
    event = asyncio.Event()
    pending_requests[request_id] = {"event": event, "response": None}

    # Forward the request to the pipecat-app service
    try:
        messages = payload.get("messages", [])
        last_user_message = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")

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
        return JSONResponse(status_code=500, content={"error": f"Failed to forward request to pipecat-app: {e}"})

    # Wait for the response to come back
    try:
        await asyncio.wait_for(event.wait(), timeout=60.0)
    except asyncio.TimeoutError:
        return JSONResponse(status_code=504, content={"error": "Request timed out"})
    finally:
        response_data = pending_requests.pop(request_id, None)

    if response_data and response_data["response"]:
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
        return JSONResponse(status_code=500, content={"error": "Failed to get a response from the agent"})

if __name__ == "__main__":
    import uvicorn
    # The port should be configured via environment variables in a real deployment
    uvicorn.run(app, host="0.0.0.0", port=8001)
