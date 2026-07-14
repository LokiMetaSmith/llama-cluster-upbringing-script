# AI Agent Integration Handbook: MCP, API, and Package/Plugin Management

This handbook is designed specifically for autonomous and human agents to understand, implement, extend, and manage the Model Context Protocol (MCP), API Gateway Router, and Plugin/Package Management features on this Tailscale mesh-networked cluster.

---

## Table of Contents

- [1. Mixture of Experts (MoE) API Gateway & Router Architecture](#1-mixture-of-experts-moe-api-gateway-router-architecture)
  - [Key Components & Directories:](#key-components-directories)
  - [Operational Workflow for the Router API:](#operational-workflow-for-the-router-api)
- [2. Model Context Protocol (MCP) Integration](#2-model-context-protocol-mcp-integration)
  - [Key Components & Directories:](#key-components-directories)
  - [Creating a New MCP Server (FastMCP Template):](#creating-a-new-mcp-server-fastmcp-template)
- [3. Package & Plugin Management System (External Apps)](#3-package-plugin-management-system-external-apps)
  - [Key Components & Directories:](#key-components-directories)
  - [The Manifest Schema (`manifest.json`):](#the-manifest-schema-manifestjson)
  - [Storage Provisioning Lifecycle:](#storage-provisioning-lifecycle)
- [4. Making Installations Optional (Ansible Toggles)](#4-making-installations-optional-ansible-toggles)
  - [1. Declaring Enablement Variables:](#1-declaring-enablement-variables)
  - [2. Guarding Playbook Roles:](#2-guarding-playbook-roles)
  - [3. Dynamic Host-by-Host Customization:](#3-dynamic-host-by-host-customization)
- [5. Summary Map of Crucial Documentation](#5-summary-map-of-crucial-documentation)

---

## 1. Mixture of Experts (MoE) API Gateway & Router Architecture

The cluster exposes its capabilities using an OpenAI-compatible API Gateway. This architecture allows external clients to interact with a dynamic Mixture of Experts (MoE) backend.

### Key Components & Directories:
- **LiteLLM Proxy Router:** Managed via `ansible/jobs/router.nomad.j2` (runs `litellm` inside Docker). For more details, see [Holistic Project Architecture](ARCHITECTURE.md).
- **API Gateway Service:** Located in `ansible/roles/moe_gateway/` and `pipecatapp/moe_gateway/gateway.py`.
- **System Service Registry:** Consul manages service discovery for expert routes.
- **TwinService Dispatcher:** `pipecatapp/app.py` registers and invokes local or remote expert clients. See also [Project Summary](PROJECT_SUMMARY.md).

### Operational Workflow for the Router API:
1. **Client Call:** The external caller requests `/v1/chat/completions` from the `moe-gateway` service.
2. **Discovery:** `moe_gateway` queries the Consul catalog to discover the active `router-api` (LiteLLM Proxy) and expert endpoints.
3. **Execution:** Requests are routed to LiteLLM, which dynamically forwards prompts to specialized experts (`coding`, `math`, `extract`, etc.) running across GGUF/llama.cpp or vLLM backends.
4. **Hashed Authentication:** Secure token validation is managed via SHA-256 API key matching declared in `group_vars/all.yaml` via `pipecat_api_keys`.

---

## 2. Model Context Protocol (MCP) Integration

The Model Context Protocol (MCP) decouples complex tool actions from the core agent execution loop. Tools run as isolated, standardized JSON-RPC microservices.

### Key Components & Directories:
- **MCP Client Adapter:** `pipecatapp/tools/mcp_client_adapter.py` translates internal Python `Tool` definitions to JSON-RPC over stdio or SSE.
- **Standalone Servers:** Standalone servers are placed in `pipecatapp/servers/` (e.g., `shell_server.py` using `mcp.server.fastmcp.FastMCP`).
- **Nomad/Ansible Deployment:** Configured via the `mcp_server` role (`ansible/roles/mcp_server/`) and templates (`ansible/roles/mcp_server/templates/mcp_server.nomad.j2`).

### Creating a New MCP Server (FastMCP Template):
To register a new tool as an MCP Server:
```python
from mcp.server.fastmcp import FastMCP
import asyncio

# Instantiate the FastMCP server
mcp = FastMCP("my_custom_tool_server")

@mcp.tool()
async def custom_action(param1: str) -> str:
    """
    Perform a custom action with parameter 1.
    """
    # Tool execution logic
    return f"Action complete for {param1}"

if __name__ == "__main__":
    mcp.run()
```
*Note:* Register the new server as a Nomad job so it binds strictly to the `tailscale0` mesh network interface (Rule 1.1) and is discovered dynamically via Consul.

---

## 3. Package & Plugin Management System (External Apps)

The cluster hosts containerized third-party services and extensions alongside the conversational pipeline using a secure Package Manager.

### Key Components & Directories:
- **Core Utility:** `pipecatapp/utils/app_manager.py` (handles manifest validation, HCL generation, storage, and webring sync). See [External Application Hosting & Package Management Guide](EXTERNAL_APP_HOSTING_GUIDE.md) for more comprehensive steps.
- **CLI Utility:** `scripts/app-manager.py` exposes subcommands (`install`, `uninstall`, `list`, `status`) to humans and automation.
- **Agent Tool:** `pipecatapp/tools/external_app_manager_tool.py` exposes the packaging manager directly to the LLM agent.
- **Nomad Templates:** Located in `pipecatapp/nomad_templates/` (e.g., `uptime-kuma.nomad.hcl`, `readeck.nomad.hcl`).

### The Manifest Schema (`manifest.json`):
External apps must define a strict metadata contract:
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

### Storage Provisioning Lifecycle:
1. **Btrfs Check:** The manager runs `findmnt -n -o FSTYPE /btrfs_root` to check if a Btrfs filesystem is mounted.
2. **Subvolume Allocation:** If Btrfs is present, a dedicated subvolume at `/btrfs_root/volumes/<app_name>` is initialized.
3. **Directory Fallback:** If absent, it safely falls back to standard directory mounting at `/opt/nomad/volumes/ext-<app_name>`.

---

## 4. Making Installations Optional (Ansible Toggles)

To prevent resource-exhaustion on low-end nodes (such as Core 2 Duo nodes with 8GB RAM), the installation of complex tools or applications must be optional.

### 1. Declaring Enablement Variables:
All service roles feature standard default toggles inside `group_vars/all.yaml` or their respective defaults folder:
```yaml
# Service Enablement Flags
enable_influxdb: true
enable_telegraf: true
enable_provisioning_api: true
enable_zigbee2mqtt: true
enable_frigate: false
enable_paperless: true
enable_opengist: true
enable_traceway: true
enable_paddler: false
```

### 2. Guarding Playbook Roles:
In the playbook runner (e.g., `playbooks/services/app_services.yaml`), roles are selectively run depending on these variables:
```yaml
    - name: Run Provisioning API
      ansible.builtin.include_role:
        name: provisioning_api
      when: enable_provisioning_api | default(true)
      tags:
        - provisioning_api
```

### 3. Dynamic Host-by-Host Customization:
If an administrator or agent wants to bypass role deployments completely on specific host instances, they should update the local inventory or host vars (e.g., `host_vars/localhost.yaml`) to declare `enable_<role>: false`.

---

## 5. Summary Map of Crucial Documentation

When guiding another agent, point them directly at this document or the following target files:

| Target Context | Primary Documentation File | Secondary Reference |
|---|---|---|
| **Holistic System Architecture** | `docs/manual/ARCHITECTURE.md` | `docs/manual/PROJECT_SUMMARY.md` |
| **Model Context Protocol (MCP)** | `docs/manual/MCP_SERVER_SETUP.md` | `docs/manual/MCP_MIGRATION_PLAN.md` |
| **External Package Manager** | `docs/manual/EXTERNAL_APP_HOSTING_GUIDE.md` | `pipecatapp/utils/app_manager.py` |
| **Agent Operating Instructions** | `AGENTS.md` | `docs/manual/AGENTS.md` |
| **Btrfs Snapshot Recovery** | `docs/manual/PERFORMANCE_OPTIMIZATION.md` | `scripts/recover_os.py` |

By adhering to this modular architecture, any agent can autonomously extend capabilities while respecting strict network isolation boundaries (Rule 1.1) and system constraints.
