# Headscale - Self-Hosted Mesh & Attestation Authority

## Overview
Headscale provides a self-hosted control plane for Tailscale network meshes. Within the `llama-cluster` architecture, Headscale functions as the **autonomous attestation authority**.

## Sovereignty & Attestation Architecture
* **Bypassing External Attestation Traps:** Third-party managed control planes (such as corporate Tailscale SaaS or cloud IDPs) may enforce remote OS attestation or device posture compliance that locks out custom Linux kernels and experimental bare-metal nodes.
* **Internal Control:** By hosting our own Headscale control plane and internal CA, node mesh registration and authorization remain 100% self-sovereign.
* **Pre-Auth Key Generation & Node Registration:** Autonomous nodes register via self-generated pre-auth keys, while human access can optionally integrate with local OIDC (Authentik) with FIDO2 MFA.

## Configuration
Default variables are stored in `defaults/main.yaml`:
* `headscale_version`: Version of Headscale binary deployed.
* `headscale_port`: Control plane HTTP API port (default: 8085).
* `headscale_ip_prefix`: Tailnet IP space allocation (default: 100.64.0.0/10).
