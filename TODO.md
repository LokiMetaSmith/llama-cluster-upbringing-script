```markdown
Last updated: 2025-10-12

# TODO

This document outlines the major refactoring, feature enhancement, and maintenance tasks for the project. It is divided into high-priority tasks for improving stability and a backlog of future enhancements.

---

## Major Feature Additions

## TODO - Implement SEAL-Inspired Self-Adaptation Loop

This file tracks the implementation of a new self-adapting capability inspired by the SEAL paper. The goal is to create a closed loop where the system can reflect on its own failures and trigger a prompt evolution process to autonomously improve its core agent prompts.

## Key Components

- [ ] **ADAPTATION_AGENT.md**: A new agent definition file to formally describe the self-improvement agent's role.
- [ ] **adaptation_manager.py**: A new script to orchestrate the adaptation process, generating test cases from failures.
- [ ] **supervisor.py modifications**: Integrate the `adaptation_manager.py` into the main system loop.
- [ ] **evolve.py modifications**: Update the prompt evolution script to accept an external test case file.
- [ ] **Documentation Updates**: Update `ARCHITECTURE.md` to reflect the new capabilities.

## Task Breakdown

1. [X] **Create `TODO.md`**: Initialize this tracking document.
2. [ ] **Define `ADAPTATION_AGENT.md`**: Create the markdown file in `prompt_engineering/agents/`.
3. [ ] **Develop `adaptation_manager.py`**:
    - [ ] Stub out the main function and argument parsing.
    - [ ] Implement logic to receive failure data.
    - [ ] Implement logic to generate a YAML test case file from the failure data.
    - [ ] Implement logic to call the `evolve.py` script with the new test case.
4. [ ] **Modify `supervisor.py`**:
    - [ ] Add a call to `adaptation_manager.py` when `reflect.py` returns an `error` action.
5. [ ] **Modify `evolve.py`**:
    - [ ] Add argument parsing for an external test case file.
    - [ ] Update the test case loading logic to use the provided file if available.
6. [ ] **Update `ARCHITECTURE.md`**:
    - [ ] Add a new section describing the "Self-Adaptation Loop".
    - [ ] Include the `ADAPTATION_AGENT.md` in the agent hierarchy.
7. [ ] **Final Review and Testing**:
    - [ ] Manually trigger a failure to test the end-to-end loop.
    - [ ] Review all new code and documentation for clarity and correctness.

---

## Critical

---

### 0. Detailed Refactoring Plan

This plan is broken into phases. Each phase is a self-contained set of tasks designed to progressively refactor the codebase.

#### Phase 1: Solidify Core Deployment & Service Management

**Goal:** Eliminate the race conditions and conflicting entry points that have caused the cascading failures. Make the system's state fully managed by Ansible in a declarative way.

1. **Create `heal_cluster.yaml`:**
    - Create a new playbook in the root directory named `heal_cluster.yaml`.
    - This playbook will have one play targeting the primary controller node.
    - It will use `ansible.builtin.include_role` to run the `bootstrap_agent` role first, followed by the `pipecatapp` role. This playbook becomes the standard way to ensure services are running.

2. **Make `llama_cpp` and `bootstrap_agent` Roles Idempotent:**
    - In `ansible/roles/bootstrap_agent/tasks/deploy_llama_cpp_model.yaml`, ensure the `nomad job run` task for `llamacpp-rpc` only runs if the job is not already running.
    - In `ansible/roles/llama_cpp/tasks/main.yaml`, ensure the compilation tasks are skipped if the aries already exist.

3. **Refactor the Main Playbook (`playbook.yaml`):**
    - Confirm that the `llama_cpp` role is included in "Play 2" and the `bootstrap_agent` role is in "Play 4", running *before* the `pipecatapp` role.
    - Confirm the `Wait for the main expert service to be healthy in Consul` task exists in the `pipecatapp` role and is correctly placed *before* the `Run pipecat-app job` task.

4. **Remove Conflicting Startup Logic:**
    - Delete the `ansible/roles/pipecatapp/templates/llama-services.service.j2` file if it exists.
    - In `ansible/roles/pipecatapp/tasks/main.yaml`, remove any task that deploys a conflicting `systemd` service.

---

#### Phase 2: Implement the OpenAI-Compatible MoE Gateway

**Goal:** Create a new, standalone service that exposes the cluster's MoE capabilities to external clients.

1. **Create a New Ansible Role (`moe_gateway`):**
    - Create the directory structure `ansible/roles/moe_gateway/`.
    - Inside, create `tasks/main.yaml` and `files/`.

2. **Develop the Gateway Application:**
    - In `ansible/roles/moe_gateway/files/`, create a Python script `gateway.py`.
    - This script will be a FastAPI application with a single `/v1/chat/completions` endpoint.
    - It will need to discover the `pipecat-app`'s text message queue (this will require a small modification to `pipecatapp` to share the queue, perhaps via a global variable or a simple singleton pattern).
    - It will need a mechanism to receive a response. The most robust method is to create a unique response queue (e.g., using `asyncio.Queue`) for each incoming request, pass the ID of this queue along with the message to `pipecatapp`, and wait for the response to appear on it.

3. **Create the Nomad Job:**
    - In `ansible/roles/moe_gateway/files/`, create a `moe-gateway.nomad` job file.
    - This job will run the `gateway.py` application. It should register a `moe-gateway` service in Consul.

4. **Update the `pipecat-app`:**
    - Modify `app.py` and `web_server.py`. The `TwinService` needs to be able to check if an incoming text message has a `response_queue_id`.
    - If it does, the final text response from the agent should be put onto that specific queue instead of being sent to the TTS service.

5. **Update the Main Playbook:**
    - Add the `moe_gateway` role to `playbook.yaml` so it gets deployed along with the other core services.

---

#### Phase 3: Documentation and Cleanup

**Goal:** Finalize the project by cleaning up obsolete files and creating clear documentation for the new features.

1. **Remove Obsolete Scripts:**
    - Delete the entire `debian_service/` directory and its contents.
    - Review the `initial-setup/` scripts and migrate any remaining essential logic into the main Ansible roles, then remove the scripts.

2. **Create API Documentation:**
    - Create a new file, `API_USAGE.md`, in the root directory.
    - This file should explain how to use the new OpenAI-compatible endpoint, including the URL, authentication method (API keys), and example `curl` or Python requests.

3. **Review and Finalize `TODO.md`:**
    - Review the updated `TODO.md`, mark all completed refactoring tasks, and re-prioritize the remaining feature enhancements.

## 1. High-Priority: Harden the Core System

These tasks are focused on addressing the brittleness of the deployment process and making the system more resilient, predictable, and maintainable.

### 1.1. Refactor for Strict Idempotency in Ansible

- [ ] **Apply `creates` argument to compilation tasks:** In roles like `llama_cpp` and `whisper_cpp`, the `cmake` and `make` tasks should be skipped if the final binary artifacts already exist. This will prevent unnecessary and potentially error-prone recompilation on every playbook run.
  - *Example (`ansible/roles/llama_cpp/tasks/main.yaml`):*

    ```yaml
    - name: Build llama.cpp
      ansible.builtin.command:
        cmd: cmake --build build --config Release -j 2
      args:
        chdir: /opt/llama.cpp-build
        creates: /opt/llama.cpp-build/build/bin/llama-server # This line prevents re-running
    ```

- [ ] **Use `when` clauses for state checks:** Before making a change, verify if it's necessary. For instance, when adding a user to the `docker` group, first check if the user is already a member to prevent the task from showing "changed" on every run.
- [ ] **Audit all roles for idempotency:** Systematically review every task in every role (`common`, `docker`, `nomad`, `consul`, etc.) and apply idempotency checks where they are missing.
- [ ] **Convert `command` and `shell` to Ansible modules where possible:** Replace generic shell commands with dedicated Ansible modules (e.g., `ansible.builtin.user`, `ansible.builtin.file`, `community.general.nmcli`), as these modules are inherently idempotent.

### 1.2. Centralize All Configuration

- [ ] **Migrate hardcoded variables to `group_vars`:** Search the entire codebase for hardcoded values (e.g., paths, usernames, ports, service names) and replace them with Ansible variables defined in `group_vars/all.yaml`.
  - *Specific examples:*
    - The `NOMAD_ADDR` in the `pipecatapp` role tasks should be a variable.
    - The log file path `/tmp/pipecat.log` in `start_pipecat.sh` should be a variable.
    - The `LLAMA_API_SERVICE_NAME` in `pipecatapp.nomad` should be a variable.
- [ ] **Convert all configuration files to templates:** Any file that contains a variable should be a Jinja2 template (`.j2`). This includes all Nomad job files (`*.nomad`), the `start_pipecat.sh` script, and systemd service files.
- [ ] **Establish a clear variable hierarchy:** Use `group_vars/all.yaml` for system-wide defaults and consider `host_vars/<hostname>.yaml` for machine-specific overrides (like `mac_address`, which is already being done correctly).

### 1.3. Pre-build a Docker Image for `pipecatapp`

- [ ] **Add a flag to `bootstrap.sh`:** As suggested, add a `--run-local` or similar flag to the bootstrap script to allow switching between the new Docker-based deployment and the old `raw_exec` method for debugging purposes.
- [ ] **Create a `Dockerfile` for the `pipecatapp` application.
- [ ] **Build and push the image to a registry as part of the development process.
- [ ] **Simplify the Nomad job to use the `docker` driver with the pre-built image.

## 2. Medium-Priority: Testing and Usability

### 2.1. Bolster Automated Testing

- [ ] **Implement Ansible Molecule tests:** Create a Molecule test scenario for at least one critical role (e.g., `nomad` or `docker`). This involves creating a test playbook that can be run against a temporary Docker container to verify the role's functionality in isolation.
- [ ] **Expand end-to-end tests:** Add a new test case to `e2e-tests.yaml` that verifies a core function of the agent, such as a simple tool call (e.g., asking the `mcp_tool` for its status).
- [ ] **Increase unit test coverage:** Write unit tests for the remaining Python tools in the `tools/` directory to ensure each function behaves as expected.

### 2.2. Improve Web UI and User Experience

- [ ] **Replace ASCII art:** As planned, a more dynamic and expressive animated character or graphic will be created.
- [ ] **Add a "Clear Terminal" button:** Provide a simple way for the user to clear the log history in the UI.
- [ ] **Improve status display:** The current status display is just a JSON dump. Format this into a more readable table or list that clearly shows the status of each pipeline and service.

---

## 3. Future Enhancements and Backlog

This section includes items from the original "For Future Review" list, expanded with more concrete action items.

- [ ] **Implement Graceful LLM Failover:**
  - The `llama-expert.nomad` job template already loops through a list of models. Enhance this by adding a final, lightweight fallback model to the end of every model list in `group_vars/models.yaml` (e.g., a 3B parameter model). This ensures that even if larger models fail to load due to memory constraints, the expert service will still start with a basic capability.
- [ ] **Re-evaluate Consul Connect Service Mesh:**
  - Once the core system is stable, create a new feature branch and attempt to re-enable `sidecar_service` in the Nomad job files. Document the exact steps needed to configure the service mesh and any performance overhead observed.
- [ ] **Add Pre-flight System Health Checks:**
  - Create a new Ansible role named `preflight_checks`. This role should run at the very beginning of `playbook.yaml`.
  - Add tasks to this role to perform non-destructive checks:
    - Verify that the filesystem is writable by creating and 'deleting a temporary file.
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

- [ ] Add a `wait_for` to the `home_assistant` role to ensure the `mqtt` service is running before starting the `home-assistant` service.
- [ ] Create a new integration test file for home assistant.
- [ ] Add the new test to `e2e-tests.yaml`.
- [ ] Modify `start_services.sh` to include the home assistant job.
- [ ] Investigate https://github.com/microsoft/agent-lightning as a possible agent improvement method
```
