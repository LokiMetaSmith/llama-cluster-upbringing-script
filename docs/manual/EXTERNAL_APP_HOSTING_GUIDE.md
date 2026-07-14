# External Application Hosting & Package Management Guide

This document describes the design, schema, and operational workflows for hosting containerized external applications alongside the conversational AI cluster.

The integration system consists of a Python-based utility, an Autonomous Agentic Tool (`external_app_manager`), and a CLI Management utility (`scripts/app-manager.py`).

---

## Table of Contents

- [1. Architecture Overview](#1-architecture-overview)
  - [System Integration Layers](#system-integration-layers)
- [2. Standardized Manifest Specification](#2-standardized-manifest-specification)
  - [Example Manifest: Uptime Kuma](#example-manifest-uptime-kuma)
- [3. Sandboxing & Security Safeguards](#3-sandboxing-security-safeguards)
- [4. Human Operator Guide (CLI Tool)](#4-human-operator-guide-cli-tool)
  - [Subcommand References](#subcommand-references)
    - [1. Install / Update an Application](#1-install-update-an-application)
    - [2. Uninstall & Purge](#2-uninstall-purge)
    - [3. List Configured Apps](#3-list-configured-apps)
    - [4. Real-time Status Inspect](#4-real-time-status-inspect)
- [5. Agent Integration (Autonomous Operations)](#5-agent-integration-autonomous-operations)
  - [Tool Methods Available](#tool-methods-available)
  - [Expected Agent Behavior Pattern](#expected-agent-behavior-pattern)

---

## 1. Architecture Overview

The External Application Package Management system allows the cluster to securely provision and host third-party services (e.g., databases, analytics, administrative web UIs) in parallel with the primary AI pipeline.

### System Integration Layers
1. **Packaging Specification:** Applications declare metadata, resource needs, storage, environment, and entrypoints inside a standardized, strict JSON manifest (`manifest.json`).
2. **Dynamic Storage Provisioning:** Persistent state is managed dynamically. If the host supports Btrfs, the manager allocates a dedicated **Btrfs Subvolume** (`/btrfs_root/volumes/<app_name>`) that automatically inherits the cluster's recovery snapshotting and rollback routines. If Btrfs is unavailable, it gracefully falls back to standard directory binding.
3. **Enforced Mesh Networking (Rule 1.1):** All external applications are bound to the `tailscale0` network interface and mapped dynamically. Communication remains strictly on the internal Tailscale/Headscale mesh network.
4. **Seamless Ingress (Traefik Host-based Routing):** If `route_public` is true, host-based routing (e.g., `http://<app_name>.local.mesh`) is automatically registered via Traefik.
5. **Webring Auto-Registration:** Upon healthy deployment, the application is dynamically registered as a member in the circular **Ouroboros Webring** dashboard (`pipecatapp/webring/members` inside Consul KV).

---

## 2. Standardized Manifest Specification

External applications must be packaged with a `manifest.json` file. Below is the strict JSON schema enforced by the validation layer:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ExternalAppManifest",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "Unique alphanumeric lowercase name of the application. May contain dashes.",
      "pattern": "^[a-z0-9-]+$"
    },
    "version": {
      "type": "string",
      "description": "Semantic versioning string.",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"
    },
    "image": {
      "type": "string",
      "description": "Complete Docker registry path for the container image."
    },
    "ui": {
      "type": "object",
      "description": "Metadata for the Ouroboros webring dashboard.",
      "properties": {
        "title": { "type": "string" },
        "description": { "type": "string" },
        "icon": { "type": "string", "description": "Emoji or icon identifier." }
      },
      "required": ["title", "icon"],
      "additionalProperties": false
    },
    "resources": {
      "type": "object",
      "description": "Nomad scheduling constraints.",
      "properties": {
        "cpu_mhz": { "type": "integer", "default": 250 },
        "memory_mb": { "type": "integer", "default": 256 }
      },
      "additionalProperties": false
    },
    "env": {
      "type": "object",
      "description": "Key-value environment variables injected into the container.",
      "additionalProperties": { "type": "string" }
    },
    "network": {
      "type": "object",
      "properties": {
        "internal_port": {
          "type": "integer",
          "minimum": 1,
          "maximum": 65535,
          "description": "The port inside the container that the app listens on."
        },
        "route_public": {
          "type": "boolean",
          "description": "Whether to expose the service to Traefik (public/mesh entrypoint)."
        },
        "domain": {
          "type": "string",
          "description": "The base domain for host routing, e.g., local.mesh"
        }
      },
      "required": ["internal_port", "route_public"],
      "additionalProperties": false
    },
    "storage": {
      "type": "object",
      "properties": {
        "enabled": { "type": "boolean" },
        "size_gb": { "type": "integer", "minimum": 1 },
        "mount_path": {
          "type": "string",
          "description": "The absolute path where the volume is mounted inside the container."
        }
      },
      "required": ["enabled"],
      "additionalProperties": false
    }
  },
  "required": ["name", "version", "image", "ui", "resources", "network", "storage"],
  "additionalProperties": false
}
```

### Example Manifest: Uptime Kuma

```json
{
  "name": "uptime-kuma",
  "version": "1.0.0",
  "image": "louislam/uptime-kuma:1",
  "ui": {
    "title": "Uptime Kuma",
    "description": "Self-hosted monitoring tool.",
    "icon": "📈"
  },
  "resources": {
    "cpu_mhz": 200,
    "memory_mb": 256
  },
  "env": {
    "UPTIME_KUMA_PORT": "3001"
  },
  "network": {
    "internal_port": 3001,
    "route_public": true
  },
  "storage": {
    "enabled": true,
    "size_gb": 5,
    "mount_path": "/app/data"
  }
}
```

---

## 3. Sandboxing & Security Safeguards

To prevent external applications from compromising the core cluster, the translation and deployment layers enforce strict boundaries:
1. **No Root Path Manipulation:** Applications can only specify a container-side `mount_path`. Host paths are generated entirely by the manager under `/btrfs_root/volumes/<name>` or the fallback `/opt/nomad/volumes/ext-<name>`. Raw host directories cannot be mounted.
2. **Forced Mesh Bound (Rule 1.1):** Network namespaces are bridge-isolated. All service registrations are automatically constrained to route through `tailscale0`.
3. **Resource Control:** CPU and Memory resource properties are strictly required. Rogue containers are prevented from starving adjacent pipeline services.
4. **Privileged Mode Rejection:** The manager strictly rejects any manifest claiming privileged execution or root capability injection.

---

## 4. Human Operator Guide (CLI Tool)

The manager utility includes a command-line wrapper for human operators to inspect and debug state.

**Note:** Always run with `sudo` if dynamic Btrfs subvolume provisioning is required on the host.

### Subcommand References

#### 1. Install / Update an Application
Creates dynamic storage volumes, generates the Nomad job file, registers inside Traefik and Ouroboros Webring, and deploys the task.
```bash
sudo python3 scripts/app-manager.py install /path/to/manifest.json
```

#### 2. Uninstall & Purge
Stops the container, deletes registered ingress configurations and webring routes, and deprovisions persistent storage volumes (subvolume deletion).
```bash
sudo python3 scripts/app-manager.py uninstall <app_name>
```

#### 3. List Configured Apps
Lists all external applications running on the cluster.
```bash
python3 scripts/app-manager.py list
```

#### 4. Real-time Status Inspect
Queries real-time execution status, allocation states, and health check failures directly from the local scheduler.
```bash
python3 scripts/app-manager.py status <app_name>
```

---

## 5. Agent Integration (Autonomous Operations)

LLM Agents are equipped with the `external_app_manager` tool, enabling them to discover, install, or repair parallel apps.

### Tool Methods Available
- `scaffold_manifest(...)`: Autogenerates a schema-compliant JSON manifest.
- `validate_manifest(manifest_json)`: Performs strict dry-run validation against the JSON Schema.
- `deploy_app(manifest_json)`: Triggers the full lifecycle deployment workflow.
- `purge_app(name)`: Stops, deletes webring routes, and deprovisions storage.
- `list_apps()`: Returns a list of installed external apps.
- `status_app(name)`: Returns real-time health and task state JSON data.

### Expected Agent Behavior Pattern
1. **Scaffold & Customize:** The agent calls `scaffold_manifest` with the base parameters.
2. **Review & Validate:** The agent reviews environment variables, configures correct internal ports, and validates the manifest using `validate_manifest`.
3. **Deploy:** Once the validation is successful, the agent triggers `deploy_app` and prints the success report.
