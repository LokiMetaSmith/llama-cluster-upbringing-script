# DESFire EV2 Cluster Integration

This document outlines the setup and testing procedures for the multi-application tap system using MIFARE DESFire EV2 authenticated wall-plate readers.

## Overview

The `tap_orchestrator` service listens for authenticated tap events originating from wall-plate readers (ESP32) and USB server daemons. Upon a successful hardware authentication, the orchestrator:
1. Validates the incoming MQTT payload.
2. Identifies the user via the Authentik core API to determine cluster access rights and attributes.
3. Orchestrates cluster startup routines (Wake-on-LAN, Nomad mounts, and ephemeral Vault credentials) mapping to the user's requirements.

## Configuration

The service configuration is managed centrally by Ansible.
The Webhook Secret is sourced from the `tap_orchestrator_secret` variable in `group_vars/all.yaml` (or vaulted files).

### Environment Variables

During Ansible deployment, the Nomad job (`tap_orchestrator.nomad.j2`) automatically passes the required environment variables to the python service:

| Variable | Description | Default |
| --- | --- | --- |
| `MQTT_BROKER_HOST` | Local MQTT Broker address | `{{ cluster_ip }}` |
| `MQTT_TOPIC_SUCCESS` | Topic for authenticated taps | `tagreader/auth/success` |
| `AUTHENTIK_API_URL` | Authentik instance API URL | `http://{{ cluster_ip }}:9000` |
| `AUTHENTIK_CLIENT_ID` | OAuth2 Client ID | dynamically sourced from Consul KV |
| `AUTHENTIK_CLIENT_SECRET` | OAuth2 Client Secret | dynamically sourced from Consul KV |
| `TAP_ORCHESTRATOR_SECRET` | Secret header for `/api/v1/tap-event` | `{{ tap_orchestrator_secret }}` |

## Cluster Resource Mapping

The mapping of `user_id` values to designated cluster resources is defined in `group_vars/all.yaml` under `tap_cluster_resource_map`. Ansible templates this into the `config.yaml` file used by the orchestrator.

Example `group_vars/all.yaml`:
```yaml
tap_cluster_resource_map:
  lawrence:
    gpu_node: "node-gpu-01"
    mac_address: "AA:BB:CC:DD:EE:FF"
    models: ["llama-3-8b"]
```

## Manual Testing

You can simulate a wall-plate hardware authentication tap event by publishing a JSON payload to the local Mosquitto broker:

```bash
# Test successful tap
mosquitto_pub -h 127.0.0.1 -p 1883 -t "tagreader/auth/success" -m '{"event": "desfire_authenticated", "user_id": "lawrence", "reader_id": "front_door_plate", "timestamp": 1785860545, "auth_type": "desfire_ev2_aes128"}'
```

To test the fallback HTTP Webhook endpoint:
```bash
curl -X POST http://127.0.0.1:8011/api/v1/tap-event \
  -H "Content-Type: application/json" \
  -H "X-Tap-Secret: your_secure_webhook_secret" \
  -d '{"event": "desfire_authenticated", "user_id": "lawrence", "reader_id": "api_test", "timestamp": 1785860545, "auth_type": "desfire_ev2_aes128"}'
```
