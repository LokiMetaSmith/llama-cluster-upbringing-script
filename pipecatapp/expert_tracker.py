import time
import threading
import asyncio
import logging

try:
    from mcp import ClientSession
    from mcp.client.sse import sse_client
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

logger = logging.getLogger(__name__)

class ExpertTracker:
    """A thread-safe class to track performance and health metrics for LLM experts.

    This class maintains a record for each expert, tracking its type, health,
    and performance metrics like latency and success/failure rates. This data
    is used by the coordinator LLM to make intelligent routing decisions.

    It also supports integration with a Memory Graph via MCP to track relationships
    and dependencies.

    Attributes:
        experts (dict): A dictionary to store the state of each expert.
        lock (threading.Lock): A lock to ensure thread-safe updates to the experts dict.
        memory_url (str): The URL of the memory-graph service SSE endpoint.
    """
    def __init__(self, memory_url: str = "http://memory-graph.service.consul:8000/sse"):
        """Initializes the ExpertTracker."""
        self.experts = {}
        self.lock = threading.Lock()
        self.memory_url = memory_url

    def register_expert(self, name: str, expert_type: str):
        """Registers a new expert to be tracked.

        Args:
            name (str): The unique name of the expert.
            expert_type (str): The type of the expert ('local' or 'external').
        """
        with self.lock:
            if name not in self.experts:
                self.experts[name] = {
                    "type": expert_type,
                    "health": "unknown",
                    "success_count": 0,
                    "failure_count": 0,
                    "total_latency": 0.0,
                    "average_latency": 0.0,
                    "last_seen": 0,
                }

    def record_success(self, name: str, latency: float):
        """Records a successful interaction with an expert.

        Args:
            name (str): The name of the expert.
            latency (float): The duration of the successful call in seconds.
        """
        with self.lock:
            if name in self.experts:
                expert = self.experts[name]
                expert["health"] = "healthy"
                expert["success_count"] += 1
                expert["total_latency"] += latency
                expert["average_latency"] = expert["total_latency"] / expert["success_count"]
                expert["last_seen"] = time.time()

    def record_failure(self, name: str):
        """Records a failed interaction with an expert.

        Args:
            name (str): The name of the expert.
        """
        with self.lock:
            if name in self.experts:
                expert = self.experts[name]
                expert["health"] = "unhealthy"
                expert["failure_count"] += 1
                expert["last_seen"] = time.time()

    def get_metrics_for_prompt(self) -> str:
        """Generates a string of all expert metrics formatted for an LLM prompt.

        Returns:
            str: A formatted string detailing the status and performance of each expert.
        """
        with self.lock:
            if not self.experts:
                return "No expert performance data available."

            metrics_string = "You have the following experts available, with their current performance metrics:\n"
            for name, data in sorted(self.experts.items()):
                metrics_string += (
                    f"- Expert: {name} (Type: {data['type']}, Health: {data['health']})\n"
                    f"  - Successes: {data['success_count']}, Failures: {data['failure_count']}\n"
                    f"  - Average Latency: {data['average_latency']:.2f}s\n"
                )
            return metrics_string

    async def connect_and_store_relation(self, source: str, relation: str, target: str, context: str = ""):
        """
        Connects to the Memory Graph service and stores a relationship.
        This is a helper method to demonstrate client integration.
        """
        if not MCP_AVAILABLE:
            logger.warning("MCP library not available. Skipping memory graph update.")
            return

        try:
            async with sse_client(self.memory_url) as streams:
                async with ClientSession(streams[0], streams[1]) as session:
                    await session.initialize()
                    # Using the tool name 'create_relationship' which we exposed in server.py
                    # Note: We exposed 'create_relationship' wrapping handle_create_relationship
                    # The args are: from_memory_id, to_memory_id, relationship_type
                    # Adapting the generic signature to match
                    result = await session.call_tool("create_relationship", {
                        "from_memory_id": source,
                        "to_memory_id": target,
                        "relationship_type": relation
                    })
                    logger.info(f"Stored relation in memory graph: {result}")
        except Exception as e:
            logger.error(f"Failed to store relation in memory graph: {e}")
