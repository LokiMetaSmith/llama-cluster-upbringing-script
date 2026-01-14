import os
import json
import asyncio
import logging
import requests
import httpx
import yaml
import time  # Added back for the backup timestamp
from fastapi import FastAPI, WebSocket, Body, Request, HTTPException, Depends, Security
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from typing import List, Dict
from workflow.runner import ActiveWorkflows, OpenGates
from workflow.history import WorkflowHistory
from api_keys import get_api_key
from .models import InternalChatRequest, SystemMessageRequest


# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Pipecat Agent API",
    description="This API exposes endpoints to interact with the Pipecat agent, including real-time communication, status checks, and state management.",
    version="1.0.0",
)

# Security Enhancement: Add CORS Middleware
# Default to "*" for development convenience, but support strict configuration via env var
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",")]

if "*" in allowed_origins and len(allowed_origins) == 1:
    logging.warning("⚠️  Security Warning: CORS is configured to allow all origins ('*'). This is acceptable for development but insecure for production. Set 'ALLOWED_ORIGINS' environment variable to a comma-separated list of trusted domains.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Enhancement: Add Security Headers
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        # Content-Security-Policy: Allow 'self' and inline scripts/styles which are used in index.html
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "img-src 'self' data:; "
            "style-src 'self' 'unsafe-inline'; "
            "script-src 'self' 'unsafe-inline'; "
            "connect-src 'self' ws: wss:;"
        )
        return response

app.add_middleware(SecurityHeadersMiddleware)

# Create queues to communicate between the web server and the TwinService
approval_queue = asyncio.Queue()
text_message_queue = asyncio.Queue()

# Simple in-memory cache for service discovery
class ServiceDiscoveryCache:
    def __init__(self, ttl=30):
        self.ttl = ttl
        self.cache = None
        self.last_update = 0
        self.lock = asyncio.Lock()

    async def get(self):
        async with self.lock:
            if self.cache is not None and time.time() - self.last_update < self.ttl:
                return self.cache
            return None

    async def set(self, value):
        async with self.lock:
            self.cache = value
            self.last_update = time.time()

service_cache = ServiceDiscoveryCache(ttl=30)
# Reusable HTTP client for service discovery
service_discovery_client = httpx.AsyncClient(timeout=2.0)

class WebSocketManager:
    """Manages active WebSocket connections.

    This class provides methods to connect, disconnect, and broadcast messages
    to all connected clients. It is used to send real-time updates (like
    logs and conversation transcripts) to the web UI.

    Attributes:
        active_connections (List[WebSocket]): A list of active WebSocket connections.
    """
    def __init__(self):
        """Initializes the ConnectionManager."""
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accepts and stores a new WebSocket connection.

        Args:
            websocket (WebSocket): The WebSocket connection to add.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Removes a WebSocket connection from the active list.

        Args:
            websocket (WebSocket): The WebSocket connection to remove.
        """
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Sends a message to all active WebSocket connections.

        Args:
            message (str): The message to broadcast.
        """
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        """Sends a message to all active WebSocket connections.

        Args:
            message (str): The message to broadcast.
        """
        for connection in self.active_connections:
            await connection.send_text(message)

manager = WebSocketManager()

script_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(script_dir, "static")
index_html_path = os.path.join(static_dir, "index.html")

app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handles the WebSocket connection for real-time communication.

    This endpoint manages the lifecycle of a WebSocket connection. It listens
    for incoming messages and, if a message is an "approval_response", it
    puts the message onto the `approval_queue` to be processed by the
    `TwinService`. It also handles user text messages.

    Args:
        websocket (WebSocket): The client's WebSocket connection.
    """
    # Note: WebSocket authentication is trickier. For now, we leave it open as per "semi-unprotected" plan.
    # If strict auth is needed later, we would check query params during connect.
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if message.get("type") == "approval_response":
                await approval_queue.put(message)
            elif message.get("type") == "user_message":
                await text_message_queue.put(message)
    except Exception:
        manager.disconnect(websocket)


@app.post("/internal/chat", summary="Process Internal Chat Message", description="Receives a chat message from an internal service like the MoE Gateway, processes it, and sends the response to a specified callback URL.", tags=["Internal"])
async def internal_chat(payload: InternalChatRequest, api_key: str = Security(get_api_key)):
    """
    Handles a chat message from another internal service.
    The payload should contain the user's text, a unique request_id,
    and a response_url where the final agent message should be sent.
    """
    # Convert model to dict for internal processing (serialized for JSON compatibility)
    data = payload.model_dump(mode="json")
    await text_message_queue.put(data)
    return JSONResponse(status_code=202, content={"message": "Request accepted"})


@app.post("/internal/system_message", summary="Process System Alert", description="Receives a system alert (e.g., from Supervisor), injecting it into the agent's workflow.", tags=["Internal"])
async def internal_system_message(payload: SystemMessageRequest, api_key: str = Security(get_api_key)):
    """
    Handles a system alert. These are treated as high-priority inputs from the infrastructure.
    """
    data = payload.model_dump(mode="json")
    # Mark it as a system alert for special handling in TwinService
    data["is_system_alert"] = True
    await text_message_queue.put(data)
    return JSONResponse(status_code=202, content={"message": "System alert accepted"})


@app.get("/", summary="Serve Web UI", description="Serves the main `index.html` file for the web user interface.", tags=["UI"])
async def get():
    """Serves the main `index.html` file for the web UI."""
    with open(index_html_path) as f:
        return HTMLResponse(f.read())

@app.get("/workflow", summary="Serve Workflow UI", description="Serves the `workflow.html` file for the workflow visualization UI.", tags=["UI"])
async def get_workflow_ui():
    """Serves the workflow visualization UI."""
    workflow_html_path = os.path.join(static_dir, "workflow.html")
    with open(workflow_html_path) as f:
        return HTMLResponse(f.read())

@app.get("/api/status", summary="Get Agent Status", description="Retrieves the current status from the agent's Master Control Program (MCP) tool, showing active pipeline tasks.", tags=["Agent"])
async def get_status(request: Request):
    """Retrieves the current status from the agent's Master Control Program (MCP) tool."""
    twin_service = request.app.state.twin_service_instance
    if twin_service and hasattr(twin_service, 'tools'):
        mcp = twin_service.tools.get('mcp')
        if mcp and hasattr(mcp, 'runner') and mcp.runner:
            tasks = mcp.runner.get_tasks()
            if not tasks:
                return {"status": "No active pipelines."}

            status_report = "Current pipeline status:\n"
            for task in tasks:
                status_report += f"- Task {task.get_name()}: {task.get_state().value}\n"
            return {"status": status_report}
        else:
            return {"status": "MCP tool or runner not available."}
    return {"status": "Agent not fully initialized. Please wait..."}

@app.get("/health", summary="Health Check", description="Provides a health check endpoint. It returns a 200 OK if the agent is initialized and ready, otherwise a 503 Service Unavailable. This is used by Nomad for service health checks.", tags=["System"])
async def get_health(request: Request):
    """A health check endpoint that verifies the agent is fully initialized."""
    if getattr(request.app.state, "is_ready", False):
        return JSONResponse(content={"status": "ok"})
    else:
        # Return 200 OK with "initializing" status to prevent Nomad from killing the allocation
        # during long startup phases (e.g., waiting for other services).
        return JSONResponse(status_code=200, content={"status": "initializing"})

@app.get("/api/workflows/active", response_class=JSONResponse)
async def get_active_workflows():
    """Returns a snapshot of the state of all active workflows."""
    active_workflows = ActiveWorkflows()
    return active_workflows.get_all_states()

@app.get("/api/workflows/history", response_class=JSONResponse, summary="Get Workflow History", description="Retrieves a list of past workflow runs.", tags=["Workflow"])
async def get_workflow_history(limit: int = 50):
    """Retrieves a list of past workflow runs."""
    history = WorkflowHistory()
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: history.get_all_runs(limit=limit))

@app.get("/api/workflows/history/{runner_id}", response_class=JSONResponse, summary="Get Workflow Run Details", description="Retrieves the full details of a specific workflow run.", tags=["Workflow"])
async def get_workflow_run(runner_id: str):
    """Retrieves the full details of a specific workflow run."""
    history = WorkflowHistory()
    loop = asyncio.get_running_loop()
    run_details = await loop.run_in_executor(None, lambda: history.get_run(runner_id))
    if not run_details:
        raise HTTPException(status_code=404, detail="Workflow run not found.")
    return run_details

@app.post("/api/gate/approve", response_class=JSONResponse)
async def approve_gate(payload: Dict = Body(...), api_key: str = Security(get_api_key)):
    """Approves a paused gate, allowing the workflow to continue."""
    request_id = payload.get("request_id")
    if not request_id:
        raise HTTPException(status_code=400, detail="request_id is required.")

    open_gates = OpenGates()
    if open_gates.approve(request_id):
        return {"message": f"Gate for request {request_id} approved."}
    else:
        raise HTTPException(status_code=404, detail=f"No open gate found for request {request_id}.")

@app.get("/api/workflows/definition/{workflow_name}", response_class=JSONResponse)
async def get_workflow_definition(workflow_name: str):
    """Loads a workflow definition from a YAML file and returns it as JSON."""
    # Basic security to prevent directory traversal
    if ".." in workflow_name or not workflow_name.endswith((".yaml", ".yml")):
        raise HTTPException(status_code=400, detail="Invalid workflow name.")

    workflow_dir = os.path.join(script_dir, "workflows")
    abs_workflow_dir = os.path.abspath(workflow_dir)

    # Security fix: Ensure resolved path is within workflow_dir
    file_path = os.path.abspath(os.path.join(workflow_dir, workflow_name))
    if os.path.commonpath([abs_workflow_dir, file_path]) != abs_workflow_dir:
        raise HTTPException(status_code=400, detail="Invalid workflow name.")

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="Workflow not found.")

    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Error loading workflow {file_path}: {e}")
        # Security fix: Do not expose internal exception details
        raise HTTPException(status_code=500, detail="An error occurred while loading the workflow.")

@app.post("/api/workflows/save", summary="Save Workflow", description="Saves a workflow definition to a YAML file.", tags=["Workflow"])
async def save_workflow_definition(payload: Dict = Body(...), api_key: str = Security(get_api_key)):
    """
    Saves a workflow definition.
    Payload: { "name": "filename.yaml", "definition": { ... } }
    """
    workflow_name = payload.get("name")
    definition = payload.get("definition")

    if not workflow_name or not definition:
        raise HTTPException(status_code=400, detail="Name and definition are required.")

    if ".." in workflow_name or not workflow_name.endswith((".yaml", ".yml")):
        raise HTTPException(status_code=400, detail="Invalid workflow name.")

    workflow_dir = os.path.join(script_dir, "workflows")
    abs_workflow_dir = os.path.abspath(workflow_dir)
    # Ensure directory exists
    os.makedirs(workflow_dir, exist_ok=True)

    # Security fix: Ensure resolved path is within workflow_dir
    file_path = os.path.abspath(os.path.join(workflow_dir, workflow_name))
    if os.path.commonpath([abs_workflow_dir, file_path]) != abs_workflow_dir:
        raise HTTPException(status_code=400, detail="Invalid workflow name.")

    # Optional: Versioning
    # If file exists, maybe backup? For now, we overwrite as per "Live Edit" requirement,
    # but the frontend can handle "Save As" logic or we can add timestamp here.
    # The user asked for "history versions", which usually implies the Run History.
    # But for "rollback", let's create a backup if it exists.
    if os.path.exists(file_path):
        backup_name = f"{workflow_name}.{int(time.time())}.bak"
        backup_path = os.path.join(workflow_dir, backup_name)
        try:
            os.rename(file_path, backup_path)
            logging.info(f"Backed up existing workflow to {backup_name}")
        except OSError as e:
            logging.warning(f"Failed to backup workflow: {e}")

    try:
        with open(file_path, 'w') as f:
            yaml.dump(definition, f, default_flow_style=False, sort_keys=False)
        return {"message": f"Workflow {workflow_name} saved successfully."}
    except Exception as e:
        logging.error(f"Error saving workflow {file_path}: {e}")
        # Security fix: Do not expose internal exception details
        raise HTTPException(status_code=500, detail="An error occurred while saving the workflow.")

@app.get("/api/web_uis")
async def get_web_uis():
    """
    Discovers web UIs from Consul.
    It explicitly adds Consul and Nomad, and then discovers other services
    that have an HTTP health check registered.
    Uses caching to reduce load on Consul.
    """
    cached_uis = await service_cache.get()
    if cached_uis is not None:
        return JSONResponse(content=cached_uis)

    web_uis = []
    consul_url = "http://127.0.0.1:8500"

    try:
        # Use the reusable client instead of creating a new one every time
        client = service_discovery_client

        # 1. Add Consul UI
        # We assume Consul itself is healthy if we can talk to it
        web_uis.append({"name": "Consul", "url": f"{consul_url}/ui", "status": "healthy"})

        # 2. Add Nomad UI
        try:
            nomad_service_response = await client.get(f"{consul_url}/v1/catalog/service/nomad")
            nomad_service_response.raise_for_status()
            nomad_services = nomad_service_response.json()
            if nomad_services:
                nomad_address = nomad_services[0].get("ServiceAddress") or nomad_services[0].get("Address")
                # Check Nomad health via Consul
                nomad_health_resp = await client.get(f"{consul_url}/v1/health/service/nomad?passing")
                nomad_status = "healthy" if nomad_health_resp.status_code == 200 and nomad_health_resp.json() else "unhealthy"
                web_uis.append({"name": "Nomad", "url": f"http://{nomad_address}:4646", "status": nomad_status})
        except Exception:
            web_uis.append({"name": "Nomad", "url": "#", "status": "unhealthy"})


        # 3. Discover other HTTP services
        services_response = await client.get(f"{consul_url}/v1/catalog/services")
        services_response.raise_for_status()
        all_services = services_response.json()

        async def check_service(service_name):
            if service_name in ["nomad", "consul"] or "pipecat" in service_name:
                return None

            try:
                # Removed ?passing to get all services including unhealthy ones
                health_response = await client.get(f"{consul_url}/v1/health/service/{service_name}")
                if health_response.status_code != 200:
                    return None

                service_instances = health_response.json()
                if not service_instances:
                    return None

                # Logic to determine if it is a web UI and its status
                ui_candidate = None
                is_healthy = False

                for instance in service_instances:
                    checks = instance.get("Checks", [])

                    # Check for HTTP check presence (loose check for "http" in Type)
                    has_http = any("http" in check.get("Type", "").lower() for check in checks)

                    if has_http:
                        # Capture address/port
                        service_info = instance.get("Service", {})
                        address = service_info.get("Address") or instance.get("Node", {}).get("Address")
                        port = service_info.get("Port")

                        if address and port:
                            candidate_url = f"http://{address}:{port}"

                            # Check health of this specific instance
                            instance_passing = all(check.get("Status") == "passing" for check in checks)

                            if instance_passing:
                                is_healthy = True
                                ui_candidate = candidate_url
                                break # Found a healthy instance
                            else:
                                # Unhealthy, store candidate but keep looking for a healthy one
                                if not ui_candidate:
                                    ui_candidate = candidate_url

                if ui_candidate:
                     return {"name": service_name, "url": ui_candidate, "status": "healthy" if is_healthy else "unhealthy"}

            except Exception:
                # Ignore failures for individual services so we don't break the whole list
                pass
            return None

        # Fetch all service health checks in parallel
        tasks = [check_service(name) for name in all_services.keys()]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result:
                web_uis.append(result)

    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        print(f"Could not connect to Consul to discover UIs: {e}")
        return JSONResponse(
            status_code=503,
            content=[
                {"name": "Consul (Not Reachable)", "url": "#", "status": "unhealthy"},
                {"name": "Nomad (Not Reachable)", "url": "#", "status": "unhealthy"},
            ]
        )

    # Dictionary deduplication logic needs to handle 'status' now.
    # We prefer 'healthy' if there are duplicates (unlikely with current logic but good practice)
    # Actually current logic returns max 1 entry per service name from check_service.
    # But Consul/Nomad are separate.
    unique_uis = [dict(t) for t in {tuple(d.items()) for d in web_uis}]
    sorted_uis = sorted(unique_uis, key=lambda x: x['name'])

    await service_cache.set(sorted_uis)
    return JSONResponse(content=sorted_uis)

@app.post("/api/state/save", summary="Save Agent State", description="Saves the agent's current conversation and internal state to a named snapshot.", tags=["Agent"])
async def save_state_endpoint(request: Request, payload: Dict = Body(..., examples=[{"save_name": "my_snapshot"}]), api_key: str = Security(get_api_key)):
    """API endpoint to save the agent's current state to a named snapshot.

    Args:
        payload (Dict): The request body, expected to contain a "save_name" key.

    Returns:
        JSONResponse: A message indicating success or failure.
    """
    save_name = payload.get("save_name")
    if not save_name:
        return JSONResponse(status_code=400, content={"message": "save_name is required"})

    # Security Fix: Input validation to prevent path traversal
    if ".." in save_name or "/" in save_name or "\\" in save_name:
        return JSONResponse(status_code=400, content={"message": "Invalid save_name. Must be a filename without path characters."})

    twin_service = request.app.state.twin_service_instance
    if twin_service:
        result = twin_service.save_state(save_name)
        return {"message": result}
    return JSONResponse(status_code=503, content={"message": "Agent not fully initialized."})

@app.post("/api/state/load", summary="Load Agent State", description="Loads the agent's state from a previously saved snapshot.", tags=["Agent"])
async def load_state_endpoint(request: Request, payload: Dict = Body(..., examples=[{"save_name": "my_snapshot"}]), api_key: str = Security(get_api_key)):
    """API endpoint to load the agent's state from a named snapshot.

    Args:
        payload (Dict): The request body, a JSON object with a "save_name" key.

    Returns:
        JSONResponse: A message indicating success or failure.
    """
    save_name = payload.get("save_name")
    if not save_name:
        return JSONResponse(status_code=400, content={"message": "save_name is required"})

    # Security Fix: Input validation to prevent path traversal
    if ".." in save_name or "/" in save_name or "\\" in save_name:
        return JSONResponse(status_code=400, content={"message": "Invalid save_name. Must be a filename without path characters."})

    twin_service = request.app.state.twin_service_instance
    if twin_service:
        result = twin_service.load_state(save_name)
        return {"message": result}
    return JSONResponse(status_code=503, content={"message": "Agent not fully initialized."})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)