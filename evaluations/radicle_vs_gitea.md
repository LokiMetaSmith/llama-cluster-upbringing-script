# Radicle vs. Gitea: Git Backbone Evaluation

## 1. Overview and Objectives

This evaluation compares **Radicle** and **Gitea** as candidates for a self-hosted, local-first Git backbone. The primary objective is to eliminate dependencies on external cloud hosting while evaluating resilience against local network partitioning and multi-node LAN synchronization without requiring internet access. This backbone must also support automated agent/CI workflows triggered within the local cluster.

## 2. Architectural Comparison

| Feature / Dimension | **Radicle** (P2P / Local-First) | **Gitea** (Self-Hosted Central Forge) |
| --- | --- | --- |
| **Topology** | Fully peer-to-peer gossip network (`radicle-node`) using Git objects & CRDTs (COBs). | Traditional Client-Server architecture (HTTP/SSH daemon with SQL backend). |
| **Offline Resilience** | **Complete:** All code, issues, and patches exist locally and sync asynchronously. | **Partial:** Standard Git offline operations; web UI/issues require connectivity to the server. |
| **Identity & Auth** | Cryptographic keypairs (Ed25519/DID). | Standard OIDC / OAuth2 / LDAP / Local Accounts. |
| **Cluster Fit (Nomad/Consul)** | Run as a seed node daemon; naturally pairs with distributed mesh/IPFS swarms. | Standard stateless/stateful Nomad service registered in Consul with SQLite/Postgres backend. |
| **CI/CD & Automation** | Event-driven CI broker (`cib`) with custom adapters. | Built-in Gitea Actions (GitHub Actions compatible syntax via `act_runner`). |
| **Footprint** | Extremely lightweight Rust binary. | Lightweight single Go binary. |

## 3. Priority Criteria Analysis

### 3.1. Local-first & Offline Survivability
*   **Radicle:** Radicle truly shines in this category. Built on a P2P gossip network, it guarantees complete offline survivability. Every node contains the full repository data, including issues and pull requests (stored as Collaborative Objects - COBs). If the local network partitions, developers can still fully interact with issues and code locally. When connectivity is restored, the gossip protocol natively synchronizes state.
*   **Gitea:** Gitea follows the traditional Git client-server model. While standard Git operations (commit, log) work offline, all meta-operations (issues, PRs, Web UI, CI status) depend on reaching the central Gitea server. A network partition isolating the server immediately halts these workflows for the disconnected nodes.

### 3.2. Resource Overhead and Container Footprint
*   **Radicle:** Extremely lightweight. Written in Rust, both the node daemon and the HTTP daemon consume very minimal CPU and memory.
*   **Gitea:** Also very lightweight for a centralized forge. Written in Go, it can easily run with minimal resources, especially when using the SQLite backend instead of PostgreSQL for smaller deployments.

### 3.3. Programmatic API Access for Autonomous Agents
*   **Radicle:** Interacting with Radicle programmatically often involves using its CLI tool (`rad`) locally on the machine where the node runs, or communicating with the local HTTP daemon. The P2P nature means agents act more like individual peers pushing changes to the network.
*   **Gitea:** Provides a comprehensive, standard REST API (and some GraphQL support) that most CI/CD tools and autonomous agents natively understand. Integration with Gitea is typically much more straightforward for existing tooling that expects a GitHub/GitLab-style API.

### 3.4. CI/CD Runner Flexibility
*   **Radicle:** Uses an event-driven CI broker (`cib`). When events happen on the node, the broker triggers custom adapters. While highly flexible, it currently requires more custom wiring to integrate with standard CI runners compared to centralized forges.
*   **Gitea:** A massive advantage for Gitea is its built-in Gitea Actions, which uses `act_runner`. This provides a GitHub Actions-compatible syntax, allowing the reuse of thousands of existing GitHub Actions steps. This significantly reduces the friction of setting up automated agent workflows.

### 3.5. Identity & Access Management
*   **Radicle:** Relies strictly on cryptographic keypairs (Ed25519) and Decentralized Identifiers (DIDs). There is no central user database. While highly secure and decentralized, it completely bypasses traditional enterprise identity systems.
*   **Gitea:** Natively supports OIDC, OAuth2, and LDAP. It can seamlessly integrate with the existing cluster infrastructure (e.g., Authentik), providing single sign-on (SSO) and centralized access management.

## 4. Proof-of-Concept Integration (Nomad/Consul)

We have created PoC Nomad job specifications for both solutions to demonstrate how they fit into the cluster infrastructure.

### 4.1. Gitea PoC (`evaluations/configs/gitea.nomad`)
The Gitea Nomad job defines a standard service running the `gitea/gitea` Docker container.
*   **Storage:** It uses a Nomad host volume (`gitea_data`) to persist the SQLite database and Git repositories, ensuring data survives container restarts.
*   **Discovery:** It registers both HTTP (port 3000) and SSH (port 2222) services in Consul, making Gitea reachable at `gitea.service.consul`.
*   **Integration:** It natively fits the standard centralized service model deployed across the cluster.

### 4.2. Radicle PoC (`evaluations/configs/radicle.nomad`)
The Radicle Nomad job defines a "seed node" deployment.
*   **Architecture:** It runs two tasks within a single group: `radicle-node` (the P2P gossip daemon on port 8776) and `radicle-httpd` (providing a read-only web interface and API on port 8080).
*   **Storage:** It uses a host volume (`radicle_data`) for the `.radicle` home directory.
*   **Discovery:** It registers the node and HTTP services in Consul.
*   **Integration:** In the cluster context, this job acts as an "always-on" seed node to ensure high availability of the repositories, while individual developer machines or agents would run their own local Radicle nodes to gossip with this seed.

## 5. Hybrid Architecture Recommendation

Instead of forcing an all-or-nothing tradeoff between Gitea's integration capabilities and Radicle's true offline resilience, running both in a **hybrid architecture** provides the best of both worlds.

### 5.1. How the Hybrid Architecture Works

```
                     +---------------------------------------+
                     |         Authentik (OIDC / SSO)        |
                     +-------------------+-------------------+
                                         |
                                         v
   +-------------------------------------------------------------------------+
   |                        Gitea (Nomad Service)                            |
   |  - Web UI & Central Repository Forge                                    |
   |  - REST/GraphQL API for autonomous AI agents                            |
   |  - Gitea Actions (act_runner) for automated CI/CD pipelines             |
   +-------------------------------------+-----------------------------------+
                                         |
                       (Git Hook / Action Push Mirror)
                                         |
                                         v
   +-------------------------------------------------------------------------+
   |                    Radicle Seed Node (Nomad Service)                    |
   |  - P2P Gossip Daemon (`radicle-node`) & Seed HTTP API                   |
   |  - Offline survivability & cryptographic keypair DID identity           |
   |  - Async LAN sync across isolated/partitioned nodes & IPFS mesh         |
   +-------------------------------------------------------------------------+
```

### 5.2. Why Running Both Makes Sense

1.  **Gitea Handles Cluster Ergonomics & Automation:**
    *   **Central Identity & Access:** Natively integrates with **Authentik** for single sign-on across the cluster.
    *   **Agent API & CI/CD:** Agents can use standard GitHub/GitLab-style REST APIs and trigger **Gitea Actions** (`act_runner`) for containerized builds and test suites.

2.  **Radicle Handles Network Partitioning & True Decentralization:**
    *   **Local-First & Offline Workflows:** When cluster nodes or development machines disconnect from the central network, developers and agents can continue committing, creating patches, and tracking issues locally via Radicle Collaborative Objects (COBs).
    *   **Automatic Gossip Sync:** Once reconnected to the LAN or IPFS mesh, the Radicle nodes automatically gossip and reconcile state.

3.  **Negligible Resource Overhead:**
    *   **Gitea** (Go) + **Radicle** (Rust) combined consume **less than 750 MB of RAM** and negligible idle CPU, making them well within the capacity of a lightweight Nomad cluster.

### 5.3. Recommended Integration Pattern

*   **Primary Forge / CI Hub:** Gitea serves as the canonical web forge registered in Consul (`gitea.service.consul`).
*   **Auto-Mirroring to Radicle:** A simple Gitea webhook or server-side `post-receive` Git hook runs `rad push` / `rad sync` on the local Radicle seed node upon every merge.
*   **Dual Remotes:** Workstations and agent environments can configure `origin` to point to Gitea for standard CI pipelines and `rad` as a fallback peer remote for zero-infrastructure offline sync.

### 5.4. Conclusion

By deploying both Gitea and Radicle as Nomad services, the cluster achieves a highly robust Git backbone. Gitea provides the necessary tooling, standard APIs, and familiar UI required for efficient AI agent integration and developer workflows, while Radicle acts as an invisible, decentralized failover mesh ensuring absolute data survivability and offline capability during network partitions.
