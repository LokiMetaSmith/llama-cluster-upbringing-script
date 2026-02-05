import logging
import inspect
import sys
import os
from typing import List, Any
from workflow.nodes.tool_nodes import ToolBase

# Try to import miniray, but don't crash if deps are missing (graceful degradation)
try:
    import miniray
    MINIRAY_AVAILABLE = True
except ImportError:
    MINIRAY_AVAILABLE = False
    logging.warning("Miniray library not found. Distributed compute tool will be disabled.")

class MinirayTool(ToolBase):
    """
    A tool for executing Python code on a distributed cluster using Miniray.
    """

    def __init__(self):
        super().__init__()
        self.available = MINIRAY_AVAILABLE

    def get_tool_info(self):
        return {
            "name": "miniray_compute",
            "description": "Execute complex Python tasks in parallel on the distributed cluster.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The full Python code string containing the function to run."
                    },
                    "entry_point": {
                        "type": "string",
                        "description": "The name of the function to execute."
                    },
                    "args": {
                        "type": "array",
                        "items": {"type": "string"}, # limit args to strings/simples for now
                        "description": "List of arguments to pass to the function."
                    }
                },
                "required": ["code", "entry_point"]
            }
        }

    async def execute(self, code: str, entry_point: str, args: List[Any] = []) -> str:
        if not self.available:
            return "Error: Miniray library is not installed in the agent environment."

        try:
            # Create a localized namespace to execute the code definition
            local_scope = {}
            exec(code, local_scope)

            if entry_point not in local_scope:
                return f"Error: Function '{entry_point}' not defined in the provided code."

            func = local_scope[entry_point]

            # Submit to Miniray
            # Note: The agent and workers must share the same 'miniray' version/protocol.
            # We assume the default Redis config (localhost:6379 or via env REDIS_HOST)
            # Miniray uses os.environ["REDIS_HOST"] if set.

            logging.info(f"Submitting task '{entry_point}' to Miniray cluster...")

            with miniray.Executor(job_name=f"agent_task_{entry_point}") as executor:
                future = executor.submit(func, *args)
                result = future.result() # This blocks until completion

            return f"Task Result: {result}"

        except Exception as e:
            logging.error(f"Miniray execution error: {e}")
            return f"Error executing distributed task: {str(e)}"
