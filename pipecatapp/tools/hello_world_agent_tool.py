class HelloWorldAgentTool:
    """A simple hello world agent tool for testing."""

    def __init__(self):
        self.description = "A simple hello world agent that returns a greeting."
        self.name = "hello_world_agent"

    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "hello_world_agent"),
                "description": getattr(self, "description", "Tool HelloWorldAgentTool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The message to send to the hello world agent."
                        }
                    },
                    "required": ["message"]
                }
            }
        }

    def say_hello(self, message: str) -> str:
        """Returns a greeting with the provided message."""
        return f"Hello World! You said: {message}"

    def execute(self, action: str, **kwargs):
        if action == "say_hello":
            return getattr(self, "say_hello")(**kwargs.get("kwargs", kwargs))
        else:
            return f"Unknown action: {action}"
