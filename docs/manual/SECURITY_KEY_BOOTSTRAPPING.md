# Security Key Bootstrapping and Cluster Access

This document details the hybrid architecture for incorporating FIDO/FIDO2 hardware security keys into the cluster provisioning and access workflow. It provides robust security for both interactive human administrators and automated, machine-to-machine interactions.

## Table of Contents

- [1. Overview](#1-overview)
- [2. Human Access: OIDC & FIDO2 Enforcement](#2-human-access-oidc--fido2-enforcement)
  - [2.1. Headscale (Tailnet) Enrollment](#21-headscale-tailnet-enrollment)
  - [2.2. Consul ACL Authentication](#22-consul-acl-authentication)
- [3. Machine-to-Machine: Automated Bootstrapping](#3-machine-to-machine-automated-bootstrapping)
  - [3.1. Headscale Pre-Auth Keys](#31-headscale-pre-auth-keys)
  - [3.2. Consul ACL Tokens](#32-consul-acl-tokens)
- [4. Direct Node Access: Declarative SSH Keys](#4-direct-node-access-declarative-ssh-keys)

---

## 1. Overview

The cluster utilizes two distinct authentication flows depending on the context:

1. **Human/Interactive Flow:** Leverages OpenID Connect (OIDC) through Authentik, mandating the use of physical FIDO2 keys (like YubiKeys or Google Titan keys) via WebAuthn for enrolling user devices onto the Tailnet or accessing management interfaces like Consul.
2. **Machine/Automated Flow:** Relies on robust, securely generated tokens (Headscale Pre-Auth keys, Consul ACL tokens) stored in Ansible Vault to completely bypass human interaction during bare-metal provisioning and Nomad job deployments.

---

## 2. Human Access: OIDC & FIDO2 Enforcement

For administrators and developers, services are integrated with Authentik via OIDC. Authentik is configured to enforce multi-factor authentication (MFA) utilizing FIDO2/WebAuthn.

This provides three layers of identity and access management for humans:

1. **SSO and Authorization Injection:** Authentik seamlessly injects authorization headers, preventing the need to manually enter application API keys.
2. **FIDO2 Hardware Key Registration:** Users can independently register and provision new FIDO2 security keys through the internal Authentik user portal.
3. **Fallback Authentication:** In the event a hardware key is lost or unavailable, users can securely fall back to an Authentik-managed password paired with TOTP.

### 2.1. Headscale (Tailnet) Enrollment

When a user attempts to join a new device to the cluster mesh network:

1. The user runs `tailscale up --login-server=https://headscale.local.mesh`.
2. Tailscale generates an interactive authentication link.
3. The user visits the link, which redirects them to Authentik (via OIDC).
4. The user authenticates with their credentials and taps their physical FIDO2 key.
5. Upon successful WebAuthn verification, Headscale registers the node and it joins the overlay network.

### 2.2. Consul ACL Authentication

Consul's ACL system is configured with an OIDC Auth Method mapping back to Authentik:

1. Accessing the Consul UI or requesting a CLI token using `consul login -type=oidc` triggers an OIDC flow.
2. The user is redirected to Authentik, where they must authenticate and provide physical presence via their FIDO2 key.
3. Consul grants a time-bound ACL token based on the user's mapped roles in Authentik.

### 2.3. Internal Web Services (Traefik ForwardAuth)

Internal application UIs (such as the Pipecat App, Nanochat, OpenGist, and Paperless) do not expose their own authentication barriers. Instead, they are protected at the mesh edge via a **Traefik ForwardAuth** middleware constraint.

1. A user navigates to an internal service (e.g., `https://pipecatapp.local.mesh`).
2. The Traefik reverse proxy intercepts the request and forwards it to the Authentik outpost.
3. Authentik challenges the user (FIDO2 tap).
4. Upon success, Authentik redirects the traffic back to the destination service, injecting identity headers (`X-authentik-username`, etc.) to facilitate zero-touch application access.

---

## 3. Machine-to-Machine: Automated Bootstrapping

Physical key taps are impossible during automated provisioning (e.g., PXE booting a new worker node). The system uses pre-generated, strict credentials managed by Ansible to ensure security without human intervention.

### 3.1. Headscale Pre-Auth Keys

During the `tailscale` Ansible role execution, new nodes must join the mesh network to establish the `cluster_ip`.

- **Mechanism:** Headscale pre-auth keys are generated (e.g., via the Headscale CLI on a controller node) and stored securely (ideally within Ansible Vault).
- **Execution:** The provisioning playbook executes `tailscale up --authkey <PRE_AUTH_KEY>`, silently authenticating the machine and joining it to the tailnet without triggering the OIDC flow.
- **Security:** These keys are typically ephemeral, scoped to specific namespaces, and heavily restricted in lifespan.

### 3.2. Consul ACL Tokens

Similarly, Nomad jobs and automated scripts require communication with the Consul service mesh.

- **Mechanism:** The initial Consul bootstrap process generates a master token. This token is used programmatically to create scoped, role-specific ACL tokens for internal infrastructure traffic.
- **Execution:** These specific tokens are injected into Nomad job definitions and systemd unit files via Ansible templates.
- **Security:** This isolates machine traffic from the human OIDC flow, ensuring the cluster can self-heal and orchestrate jobs without requiring manual FIDO2 validation for internal actions.

---

## 4. Direct Node Access: Declarative SSH Keys

While Tailscale provides the secure overlay, direct SSH access to nodes is governed declaratively via Ansible. This includes support for FIDO2-backed OpenSSH keys.

1. Administrators generate a FIDO2 SSH key locally: `ssh-keygen -t ed25519-sk`.
2. The resulting public key string (e.g., `sk-ssh-ed25519@openssh.com AAAA...`) is added to the `fido_ssh_keys` list in `group_vars/all.yaml`.
3. The `common-tools` Ansible role ensures that any defined FIDO keys are appended to the `authorized_keys` file for the primary `target_user` on every node, allowing hardware-backed SSH authentication.
