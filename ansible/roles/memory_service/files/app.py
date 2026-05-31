from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from pmm_memory import PMMMemory
import os
import uvicorn

app = FastAPI()

import asyncio
import httpx
import logging

logger = logging.getLogger(__name__)


async def background_sync_task():
    """Periodically syncs work items with remote ledgers."""
    remote_ledgers_env = os.getenv("REMOTE_LEDGERS", "")
    if not remote_ledgers_env:
        return

    remote_urls = [url.strip() for url in remote_ledgers_env.split(",") if url.strip()]
    if not remote_urls:
        return

    logger.info(f"Starting background sync task with remote ledgers: {remote_urls}")
    last_local_sync_time = 0.0
    remote_sync_times = {url: 0.0 for url in remote_urls}

    while True:
        try:
            # 1. Get local items updated since last sync to push out
            local_items = await memory.get_work_items_since(last_local_sync_time)

            if local_items:
                last_local_sync_time = max(item['updated_at'] for item in local_items)

            for remote_url in remote_urls:
                # 2. Push local updates to remote
                if local_items:
                    try:
                        async with httpx.AsyncClient() as client:
                            resp = await client.post(f"{remote_url}/work_items/sync", json=local_items)
                            resp.raise_for_status()
                    except Exception as e:
                        logger.error(f"Failed to push to {remote_url}: {e}")

                # 3. Pull remote updates
                try:
                    async with httpx.AsyncClient() as client:
                        resp = await client.get(f"{remote_url}/work_items/sync", params={"since": remote_sync_times[remote_url]})
                        resp.raise_for_status()
                        remote_items = resp.json()
                        if remote_items:
                            await memory.sync_work_items(remote_items)
                            remote_sync_times[remote_url] = max(item['updated_at'] for item in remote_items)
                            # Also update last_local_sync_time so we don't push these back immediately
                            # (though pushing back is idempotent if timestamps match, it saves bandwidth)
                            last_local_sync_time = max(last_local_sync_time, remote_sync_times[remote_url])
                except Exception as e:
                    logger.error(f"Failed to pull from {remote_url}: {e}")

        except Exception as e:
            logger.error(f"Error in background sync task: {e}")

        await asyncio.sleep(30) # Sync every 30 seconds

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_sync_task())



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

# DLQ Models
class DLQItemCreate(BaseModel):
    event_type: str
    payload: Dict[str, Any]
    error_reason: str
    retry_count: Optional[int] = 0

class DLQClaimRequest(BaseModel):
    worker_id: str
    supported_types: Optional[List[str]] = None

class DLQItemUpdate(BaseModel):
    status: str
    result: Optional[str] = None
    retry_after: Optional[float] = None
    increment_retry: Optional[bool] = False

@app.post("/events")
async def add_event(event: Event):
    try:
        await memory.add_event(event.kind, event.content, event.meta)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events")
async def get_events(kind: Optional[str] = None, limit: int = 10):
    try:
        events = await memory.get_events(kind, limit)
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


@app.get("/work_items/sync")
async def get_work_items_sync(since: float = 0.0):
    try:
        items = await memory.get_work_items_since(since)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/work_items/sync")
async def post_work_items_sync(items: List[Dict[str, Any]]):
    try:
        merged = await memory.sync_work_items(items)
        return {"status": "success", "merged_count": len(merged)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/{agent_id}/stats")
async def get_agent_stats(agent_id: str):
    try:
        stats = await memory.get_agent_stats(agent_id)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DLQ Endpoints
@app.post("/dlq")
async def enqueue_dlq(item: DLQItemCreate):
    try:
        item_id = await memory.enqueue_dlq_item(
            event_type=item.event_type,
            payload=item.payload,
            error_reason=item.error_reason,
            retry_count=item.retry_count
        )
        return {"status": "success", "dlq_item_id": item_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/dlq/claim")
async def claim_dlq_item(request: DLQClaimRequest):
    try:
        item = await memory.claim_dlq_item(
            worker_id=request.worker_id,
            supported_types=request.supported_types
        )
        # If no item is found, return None (JSON null)
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/dlq/{item_id}")
async def update_dlq_item(item_id: str, update: DLQItemUpdate):
    try:
        success = await memory.update_dlq_item(
            item_id=item_id,
            status=update.status,
            result=update.result,
            retry_after=update.retry_after,
            increment_retry=update.increment_retry
        )
        if not success:
             raise HTTPException(status_code=404, detail="DLQ item not found")
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
