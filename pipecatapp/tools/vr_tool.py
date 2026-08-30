import json
import logging
import asyncio

class VRTool:
    def __init__(self):
        self.available_rooms = {
            "Main": {"x": 0, "y": 0, "z": 4},
            "Server Room": {"x": 10, "y": 0, "z": 4},
            "Chill Zone": {"x": -10, "y": 0, "z": 4}
        }
        self.spatial_nodes = {}
        self.trajectories = []

    def compute_spatial_grid(self, node_ids: list, use_procedural_steering: bool = True) -> dict:
        """Computes 3D spatial grid coordinates for cluster nodes and active Pipecat workers.
        Leverages room partitioning and steering vector repulsion to avoid node collisions in 3D space.
        """
        import math

        grid = {}
        spacing = 4.0
        cols = max(1, int(len(node_ids) ** 0.5))

        for idx, node_id in enumerate(node_ids):
            col = idx % cols
            row = idx // cols
            # Room partitioning offset based on hash of node_id
            room_hash = sum(ord(c) for c in str(node_id)) % 3
            room_offset_x = (room_hash - 1) * 12.0

            base_x = (col - cols / 2) * spacing + room_offset_x
            base_z = (row - cols / 2) * spacing

            # Apply steering vector repulsion if enabled
            if use_procedural_steering and idx > 0:
                repulsion_x, repulsion_z = 0.0, 0.0
                for existing_id, pos in grid.items():
                    dx = base_x - pos["x"]
                    dz = base_z - pos["z"]
                    dist = math.sqrt(dx * dx + dz * dz)
                    if 0.001 < dist < spacing:
                        repulsion_x += (dx / dist) * (spacing - dist) * 0.5
                        repulsion_z += (dz / dist) * (spacing - dist) * 0.5
                base_x += repulsion_x
                base_z += repulsion_z

            grid[node_id] = {
                "x": round(base_x, 2),
                "y": 1.5,
                "z": round(base_z, 2)
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

    async def broadcast_complexity_heatmap(self, filepath: str, complexity: int, maintainability: float) -> str:
        """Broadcasts AST code complexity heatmap metrics to the Web/VR visualizer."""
        try:
            from pipecatapp import web_server
            await web_server.manager.broadcast(json.dumps({
                "type": "complexity_heatmap_update",
                "filepath": filepath,
                "complexity": complexity,
                "maintainability": maintainability
            }))
            return f"Broadcasted complexity heatmap for {filepath}."
        except Exception as e:
            logging.error(f"Failed to broadcast complexity heatmap: {e}")
            return f"Error: Failed to broadcast complexity heatmap: {e}"

    async def broadcast_visual_ai_image(self, prompt_id: str, image_url: str, prompt: str) -> str:
        """Broadcasts ComfyUI generated visual AI image updates to the Web/VR visualizer."""
        try:
            from pipecatapp import web_server
            await web_server.manager.broadcast(json.dumps({
                "type": "comfyui_image_update",
                "prompt_id": prompt_id,
                "image_url": image_url,
                "prompt": prompt
            }))
            return f"Broadcasted visual AI image update for {prompt_id}."
        except Exception as e:
            logging.error(f"Failed to broadcast visual AI image: {e}")
            return f"Error: Failed to broadcast visual AI image: {e}"


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
            if callable(web_server.manager.broadcast):
                res = web_server.manager.broadcast(json.dumps({
                    "type": "navigation",
                    "destination": destination,
                    "coordinates": self.available_rooms[destination]
                }))
                if hasattr(res, "__await__"):
                    await res
            return f"Navigating user to {destination}."
        except Exception as e:
            logging.error(f"Failed to send navigation command: {e}")
            return f"Error: Failed to send navigation command: {e}"
