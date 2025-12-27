import os
import aiohttp
from .mcp_tool import MCP_Tool

class ArchivistTool(MCP_Tool):
    """
    A tool that interacts with the Archivist service to perform deep research
    on the agent's long-term memory (historical events).
    """
    def __init__(self, archivist_url="http://localhost:8008"):
        # We don't need twin_service/runner for this simple tool usually,
        # but MCP_Tool might expect them. However, since we are just wrapping an API call,
        # we can define a minimal tool.
        # Actually, inheriting from MCP_Tool implies we use the generic MCP protocol.
        # But here we are building a specific client tool.
        # Let's just make it a standard tool class that fits the Agent's tool interface.
        self.name = "archivist"
        self.description = (
            "Access the agent's episodic memory and history. "
            "Use this to answer questions about past events, conversations, or actions "
            "that are not in the current context. "
            "The tool performs a 'Deep Research' process to find relevant information."
        )
        self.archivist_url = archivist_url

    async def run(self, query: str) -> str:
        """
        Queries the Archivist service.

        Args:
            query (str): The question or topic to research in memory.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.archivist_url}/research",
                    json={"query": query, "max_steps": 5} # Default steps
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("content", "No content returned.")
                    else:
                        error_text = await resp.text()
                        return f"Error querying Archivist: {resp.status} - {error_text}"
        except Exception as e:
            return f"Failed to connect to Archivist service: {e}"

    # Compatibility with sync tool execution if needed (the agent runner handles async)
    def __call__(self, query: str):
        # We assume the caller handles the loop or we are in a thread where we can run new loop.
        # But safest is to just point to run and expect caller to await.
        return self.run(query)
