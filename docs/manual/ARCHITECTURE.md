# Holistic Project Architecture

Last updated: 2026-01-23

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
  - **Agent Bootstrapping:** After the core infrastructure is configured, the `pipecatapp` and `llama_cpp` roles are executed. These roles are responsible for deploying the core AI services, including the main `pipecatapp` voice agent and the `llamacpp-rpc` model servers, as Nomad jobs. This action transforms a freshly provisioned control node into a fully autonomous AI agent. The `bootstrap_agent` role runs at the end of the playbook to verify that the cluster has formed correctly and is ready for operation.
- **Workflow:**
  1. An administrator manually sets up the first control node and runs the main Ansible playbook. This playbook installs the `provisioning_api` and then runs the necessary roles to deploy all AI services.
  2. A new, PXE-booted client runs a "call home" script on its first boot, sending its hostname and IP address to the `provisioning_api`.
  3. The API validates the request, safely updates the Ansible inventory file, and triggers an asynchronous `ansible-playbook` run targeting the new node.
- **Outcome:** All nodes in the cluster are automatically and consistently configured with all necessary dependencies, ready to run application workloads.

## Layer 3: Application Orchestration (Nomad & Consul)

This layer is responsible for deploying, managing, and scaling the various services that make up the AI agent.

- **Technology:** [HashiCorp Nomad](https://www.nomadproject.io/) for orchestration and [HashiCorp Consul](https://www.consul.io/) for service discovery.
- **Implementation:** Services are defined as declarative job files (e.g., `pipecatapp.nomad`, `llamacpp-rpc.nomad`).
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
  - **Workflow Engine:** A new, flexible engine that defines the agent's thought process using declarative YAML workflows (e.g., `default_agent_loop.yaml`).
  - **Memory:** A dual-component memory system with short-term conversational history and a long-term FAISS vector store for semantic search.
  - **Tools:** The `TwinService` can access a comprehensive library of over 25 tools, including `ansible` for cluster management, `code_runner` for secure Python execution, `vision` for seeing the world, and specialized tools like `orchestrator`, `planner`, and `swarm` for complex tasks.
  - **Mixture of Experts (MoE) Routing:** The system uses the workflow to route queries to specialized LLM backends (e.g., Coding, Math, Vision) discovered via Consul.

## Layer 5: Web UI & Control Plane

This layer provides a user-facing interface for interacting with and monitoring the agent.

- **Technology:** [FastAPI](https://fastapi.tiangolo.com/) and WebSockets.
- **Implementation:** The `web_server.py` file runs a web server in a separate thread within the `pipecatapp` container.
- **Workflow:**
  1. A WebSocket provides a real-time stream of agent logs to the frontend UI.
  2. The UI can now send messages back to the backend to approve or deny actions.
  3. REST endpoints are provided for saving and loading agent state.
- **Outcome:** A real-time, interactive "Mission Control" dashboard for the agent.

## Layer 6: External API Gateway

To expose the cluster's capabilities to the outside world, a dedicated gateway service provides a standard, OpenAI-compatible REST API.

- **Technology:** [FastAPI](https://fastapi.tiangolo.com/) running as a dedicated Nomad service.
- **Implementation:** The `moe_gateway` service acts as a secure entry point to the cluster.
- **Workflow:**
  1. The gateway service discovers the main `pipecatapp` service via Consul.
  2. It exposes a `/v1/chat/completions` endpoint, validating requests with API keys.
  3. Incoming requests are transformed and injected into the `pipecat` pipeline via its text message queue.
  4. The `TwinService` processes the request, routes it to the appropriate expert, and generates a response.
  5. A new mechanism captures the final text response and sends it back to the gateway.
  6. The gateway formats the text into a valid OpenAI API JSON response and returns it to the external client.
- **Outcome:** Any application capable of communicating with the OpenAI API can now leverage the power of the distributed, self-hosted Mixture of Experts.

---

## Layer 7: Self-Adaptation Loop (SEAL-Inspired)

This layer represents the highest level of system autonomy. Inspired by the principles of Self-Adapting Language Models (SEAL), this is a closed-loop feedback system that allows the agent to learn from its own failures and autonomously improve its core programming.

- **Technology:** Python, Ansible, Nomad, and the `openevolve` library.
- **Implementation:** This loop connects the `supervisor.py` script with the `reflection` and `prompt_engineering` workflows.
- **Workflow:**
  1. **Detection:** The `supervisor.py` script continuously monitors the health of all Nomad jobs using the `health_check.yaml` playbook.
  2. **Diagnosis:** If a failure is detected, the `diagnose_failure.yaml` playbook is run to gather detailed logs and status information.
  3. **Reflection:** The supervisor then triggers the `reflection/reflect.py` script. This script uses an LLM to analyze the failure's diagnostic data.
  4. **Triage & Healing:**
      - If the failure is simple and understood (e.g., an Out-of-Memory error), the reflection script returns a structured solution (e.g., `{"action": "increase_memory", ...}`), and the `heal_job.yaml` playbook is run to fix it directly.
      - If the failure is complex or novel and cannot be diagnosed as a simple issue, the reflection script returns `{"action": "error", ...}`.
  5. **Adaptation:** This "error" action is the trigger for the self-adaptation loop. The supervisor calls the `reflection/adaptation_manager.py` script, which acts as the **Adaptation Agent**.
  6. **Test Case Generation:** The Adaptation Manager takes the raw diagnostic data and generates a new, specific YAML test case that programmatically encapsulates the failure.
  7. **Evolution:** The manager then invokes the `prompt_engineering/evolve.py` script as a background process, injecting the new test case into the workflow. This script uses an evolutionary algorithm (`openevolve`) to mutate the agent's core `reflect.py` logic, searching for a new version that can successfully produce a valid healing action for the failure, thus passing the test.
- **Agent Definition:** The logic and role of this process are formally defined in `prompt_engineering/agents/ADAPTATION_AGENT.md`.
- **Outcome:** The system can automatically learn from novel failures, hardening its own source code and becoming more robust over time without direct human intervention in the learning process.

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

## Future Architecture

This section outlines planned enhancements to the system architecture.

- **Graceful LLM Failover:** The `llama-expert.nomad` job will be enhanced to include a final, lightweight fallback model to ensure the expert service always starts with a basic capability.
- **Consul Connect Service Mesh:** Once the core system is stable, a new feature branch will be created to attempt to re-enable `sidecar_service` in the Nomad job files and document the process and performance overhead.
- **Pre-flight System Health Checks:** A new Ansible role will be created to perform non-destructive checks (filesystem writability, disk space, network connection) at the beginning of the main playbook.
- **Advanced Power Management:** A more advanced power management system using Wake-on-LAN will be researched and prototyped, triggered by the `power_agent.py`.
