from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from pmm_memory import PMMMemory
import os
import uvicorn

app = FastAPI()

# Initialize PMMMemory with a persistent path
# In Nomad, this should be a mounted volume
DB_PATH = os.getenv("MEMORY_DB_PATH", "/data/pmm_memory.db")
memory = PMMMemory(db_path=DB_PATH)

class Event(BaseModel):
    kind: str
    content: str
    meta: Optional[Dict[str, Any]] = None

@app.post("/events")
async def add_event(event: Event):
    try:
        memory.add_event(event.kind, event.content, event.meta)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events")
async def get_events(kind: Optional[str] = None, limit: int = 10):
    try:
        events = memory.get_events(kind, limit)
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
