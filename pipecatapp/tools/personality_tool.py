import logging
import requests
import json
import os

class PersonalityTool:
    """
    Tool for managing LLM personality/steering via Control Vectors.
    Allows real-time adjustment of the model's behavior along specific axes (e.g., Assistant vs. Creative).
    """
    def __init__(self, api_url: str = None):
        # Default to local router or direct llama server if not specified
        self.api_url = (api_url or "http://localhost:8080").rstrip("/")
        # Base directory where control vectors are stored on the server side
        self.vectors_dir = "/opt/nomad/models/vectors"

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
