# SPIFFE/SPIRE Integration PoC

## 1. Overview
SPIFFE (Secure Production Identity Framework for Everyone) provides a secure identity, in the form of a specially crafted X.509 certificate (or JWT), to every workload in a modern production environment. SPIRE (the SPIFFE Runtime Environment) is a toolchain of APIs for establishing trust between software systems across a wide variety of hosting platforms. It implements the SPIFFE specification and issues short-lived cryptographic identities (SVIDs) to workloads.

The objective of this Proof of Concept (PoC) is to research integrating SPIFFE/SPIRE with our existing Nomad/Consul cluster. This will provide cryptographic identities to individual agent allocations, enabling zero-trust communication and precise authentication across the distributed AI pipeline.

## 2. SPIRE Architecture on Nomad
A SPIRE deployment consists of a SPIRE Server and one or more SPIRE Agents.

- **SPIRE Server:** Manages the identity control plane. It signs SVIDs, manages the registration entries defining which workloads get which identities, and coordinates with external systems via Node and Workload Attestors. On Nomad, the SPIRE Server runs as a centralized service or a highly available quorum.
- **SPIRE Agent:** Runs on every node in the cluster. It talks to the SPIRE Server to obtain an identity for the node itself, then exposes the SPIFFE Workload API locally (via a Unix Domain Socket). When a workload (e.g., a Nomad task) requests an identity, the Agent verifies the workload's properties using Workload Attestors (like the Unix/Docker attestors) against registered entries.

To deploy on Nomad:
1.  **SPIRE Server Job:** Run `spire-server` using the Nomad Docker or exec driver.
2.  **SPIRE Agent System Job:** Run `spire-agent` as a `system` job on all Nomad clients. The agent requires host path mounting to expose the Workload API socket (`/tmp/agent.sock` or `/run/spire/sockets/agent.sock`) to local tasks.

## 3. Integrating SPIRE with Consul Service Mesh
Consul Connect (Service Mesh) can be configured to use SPIRE as its Certificate Authority (CA).

- Instead of Consul's built-in CA, Consul can be configured to integrate with SPIFFE.
- Consul proxies (Envoy sidecars) request TLS certificates. With SPIRE integration, the identities mapped in Consul directly correspond to SPIFFE IDs.
- By configuring Consul to use an external SPIFFE/SPIRE provider, agent-to-agent communication governed by Consul service mesh automatically leverages the cryptographic SVIDs issued by SPIRE.

## 4. Providing SVIDs to Agent Allocations
Within the Nomad cluster, each AI expert or task (e.g., `llama-expert.nomad`, `TwinService`) needs its own cryptographic identity.

1.  **Workload API Mounting:** The Nomad task specification must mount the SPIRE Agent's Unix Domain Socket.
    ```hcl
    volume_mount {
      volume      = "spire-agent-socket"
      destination = "/run/spire/sockets"
      read_only   = true
    }
    ```
2.  **Registration Entries:** The SPIRE Server must be configured with registration entries that map Nomad tasks to SPIFFE IDs. E.g., `spiffe://cluster.local/ns/nomad/job/llama-expert`. This mapping can be managed using the SPIRE Server API.
3.  **Workload Attestation:** The SPIRE Agent needs an attestor that understands Nomad. While SPIRE has built-in Unix/Docker attestors, utilizing a specific Nomad workload attestor (if available or written as a plugin) ensures tight coupling with Nomad's security properties.
4.  **Agent Application Changes:** The Python-based AI tools and services must fetch their SVID from the local Workload API. This can be done using the `pyspiffe` library. They use this SVID to authenticate requests when invoking other tools or communicating with the orchestration router, establishing a cryptographic receipt for tool execution.

## 5. Pros and Cons of SPIFFE/SPIRE Integration

### Pros (Why we should implement it)
- **True Zero-Trust Security:** It shifts the trust boundary from the network (e.g., VPNs, firewalls, IP boundaries) directly to the workload itself. If a node is compromised, the blast radius is strictly limited to the permissions of the identities running on that specific node.
- **Cryptographic Receipts:** Solves the core governance requirement for immutable proof of execution. When an agent executes a tool, the payload is signed with a private, short-lived SVID that cannot be forged or hallucinated by a rogue LLM.
- **Dynamic & Short-lived Credentials:** Eliminates the risk of long-lived, leaked API keys. Certificates are rotated automatically (often every few hours or minutes) by the SPIRE Agent without any application downtime.
- **Native Consul Integration:** Consul Connect already supports SPIFFE natively, meaning service mesh communication between Taskers, Automators, and Orchestrators becomes inherently secure with minimal configuration changes.

### Cons (Challenges and Costs)
- **Significant Infrastructure Complexity:** Introducing the SPIRE Server and Agent components adds two more critical stateful layers to the cluster that must be monitored, maintained, and scaled (alongside Nomad, Consul, and the AI workloads).
- **Workload Attestation Friction:** Verifying Nomad workloads can be tricky. Built-in attestors (like Docker) might not capture Nomad-specific metadata accurately without custom plugins, meaning identities might be mapped too broadly initially.
- **Application Refactoring Required:** All Python agents and the `TwinService` orchestrator will need to be refactored to use `pyspiffe`, fetch SVIDs via Unix sockets, and implement cryptographic signing and validation logic.
- **Performance Overhead:** Cryptographic signing, validation, and frequent SVID rotation inject CPU overhead and latency into every inter-agent and agent-to-tool API call, which may be noticeable on our legacy edge hardware.

## 6. Recommendation (Verdict)

**Recommendation: Implement, but via a Phased, Deferred Approach.**

Given the current architecture's reliance on implicit trust and long-lived API keys, moving to a Zero-Trust architecture is fundamentally necessary for the long-term safety of the autonomous AI cluster. However, the operational complexity of SPIRE is high.

**Action Plan:**
1.  **Phase 1 (Do Not Implement SPIRE Yet):** Focus first on standardizing the internal communication using the Model Context Protocol (MCP). Implement application-level signing using simpler, self-managed Ed25519 keypairs generated per Nomad allocation (e.g., via an init script) before jumping to a full SPIFFE control plane. This proves the *value* of cryptographic receipts without the infrastructure cost.
2.  **Phase 2 (Implement SPIRE):** Once the application logic for cryptographic receipts is stable and MCP is fully integrated, revisit deploying the SPIRE infrastructure to handle the automated rotation and attestation of those keys at the cluster level.

## 7. Next Steps for Implementation (When Phase 2 Begins)
1.  **Deploy SPIRE Infrastructure:** Write Ansible playbooks to provision SPIRE Server and SPIRE Agent on the Nomad cluster.
2.  **Consul CA Integration:** Update the Consul server configuration to use SPIFFE/SPIRE as the CA provider.
3.  **Nomad Job Templates:** Update existing Nomad job definitions (e.g., `llama-expert.nomad`) to mount the SPIRE socket.
4.  **Python Agent Integration:** Swap out the Phase 1 self-managed keys and integrate `pyspiffe` into the `TwinService` and `ToolExecutorNode` to request SVIDs.
5.  **Enforce Validation:** Update the orchestration router logic to validate SVIDs before allowing transitions.