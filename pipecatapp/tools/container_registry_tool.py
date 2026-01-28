import os
import requests
import logging
from typing import Optional

class ContainerRegistryTool:
    """A tool for interacting with a Docker Registry to search for images and tags.

    This tool allows the agent to discover available container images and their versions
    in the configured Docker Registry (e.g., a local self-hosted registry).
    It uses Consul for service discovery to locate the registry.

    Attributes:
        description (str): A brief description of the tool's purpose.
        name (str): The name of the tool.
    """
    def __init__(self, registry_url: Optional[str] = None):
        """Initializes the ContainerRegistryTool.

        Args:
            registry_url (str, optional): Direct URL to the registry. If not provided,
                                          attempts to discover via Consul.
        """
        self.description = "Search for container images and tags in the Docker Registry."
        self.name = "container_registry"
        self._registry_url = registry_url
        self.logger = logging.getLogger(__name__)

    def _discover_registry(self) -> str:
        """Discovers the registry URL via Consul or returns the configured/fallback URL."""
        if self._registry_url:
            return self._registry_url

        consul_host = os.getenv("CONSUL_HTTP_ADDR", "localhost:8500")
        if not consul_host.startswith("http"):
            consul_host = f"http://{consul_host}"

        service_name = "docker-registry"

        try:
            url = f"{consul_host}/v1/catalog/service/{service_name}"
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                services = response.json()
                if services:
                    # Pick the first one
                    svc = services[0]
                    address = svc.get("ServiceAddress") or svc.get("Address")
                    port = svc.get("ServicePort")
                    if address and port:
                        return f"http://{address}:{port}"
        except Exception as e:
            self.logger.warning(f"Failed to discover {service_name} via Consul: {e}")

        # Fallback to standard local registry port
        return "http://localhost:5001"

    def list_repositories(self) -> str:
        """Lists all repositories available in the registry.

        Returns:
            str: A formatted list of repositories or error message.
        """
        base_url = self._discover_registry()
        try:
            response = requests.get(f"{base_url}/v2/_catalog", timeout=5)
            if response.status_code == 200:
                data = response.json()
                repos = data.get("repositories", [])
                if not repos:
                    return "Registry is empty (no repositories found)."
                return f"Available Repositories:\n" + "\n".join([f"- {repo}" for repo in repos])
            else:
                return f"Error listing repositories: {response.status_code} {response.text}"
        except Exception as e:
            return f"Error connecting to registry at {base_url}: {e}"

    def list_tags(self, repository: str) -> str:
        """Lists all tags for a specific repository.

        Args:
            repository (str): The name of the repository (e.g., 'pipecatapp').

        Returns:
            str: A formatted list of tags or error message.
        """
        base_url = self._discover_registry()
        try:
            response = requests.get(f"{base_url}/v2/{repository}/tags/list", timeout=5)
            if response.status_code == 200:
                data = response.json()
                tags = data.get("tags", [])
                # Handle case where tags is None (empty repo)
                if tags is None:
                    tags = []
                if not tags:
                    return f"No tags found for repository '{repository}'."
                return f"Tags for '{repository}':\n" + "\n".join([f"- {tag}" for tag in tags])
            elif response.status_code == 404:
                return f"Repository '{repository}' not found."
            else:
                return f"Error listing tags: {response.status_code} {response.text}"
        except Exception as e:
            return f"Error connecting to registry at {base_url}: {e}"

    def search_images(self, query: str) -> str:
        """Searches for repositories matching a query string and lists their tags.

        Args:
            query (str): The search term.

        Returns:
            str: Matching repositories and their tags.
        """
        base_url = self._discover_registry()
        try:
            # First get catalog
            response = requests.get(f"{base_url}/v2/_catalog", timeout=5)
            if response.status_code != 200:
                return f"Error searching registry: {response.status_code}"

            repos = response.json().get("repositories", [])
            matches = [r for r in repos if query in r]

            if not matches:
                return f"No repositories found matching '{query}'."

            result = f"Found {len(matches)} matching repositories:\n"
            for repo in matches:
                # Fetch tags for each match to be helpful
                tags_resp = requests.get(f"{base_url}/v2/{repo}/tags/list", timeout=2)
                tags_info = "Error fetching tags"
                if tags_resp.status_code == 200:
                    tags = tags_resp.json().get("tags", [])
                    tags_info = ", ".join(tags) if tags else "No tags"

                result += f"- {repo}: [{tags_info}]\n"

            return result

        except Exception as e:
            return f"Error searching registry at {base_url}: {e}"
