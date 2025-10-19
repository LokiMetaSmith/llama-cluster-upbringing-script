import os
import requests
import logging

class HomeAssistantTool:
    """A tool for interacting with the Home Assistant API."""

    def __init__(self, ha_url: str = None, ha_token: str = None):
        """Initializes the HomeAssistantTool.

        Args:
            ha_url (str, optional): The base URL of the Home Assistant API.
                Defaults to 'http://home-assistant.service.consul:8123'.
            ha_token (str, optional): The Long-Lived Access Token for authentication.
        """
        self.name = "home_assistant"
        self.description = "Controls smart home devices via Home Assistant."
        self.base_url = ha_url or "http://home-assistant.service.consul:8123"
        self.token = ha_token
        self.headers = {}
        if not self.token:
            logging.error("Home Assistant token not provided. Home Assistant tool will not work.")
        else:
            self.headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }

    def call_service(self, domain: str, service: str, entity_id: str, service_data: dict = None) -> str:
        """Calls a service in Home Assistant.

        Args:
            domain (str): The domain of the service (e.g., 'light', 'switch').
            service (str): The name of the service to call (e.g., 'turn_on', 'toggle').
            entity_id (str): The entity_id of the device to control (e.g., 'light.living_room').
            service_data (dict, optional): A dictionary of additional data to pass
                to the service. Defaults to None.

        Returns:
            str: A message indicating the result of the API call.
        """
        if not self.token:
            return "Error: Home Assistant token is not configured."

        url = f"{self.base_url}/api/services/{domain}/{service}"
        payload = {"entity_id": entity_id}
        if service_data:
            payload.update(service_data)

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=10)
            response.raise_for_status()
            return f"Successfully called service {domain}.{service} on {entity_id}."
        except requests.exceptions.RequestException as e:
            logging.error(f"Error calling Home Assistant API: {e}")
            return f"Error: Could not call service {domain}.{service}. {e}"

    def get_state(self, entity_id: str) -> str:
        """Gets the state of a specific entity in Home Assistant.

        Args:
            entity_id (str): The entity_id of the device to query (e.g., 'light.living_room').

        Returns:
            str: The state of the entity, or an error message.
        """
        if not self.token:
            return "Error: Home Assistant token is not configured."

        url = f"{self.base_url}/api/states/{entity_id}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            state_data = response.json()
            return f"The state of {entity_id} is {state_data.get('state')}."
        except requests.exceptions.RequestException as e:
            logging.error(f"Error getting Home Assistant state: {e}")
            return f"Error: Could not get state for {entity_id}. {e}"