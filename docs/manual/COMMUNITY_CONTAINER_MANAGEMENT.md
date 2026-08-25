# Community Container Management System Manual

## Overview

The Community Container Management System expands the Llama Cluster swarm beyond AI inference into hosting, deploying, and managing common open-source homelab, developer, and operational software applications (e.g., Pi-hole, Nextcloud, Vaultwarden, Home Assistant, Gitea).

By leveraging HashiCorp Nomad, Consul Service Mesh, and Traefik dynamic ingress routing, the swarm provides an "app store" experience without secondary orchestrators.

---

## Architecture & Components

```
+-------------------------------------------------------------------------+
|                      PipecatApp Web UI (/apps)                          |
|                       & Interactive Apps CLI                            |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                  PipecatApp REST API (/api/apps/*)                       |
|           [Catalog, Install, Status, Upgrade, Remove, Sync]              |
+------------------------------------+------------------------------------+
                                     |
                                     v
+------------------------------------+------------------------------------+
|               Ansible Deployment & Reconciliation                       |
|                 (playbooks/deploy_community_app.yaml)                   |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                        HashiCorp Nomad Cluster                          |
|    - Dynamic Resource Allocation                                         |
|    - Consul Connect mTLS Sidecars                                       |
|    - Zero-Downtime Canary Updates & Auto-Revert                         |
|    - Persistent Host Volumes (Btrfs)                                    |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                       Consul & Traefik Ingress                          |
|    - Dynamic Health Checking & Catalog Service Discovery                |
|    - Dynamic Domain Routing (Host(`*.local`))                           |
|    - Wildcard TLS Termination from Consul KV Store                      |
+-------------------------------------------------------------------------+
```

---

## 1. Application Catalog

The pre-populated application catalog includes verified community software templates:

| Application ID | Name | Category | Description | Ports | Default Domain |
|---|---|---|---|---|---|
| `pihole` | Pi-hole | Networking & Security | Network-wide ad blocking via DNS sinkhole with web dashboard | 53/UDP, 53/TCP, 80/TCP | `pihole.local` |
| `nextcloud` | Nextcloud | Storage & Collaboration | Self-hosted productivity suite and cloud storage platform | 443/TCP | `nextcloud.local` |
| `vaultwarden` | Vaultwarden | Security & Identity | Lightweight Bitwarden-compatible password manager in Rust | 80/TCP | `vaultwarden.local` |
| `homeassistant` | Home Assistant | Smart Home | Open-source home automation platform focused on local control | 8123/TCP | `homeassistant.local` |
| `gitea` | Gitea | Developer Tools | Painless self-hosted Git service and forge | 3000/TCP, 2222/TCP | `gitea.local` |

---

## 2. REST API Reference

All management routes are hosted by `pipecatapp/web_server.py`. Mutating routes require `admin` or `operator` privileges supplied via the `X-User-Role` header.

* **`GET /api/apps/catalog`**: List pre-populated community application catalog.
* **`POST /api/apps/catalog/sync`**: Sync upstream application catalog metadata feeds. *(Admin only)*
* **`GET /api/apps/installed`**: Retrieve list of active community applications from Nomad and Consul.
* **`GET /api/apps/status/{app_id}`**: Fetch detailed Nomad job specs, allocation tasks, and Consul health check status.
* **`POST /api/apps/install`**: Trigger deployment of a community container application. *(Admin only)*
  * Payload: `{"app_id": "pihole", "domain_name": "pihole.local"}`
* **`POST /api/apps/upgrade`**: Trigger canary update or image upgrade. *(Admin only)*
  * Payload: `{"app_id": "pihole", "target_image": "pihole/pihole:latest"}`
* **`DELETE /api/apps/remove/{app_id}`**: Purge and stop the specified community application job. *(Admin only)*

---

## 3. Command-Line Interface (CLI)

Manage community applications directly from the terminal using `scripts/pipecat_apps_cli.py`:

```bash
# List available application catalog
python3 scripts/pipecat_apps_cli.py catalog

# List currently installed applications
python3 scripts/pipecat_apps_cli.py list

# Install an application
python3 scripts/pipecat_apps_cli.py install pihole --domain pihole.local

# Check status details
python3 scripts/pipecat_apps_cli.py status pihole

# Upgrade an application
python3 scripts/pipecat_apps_cli.py upgrade pihole --image pihole/pihole:latest

# Remove/purge an application
python3 scripts/pipecat_apps_cli.py remove pihole
```

---

## 4. Operational MCP Servers

The system integrates four microservices in `tools/mcp-*/`:

1. **Slack Operations Server (`tools/mcp-slack/index.js`)**: Sends operational alerts and status messages to Slack channels.
2. **Stripe Ledger Server (`tools/mcp-stripe/server.py`)**: Computes monthly burn rate, revenue metrics, and runway calculations.
3. **Gmail Lead Monitor (`tools/mcp-google/gmail_server.py`)**: Scans inbound email queries for customer leads.
4. **Google Drive Sync Server (`tools/mcp-google/drive_server.py`)**: Synchronizes document templates.

---

## 5. Day-2 Operations & Self-Healing

* **Autonomous Health Monitor (`pipecatapp/services/app_health_monitor.py`)**: Polls Consul and Nomad APIs every 5 minutes. If a job enters a `dead` or `degraded` state, it automatically triggers Ansible reconciliation.
* **Btrfs Volume Snapshot Backups (`playbooks/ops/btrfs_community_apps_snapshot.yaml`)**: Archives host volumes (`/var/lib/pihole`, `/data`, etc.) and optionally syncs backup archives to remote S3 or Backblaze B2 buckets.
* **TLS Certificate Provisioning (`playbooks/services/provision_community_tls.yaml`)**: Stores wildcard certificate authority keys into Consul KV (`certs/mesh/tls.crt` / `tls.key`) for Traefik HTTPS ingress termination.
