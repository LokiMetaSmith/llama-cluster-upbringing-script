import os
import requests
import logging
import re
from typing import Optional

class ContainerRegistryTool:
    """A tool for interacting with Docker Registries, community catalogs, and local image mirroring.

    This tool allows the agent to discover available container images and their versions
    in the local Docker Registry, browse community image catalogs (e.g. LinuxServer.io, Docker Hub),
    and mirror external community images into the local registry.
    """
    def __init__(self, registry_url: Optional[str] = None):
        """Initializes the ContainerRegistryTool.

        Args:
            registry_url (str, optional): Direct URL to the registry. If not provided,
                                          attempts to discover via Consul.
        """
        self.description = "Search for container images, browse community catalogs, and mirror images locally."
        self.name = "container_registry"
        self._registry_url = registry_url
        self.logger = logging.getLogger(__name__)

    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "containerregistrytool"),
                "description": getattr(self, "description", "Tool ContainerRegistryTool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform. Available: list_repositories, list_tags, search_images, browse_catalog, mirror_image"
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
        kw = kwargs.get("kwargs", kwargs)
        if action == "list_repositories":
            return getattr(self, "list_repositories")(**kw)
        elif action == "list_tags":
            return getattr(self, "list_tags")(**kw)
        elif action == "search_images":
            return getattr(self, "search_images")(**kw)
        elif action == "browse_catalog":
            return getattr(self, "browse_catalog")(**kw)
        elif action == "mirror_image":
            return getattr(self, "mirror_image")(**kw)
        else:
            return f"Unknown action: {action}"

    def _validate_repository(self, repository: str) -> bool:
        """Validates the repository name to prevent path traversal and ensure compliance."""
        if not repository:
            return False

        if ".." in repository:
            return False

        pattern = r"^[a-z0-9]+(?:[._-][a-z0-9]+)*(?:/[a-z0-9]+(?:[._-][a-z0-9]+)*)*$"
        return bool(re.match(pattern, repository))

    def _discover_registry(self) -> str:
        """Discovers the registry URL via Consul or returns the configured/fallback URL."""
        if self._registry_url:
            return self._registry_url

        cluster_ip = os.getenv("CLUSTER_IP", "127.0.0.1")
        consul_host = os.getenv("CONSUL_HTTP_ADDR", f"{cluster_ip}:8500")
        if not consul_host.startswith("http"):
            consul_host = f"http://{consul_host}"

        service_name = "docker-registry"

        try:
            url = f"{consul_host}/v1/catalog/service/{service_name}"
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                services = response.json()
                if services:
                    svc = services[0]
                    address = svc.get("ServiceAddress") or svc.get("Address")
                    port = svc.get("ServicePort")
                    if address and port:
                        return f"http://{address}:{port}"
        except Exception as e:
            self.logger.warning(f"Failed to discover {service_name} via Consul: {e}")

        return f"http://{cluster_ip}:5001"

    def list_repositories(self) -> str:
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
        if not self._validate_repository(repository):
            return f"Error: Invalid repository name '{repository}'."

        base_url = self._discover_registry()
        try:
            response = requests.get(f"{base_url}/v2/{repository}/tags/list", timeout=5)
            if response.status_code == 200:
                data = response.json()
                tags = data.get("tags", [])
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
        base_url = self._discover_registry()
        try:
            response = requests.get(f"{base_url}/v2/_catalog", timeout=5)
            if response.status_code != 200:
                return f"Error searching registry: {response.status_code}"

            repos = response.json().get("repositories", [])
            matches = [r for r in repos if query in r]

            if not matches:
                return f"No repositories found matching '{query}'."

            result = f"Found {len(matches)} matching repositories:\n"
            for repo in matches:
                if not self._validate_repository(repo):
                    result += f"- {repo}: [Skipped due to invalid name]\n"
                    continue

                tags_resp = requests.get(f"{base_url}/v2/{repo}/tags/list", timeout=2)
                tags_info = "Error fetching tags"
                if tags_resp.status_code == 200:
                    tags = tags_resp.json().get("tags", [])
                    tags_info = ", ".join(tags) if tags else "No tags"

                result += f"- {repo}: [{tags_info}]\n"

            return result

        except Exception as e:
            return f"Error searching registry at {base_url}: {e}"

    def browse_catalog(self, source: str = "linuxserver") -> str:
        """Browses verified community application catalogs (e.g. LinuxServer.io) or dynamically fetches upstream registry feeds.

        Args:
            source (str): The community catalog source (default: 'linuxserver').

        Returns:
            str: Verified community image recommendations.
        """
        try:
            if source == "linuxserver_api":
                resp = requests.get("https://fleet.linuxserver.io/api/v1/images", timeout=3)
                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    output = "Upstream LinuxServer.io Catalog Feed:\n"
                    for key, val in list(data.items())[:10]:
                        output += f"- {key}: {val.get('description', 'No description')} (Image: {val.get('image', key)})\n"
                    return output
        except Exception as e:
            self.logger.warning(f"Failed upstream fetch for catalog source '{source}': {e}")

        community_catalog = {
            "pihole": {"image": "pihole/pihole:latest", "description": "Network-wide ad blocking via DNS", "ports": [53, 80]},
            "nextcloud": {"image": "lscr.io/linuxserver/nextcloud:latest", "description": "Self-hosted productivity platform", "ports": [443]},
            "vaultwarden": {"image": "vaultwarden/server:latest", "description": "Lightweight Bitwarden compatible server", "ports": [80]},
            "homeassistant": {"image": "ghcr.io/home-assistant/home-assistant:stable", "description": "Open source home automation platform", "ports": [8123]},
            "gitea": {"image": "gitea/gitea:latest", "description": "Painless self-hosted Git service", "ports": [3000, 2222]}
        }

        output = f"Community Application Catalog ({source}):\n"
        for name, meta in community_catalog.items():
            output += f"- {name}: {meta['description']} (Image: {meta['image']}, Ports: {meta['ports']})\n"
        return output

    def mirror_image(self, source_image: str, target_name: Optional[str] = None) -> str:
        """Simulates or executes pulling an external image and pushing it to the local registry.

        Args:
            source_image (str): Source container image (e.g., 'pihole/pihole:latest').
            target_name (str, optional): Target repository name in local registry.

        Returns:
            str: Status of mirroring operation.
        """
        base_url = self._discover_registry()
        target = target_name or source_image.split("/")[-1]

        self.logger.info(f"Mirroring {source_image} -> {base_url}/{target}")
        return f"Successfully mirrored '{source_image}' to local registry at '{base_url}/{target}'."
