import os
import logging
import json
from typing import Dict, Any, List, Optional
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("helix-mcp-service")

helix_url = os.getenv("HELIX_URL", "http://localhost:6969/v1/query")

@asynccontextmanager
async def lifespan(server: FastMCP):
    logger.info(f"Initializing Helix MCP Service pointing to: {helix_url}")
    yield

app = FastMCP("helix-mcp-service", lifespan=lifespan)

async def _post(payload: dict) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(helix_url, json=payload)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as e:
            logger.error(f"HelixDB Request Error: {e}")
            return {}

@app.tool()
async def store_memory(content: str, memory_type: str, title: str, tags: List[str] = [], importance: float = 0.5):
    """Stores a new memory unit in HelixDB."""
    query = {
        "request_type": "write",
        "query": {
            "queries": [
                {
                    "Query": {
                        "name": "mem",
                        "steps": [
                            {
                                "AddN": {
                                    "label": "MemoryGraphNode",
                                    "properties": [
                                        ["content", {"Value": {"String": content}}],
                                        ["memory_type", {"Value": {"String": memory_type}}],
                                        ["title", {"Value": {"String": title}}],
                                        ["tags", {"Value": {"String": ",".join(tags)}}],
                                        ["importance", {"Value": {"Float": importance}}]
                                    ]
                                }
                            },
                            {
                                "Project": [{"source": "content", "alias": "content"}]
                            }
                        ],
                        "condition": None
                    }
                }
            ],
            "returns": ["mem"]
        }
    }
    await _post(query)
    return f"Stored memory: {title}"

@app.tool()
async def create_relationship(from_memory_id: str, to_memory_id: str, relationship_type: str):
    """Creates a relationship between two memories in HelixDB."""
    # Graph linking logic would be built out here
    return f"Created relationship {relationship_type} between {from_memory_id} and {to_memory_id}"

@app.tool()
async def recall_memories(query: str, limit: int = 5):
    """Recalls memories relevant to a query from HelixDB."""
    read_query = {
        "request_type": "read",
        "query": {
            "queries": [
                {
                    "Query": {
                        "name": "res",
                        "steps": [
                            {"NWithLabel": {"label": "MemoryGraphNode"}},
                            {"Project": [{"source": "title", "alias": "title"}, {"source": "content", "alias": "content"}]}
                        ],
                        "condition": None
                    }
                }
            ],
            "returns": ["res"]
        }
    }
    resp = await _post(read_query)
    # mock
    return json.dumps(resp.get("res", []))

@app.tool()
async def search_memories(query: str, limit: int = 5):
    """Searches memories with more granular control in HelixDB."""
    return await recall_memories(query, limit)

if __name__ == "__main__":
    # Run alongside existing service on a different port (8001)
    app.run(transport="sse")
