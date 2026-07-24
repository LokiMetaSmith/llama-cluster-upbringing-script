import os
import json
import logging
import httpx
from typing import List, Dict, Optional
from .retry_utils import retry

class OuroborosTool:
    """
    A tool for managing and navigating the Ouroboros webring.
    Ouroboros is a circular linked list of cluster services and friend agents.
    """
    def __init__(self, consul_host: str = None, consul_port: int = 8500):
        self.consul_host = consul_host or os.getenv("CONSUL_HOST", os.getenv("CLUSTER_IP", "127.0.0.1"))
        self.consul_port = consul_port
        self.consul_url = f"http://{self.consul_host}:{self.consul_port}"
        self.client = httpx.AsyncClient(timeout=5.0)


    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "ouroborostool"),
                "description": getattr(self, "description", "Tool OuroborosTool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform. Available: get_members, save_members, add_member, remove_member, list_members, navigate"
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
        if action == "get_members":
            return getattr(self, "get_members")(**kwargs.get("kwargs", kwargs))
        if action == "save_members":
            return getattr(self, "save_members")(**kwargs.get("kwargs", kwargs))
        if action == "add_member":
            return getattr(self, "add_member")(**kwargs.get("kwargs", kwargs))
        if action == "remove_member":
            return getattr(self, "remove_member")(**kwargs.get("kwargs", kwargs))
        if action == "list_members":
            return getattr(self, "list_members")(**kwargs.get("kwargs", kwargs))
        if action == "navigate":
            return getattr(self, "navigate")(**kwargs.get("kwargs", kwargs))
        else:
            return f"Unknown action: {action}"

    async def get_members(self) -> List[Dict]:
        """Returns the list of members in the Ouroboros webring."""
        # We can call the local web server or Consul directly.
        # Calling Consul directly is more robust if the web server is busy.
        import base64
        key = "pipecatapp/webring/members"
        try:
            response = await self.client.get(f"{self.consul_url}/v1/kv/{key}")
            if response.status_code == 200:
                data = response.json()
                if data and "Value" in data[0] and data[0]["Value"]:
                    decoded_value = base64.b64decode(data[0]["Value"]).decode("utf-8")
                    return json.loads(decoded_value)
        except Exception as e:
            logging.error(f"OuroborosTool: Error fetching members: {e}")
        return []

    async def save_members(self, members: List[Dict]) -> bool:
        """Saves the list of members to the Ouroboros webring."""
        key = "pipecatapp/webring/members"
        try:
            value = json.dumps(members)
            response = await self.client.put(f"{self.consul_url}/v1/kv/{key}", content=value)
            return response.status_code == 200
        except Exception as e:
            logging.error(f"OuroborosTool: Error saving members: {e}")
        return False

    async def add_member(self, name: str, url: str) -> str:
        """Adds a new member to the Ouroboros webring."""
        members = await self.get_members()
        # Check if already exists
        for m in members:
            if m["url"] == url:
                return f"Member with URL {url} already exists in Ouroboros."

        members.append({"name": name, "url": url, "source": "manual"})
        if await self.save_members(members):
            return f"Successfully added '{name}' ({url}) to the Ouroboros webring."
        return "Failed to add member to Ouroboros."

    async def remove_member(self, url: str) -> str:
        """Removes a member from the Ouroboros webring by URL."""
        members = await self.get_members()
        new_members = [m for m in members if m["url"] != url]

        if len(new_members) == len(members):
            return f"No member found with URL {url} in Ouroboros."

        if await self.save_members(new_members):
            return f"Successfully removed member with URL {url} from Ouroboros."
        return "Failed to remove member from Ouroboros."

    async def list_members(self) -> str:
        """Lists all members in the Ouroboros webring."""
        members = await self.get_members()
        if not members:
            return "The Ouroboros webring is currently empty."

        report = "Ouroboros Webring Members:\n"
        for m in members:
            report += f"- {m['name']}: {m['url']} (Source: {m.get('source', 'unknown')})\n"
        return report

    async def navigate(self, direction: str) -> str:
        """Returns the URL of the next, previous, or a random member in the ring."""
        if direction not in ["next", "prev", "random"]:
            return "Invalid direction. Choose 'next', 'prev', or 'random'."

        # Navigation usually happens in the UI, but the agent can "recommend" where to go next.
        members = await self.get_members()
        if not members:
            return "The Ouroboros webring is empty."

        if direction == "random":
            import random
            member = random.choice(members)
            return f"I recommend spinning the ring to: {member['name']} ({member['url']})"

        # For next/prev, we'd need to know the "current" member.
        # Since the agent might not know where the user is, we can just list the ring
        # or recommend the first one if we can't determine current.
        return f"To navigate the ring, use the links in the UI, or I can give you a random recommendation. Currently I have {len(members)} members in the ring."
