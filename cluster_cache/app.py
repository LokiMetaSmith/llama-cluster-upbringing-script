from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Cluster Cache",
    description="A GWebCache-style stateless bootstrap cache for dynamic node discovery",
    version="1.0.0"
)

# In-memory store of active nodes
# Mapping of IP address to last seen timestamp
active_nodes = {}

# Expiration time for nodes (in seconds)
NODE_TTL = 300  # 5 minutes

class NodeRegistration(BaseModel):
    ip_address: Optional[str] = None

class NodeList(BaseModel):
    nodes: List[str]

def cleanup_expired_nodes():
    """Removes nodes that haven't been seen within the TTL."""
    current_time = time.time()
    expired = [ip for ip, last_seen in active_nodes.items() if current_time - last_seen > NODE_TTL]
    for ip in expired:
        logger.info(f"Removing expired node from cache: {ip}")
        del active_nodes[ip]

@app.post("/register", summary="Register or update a node's active status")
async def register_node(request: Request, node: NodeRegistration = None):
    """
    Register a node to the cluster cache.
    If no IP is provided in the body, the client's IP from the request is used.
    """
    ip_address = None
    if node and node.ip_address:
        ip_address = node.ip_address
    else:
        ip_address = request.client.host

    if not ip_address:
        raise HTTPException(status_code=400, detail="Could not determine IP address")

    active_nodes[ip_address] = time.time()
    logger.info(f"Registered node: {ip_address}")

    # Cleanup on registration to keep the list fresh
    cleanup_expired_nodes()

    return {"status": "success", "ip_address": ip_address}

@app.get("/nodes", response_model=NodeList, summary="Get active nodes")
async def get_nodes():
    """
    Retrieve the list of currently active nodes.
    """
    cleanup_expired_nodes()
    return {"nodes": list(active_nodes.keys())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
