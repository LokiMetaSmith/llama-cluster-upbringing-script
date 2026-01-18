import os
from mcp.server.fastmcp import FastMCP
from memory_graph.graph_store import MemoryGraph

# Initialize FastMCP server
# We name it 'app' so that uvicorn finds it easily (uvicorn server:app)
app = FastMCP("memory-graph-service")

# Initialize the Graph Store (Persisted to volume)
# Ensure this path is mounted in Nomad
DB_PATH = os.getenv("MEMORY_DB_PATH", "/data/memory_graph.db")
graph = MemoryGraph(db_path=DB_PATH)

@app.tool()
async def store_relation(source: str, relation: str, target: str, context: str = ""):
    """Stores a relationship: e.g., 'LoginService' 'DEPENDS_ON' 'UserTable'"""
    return graph.add_relation(source, relation, target, context)

@app.tool()
async def search_related(entity: str, hops: int = 1):
    """Finds all entities related to the given entity."""
    return graph.search(entity, depth=hops)

if __name__ == "__main__":
    # FastMCP handles the SSE/Starlette serving automatically
    app.run(transport="sse")
