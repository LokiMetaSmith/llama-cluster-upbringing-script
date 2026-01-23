import os
import logging
import sqlite3
import json
import asyncio
from typing import Dict, Any, List, Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, Body
from fastapi.responses import JSONResponse

# Import the original MCP server
# We need to import both the app and the lifespan function to manually manage it
mcp_app = None
mcp_lifespan_func = None

try:
    from mcp_server import app as _mcp_app, lifespan as _mcp_lifespan
    mcp_app = _mcp_app
    mcp_lifespan_func = _mcp_lifespan
except ImportError:
    try:
        # Try relative import for package context
        from .mcp_server import app as _mcp_app, lifespan as _mcp_lifespan
        mcp_app = _mcp_app
        mcp_lifespan_func = _mcp_lifespan
    except ImportError:
        logging.warning("Could not import mcp_server. MCP functionality will be disabled.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("event-bus")

EVENTS_DB_PATH = os.getenv("EVENTS_DB_PATH", "/data/events.db")

def init_db():
    conn = sqlite3.connect(EVENTS_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT,
            kind TEXT,
            content TEXT,
            meta TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log_event(task_id, kind, content, meta):
    conn = sqlite3.connect(EVENTS_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (task_id, kind, content, meta)
        VALUES (?, ?, ?, ?)
    """, (task_id, kind, content, json.dumps(meta)))
    conn.commit()
    conn.close()

def get_events(limit=50):
    conn = sqlite3.connect(EVENTS_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM events ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_task_events(task_id):
    conn = sqlite3.connect(EVENTS_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM events WHERE task_id = ? ORDER BY id ASC
    """, (task_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize our DB
    logger.info(f"Initializing Event Bus DB at {EVENTS_DB_PATH}")
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, init_db)

    # Initialize MCP Server lifespan if available
    # This ensures the memory graph DB connection is opened
    if mcp_app and mcp_lifespan_func:
        logger.info("Initializing MCP Server lifespan (Memory Graph connection)")
        async with mcp_lifespan_func(mcp_app):
            yield
    else:
        yield

    logger.info("Event Bus shutting down")

app = FastAPI(title="Pipecat Event Bus & Memory Service", lifespan=lifespan)

# Mount the MCP app
if mcp_app:
    # We mount at /mcp to avoid conflict with /events
    app.mount("/mcp", mcp_app)
    logger.info("Mounted MCP server at /mcp")

@app.post("/events")
async def post_event(request: Request):
    try:
        data = await request.json()

        # Robust extraction
        meta = data.get("meta", {})
        if not isinstance(meta, dict):
            meta = {}

        task_id = meta.get("task_id") or data.get("task_id", "unknown")
        kind = data.get("kind", "unknown")
        content = data.get("content", "")

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, log_event, task_id, kind, content, meta)

        return {"status": "ok", "message": "Event recorded"}
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events")
async def read_events(limit: int = 50):
    loop = asyncio.get_running_loop()
    events = await loop.run_in_executor(None, get_events, limit)
    return events

@app.get("/tasks/{task_id}")
async def read_task_events(task_id: str):
    loop = asyncio.get_running_loop()
    events = await loop.run_in_executor(None, get_task_events, task_id)
    return events

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
