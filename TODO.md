# TODO

Last updated: 2025-11-26

```markdown
Last updated: 2025-11-26

# TODO

This document outlines the major refactoring, feature enhancement, and maintenance tasks for the project. It is divided into high-priority tasks for improving stability and a backlog of future enhancements.

---

## Prompt Engineering Enhancements

This section tracks future improvements for the DGM-style evolutionary workflow.

- [ ] **Implement Automated Testing for `prompt_engineering`:**
    - Create a new test suite (e.g., `tests/unit/test_prompt_engineering.py`).
    - Add unit tests for the core logic in `run_campaign.py`, `visualize_archive.py`, and `promote_agent.py`.
    - Mock the `subprocess` calls to `evolve.py` to test the campaign loop without running the full, slow evolution process.
    - Create a small, temporary mock archive to test the analysis, visualization, and promotion scripts against a known, controlled dataset.

- [ ] **Improve Parent Selection Algorithm:**
    - Research alternative selection strategies from evolutionary computation (e.g., tournament selection, novelty search).
    - Add a new command-line argument to `evolve.py` to allow the user to choose the selection strategy (e.g., `--selection-method tournament`).
    - Implement the new selection logic in the `select_parent_from_archive` function.

- [ ] **Web-Based UI for Campaign Analysis:**
    - Create a new script `archive_server.py` using a lightweight web framework like Flask or FastAPI.
    - The server should have an endpoint that reads the entire `archive/` directory and constructs a JSON representation of the evolutionary tree.
    - Create a simple, single-page HTML/JavaScript frontend that fetches this JSON and uses a library (like D3.js or vis.js) to render an interactive evolutionary tree.
    - The UI should allow clicking on a node to display the agent's full details (code, rationale, fitness, parent) in a side panel.

---

## Major Feature Additions

### [COMPLETED] Implement SEAL-Inspired Self-Adaptation Loop

This file tracks the implementation of a new self-adapting capability inspired by the SEAL paper. The goal is to create a closed loop where the system can reflect on its own failures and trigger a prompt evolution process to autonomously improve its core agent prompts.

#### Key Components

- [X] **ADAPTATION_AGENT.md**: A new agent definition file to formally describe the self-improvement agent's role.
- [X] **adaptation_manager.py**: A new script to orchestrate the adaptation process, generating test cases from failures.
- [X] **supervisor.py modifications**: Integrate the `adaptation_manager.py` into the main system loop.
- [X] **evolve.py modifications**: Update the prompt evolution script to accept an external test case file.
- [X] **Documentation Updates**: Update `ARCHITECTURE.md` to reflect the new capabilities.

#### Task Breakdown

1. [X] **Create `TODO.md`**: Initialize this tracking document.
2. [X] **Define `ADAPTATION_AGENT.md`**: Create the markdown file in `prompt_engineering/agents/`.
3. [X] **Develop `adaptation_manager.py`**:
    - [X] Stub out the main function and argument parsing.
    - [X] Implement logic to receive failure data.
    - [X] Implement logic to generate a YAML test case file from the failure data.
    - [X] Implement logic to call the `evolve.py` script with the new test case.
4. [X] **Modify `supervisor.py`**:
    - [X] Add a call to `adaptation_manager.py` when `reflect.py` returns an `error` action.
5. [X] **Modify `evolve.py`**:
    - [X] Add argument parsing for an external test case file.
    - [X] Update the test case loading logic to use the provided file if available.
6. [X] **Update `ARCHITECTURE.md`**:
    - [X] Add a new section describing the "Self-Adaptation Loop".
    - [X] Include the `ADAPTATION_AGENT.md` in the agent hierarchy.
7. [X] **Final Review and Testing**:
    - [X] Manually trigger a failure to test the end-to-end loop.
    - [X] Review all new code and documentation for clarity and correctness.

---

### [COMPLETED] Phase 2: Implement the OpenAI-Compatible MoE Gateway

**Goal:** Create a new, standalone service that exposes the cluster's MoE capabilities to external clients.

1. [X] **Create a New Ansible Role (`moe_gateway`):**
    - Create the directory structure `ansible/roles/moe_gateway/`.
    - Inside, create `tasks/main.yaml` and `files/`.

2. [X] **Develop the Gateway Application:**
    - In `ansible/roles/moe_gateway/files/`, create a Python script `gateway.py`.
    - This script will be a FastAPI application with a single `/v1/chat/completions` endpoint.
    - It will need to discover the `pipecat-app`'s text message queue.
    - It will need a mechanism to receive a response.

3. [X] **Create the Nomad Job:**
    - In `ansible/roles/moe_gateway/files/`, create a `moe-gateway.nomad` job file.
    - This job will run the `gateway.py` application. It should register a `moe-gateway` service in Consul.

4. [X] **Update the `pipecat-app`:**
    - Modify `app.py` and `web_server.py`. The `TwinService` needs to be able to check if an incoming text message has a `response_queue_id`.
    - If it does, the final text response from the agent should be put onto that specific queue instead of being sent to the TTS service.

5. [X] **Update the Main Playbook:**
    - Add the `moe_gateway` role to `playbook.yaml` so it gets deployed along with the other core services.

---

## High-Priority: Harden the Core System
#### Phase 3: Documentation and Cleanup [COMPLETED]

**Goal:** Finalize the project by cleaning up obsolete files and creating clear documentation for the new features.

1. **[COMPLETED] Remove Obsolete Scripts:**
    - The `debian_service/` and `initial-setup/` directories have been removed and their logic migrated.

2. **[COMPLETED] Create API Documentation:**
    - `API_USAGE.md` has been created and documented.

3. **[COMPLETED] Review and Finalize `TODO.md`:**
    - The `TODO.md` has been reviewed and updated.

---

#### Phase 4: Implement the "ComfyUI for Agents" Workflow Engine

**Goal:** Refactor the monolithic agent loop into a modular, declarative workflow engine, as outlined in `docs/TOOL_EVALUATION.md`.

1.  **[COMPLETED] Refactor Core Logic into a Workflow Runner:**
    - **[COMPLETED]** The main `run_agent_loop` in `app.py` has been replaced with a `WorkflowRunner` class.
    - **[COMPLETED]** Agent behavior is now defined in `workflows/default_agent_loop.yaml`.
    - **[COMPLETED]** Created a `nodes` directory with modular classes for each step (e.g., `LLMNode`, `ToolNode`, `GateNode`).

2.  **[COMPLETED] Create a Real-time Visualization UI:**
    - **[COMPLETED]** A new `/workflow` endpoint serves a web UI using Cytoscape.js.
    - **[COMPLETED]** New API endpoints (`/api/workflows/definition/*` and `/api/workflows/active`) provide the UI with the graph structure and real-time execution state.
    - **[COMPLETED]** The UI now includes an interactive modal to inspect the outputs of each executed node.

3.  **[TODO] Persist and Expose Workflow History:**
    - **[ ]** Modify the `WorkflowRunner` to save its final context to a persistent store (e.g., a local SQLite database or a JSONL file) upon completion.
    - **[ ]** Create a new API endpoint (e.g., `/api/workflows/history`) to retrieve a list of past workflow runs.
    - **[ ]** Add a history browser to the web UI to allow users to select and view the final state of previous runs.

4.  **[TODO] Build a Visual Workflow Editor:**
    - **[ ]** Integrate a library like `litegraph.js` or extend the existing Cytoscape UI to allow drag-and-drop creation and modification of workflows.
    - **[ ]** Create a backend API endpoint (`/api/workflows/save`) to receive the new graph definition from the UI and save it as a YAML file.

## 1. High-Priority: Harden the Core System

These tasks are focused on addressing the brittleness of the deployment process and making the system more resilient, predictable, and maintainable.

### 1.1. Refactor for Strict Idempotency in Ansible

- [X] **Apply `creates` argument to compilation tasks:** In roles like `llama_cpp` and `whisper_cpp`, the `cmake` and `make` tasks should be skipped if the final binary artifacts already exist. This will prevent unnecessary and potentially error-prone recompilation on every playbook run.
  - *Example (`ansible/roles/llama_cpp/tasks/main.yaml`):*

    ```yaml
    - name: Build llama.cpp
      ansible.builtin.command:
        cmd: cmake --build build --config Release -j 2
      args:
        chdir: /opt/llama.cpp-build
        creates: /opt/llama.cpp-build/build/bin/llama-server # This line prevents re-running
    ```

- [X] **Audit all roles for idempotency:** Systematically review every task in every role (`common`, `docker`, `nomad`, `consul`, etc.) and apply idempotency checks where they are missing.

### 1.2. Centralize All Configuration

- [ ] **Migrate hardcoded variables to `group_vars`:** Search the entire codebase for hardcoded values (e.g., paths, usernames, ports, service names) and replace them with Ansible variables defined in `group_vars/all.yaml`.
- [ ] **Convert all configuration files to templates:** Any file that contains a variable should be a Jinja2 template (`.j2`).
- [ ] **Establish a clear variable hierarchy:** Use `group_vars/all.yaml` for system-wide defaults and consider `host_vars/<hostname>.yaml` for machine-specific overrides.

### 1.3. Pre-build a Docker Image for `pipecatapp`

- [ ] **Add a flag to `bootstrap.sh`:** Add a `--run-local` or similar flag to the bootstrap script to allow switching between a Docker-based deployment and the old `raw_exec` method for debugging.
- [ ] **Create a `Dockerfile` for the `pipecatapp` application.
- [ ] **Build and push the image to a registry as part of the development process.
- [ ] **Simplify the Nomad job to use the `docker` driver with the pre-built image.

## 2. Medium-Priority: Testing and Usability

### 2.1. Bolster Automated Testing

- [ ] **Implement Ansible Molecule tests:** Create a Molecule test scenario for at least one critical role (e.g., `nomad` or `docker`).
- [ ] **Expand end-to-end tests:** Add a new test case to `e2e-tests.yaml` that verifies a core function of the agent.
- [ ] **Increase unit test coverage:** Write unit tests for the remaining Python tools in the `tools/` directory.

### 2.2. Improve Web UI and User Experience

- [ ] **Replace ASCII art:** Create a more dynamic and expressive animated character or graphic.
- [ ] **Add a "Clear Terminal" button:** Provide a simple way for the user to clear the log history in the UI.
- [ ] **Improve status display:** Format the status display into a more readable table or list.

---

## 3. Future Enhancements and Backlog

- [ ] **Implement Graceful LLM Failover:** Enhance the `llama-expert.nomad` job to include a final, lightweight fallback model.
- [ ] **Re-evaluate Consul Connect Service Mesh:** Create a new feature branch to attempt to re-enable `sidecar_service` in the Nomad job files and document the process.
- [ ] **Add Pre-flight System Health Checks:** Create a new Ansible role to perform non-destructive checks at the beginning of `playbook.yaml`.
- [ ] **Investigate Advanced Power Management:** Research and prototype a more advanced version that uses Wake-on-LAN.
- [ ] **Expand the Model Collection:** Systematically test and add the remaining LiquidAI nano models to `group_vars/models.yaml`.
- [ ] **Security Hardening:**
  - **Remove passwordless sudo:** Modify the sudoers file configuration to require a password for the `target_user`.
  - **Run services as non-root users:** Audit all services and ensure they are running as dedicated, non-privileged users where possible.
- [ ] **Monitoring and Observability:** Deploy a monitoring stack like Prometheus and Grafana.
- [ ] Add a `wait_for` to the `home_assistant` role to ensure the `mqtt` service is running before starting the `home-assistant` service.
- [ ] Create a new integration test file for home assistant.
- [ ] Add the new test to `e2e-tests.yaml`.
- [ ] Modify `start_services.sh` to include the home assistant job.
- [ ] Investigate https://github.com/microsoft/agent-lightning as a possible agent improvement method.

## 4. Maintenance & Clean Up

This section tracks identified placeholder files, corrupted binaries, and code that needs to be fixed or removed.

- [X] **Remove or Implement Empty Handler:**
  - `ansible/roles/bootstrap_agent/handlers/main.yaml` is currently empty.

- [X] **Fix Corrupted Model Files:**
  - The following files are 0 bytes and appear to be corrupted:
    - `en_US-lessac-medium.onnx`
    - `chat.prompt.bin`
    - `bob.prompt.bin`

- [X] **Fix Corrupted Binaries:**
  - The following executable files are 0 bytes:
    - `distributed-llama-repo/dllama`
    - `distributed-llama-repo/dllama-api`

- [X] **Refactor Brittle Code:**
  - `ansible/roles/pipecatapp/files/tools/smol_agent_tool.py`: Contains a TODO about brittle code extraction logic.

- [X] **Fix Skipped Test:**
  - `tests/unit/test_home_assistant_template.py`: Test is currently skipped and contains a TODO to re-add it without breaking tests.

- [X] **Reconcile Stale Artifacts:**
  - `docker/pipecatapp/app.py` contains code and TODOs (e.g., vision model failover) that are not present in the source `ansible/roles/pipecatapp/files/app.py`. Determine if these changes should be merged or if the artifact should be regenerated.
