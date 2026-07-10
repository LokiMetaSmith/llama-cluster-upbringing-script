import os
import json
import logging
from typing import Optional, Dict, Union
from utils.app_manager import AppManager

class ExternalAppManagerTool:
    """
    A unified package/plugin management tool for hosting containerized external applications on the cluster.
    Enables the AI agent to autonomously scaffold, validate, deploy, list, check status, and purge external applications.

    All external applications are strictly bound to the tailscale0 interface (Rule 1.1) and routed securely.
    Dynamic storage is provisioned via Btrfs subvolumes when available.

    The expected JSON manifest schema for deployments is:
    {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "ExternalAppManifest",
      "type": "object",
      "properties": {
        "name": { "type": "string", "pattern": "^[a-z0-9-]+$" },
        "version": { "type": "string", "pattern": "^[0-9]+\\\\.[0-9]+\\\\.[0-9]+$" },
        "image": { "type": "string" },
        "ui": {
          "type": "object",
          "properties": {
            "title": { "type": "string" },
            "description": { "type": "string" },
            "icon": { "type": "string" }
          },
          "required": ["title", "icon"]
        },
        "resources": {
          "type": "object",
          "properties": {
            "cpu_mhz": { "type": "integer" },
            "memory_mb": { "type": "integer" }
          }
        },
        "env": {
          "type": "object",
          "additionalProperties": { "type": "string" }
        },
        "network": {
          "type": "object",
          "properties": {
            "internal_port": { "type": "integer", "minimum": 1, "maximum": 65535 },
            "route_public": { "type": "boolean" },
            "domain": { "type": "string" }
          },
          "required": ["internal_port", "route_public"]
        },
        "storage": {
          "type": "object",
          "properties": {
            "enabled": { "type": "boolean" },
            "size_gb": { "type": "integer", "minimum": 1 },
            "mount_path": { "type": "string" }
          },
          "required": ["enabled"]
        }
      },
      "required": ["name", "version", "image", "ui", "resources", "network", "storage"]
    }
    """
    def __init__(self, consul_url: Optional[str] = None, nomad_url: Optional[str] = None):
        self.name = "external_app_manager"
        self.description = (
            "A hybrid tool to scaffold, validate, deploy, list, inspect, and purge containerized external applications on the cluster. "
            "All applications automatically inherit Headscale/Tailscale mesh routing (Rule 1.1) and dynamic Btrfs storage backups."
        )
        self.manager = AppManager(consul_url=consul_url, nomad_url=nomad_url)
        self.logger = logging.getLogger(__name__)

    def scaffold_manifest(self,
                          name: str,
                          image: str,
                          ui_title: str,
                          ui_icon: str,
                          internal_port: int,
                          route_public: bool = True,
                          storage_enabled: bool = False,
                          mount_path: str = "",
                          cpu_mhz: int = 250,
                          memory_mb: int = 256,
                          env: Optional[Dict[str, str]] = None) -> str:
        """
        Scaffolds a skeleton schema-compliant JSON manifest for the application.

        Args:
            name: Lowercase alphanumeric name (with dashes).
            image: Docker registry path of the container image.
            ui_title: Title of the application on the Ouroboros dashboard.
            ui_icon: Icon or emoji for the dashboard.
            internal_port: Container internal port.
            route_public: Expose public ingress via Traefik host-based routing.
            storage_enabled: Enable dynamic persistent Btrfs subvolume.
            mount_path: Absolute mount target path inside the container.
            cpu_mhz: Allocated CPU resource.
            memory_mb: Allocated RAM resource.
            env: Dict of key-value environment pairs.
        """
        manifest = {
            "name": name.lower().strip(),
            "version": "1.0.0",
            "image": image,
            "ui": {
                "title": ui_title,
                "description": f"Containerized instance of {ui_title} deployed via external_app_manager.",
                "icon": ui_icon
            },
            "resources": {
                "cpu_mhz": cpu_mhz,
                "memory_mb": memory_mb
            },
            "env": env or {},
            "network": {
                "internal_port": internal_port,
                "route_public": route_public
            },
            "storage": {
                "enabled": storage_enabled,
                "mount_path": mount_path if storage_enabled else ""
            }
        }
        if storage_enabled and mount_path:
            manifest["storage"]["size_gb"] = 2  # Default to 2GB allocation

        return json.dumps(manifest, indent=2)

    def validate_manifest(self, manifest_json: str) -> str:
        """
        Parses and validates the JSON string of the application manifest.
        """
        try:
            manifest = json.loads(manifest_json)
        except Exception as e:
            return f"Error: Invalid JSON syntax. {e}"

        is_valid, errors = self.manager.validate_manifest(manifest)
        if is_valid:
            return "Success: The manifest is valid and strictly schema-compliant."
        else:
            return "Validation Failed:\n" + "\n".join([f"- {err}" for err in errors])

    def deploy_app(self, manifest_json: str) -> str:
        """
        Validates, provisions Btrfs subvolume, translates, and deploys the containerized application.
        """
        try:
            manifest = json.loads(manifest_json)
        except Exception as e:
            return f"Error: Invalid JSON syntax. {e}"

        success, msg = self.manager.deploy_app(manifest)
        if success:
            return f"Success: {msg}"
        else:
            return f"Failure: {msg}"

    def purge_app(self, name: str) -> str:
        """
        Stops the application task, deletes its Btrfs/standard volumes, and removes it from Ouroboros.
        """
        success, msg = self.manager.purge_app(name.lower().strip())
        if success:
            return f"Success: {msg}"
        else:
            return f"Failure: {msg}"

    def list_apps(self) -> str:
        """
        Lists all containerized external applications currently registered in Nomad/Consul.
        """
        apps = self.manager.list_apps()
        if not apps:
            return "No containerized external applications found."

        report = "Installed External Applications:\n"
        for app in apps:
            report += f"- {app['name']} (Status: {app['status']}, Type: {app['type']})\n"
        return report

    def status_app(self, name: str) -> str:
        """
        Retrieves real-time execution, network, and allocation status for the given application.
        """
        status_info = self.manager.get_app_status(name.lower().strip())
        return json.dumps(status_info, indent=2)
