from fastapi import FastAPI, WebSocket, Body
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List, Dict
import asyncio
from asyncio import Queue
import json

app = FastAPI()

# Create queues to communicate between the web server and the TwinService
approval_queue = Queue()
text_message_queue = Queue()

class ConnectionManager:
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

    async def broadcast(self, message: str):
        """Sends a message to all active WebSocket connections.

        Args:
            message (str): The message to broadcast.
        """
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handles the WebSocket connection for real-time communication.

    This endpoint manages the lifecycle of a WebSocket connection. It listens
    for incoming messages and, if a message is an "approval_response", it
    puts the message onto the `approval_queue` to be processed by the
    `TwinService`.

    Args:
        websocket (WebSocket): The client's WebSocket connection.
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Assuming the data is JSON
            message = json.loads(data)
            if message.get("type") == "approval_response":
                await approval_queue.put(message)
            elif message.get("type") == "user_message":
                await text_message_queue.put(message)
    except Exception:
        manager.disconnect(websocket)

import os
from fastapi.staticfiles import StaticFiles

# This will be set by the main application
twin_service_instance = None

# Get the absolute path to the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(script_dir, "static")
index_html_path = os.path.join(static_dir, "index.html")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def get():
    """Serves the main `index.html` file for the web UI."""
    with open(index_html_path) as f:
        return HTMLResponse(f.read())

@app.get("/api/status")
async def get_status():
    """Retrieves the current status from the agent's Master Control Program (MCP) tool."""
    if twin_service_instance and hasattr(twin_service_instance, 'tools'):
        mcp = twin_service_instance.tools.get('mcp')
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

@app.get("/health")
async def get_health():
    """A simple health check endpoint that returns a 200 OK status."""
    return {"status": "ok"}

@app.post("/api/state/save")
async def save_state_endpoint(payload: Dict = Body(...)):
    """API endpoint to save the agent's current state to a named snapshot.

    Args:
        payload (Dict): The request body, expected to contain a "save_name" key.

    Returns:
        JSONResponse: A message indicating success or failure.
    """
    save_name = payload.get("save_name")
    if not save_name:
        return JSONResponse(status_code=400, content={"message": "save_name is required"})
    if twin_service_instance:
        result = twin_service_instance.save_state(save_name)
        return {"message": result}
    return JSONResponse(status_code=503, content={"message": "Agent not fully initialized."})

@app.post("/api/state/load")
async def load_state_endpoint(payload: Dict = Body(...)):
    """API endpoint to load the agent's state from a named snapshot.

    Args:
        payload (Dict): The request body, expected to contain a "save_name" key.

    Returns:
        JSONResponse: A message indicating success or failure.
    """
    save_name = payload.get("save_name")
    if not save_name:
        return JSONResponse(status_code=400, content={"message": "save_name is required"})
    if twin_service_instance:
        result = twin_service_instance.load_state(save_name)
        return {"message": result}
    return JSONResponse(status_code=503, content={"message": "Agent not fully initialized."})

# We will need a way to get the server to run.
# This will be handled in the main app.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)