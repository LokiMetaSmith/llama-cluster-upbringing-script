import os
import logging
from typing import Dict, Any, List, Optional
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP
from memorygraph.server import SQLiteMemoryDatabase, SQLiteFallbackBackend
import memorygraph.tools as tools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("memory-graph-service")

# Global DB instance
db = None

@asynccontextmanager
async def lifespan(server: FastMCP):
    global db
    db_path = os.getenv("MEMORY_DB_PATH", "/data/memory_graph.db")
    logger.info(f"Initializing MemoryGraph with DB: {db_path}")

    # Initialize backend and DB
    # Based on inspection: SQLiteFallbackBackend(db_path)
    backend = SQLiteFallbackBackend(db_path)
    await backend.connect()
    await backend.initialize_schema()

    # Based on inspection: SQLiteMemoryDatabase(backend)
    db = SQLiteMemoryDatabase(backend)
    # The official server calls initialize_schema on DB too
    await db.initialize_schema()

    yield

    # Cleanup
    if backend:
        await backend.disconnect()

# Initialize FastMCP server with lifespan
app = FastMCP("memory-graph-service", lifespan=lifespan)

# Tool Wrappers
# The handlers expect (db, arguments_dict) and return CallToolResult
# We need to expose them as FastMCP tools with typed arguments for the client to see schema.

@app.tool()
async def store_memory(content: str, memory_type: str, title: str, tags: List[str] = [], importance: float = 0.5):
    """Stores a new memory unit."""
    args = {
        "content": content,
        "memory_type": memory_type,
        "title": title,
        "tags": tags,
        "importance": importance
    }
    result = await tools.handle_store_memory(db, args)
    # result is CallToolResult, we should return the content text
    return result.content[0].text

@app.tool()
async def create_relationship(from_memory_id: str, to_memory_id: str, relationship_type: str):
    """Creates a relationship between two memories."""
    args = {
        "from_memory_id": from_memory_id,
        "to_memory_id": to_memory_id,
        "relationship_type": relationship_type
    }
    result = await tools.handle_create_relationship(db, args)
    return result.content[0].text

@app.tool()
async def recall_memories(query: str, limit: int = 5):
    """Recalls memories relevant to a query."""
    args = {
        "query": query,
        "limit": limit
    }
    result = await tools.handle_recall_memories(db, args)
    return result.content[0].text

@app.tool()
async def search_memories(query: str, limit: int = 5):
    """Searches memories with more granular control."""
    args = {
        "query": query,
        "limit": limit
    }
    result = await tools.handle_search_memories(db, args)
    return result.content[0].text

if __name__ == "__main__":
    app.run(transport="sse")
