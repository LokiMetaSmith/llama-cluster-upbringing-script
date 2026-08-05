# DESFire EV2 Cluster Integration

This document outlines the setup and testing procedures for the multi-application tap system using MIFARE DESFire EV2 authenticated wall-plate readers.

## Overview

The `tap_orchestrator` service listens for authenticated tap events originating from wall-plate readers (ESP32) and USB server daemons. Upon a successful hardware authentication, the orchestrator:
1. Validates the incoming MQTT payload.
2. Identifies the user via the Authentik core API to determine cluster access rights and attributes.
3. Orchestrates cluster startup routines (Wake-on-LAN, Nomad mounts, and ephemeral Vault credentials) mapping to the user's requirements.

## Environment Variables

The service relies on `.env` files for secrets and dynamic configuration. Copy `.env.example` to `.env` and populate the values:

```bash
cp .env.example .env
```

| Variable | Description | Default |
| --- | --- | --- |
| `MQTT_BROKER_HOST` | Local MQTT Broker address | 127.0.0.1 |
| `MQTT_TOPIC_SUCCESS` | Topic for authenticated taps | tagreader/auth/success |
| `AUTHENTIK_API_URL` | Authentik instance API URL | http://127.0.0.1:9000 |
| `AUTHENTIK_CLIENT_ID` | OAuth2 Client ID | - |
| `AUTHENTIK_CLIENT_SECRET` | OAuth2 Client Secret | - |
| `AUTHENTIK_TOKEN` | (Optional) Static Bearer Token for dev | - |
| `TAP_ORCHESTRATOR_SECRET` | Secret header for `/api/v1/tap-event` | change_me_secret |

## Cluster Resource Mapping

The service requires a `config.yaml` to map `user_id` values to their designated cluster resources.

Example `config.yaml`:
```yaml
CLUSTER_RESOURCE_MAP:
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
