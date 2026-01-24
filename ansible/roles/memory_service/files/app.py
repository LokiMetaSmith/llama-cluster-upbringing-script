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

# Gas Town Work Item Models
class WorkItemCreate(BaseModel):
    title: str
    created_by: str
    assignee_id: Optional[str] = None
    parent_id: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

class WorkItemUpdate(BaseModel):
    status: Optional[str] = None
    assignee_id: Optional[str] = None
    validation_results: Optional[Dict[str, Any]] = None
    meta_update: Optional[Dict[str, Any]] = None

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

# Gas Town Work Item Endpoints
@app.post("/work_items")
async def create_work_item(item: WorkItemCreate):
    try:
        item_id = await memory.create_work_item(
            title=item.title,
            created_by=item.created_by,
            assignee_id=item.assignee_id,
            parent_id=item.parent_id,
            meta=item.meta
        )
        return {"status": "success", "work_item_id": item_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/work_items")
async def list_work_items(status: Optional[str] = None, assignee_id: Optional[str] = None, limit: int = 50):
    try:
        items = await memory.list_work_items(status, assignee_id, limit)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/work_items/{item_id}")
async def get_work_item(item_id: str):
    try:
        item = await memory.get_work_item(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Work item not found")
        return item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/work_items/{item_id}")
async def update_work_item(item_id: str, update: WorkItemUpdate):
    try:
        success = await memory.update_work_item(
            item_id=item_id,
            status=update.status,
            assignee_id=update.assignee_id,
            validation_results=update.validation_results,
            meta_update=update.meta_update
        )
        if not success:
             raise HTTPException(status_code=404, detail="Work item not found")
        return {"status": "success"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
