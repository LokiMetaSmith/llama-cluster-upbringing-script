import json
import logging

class VRTool:
    def __init__(self):
        self.available_rooms = {
            "Main": {"x": 0, "y": 0, "z": 4},
            "Server Room": {"x": 10, "y": 0, "z": 4},
            "Chill Zone": {"x": -10, "y": 0, "z": 4}
        }
        self.spatial_nodes = {}
        self.trajectories = []

    def compute_spatial_grid(self, node_ids: list) -> dict:
        """Computes 3D spatial grid coordinates for cluster nodes and active Pipecat workers."""
        grid = {}
        spacing = 4.0
        cols = max(1, int(len(node_ids) ** 0.5))
        for idx, node_id in enumerate(node_ids):
            col = idx % cols
            row = idx // cols
            grid[node_id] = {
                "x": round((col - cols / 2) * spacing, 2),
                "y": 1.5,
                "z": round((row - cols / 2) * spacing, 2)
            }
        self.spatial_nodes = grid
        return grid

    def emit_signal_trajectory(self, source_agent: str, target_agent: str, signal_type: str = "liminal_mesh") -> dict:
        """Emits a signal pulse/trajectory ray between two spatial nodes in the 3D VR environment."""
        source_pos = self.spatial_nodes.get(source_agent, {"x": 0, "y": 1.5, "z": 0})
        target_pos = self.spatial_nodes.get(target_agent, {"x": 5, "y": 1.5, "z": 5})
        trajectory = {
            "type": "signal_trajectory",
            "signal_type": signal_type,
            "source": {"agent_id": source_agent, "pos": source_pos},
            "target": {"agent_id": target_agent, "pos": target_pos}
        }
        self.trajectories.append(trajectory)
        return trajectory

    async def broadcast_circuit_breaker(self, agent_id: str, level: str) -> str:
        """Broadcasts a visual circuit breaker status update ('Normal' -> 'Throttled' -> 'Escalated' -> 'Stopped') to the Web/VR visualizer."""
        try:
            from pipecatapp import web_server
            await web_server.manager.broadcast(json.dumps({
                "type": "circuit_breaker_update",
                "agent_id": agent_id,
                "circuit_breaker_level": level
            }))
            return f"Broadcasted circuit breaker status '{level}' for agent {agent_id}."
        except Exception as e:
            logging.error(f"Failed to broadcast circuit breaker status: {e}")
            return f"Error: Failed to broadcast circuit breaker status: {e}"

    async def broadcast_hitl_gate(self, request_id: str, agent_id: str, proposal: str) -> str:
        """Broadcasts a Human-In-The-Loop gate approval request to the Web/VR visualizer."""
        try:
            from pipecatapp import web_server
            await web_server.manager.broadcast(json.dumps({
                "type": "hitl_gate_request",
                "request_id": request_id,
                "agent_id": agent_id,
                "proposal": proposal
            }))
            return f"Broadcasted HITL approval gate request '{request_id}' for agent {agent_id}."
        except Exception as e:
            logging.error(f"Failed to broadcast HITL gate request: {e}")
            return f"Error: Failed to broadcast HITL gate request: {e}"


    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "vrtool"),
                "description": getattr(self, "description", "Tool VRTool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform. Available: get_tool_def"
                        },
                        "kwargs": {
                            "type": "object",
                            "description": "Additional arguments for the action."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def execute(self, action: str, **kwargs):
        if action == "get_tool_def":
            return getattr(self, "get_tool_def")(**kwargs.get("kwargs", kwargs))
        else:
            return f"Unknown action: {action}"

    def get_tool_def(self):
        return {
            "type": "function",
            "function": {
                "name": "vr_navigate",
                "description": "Navigate the user to a different room in the VR environment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "destination": {
                            "type": "string",
                            "description": "The name of the room to navigate to.",
                            "enum": list(self.available_rooms.keys())
                        }
                    },
                    "required": ["destination"]
                }
            }
        }

    async def execute(self, destination: str):
        if destination not in self.available_rooms:
            return f"Error: Room '{destination}' not found. Available rooms: {', '.join(self.available_rooms.keys())}"

        try:
            from pipecatapp import web_server
            await web_server.manager.broadcast(json.dumps({
                "type": "navigation",
                "destination": destination,
                "coordinates": self.available_rooms[destination]
            }))
            return f"Navigating user to {destination}."
        except Exception as e:
            logging.error(f"Failed to send navigation command: {e}")
            return f"Error: Failed to send navigation command: {e}"
