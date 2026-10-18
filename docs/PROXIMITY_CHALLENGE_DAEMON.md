# Proximity Challenge-Response Daemon

This document details the architecture, integration, and usage of the Proximity Challenge-Response Daemon added to the `tap_orchestrator` service. This daemon is designed to bridge hardware-anchored identity, spatial presence detection, and mutual credit resource allocation (REA) within the cluster.

## Overview

To treat compute as a fundamental right regulated by interactive value, the Pipecatapp cluster utilizes physical presence as an identity factor. When an agent or user enters a room equipped with boundary nodes (e.g., UWB or NFC readers), they can authenticate their identity and secure real-time compute resource prioritization dynamically.

The Challenge-Response daemon implements a "Something You Have" (a hardware token holding a private key) proximity verification flow.

1. **Challenge Generation:** An entry node requests a cryptographic challenge bound to a specific room.
2. **Device Attestation:** The user's hardware signs the challenge using its Secure Element.
3. **Verification & Accounting:** The cluster verifies the signature, updates the user's presence, recalculates their available compute credit via the Datalog Engine, and propagates this compute weight across the cluster via Consul.

## Component Integration

The Proximity Challenge-Response logic is integrated directly into the `services/tap_orchestrator/main.py` service. It bridges the following existing primitives:
* **Cryptographic Identity:** Uses `pipecatapp.atproto_crypto.verify_payload` to handle decentralized identifier (DID) and signature validation.
* **REA Accounting Ledger:** Connects to `pipecatapp.datalog_engine.DatalogEngine` to log presence interactions and determine dynamic credit weights.
* **Consul Fast State:** Writes real-time active compute weight into `pipecatapp.memory_backends_impl.consul_kv_backend.ConsulKVBackend` so that orchestration components like `queue_manager.py` and `moe_gateway` can allocate priorities dynamically.

## API Usage

The Daemon exposes two main REST endpoints over HTTP/FastAPI.

### 1. `GET /api/v1/challenge`

Generates an ephemeral, randomized cryptographic challenge nonce bound to the requesting room.

**Request:**
```http
GET /api/v1/challenge?room_id=room_101
```

**Response (200 OK):**
```json
{
  "nonce": "c4d5a9b8e2f1...",
  "room_id": "room_101",
  "expires_in": 10
}
```

*Notes:* Nonces have a strict time-to-live (default 10 seconds) to prevent replay attacks.

### 2. `POST /api/v1/verify`

Validates the signed payload from the device and allocates compute right weight to the user.

**Request:**
The device signs a deterministic JSON representation of `{"challenge_nonce": "...", "room_id": "..."}`.
```http
POST /api/v1/verify
Content-Type: application/json

{
  "did": "did:example:12345",
  "challenge_nonce": "c4d5a9b8e2f1...",
  "signature": "base64_encoded_signature...",
  "room_id": "room_101",
  "public_key_hex": "04a1b2c3d4..."
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Presence verified and compute weight allocated.",
  "weight": 95.5
}
```

### 3. Compute Weight Allocation

Behind the scenes, a successful `/verify` call triggers the following logic:

1. **Assertion:** `datalog.assert_fact("presence", request.did, request.room_id, now)` is called, logging the interaction event to the REA ledger.
2. **Calculation:** The Datalog Engine evaluates `get_available_credit(request.did)` to resolve the active mutual credit score, applying decay/demurrage logic.
3. **State Sync:** The resulting float value is written to the Consul Key-Value store at the path `swarm/compute_rights/<did>`.

Cluster execution mechanisms (like `queue_manager.py`) continually poll `swarm/compute_rights/` via Consul to allocate hardware resources (e.g. LLM routing priority, concurrent Nomad scaling) based on this derived value.

## Testing

You can manually trigger tests and verification to ensure integration remains healthy using standard Pytest execution.

```bash
uv run --no-sync python -m pytest tests/test_tap_orchestrator_challenge.py
```

## Reference Implementations

We provide two reference implementations demonstrating how to interact with this daemon using different hardware profiles. These can be found in `examples/proximity_hardware_reference/`:

1. **Python Client (`python_token.py`)**: Demonstrates the full flow (generating a SECP256R1 keypair, requesting a challenge, deterministically signing the JSON payload, and submitting verification) using standard `cryptography` and `httpx` libraries. Ideal for Raspberry Pi or capable smart badges.
2. **ESP32 Arduino (`esp32_reader.ino`)**: A low-level C++ implementation for ESP32 microcontrollers. It uses `mbedtls` for hardware-accelerated ECDSA cryptography and deterministic DER signature formatting. Ideal for embedding into wall-plates or ultra-low-power BLE/UWB tags.
