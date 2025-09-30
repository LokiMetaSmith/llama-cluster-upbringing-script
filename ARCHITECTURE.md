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
  - **Auto-Provisioning API:** The `provisioning_api` role deploys a robust FastAPI web service on the control node. This service acts as the entrypoint for new nodes joining the cluster. It provides a secure endpoint for nodes to "call home" to, and it is responsible for orchestrating the provisioning process. Key features include:
    - **Asynchronous Job Handling:** It runs long `ansible-playbook` jobs in the background, preventing API timeouts.
    - **Status Tracking:** It provides API endpoints to monitor the status of ongoing and completed provisioning jobs.
    - **Failure Logging:** If a provisioning run fails, it automatically captures the error log and appends it to a `TODO.md` file for administrative review.
    - **Race Condition Prevention:** It uses file locking to ensure the integrity of the inventory file when multiple nodes call home simultaneously.
  - **Agent Bootstrapping:** A new role, `bootstrap_agent`, runs at the end of the initial playbook run. Its sole purpose is to perform the "Day 2" setup of the primary control node, automatically deploying the `llamacpp-rpc` and `pipecatapp` Nomad jobs. This action transforms the freshly provisioned control node into a fully autonomous AI agent, ready to manage the cluster.
- **Workflow:**
  1. An administrator manually sets up the first control node and runs the main Ansible playbook. This playbook installs the `provisioning_api` and runs the `bootstrap_agent` role to make the node self-aware.
  2. A new, PXE-booted client runs a "call home" script on its first boot, sending its hostname and IP address to the `provisioning_api`.
  3. The API validates the request, safely updates the Ansible inventory file, and triggers an asynchronous `ansible-playbook` run targeting the new node.
- **Outcome:** All nodes in the cluster are automatically and consistently configured with all necessary dependencies, ready to run application workloads.

## Layer 3: Application Orchestration (Nomad & Consul)

This layer is responsible for deploying, managing, and scaling the various services that make up the AI agent.

- **Technology:** [HashiCorp Nomad](https://www.nomadproject.io/) for orchestration and [HashiCorp Consul](https://www.consul.io/) for service discovery.
- **Implementation:** Services are defined as declarative job files (e.g., `pipecatapp.nomad`, `primacpp.nomad`).
- **Workflow:**
  1. The `bootstrap_agent` Ansible role automatically deploys the core `llamacpp-rpc` and `pipecatapp` jobs to Nomad on the primary control node.
  2. For advanced use cases, an administrator can still manually deploy additional jobs (e.g., specialized experts) using the `nomad job run` command.
  3. Nomad schedules all jobs on available worker nodes based on their resource requirements.
  4. **Service Discovery:** As jobs start, they automatically register with Consul. For example, the `TwinService` can dynamically discover all available "expert" LLM backends by querying Consul for services tagged with a specific pattern.
- **Outcome:** All microservices are running, monitored, and can find each other dynamically on the network.

## Layer 4: The AI Application Stack

This layer contains the core Python application that constitutes the agent itself. It runs as the `pipecatapp` Nomad job.

- **Framework:** [pipecat](https://github.com/pipecat-ai/pipecatapp), a real-time streaming media framework.
- **Entrypoint:** `app.py`.
- **Core Components:**
  - **`TwinService`:** The agent's "brain," implemented as a `pipecat` `FrameProcessor`. It handles conversation, memory, and tool use.
  - **Memory:** A dual-component memory system with short-term conversational history and a long-term FAISS vector store for semantic search.
  - **Tools:** The `TwinService` can use a variety of tools, including `ssh`, a sandboxed `code_runner`, `vision`, and most importantly, `ansible`. The `ansible` tool allows the agent to call back to the Ansible control plane, enabling it to provision new nodes or reconfigure the cluster in response to conversational commands.
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

### API Key Authentication

To enhance security, the system now supports API key authentication for its control plane endpoints (e.g., `/api/status`, `/api/state/save`). This ensures that only authorized clients can interact with the agent's core functions.

- **Implementation:** Authentication is handled by a FastAPI middleware that checks for a valid API key in the `Authorization` header of incoming requests. Keys are loaded at startup from an environment variable.

- **Configuration:**
  1. **Generate a Key:** Create a new, secure API key. A simple way to do this is with `python -c "import secrets; print(secrets.token_hex(32))"`.
  2. **Hash the Key:** The application stores a SHA-256 hash of the key, not the key itself. Hash your new key using a command like `echo -n "<your_new_key>" | sha256sum`.
  3. **Update Nomad Job:** Open the `ansible/jobs/pipecatapp.nomad` job file and find the `env` block for the `pipecat-task`. Add the hashed key to the `PIECAT_API_KEYS` environment variable. You can add multiple keys by separating them with a comma.

- **Usage:** When making a request to a protected endpoint, include the API key in the `Authorization` header:

  ```sh
  curl -X GET http://<agent_ip>:8000/api/status \
       -H "Authorization: Bearer <your_new_key>"
  ```
