import json
import logging

class VRTool:
    def __init__(self):
        self.available_rooms = {
            "Main": {"x": 0, "y": 0, "z": 4},
            "Server Room": {"x": 10, "y": 0, "z": 4},
            "Chill Zone": {"x": -10, "y": 0, "z": 4}
        }

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
            import web_server
            await web_server.manager.broadcast(json.dumps({
                "type": "navigation",
                "destination": destination,
                "coordinates": self.available_rooms[destination]
            }))
            return f"Navigating user to {destination}."
        except Exception as e:
            logging.error(f"Failed to send navigation command: {e}")
            return f"Error: Failed to send navigation command: {e}"
