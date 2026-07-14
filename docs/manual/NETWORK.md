# Network Architecture

The cluster utilizes a **Tiered Network Architecture** designed to support nodes throughout their entire lifecycle, from bare-metal provisioning to production service mesh participation.

This design separates the **hardware initialization** phase from the **application runtime** phase.

## Table of Contents

- [Mental Model: Underlay vs. Overlay](#mental-model-underlay-vs-overlay)
  - [1. The Provisioning Underlay (`10.0.0.x`)](#1-the-provisioning-underlay-1000x)
  - [2. The Cluster Overlay (`100.64.x.y`)](#2-the-cluster-overlay-10064xy)
  - [Visual Diagram](#visual-diagram)
- [Technical Implementation](#technical-implementation)
  - [1. Network Segmentation](#1-network-segmentation)
    - [A. Provisioning Underlay (10.0.0.x)](#a-provisioning-underlay-1000x)
    - [B. Cluster Overlay (Tailscale)](#b-cluster-overlay-tailscale)
  - [2. Variable Logic (`group_vars/all.yaml`)](#2-variable-logic-group_varsallyaml)
  - [3. Service Configuration](#3-service-configuration)
    - [Consul & Nomad](#consul-nomad)
  - [4. Addressing Scheme (Fallback/Underlay)](#4-addressing-scheme-fallbackunderlay)

---

## Mental Model: Underlay vs. Overlay

To understand this structure, visualize the network as two distinct layers:

### 1. The Provisioning Underlay (`10.0.0.x`)

* **What it is:** The "Hardware-Level" network. It operates on Layer 2 (LAN) and does not rely on complex software stacks.
* **Primary Role:** **Bootstrapping & Fallback.**
* **Key Use Case:** **PXE Booting.** New nodes (defined in `pxe_subnet`) need a simple, deterministic local network to pull boot images and initial configurations before an OS is installed. See [iPXE Boot Server Setup](PXE_BOOT_SETUP.md) and [NixOS-based PXE Boot Server Setup](NIXOS_PXE_BOOT_SETUP.md) for details on provisioning.
* **Why not Tailscale?** Tailscale requires an OS and a running daemon. You cannot easily use it inside an iPXE environment or during the early stages of an OS install.
* **Secondary Role:** Functions as a "Backstage" sync channel if the internet is down or the overlay mesh fails.

### 2. The Cluster Overlay (`100.64.x.y`)

* **What it is:** The "Production-Level" network provided by **Tailscale**.
* **Primary Role:** **Secure Service Mesh.**
* **Key Use Case:** Secure, encrypted communication between Nomad, Consul, and application services.
* **Behavior:** Once a node is fully provisioned and the Tailscale daemon starts, the system promotes this interface to be the primary `cluster_ip`.
* **Reachability:** Enables seamless cross-site connectivity (e.g., spanning different physical locations or subnets) without complex firewall rules. See [AI Cluster Network Isolation Guide](NETWORK_ISOLATION.md) for recommendations on securing and isolating the cluster mesh network, and [Cluster Load Testing and Network Validation](LOAD_TESTING.md) for diagnostics.

### Visual Diagram

```mermaid
graph TD
    subgraph Physical_Layer ["Physical Layer (Hardware)"]
        Node_HW[Bare Metal Node]
        Switch[Local Network Switch]
    end

    subgraph Provisioning_Underlay ["Provisioning Underlay (10.0.0.x)"]
        direction TB
        PXE_Server[PXE Server<br>10.0.0.1]
        DHCP[DHCP Service]
        Boot_Traffic[Boot Images / Configs]
    end

    subgraph Cluster_Overlay ["Cluster Overlay (Tailscale 100.64.x.y)"]
        direction TB
        Consul[Consul Service Mesh]
        Nomad[Nomad Scheduling]
        App_Traffic[Encrypted App Traffic]
    end

    %% Connections
    Node_HW <--> Switch
    Switch <--> PXE_Server

    Node_HW -. "PXE Boot (Layer 2)" .-> Provisioning_Underlay
    Node_HW == "WireGuard Tunnel (Layer 3)" ==> Cluster_Overlay

    %% Styling
    style Provisioning_Underlay fill:#e1f5fe,stroke:#01579b
    style Cluster_Overlay fill:#f3e5f5,stroke:#4a148c
    style Physical_Layer fill:#fff3e0,stroke:#e65100
```

---

## Technical Implementation

### 1. Network Segmentation

#### A. Provisioning Underlay (10.0.0.x)

* **Interface:** Physical Ethernet or Bridge.
* **Addressing:** Static or DHCP reserved based on MAC address.
* **Status:** Always available (Layer 2).

#### B. Cluster Overlay (Tailscale)

* **Interface:** `tailscale0`
* **Addressing:** CGNAT range (`100.64.0.0/10`) assigned by Tailscale.
* **Status:** Available post-boot.

### 2. Variable Logic (`group_vars/all.yaml`)

The system dynamically selects the `cluster_ip` based on the node's state:

1. **Check for Tailscale:** If the `tailscale0` interface exists, its IP is used as the `cluster_ip`.
2. **Fallback:** If `tailscale0` is missing (e.g., during early boot or if Tailscale is disabled), it falls back to the static `10.0.0.x` alias derived from the hostname.

```yaml
# Simplified Logic
cluster_ip: "{{ ansible_facts.get('tailscale0', {}).get('ipv4', {}).get('address', '10.0.0.' + node_id) }}"
```

### 3. Service Configuration

#### Consul & Nomad

* **Bind Address:** `cluster_ip` (Prefers Tailscale).
* **Benefit:** Traffic between nodes is automatically encrypted by WireGuard (Tailscale), removing the need for complex mTLS setups for basic node-to-node security.

### 4. Addressing Scheme (Fallback/Underlay)

When operating on the underlay, nodes use a deterministic ID:

| Hostname | Node ID | Underlay IP | Role |
| :--- | :--- | :--- | :--- |
| `devbox` | 10 | `10.0.0.10` | Single-node Dev Cluster |
| `worker1` | 11 | `10.0.0.11` | Worker Node |
| `pxe-server` | 1 | `10.0.0.1` | PXE / Gateway |

**Formula:** `Underlay IP = "10.0.0." + node_id`
