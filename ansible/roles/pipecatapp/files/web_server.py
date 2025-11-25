import os
import json
import asyncio
import logging
import requests
from fastapi import FastAPI, WebSocket, Body, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Dict
from workflow.runner import ActiveWorkflows


# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Pipecat Agent API",
    description="This API exposes endpoints to interact with the Pipecat agent, including real-time communication, status checks, and state management.",
    version="1.0.0",
)

# Create queues to communicate between the web server and the TwinService
approval_queue = asyncio.Queue()
text_message_queue = asyncio.Queue()

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
async def internal_chat(payload: Dict = Body(...)):
    """
    Handles a chat message from another internal service.
    The payload should contain the user's text, a unique request_id,
    and a response_url where the final agent message should be sent.
    """
    await text_message_queue.put(payload)
    return JSONResponse(status_code=202, content={"message": "Request accepted"})


@app.get("/", summary="Serve Web UI", description="Serves the main `index.html` file for the web user interface.", tags=["UI"])
async def get():
    """Serves the main `index.html` file for the web UI."""
    with open(index_html_path) as f:
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
        return JSONResponse(status_code=503, content={"status": "initializing"})

@app.get("/api/workflows/active", response_class=JSONResponse)
async def get_active_workflows():
    """Returns a snapshot of the state of all active workflows."""
    active_workflows = ActiveWorkflows()
    return active_workflows.get_all_states()

@app.get("/api/web_uis")
async def get_web_uis():
    """
    Discovers web UIs from Consul.
    It explicitly adds Consul and Nomad, and then discovers other services
    that have an HTTP health check registered.
    """
    web_uis = []
    consul_url = "http://127.0.0.1:8500"

    try:
        # 1. Add Consul UI
        web_uis.append({"name": "Consul", "url": f"{consul_url}/ui"})

        # 2. Add Nomad UI
        nomad_service_response = requests.get(f"{consul_url}/v1/catalog/service/nomad")
        nomad_service_response.raise_for_status()
        nomad_services = nomad_service_response.json()
        if nomad_services:
            nomad_address = nomad_services[0].get("ServiceAddress") or nomad_services[0].get("Address")
            web_uis.append({"name": "Nomad", "url": f"http://{nomad_address}:4646"})

        # 3. Discover other HTTP services
        services_response = requests.get(f"{consul_url}/v1/catalog/services")
        services_response.raise_for_status()
        all_services = services_response.json()

        for service_name in all_services.keys():
            if service_name in ["nomad", "consul"] or "pipecat" in service_name:
                continue

            health_response = requests.get(f"{consul_url}/v1/health/service/{service_name}?passing")
            if health_response.status_code != 200:
                continue

            service_instances = health_response.json()
            if not service_instances:
                continue

            has_http_check = any(
                "http" in check.get("Type", "") and check.get("Status") == "passing"
                for instance in service_instances
                for check in instance.get("Checks", [])
            )

            if has_http_check:
                instance = service_instances[0]
                service_info = instance.get("Service", {})
                address = service_info.get("Address") or instance.get("Node", {}).get("Address")
                port = service_info.get("Port")
                if address and port:
                    web_uis.append({"name": service_name, "url": f"http://{address}:{port}"})

    except requests.RequestException as e:
        print(f"Could not connect to Consul to discover UIs: {e}")
        return JSONResponse(
            status_code=503,
            content=[
                {"name": "Consul (Not Reachable)", "url": "#"},
                {"name": "Nomad (Not Reachable)", "url": "#"},
            ]
        )

    unique_uis = [dict(t) for t in {tuple(d.items()) for d in web_uis}]
    sorted_uis = sorted(unique_uis, key=lambda x: x['name'])

    return JSONResponse(content=sorted_uis)

@app.post("/api/state/save", summary="Save Agent State", description="Saves the agent's current conversation and internal state to a named snapshot.", tags=["Agent"])
async def save_state_endpoint(request: Request, payload: Dict = Body(..., examples=[{"save_name": "my_snapshot"}])):
    """API endpoint to save the agent's current state to a named snapshot.

    Args:
        payload (Dict): The request body, expected to contain a "save_name" key.

    Returns:
        JSONResponse: A message indicating success or failure.
    """
    save_name = payload.get("save_name")
    if not save_name:
        return JSONResponse(status_code=400, content={"message": "save_name is required"})

    twin_service = request.app.state.twin_service_instance
    if twin_service:
        result = twin_service.save_state(save_name)
        return {"message": result}
    return JSONResponse(status_code=503, content={"message": "Agent not fully initialized."})

@app.post("/api/state/load", summary="Load Agent State", description="Loads the agent's state from a previously saved snapshot.", tags=["Agent"])
async def load_state_endpoint(request: Request, payload: Dict = Body(..., examples=[{"save_name": "my_snapshot"}])):
    """API endpoint to load the agent's state from a named snapshot.

    Args:
        payload (Dict): The request body, a JSON object with a "save_name" key.

    Returns:
        JSONResponse: A message indicating success or failure.
    """
    save_name = payload.get("save_name")
    if not save_name:
        return JSONResponse(status_code=400, content={"message": "save_name is required"})

    twin_service = request.app.state.twin_service_instance
    if twin_service:
        result = twin_service.load_state(save_name)
        return {"message": result}
    return JSONResponse(status_code=503, content={"message": "Agent not fully initialized."})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)