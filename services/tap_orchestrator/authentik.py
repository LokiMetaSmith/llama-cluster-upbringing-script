import httpx
import logging
from typing import Optional
from config import settings
from models import AuthentikUser

logger = logging.getLogger(__name__)

class AuthentikClient:
    def __init__(self):
        self.api_url = settings.authentik_api_url.rstrip('/')
        self.client_id = settings.authentik_client_id
        self.client_secret = settings.authentik_client_secret
        self.static_token = settings.authentik_token
        self._access_token: Optional[str] = None
        self._http_client = httpx.AsyncClient(verify=False) # Internal cluster traffic might be self-signed

    async def _get_token(self) -> str:
        """
        Get an access token using Client Credentials Grant or static token fallback.
        """
        if self.static_token:
            return self.static_token

        if not self.client_id or not self.client_secret:
            raise ValueError("No Authentik credentials provided (token or client_id/secret)")

        if self._access_token:
            # We could implement token expiration handling here
            return self._access_token

        try:
            # Depending on the Authentik setup, the token endpoint is usually /application/o/token/
            # but we'll use standard OAuth2 flow. This might need adjustment based on exact Authentik config.
            url = f"{self.api_url}/application/o/token/"
            data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            response = await self._http_client.post(url, data=data)
            response.raise_for_status()
            token_data = response.json()
            self._access_token = token_data["access_token"]
            return self._access_token
        except httpx.HTTPError as e:
            logger.error(f"Failed to obtain Authentik token: {e}")
            raise

    async def get_user(self, username: str) -> Optional[AuthentikUser]:
        """
        Fetch a user's details and groups from Authentik.
        """
        try:
            token = await self._get_token()
            headers = {"Authorization": f"Bearer {token}"}

            # Use the /api/v3/core/users/ endpoint and filter by username
            url = f"{self.api_url}/api/v3/core/users/"
            params = {"username": username}

            response = await self._http_client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            if not results:
                logger.warning(f"User {username} not found in Authentik")
                return None

            user_data = results[0]

            # Map Authentik response to our model
            # Authentik API returns groups as a list of UUIDs, or detailed objects depending on expansion
            # We'll extract group names if they're dicts, otherwise leave as IDs or empty
            groups = []
            for g in user_data.get("groups_obj", []):
                if isinstance(g, dict):
                    groups.append(g.get("name", ""))

            user = AuthentikUser(
                username=user_data.get("username", username),
                name=user_data.get("name"),
                is_active=user_data.get("is_active", False),
                groups=groups,
                attributes=user_data.get("attributes", {})
            )
            return user

        except httpx.HTTPError as e:
            logger.error(f"Error fetching Authentik user {username}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error formatting Authentik user {username}: {e}")
            return None

    async def close(self):
        await self._http_client.aclose()

authentik_client = AuthentikClient()
