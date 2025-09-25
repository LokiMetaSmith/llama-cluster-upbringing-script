from fastapi import FastAPI, WebSocket, Body
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List, Dict
import asyncio
from asyncio import Queue
import json

app = FastAPI()

# Create a queue to communicate between the web server and the TwinService
approval_queue = Queue()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Assuming the data is JSON
            message = json.loads(data)
            if message.get("type") == "approval_response":
                await approval_queue.put(message)
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
    with open(index_html_path) as f:
        return HTMLResponse(f.read())

@app.get("/api/status")
async def get_status():
    if twin_service_instance and hasattr(twin_service_instance, 'tools'):
        mcp = twin_service_instance.tools.get('mcp')
        if mcp:
            return {"status": mcp.get_status()}
    return {"status": "Agent not fully initialized."}

@app.get("/health")
async def get_health():
    """A simple health check endpoint that returns a 200 OK status."""
    return {"status": "ok"}

@app.post("/api/state/save")
async def save_state_endpoint(payload: Dict = Body(...)):
    save_name = payload.get("save_name")
    if not save_name:
        return JSONResponse(status_code=400, content={"message": "save_name is required"})
    if twin_service_instance:
        result = twin_service_instance.save_state(save_name)
        return {"message": result}
    return JSONResponse(status_code=503, content={"message": "Agent not fully initialized."})

@app.post("/api/state/load")
async def load_state_endpoint(payload: Dict = Body(...)):
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
