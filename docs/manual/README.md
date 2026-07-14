# Cluster User Manuals & Design Documents

Welcome to the central documentation index for the Distributed Conversational AI Pipeline and Cluster. This directory contains detailed manuals and architectural blueprints to help administrators, developers, and autonomous agents understand, deploy, maintain, and interact with the system.

These manuals are organized thematically to provide a logical path from high-level architecture down to low-level operational playbooks.

---

## 1. Core Architecture & System Summary

These documents provide a holistic view of the cluster design, core components, and high-level summaries of the entire hardware and software stack.

*   **[Holistic Project Architecture](ARCHITECTURE.md)**
    *   *Description:* A comprehensive overview of all seven layers of the cluster architecture, from physical PXE-boot provisioning and Ansible configuration, to Nomad orchestration, IPFS decentralized storage, Btrfs snapshot recovery, and the autonomous Self-Adaptation Loop (SEAL).
*   **[Project Summary: Conversational AI Pipeline](PROJECT_SUMMARY.md)**
    *   *Description:* A condensed, high-level summary detailing the final operational architecture, implemented real-time features, and reference designs.
*   **[GEMINI Overview & Setup Instructions](GEMINI.md)**
    *   *Description:* High-level guide for building, bootstrapping, and bringing up the cluster on single or multi-node configurations.

---

## 2. AI Agents & Cognitive Architectures

These guides describe the cognitive models, Mixture of Experts (MoE) routing backends, and governance models that dictate the agent's behavior and intelligence.

*   **[AI Agent Architectures](AGENTS.md)**
    *   *Description:* Explains the dual agent architectures used in the system: the runtime Mixture of Experts (MoE) workflow engine for the production application and the multi-agent development Ensemble for code generation.
*   **[AI Agent Integration Handbook](AGENT_HANDBOOK.md)**
    *   *Description:* A practical handbook for extending and managing the MoE gateway, creating custom Model Context Protocol (MCP) servers, and optional Ansible role toggles.
*   **[AI Governance & Architecture Plan](AI_GOVERNANCE.md)**
    *   *Description:* Outlines the structural taxonomic definitions (KPMG TACO mapping) and the five core pillars of agentic governance (Identity, Capability Alignment, Logging/Auditing, Security, and Resource Bounds).
*   **[Agent Memories & Operational Lessons](MEMORIES.md)**
    *   *Description:* A living directory compiling critical operational best practices, lessons, and troubleshooting experiences across Ansible, Nomad, Consul, and development workflows.
*   **[Frontier Agent Roadmap](FRONTIER_AGENT_ROADMAP.md)**
    *   *Description:* A strategic gap analysis and multi-phase implementation roadmap for moving from simple chat loops to advanced reasoning and self-evolving autonomy.

---

## 3. Tool Integrations & Declarative Workflows

These documents describe how the conversational agent interacts with host systems, external applications, and knowledge bases.

*   **[Obsidian Workflow Design: The Active Vault](OBSIDIAN_WORKFLOW_DESIGN.md)**
    *   *Description:* Details the design of the "Active Vault" architecture which bridges the gap between Obsidian's 2D/3D Canvas interface and Pipecat's declarative YAML workflow runner.
*   **[MCP Migration Plan](MCP_MIGRATION_PLAN.md)**
    *   *Description:* The strategy and roadmap for decoupling tightly-coupled legacy tool executors into standardized, isolated JSON-RPC Model Context Protocol (MCP) servers.
*   **[MCP Server Setup with Service Discovery](MCP_SERVER_SETUP.md)**
    *   *Description:* Explores the implementation patterns for running MCP servers alongside dynamic discovery backends like Consul, etcd, or Kubernetes.
*   **[External Application Hosting & Package Management](EXTERNAL_APP_HOSTING_GUIDE.md)**
    *   *Description:* A developer guide to the containerized package manager, detailing the strict JSON manifest schemas, Btrfs subvolume provisioning lifecycle, and the companion CLI utility.
*   **[TwinService Demonolithization Design](TWINSERVICE_DEMONOLITHIZATION_DESIGN.md)**
    *   *Description:* An architectural design for decomposing the monolithic `TwinService` into clean, decoupled microservices separating real-time audio/video streaming from cognitive LLM routing.

---

## 4. Network Architecture & Zero-Trust Security

These blueprints describe the dual-layer network, mesh tunnels, firewall rules, and cryptographic security features of the cluster.

*   **[Network Architecture Blueprints](NETWORK.md)**
    *   *Description:* Details the split between the Provisioning Underlay (static 10.0.0.x Layer 2 network for PXE booting) and the Production Overlay (Tailscale WireGuard mesh service network).
*   **[AI Cluster Network Isolation Guide](NETWORK_ISOLATION.md)**
    *   *Description:* Guarantees the absolute security of the cluster, outlining VLAN configurations, dedicated routing interfaces, and how to avoid standard "Double NAT" network traps.
*   **[Cluster Load Testing and Network Validation](LOAD_TESTING.md)**
    *   *Description:* Practical test playbooks to validate network isolation, verify Traefik Layer 7 load-balancing performance, and diagnose mesh network latency.
*   **[SPIFFE/SPIRE Integration PoC](SPIRE_POC.md)**
    *   *Description:* A proof-of-concept design for implementing a Zero-Trust service mesh with cryptographic SPIFFE IDs and SVID credentials on Nomad.

---

## 5. Bare-Metal Provisioning & Deployment

These guides explain how to build, deploy, boot, and optimize cluster nodes and core AI software.

*   **[iPXE Boot Server Setup (Debian)](PXE_BOOT_SETUP.md)**
    *   *Description:* Step-by-step setup of the local DHCP/TFTP/HTTP PXE server to automate headless Debian 13 installations.
*   **[NixOS-based PXE Boot Server Setup](NIXOS_PXE_BOOT_SETUP.md)**
    *   *Description:* Experimental Netboot setup for PXE-booting NixOS configurations across the hardware cluster.
*   **[Deploying and Profiling AI Services](DEPLOYMENT_AND_PROFILING.md)**
    *   *Description:* Detailed deployment playbooks for LLM experts (vLLM and llama.cpp rpc-servers) and software performance profiling (CPU/Memory/GPU).
*   **[Performance & I/O Optimization](PERFORMANCE_OPTIMIZATION.md)**
    *   *Description:* Identifies performance bottlenecks, proposing syscall reductions for heavy tools, git command optimizations, and Btrfs snapshot-based disaster recovery rollbacks.
*   **[Improving Remote Workflows](REMOTE_WORKFLOW.md)**
    *   *Description:* Best practices for optimizing remote cluster development using Mosh and Tmux.

---

## 6. Operations, Self-Healing & Diagnostics

These operational playbooks outline self-healing scripts, failure handling, troubleshooting, and front-end user verification.

*   **[Cluster Health Probing and Self-Healing](CLUSTER_HEALTH_AND_HEALING.md)**
    *   *Description:* Describes the interactive health-check command CLI (`probe` and `heal`) that acts as a standalone operational agent to diagnose and repair failed Nomad jobs and systemd daemons.
*   **[Automated Ansible Exception Handler & Git PR Loop](ANSIBLE_EXCEPTION_HANDLER_GUIDE.md)**
    *   *Description:* Documents "Jules", an autonomous debugging loop that parses failed Ansible playbooks, replicates failure contexts, generates fixes using LLMs, runs local linting/syntax checks, and creates Opengist pull request summaries.
*   **[Troubleshooting Guide](TROUBLESHOOTING.md)**
    *   *Description:* Resolving common operational issues, including stale Consul service registries, locked cache issues, and failed network bindings.
*   **[Frontend Verification via Playwright](FRONTEND_VERIFICATION.md)**
    *   *Description:* Detailed instructions on running headless accessibility audits, focusing interactive outlines, and capturing audit screenshots using Playwright.
