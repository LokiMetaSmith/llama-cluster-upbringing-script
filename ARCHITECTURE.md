# Holistic Project Architecture

This document provides a detailed overview of the system architecture, from the hardware provisioning layer to the application logic and user interface. The system is designed as a multi-layered stack to deploy a responsive, distributed, and embodied conversational AI agent on a cluster of legacy machines.

---

## Layer 1: Bare-Metal & OS Provisioning

This layer is responsible for taking bare-metal machines and installing a fully configured operating system.

- **Technology:** [PXE (Preboot Execution Environment)](https://en.wikipedia.org/wiki/Preboot_Execution_Environment) and [iPXE](https://ipxe.org/), leveraging HTTP for speed and reliability.
- **Implementation:** The `pxe_server` Ansible role configures a dedicated node to act as an iPXE server. This server provides DHCP, TFTP (for chainloading), and Nginx (for HTTP) services.
- **Workflow:**
  1. A new, bare-metal machine is configured in its BIOS to boot from the network.
  2. The DHCP server answers and provides the iPXE bootloader (`.kpxe` or `.efi`) from the TFTP server.
  3. iPXE loads, then makes a new DHCP request. This time, it's served a URL to an iPXE script from the Nginx web server.
  4. The iPXE script instructs the client to download the Debian kernel, initrd, and a preseed file over fast HTTP, beginning a fully automated installation.
- **Outcome:** A new machine is automatically installed with Debian 13 and is ready for the next layer of configuration.

## Layer 2: System Configuration (Ansible)

This layer takes the base Debian installs and configures them into a functional, cohesive cluster.

- **Technology:** [Ansible](https://www.ansible.com/).
- **Implementation:** The root `playbook.yaml` and the roles within the `ansible/roles/` directory define the entire cluster configuration.
- **Key Components:**
  - **Roles:** The playbook is composed of modular roles for each piece of software (`common`, `docker`, `consul`, `nomad`, etc.).
  - **Auto-Provisioning API:** A new role, `provisioning_api`, deploys a small FastAPI web service onto the control node. This service listens for "call home" messages from newly installed nodes, automatically adds them to the Ansible inventory, and triggers a provisioning run against them. This enables a fully automated, zero-touch provisioning workflow for the cluster after the first node is set up.
- **Workflow:**
  1. An administrator manually sets up the first control node.
  2. The `initial-setup.sh` script on a newly PXE-booted client runs a "call home" script on its first boot.
  3. The `provisioning_api` on the control node catches this call, updates its inventory, and automatically runs `ansible-playbook` on the new node.
- **Outcome:** All nodes in the cluster are automatically and consistently configured with all necessary dependencies, ready to run application workloads.

## Layer 3: Application Orchestration (Nomad & Consul)

This layer is responsible for deploying, managing, and scaling the various services that make up the AI agent.

- **Technology:** [HashiCorp Nomad](https://www.nomadproject.io/) for orchestration and [HashiCorp Consul](https://www.consul.io/) for service discovery.
- **Implementation:** Services are defined as declarative job files (e.g., `pipecatapp.nomad`, `primacpp.nomad`).
- **Workflow:**
  1. The administrator uses the `nomad job run` command to submit job files to the Nomad cluster.
  2. Nomad schedules the jobs on available worker nodes.
  3. **Service Discovery:** As jobs start, they automatically register with Consul. For example, the `TwinService` can dynamically discover all available "expert" LLM backends by querying Consul for services tagged with a specific pattern.
- **Outcome:** All microservices are running, monitored, and can find each other dynamically on the network.

## Layer 4: The AI Application Stack

This layer contains the core Python application that constitutes the agent itself. It runs as the `pipecatapp` Nomad job.

- **Framework:** [pipecat](https://github.com/pipecat-ai/pipecatapp), a real-time streaming media framework.
- **Entrypoint:** `app.py`.
- **Core Components:**
  - **`TwinService`:** The agent's "brain," implemented as a `pipecat` `FrameProcessor`. It handles conversation, memory, and tool use.
  - **Memory:** A dual-component memory system with short-term conversational history and a long-term FAISS vector store for semantic search.
  - **Tools:** The `TwinService` can use a variety of tools, including `ssh`, a sandboxed `code_runner`, and `vision`.
  - **Mixture of Experts (MoE) Routing:** The `TwinService` can act as a router, forwarding queries to specialized LLM backends discovered via Consul.
- **Newly Implemented Features:**
  - **Debug Mode:** Enables verbose logging of tool inputs and outputs.
  - **Interactive Approval:** Pauses execution and prompts for user confirmation in the UI before running sensitive tools.
  - **State Management:** Allows the agent's memory state to be saved and loaded from named snapshots via the UI.

## Layer 5: Web UI & Control Plane

This layer provides a user-facing interface for interacting with and monitoring the agent.

- **Technology:** [FastAPI](https://fastapi.tiangolo.com/) and WebSockets.
- **Implementation:** The `web_server.py` file runs a web server in a separate thread within the `pipecatapp` container.
- **Workflow:**
  1. A WebSocket provides a real-time stream of agent logs to the frontend UI.
  2. The UI can now send messages back to the backend to approve or deny actions.
  3. REST endpoints are provided for saving and loading agent state.
- **Outcome:** A real-time, interactive "Mission Control" dashboard for the agent.
