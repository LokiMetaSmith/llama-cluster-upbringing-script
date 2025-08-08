from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from typing import List
import asyncio

app = FastAPI()

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
            # We are not expecting messages from the client, just broadcasting to it.
            # This loop keeps the connection open.
            await asyncio.sleep(1)
    except Exception:
        manager.disconnect(websocket)

from fastapi.staticfiles import StaticFiles

# This will be set by the main application
twin_service_instance = None

app.mount("/static", StaticFiles(directory="ansible/roles/pipecatapp/files/static"), name="static")

@app.get("/")
async def get():
    with open("ansible/roles/pipecatapp/files/static/index.html") as f:
        return HTMLResponse(f.read())

@app.get("/api/status")
async def get_status():
    if twin_service_instance and hasattr(twin_service_instance, 'tools'):
        mcp = twin_service_instance.tools.get('mcp')
        if mcp:
            return {"status": mcp.get_status()}
    return {"status": "Agent not fully initialized."}

# We will need a way to get the server to run.
# This will be handled in the main app.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
