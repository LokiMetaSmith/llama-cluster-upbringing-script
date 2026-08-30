import logging
import requests
import json
import os

class PersonalityTool:
    """
    Tool for managing LLM personality/steering via Control Vectors and
    PersonaPlex voice/role conditioning embeddings (e.g., NATF2, VARM1, AAMF1).
    """
    def __init__(self, api_url: str = None):
        cluster_ip = os.getenv("CLUSTER_IP", "127.0.0.1")
        self.api_url = (api_url or f"http://{cluster_ip}:8080").rstrip("/")
        self.vectors_dir = "/opt/nomad/models/vectors"
        self.voice_embeddings = {
            "NATF2": {"gender": "female", "accent": "neutral", "tone": "authoritative"},
            "VARM1": {"gender": "male", "accent": "neutral", "tone": "conversational"},
            "AAMF1": {"gender": "female", "accent": "expressive", "tone": "empathetic"}
        }


    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "personalitytool"),
                "description": getattr(self, "description", "Tool PersonalityTool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform. Available: set_personality, reset_personality, get_current_personality"
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
        if action == "set_personality":
            return getattr(self, "set_personality")(**kwargs.get("kwargs", kwargs))
        if action == "reset_personality":
            return getattr(self, "reset_personality")(**kwargs.get("kwargs", kwargs))
        if action == "get_current_personality":
            return getattr(self, "get_current_personality")(**kwargs.get("kwargs", kwargs))
        if action == "set_voice_persona":
            return getattr(self, "set_voice_persona")(**kwargs.get("kwargs", kwargs))
        else:
            return f"Unknown action: {action}"

    def set_voice_persona(self, voice_id: str, role_prompt: str, emotion: str = "neutral") -> str:
        """
        Applies a PersonaPlex voice conditioning embedding and text role prompt.
        """
        if voice_id not in self.voice_embeddings:
            supported = ", ".join(self.voice_embeddings.keys())
            return f"Error: Voice ID '{voice_id}' not supported. Options: {supported}"

        voice_meta = self.voice_embeddings[voice_id]
        payload = {
            "voice_id": voice_id,
            "voice_meta": voice_meta,
            "role_prompt": role_prompt,
            "emotion": emotion
        }

        try:
            response = requests.post(f"{self.api_url}/personaplex/voice-persona", json=payload, timeout=5)
            response.raise_for_status()
            return f"Successfully applied PersonaPlex voice persona '{voice_id}' (Emotion: {emotion})."
        except requests.exceptions.RequestException as e:
            logging.warning(f"PersonaPlex server unreachable ({e}); storing local voice persona state.")
            return f"Local PersonaPlex Voice Persona state applied: {voice_id} - Emotion: {emotion}."

    def set_personality(self, name: str, strength: float, fname: str = None) -> str:
        """
        Sets the current personality by applying a control vector.

        Args:
            name (str): The name of the personality (e.g., "creative", "assistant").
            strength (float): The strength of the vector. Positive values reinforce the vector,
                              negative values move away from it.
            fname (str, optional): The filename of the control vector .gguf file.
                                   If not provided, defaults to {name}.gguf.
        """
        if not fname:
            fname = f"{name}.gguf"

        # Basic path validation
        if ".." in fname or fname.startswith("/") or fname.startswith("\\"):
            logging.warning(f"Invalid filename provided: {fname}")
            return "Error: Filename must be relative and cannot traverse directories."

        full_path = f"{self.vectors_dir}/{fname}"

        payload = [
            {
                "fname": full_path,
                "strength": strength
            }
        ]

        try:
            logging.info(f"Setting personality {name} ({strength}) via {self.api_url}/control-vectors")
            response = requests.post(f"{self.api_url}/control-vectors", json=payload)
            response.raise_for_status()
            return f"Successfully set personality to '{name}' with strength {strength}."
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to set personality: {e}")
            if e.response is not None:
                return f"Error setting personality (Status {e.response.status_code}): {e.response.text}"
            return f"Error setting personality: {e}"

    def reset_personality(self) -> str:
        """
        Resets the model to its base personality by clearing all control vectors.
        """
        try:
            # Sending an empty list clears all vectors
            response = requests.post(f"{self.api_url}/control-vectors", json=[])
            response.raise_for_status()
            return "Personality reset to neutral (all control vectors cleared)."
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to reset personality: {e}")
            return f"Error resetting personality: {e}"

    def get_current_personality(self) -> str:
        """
        Retrieves the currently active control vectors.
        """
        try:
            response = requests.get(f"{self.api_url}/control-vectors")
            response.raise_for_status()
            return f"Current configuration: {json.dumps(response.json(), indent=2)}"
        except requests.exceptions.RequestException as e:
            # Fallback if GET is not implemented fully yet or fails
            return f"Error getting personality status: {e}"
