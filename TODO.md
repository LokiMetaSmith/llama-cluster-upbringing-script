# TODO

This document outlines the major refactoring, feature enhancement, and maintenance tasks for the project. It is divided into high-priority tasks for improving stability and a backlog of future enhancements.

-----

# Critical

---
## 0. Detailed Refactoring Plan

This plan is broken into phases. Each phase is a self-contained set of tasks designed to progressively refactor the codebase.

### Phase 1: Solidify Core Deployment & Service Management

**Goal:** Eliminate the race conditions and conflicting entry points that have caused the cascading failures. Make the system's state fully managed by Ansible in a declarative way.

1.  **Create `heal_cluster.yaml`:**
    * Create a new playbook in the root directory named `heal_cluster.yaml`.
    * This playbook will have one play targeting the primary controller node.
    * It will use `ansible.builtin.include_role` to run the `bootstrap_agent` role first, followed by the `pipecatapp` role. This playbook becomes the standard way to ensure services are running.

2.  **Make `llama_cpp` and `bootstrap_agent` Roles Idempotent:**
    * In `ansible/roles/bootstrap_agent/tasks/deploy_llama_cpp_model.yaml`, ensure the `nomad job run` task for `prima-expert-main` only runs if the job is not already running.
    * In `ansible/roles/llama_cpp/tasks/main.yaml`, ensure the compilation tasks are skipped if the binaries already exist.

3.  **Refactor the Main Playbook (`playbook.yaml`):**
    * Confirm that the `llama_cpp` role is included in "Play 2" and the `bootstrap_agent` role is in "Play 4", running *before* the `pipecatapp` role.
    * Confirm the `Wait for the main expert service to be healthy in Consul` task exists in the `pipecatapp` role and is correctly placed *before* the `Run pipecat-app job` task.

4.  **Remove Conflicting Startup Logic:**
    * Delete the `ansible/roles/pipecatapp/templates/prima-services.service.j2` file if it exists.
    * In `ansible/roles/pipecatapp/tasks/main.yaml`, remove any task that deploys a conflicting `systemd` service.

---
### Phase 2: Implement the OpenAI-Compatible MoE Gateway

**Goal:** Create a new, standalone service that exposes the cluster's MoE capabilities to external clients.

1.  **Create a New Ansible Role (`moe_gateway`):**
    * Create the directory structure `ansible/roles/moe_gateway/`.
    * Inside, create `tasks/main.yaml` and `files/`.

2.  **Develop the Gateway Application:**
    * In `ansible/roles/moe_gateway/files/`, create a Python script `gateway.py`.
    * This script will be a FastAPI application with a single `/v1/chat/completions` endpoint.
    * It will need to discover the `pipecat-app`'s text message queue (this will require a small modification to `pipecat-app` to share the queue, perhaps via a global variable or a simple singleton pattern).
    * It will need a mechanism to receive a response. The most robust method is to create a unique response queue (e.g., using `asyncio.Queue`) for each incoming request, pass the ID of this queue along with the message to `pipecat-app`, and wait for the response to appear on it.

3.  **Create the Nomad Job:**
    * In `ansible/roles/moe_gateway/files/`, create a `moe-gateway.nomad` job file.
    * This job will run the `gateway.py` application. It should register a `moe-gateway` service in Consul.

4.  **Update the `pipecat-app`:**
    * Modify `app.py` and `web_server.py`. The `TwinService` needs to be able to check if an incoming text message has a `response_queue_id`.
    * If it does, the final text response from the agent should be put onto that specific queue instead of being sent to the TTS service.

5.  **Update the Main Playbook:**
    * Add the `moe_gateway` role to `playbook.yaml` so it gets deployed along with the other core services.

---
### Phase 3: Documentation and Cleanup

**Goal:** Finalize the project by cleaning up obsolete files and creating clear documentation for the new features.

1.  **Remove Obsolete Scripts:**
    * Delete the entire `debian_service/` directory and its contents.
    * Review the `initial-setup/` scripts and migrate any remaining essential logic into the main Ansible roles, then remove the scripts.

2.  **Create API Documentation:**
    * Create a new file, `API_USAGE.md`, in the root directory.
    * This file should explain how to use the new OpenAI-compatible endpoint, including the URL, authentication method (API keys), and example `curl` or Python requests.

3.  **Review and Finalize `TODO.md`:**
    * Review the updated `TODO.md`, mark all completed refactoring tasks, and re-prioritize the remaining feature enhancements.

## 1. High-Priority: Harden the Core System

These tasks are focused on addressing the brittleness of the deployment process and making the system more resilient, predictable, and maintainable.

### 1.1. Refactor for Strict Idempotency in Ansible

**Goal:** Ensure that the Ansible playbook can be run multiple times without causing errors or unintended side effects. This is the most critical step to achieving a stable and predictable deployment process.

- [ ] **Apply `creates` argument to compilation tasks:** In roles like `llama_cpp` and `whisper_cpp`, the `cmake` and `make` tasks should be skipped if the final binary artifacts already exist. This will prevent unnecessary and potentially error-prone recompilation on every playbook run.
  - *Example (`ansible/roles/llama_cpp/tasks/main.yaml`):*

    ```yaml
    - name: Build llama.cpp
      ansible.builtin.command:
        cmd: cmake --build build --config Release -j
      args:
        chdir: /opt/llama.cpp-build
        creates: /opt/llama.cpp-build/build/bin/llama-server # This line prevents re-running
    ```

- [ ] **Use `when` clauses for state checks:** Before making a change, verify if it's necessary. For instance, when adding a user to the `docker` group, first check if the user is already a member to prevent the task from showing "changed" on every run.
- [ ] **Audit all roles for idempotency:** Systematically review every task in every role (`common`, `docker`, `nomad`, `consul`, etc.) and apply idempotency checks where they are missing.
- [ ] **Convert `command` and `shell` to Ansible modules where possible:** Replace generic shell commands with dedicated Ansible modules (e.g., `ansible.builtin.user`, `ansible.builtin.file`, `community.general.nmcli`), as these modules are inherently idempotent.

### 1.2. Centralize All Configuration

**Goal:** Create a single source of truth for all configuration variables to simplify management and reduce the risk of inconsistencies.

- [ ] **Migrate hardcoded variables to `group_vars`:** Search the entire codebase for hardcoded values (e.g., paths, usernames, ports, service names) and replace them with Ansible variables defined in `group_vars/all.yaml`.
  - *Specific examples:*
    - The `NOMAD_ADDR` in the `pipecatapp` role tasks should be a variable.
    - The log file path `/tmp/pipecat.log` in `start_pipecat.sh` should be a variable.
    - The `PRIMA_API_SERVICE_NAME` in `pipecatapp.nomad` should be a variable.
- [ ] **Convert all configuration files to templates:** Any file that contains a variable should be a Jinja2 template (`.j2`). This includes all Nomad job files (`*.nomad`), the `start_pipecat.sh` script, and systemd service files.
- [ ] **Establish a clear variable hierarchy:** Use `group_vars/all.yaml` for system-wide defaults and consider `host_vars/<hostname>.yaml` for machine-specific overrides (like `mac_address`, which is already being done correctly).

### 1.3. Pre-build a Docker Image for `pipecatapp`

**Goal:** Decouple the application build process from the deployment process. This is the most effective way to eliminate the dependency and environment-related errors you've been facing.

- [ ] **Create a comprehensive `Dockerfile`:** This file will be the blueprint for the `pipecatapp` image. It should:
  1. Start from a base Python image (e.g., `python:3.12-slim`).
  2. Install all necessary system-level dependencies (`build-essential`, `portaudio19-dev`, etc.) using `apt-get`.
  3. Copy the `requirements.txt` file and run `pip install` to create a self-contained Python environment.
  4. Copy the entire application directory (`app.py`, `tools/`, `prompts/`, etc.) into the image.
  5. Set the `CMD` to run the `start_pipecat.sh` script.
- [ ] **Add a build stage to `bootstrap.sh`:** Before running `ansible-playbook`, the bootstrap script should build the Docker image locally (e.g., `docker build -t pipecat-app:latest .`).
- [ ] **Refactor the `pipecatapp.nomad` job:** Change the task driver from `raw_exec` to `docker`. The configuration will become much simpler, just needing to specify the image name (`pipecat-app:latest`).
- [ ] **Update the Ansible Role:** The `pipecatapp` Ansible role will be simplified. It will no longer need to install Python dependencies or copy application files; its main job will be to deploy the Nomad job file.
- [ ] **Add a flag to `bootstrap.sh`:** As suggested, add a `--run-local` or similar flag to the bootstrap script to allow switching between the new Docker-based deployment and the old `raw_exec` method for debugging purposes.

-----

## 2. Medium-Priority: Testing and Usability

### 2.1. Bolster Automated Testing

**Goal:** Create a robust safety net that allows for confident refactoring and development by automatically catching regressions.

- [ ] **Implement Ansible Molecule tests:** Create a Molecule test scenario for at least one critical role (e.g., `nomad` or `docker`). This involves creating a test playbook that can be run against a temporary Docker container to verify the role's functionality in isolation.
- [ ] **Expand end-to-end tests:** Add a new test case to `e2e-tests.yaml` that verifies a core function of the agent, such as a simple tool call (e.g., asking the `mcp_tool` for its status).
- [ ] **Increase unit test coverage:** Write unit tests for the remaining Python tools in the `tools/` directory to ensure each function behaves as expected.

### 2.2. Improve Web UI and User Experience

**Goal:** Make the Mission Control UI more intuitive and visually appealing.

- [ ] **Replace ASCII art:** As planned, replace the placeholder ASCII art with a more dynamic and expressive animated character or graphic.
- [ ] **Add a "Clear Terminal" button:** Provide a simple way for the user to clear the log history in the UI.
- [ ] **Improve status display:** The current status display is just a JSON dump. Format this into a more readable table or list that clearly shows the status of each pipeline and service.

-----

## 3. Future Enhancements and Backlog

This section includes items from the original "For Future Review" list, expanded with more concrete action items.

- [ ] **Implement Graceful LLM Failover:**
  - The `prima-expert.nomad` job template already loops through a list of models. Enhance this by adding a final, lightweight fallback model to the end of every model list in `group_vars/models.yaml` (e.g., a 3B parameter model). This ensures that even if larger models fail to load due to memory constraints, the expert service will still start with a basic capability.
- [ ] **Re-evaluate Consul Connect Service Mesh:**
  - Once the core system is stable, create a new feature branch and attempt to re-enable `sidecar_service` in the Nomad job files. Document the exact steps needed to configure the service mesh and any performance overhead observed.
- [ ] **Add Pre-flight System Health Checks:**
  - Create a new Ansible role named `preflight_checks`. This role should run at the very beginning of `playbook.yaml`.
  - Add tasks to this role to perform non-destructive checks:
    - Verify that the filesystem is writable by creating and deleting a temporary file.
    - Check for adequate free disk space.
    - Check for a stable network connection to the outside world.
  - If any of these checks fail, the playbook should fail early with a clear, informative error message.
- [ ] **Investigate Advanced Power Management:**
  - The current power management system stops and starts Nomad jobs. Research and prototype a more advanced version that uses Wake-on-LAN.
  - Create a new Ansible task that collects the MAC address of each node and stores it in `host_vars`.
  - Modify the `power_agent.py` to call a script that sends a Wake-on-LAN packet when it detects traffic for a sleeping node that is completely powered off.
- [ ] **Expand the Model Collection:**
  - Systematically test and add the remaining LiquidAI nano models to `group_vars/models.yaml`.
  - Create new "expert" deployment playbooks (like `deploy_expert.yaml`) for specialized tasks like "summarization" or "translation" and document how to use them.
- [ ] **Security Hardening:**
  - **Remove passwordless sudo:** Modify the sudoers file configuration to require a password for the `target_user`, enhancing security.
  - **Run services as non-root users:** Audit all services (Nomad, Consul, etc.) and ensure they are running as dedicated, non-privileged users where possible. The `pipecatapp` already does this well; apply the same principle to the system services.
- [ ] **Monitoring and Observability:**
  - Deploy a monitoring stack like Prometheus and Grafana to collect and visualize metrics from Nomad, Consul, and the application itself.
  - Expose custom application metrics from the `pipecatapp` (e.g., pipeline latency, number of tool calls) for Prometheus to scrape.

## 1. Refactor for Strict Idempotency in Ansible

- [ ] Use `creates` and `when` to ensure tasks only run when necessary.
- [ ] Check for existing state before making changes.
- [ ] Use handlers for service restarts consistently.

## 2. Centralize All Configuration

- [ ] Consolidate all configurable parameters into `group_vars/all.yaml` and `group_vars/models.yaml`.
- [ ] Use templates for all files containing configurable values.
- [ ] Eliminate hardcoded values from the codebase.

## 3. Pre-build a Docker Image for `pipecatapp`

- [ ] Add a flag in the bootstrap script to select running the `pipecatapp` application locally or in a Docker container
- [ ] Create a `Dockerfile` for the `pipecatapp` application.
- [ ] Build and push the image to a registry as part of the development process.
- [ ] Simplify the Nomad job to use the `docker` driver with the pre-built image.

## 4. Bolster Your Automated Testing

- [ ] Use Molecule to test Ansible roles in isolation.
- [ ] Expand unit tests for Python tools.
- [ ] Expand end-to-end tests to cover more critical paths.

-----

- [x] State Export/Import: Allowing tasks to be saved and resumed.
- [x] Interactive approval of actions: For enhanced safety and user control.
- [x] Enhanced Debugging Modes: For better transparency.
- [x] WebBrowserTool: For browsing the web.
- [ ] Web UI: Replace the placeholder ASCII art with a more expressive cartoon robot face.

## 5. High-Priority Feature: Create OpenAI-Compatible API Gateway

**Goal:** Expose the cluster's Mixture of Experts (MoE) routing capabilities to external applications through a standard, OpenAI-compatible REST API. This will transform the cluster from a standalone agent into a private, powerful AI cloud.

-   [ ] **Create a New "MoE Gateway" Service:**
    -   Develop a lightweight FastAPI application that will run as a new, dedicated Nomad job.
    -   This service's sole responsibility will be to act as a secure entry point to the cluster.

-   [ ] **Implement an OpenAI-Compatible Endpoint:**
    -   The gateway must expose a `/v1/chat/completions` endpoint that mirrors the official OpenAI API specification.
    -   It should handle API key authentication for external clients.

-   [ ] **Integrate with the `pipecat` Pipeline:**
    -   When the gateway receives a request, it will transform the payload into a text message.
    -   It will then inject this message into the `pipecatapp`'s existing `text_message_queue`.

-   [ ] **Handle the Response Path:**
    -   The `pipecat-app` will process the request via the `TwinService` and generate a response.
    -   A mechanism needs to be created to capture this final text response and route it back to the originating API call in the gateway service.
    -   The gateway will then format this text into a valid OpenAI API JSON response and send it back to the client.

## For Future Review

- [ ] Review `llama.cpp` optimization guide for server performance tuning: <https://blog.steelph0enix.dev/posts/llama-cpp-guide/#llamacpp-server-settings>
- [ ] Investigate re-enabling Consul Connect (`sidecar_service`) for Nomad jobs once the base cluster is stable. This was disabled to resolve initial scheduling failures in the bootstrap environment.
- [ ] Consider adding a pre-flight check to detect a read-only filesystem. Investigate if a safe, non-destructive diagnostic can be run automatically. (Note: Direct filesystem repair tools like e2fsck are likely too dangerous to automate).
- [ ] Consolidate all AI models (LLM, Whisper, Vision) into a single, unified directory to avoid duplication.
- [ ] Implement a graceful failover mechanism for LLM services, allowing them to fall back to a smaller model if the primary one fails to load.
- [ ] Add the remaining LiquidAI nano models from the collection: <https://huggingface.co/collections/LiquidAI/liquid-nanos-68b98d898414dd94d4d5f99a>