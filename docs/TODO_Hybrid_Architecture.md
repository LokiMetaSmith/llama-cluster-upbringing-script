# Hybrid Architecture Implementation To-Do List

This document tracks the engineering tasks required to migrate to the Hybrid / Cluster-Native architecture defined in [REFACTOR_PROPOSAL_hybrid_architecture.md](./REFACTOR_PROPOSAL_hybrid_architecture.md).

## Phase 1: Configurable Tool Factory (Local vs Remote)

Objective: Allow the application to choose between running tools in-process (Monolith) or via the Tool Server (Distributed) based on configuration.

- [ ] **Define Configuration Schema**
  - [ ] Add `tool_execution_mode` (enum: `local`, `remote`) to `config/app/settings` in Consul.
  - [ ] Update `ansible/roles/pipecatapp/templates/pipecat.env.j2` to expose this as an environment variable `TOOL_EXECUTION_MODE`.

- [ ] **Implement Remote Tool Proxy**
  - [ ] Create `pipecatapp/tools/remote_tool_proxy.py`.
  - [ ] Implement a generic `RemoteToolProxy` class that accepts a `tool_name` and `base_url`.
  - [ ] Implement `__getattr__` or explicit methods to forward calls to the Tool Server API (`POST /run_tool`).
  - [ ] Handle authentication (forward `TOOL_SERVER_API_KEY`).

- [ ] **Refactor Agent Factory (`pipecatapp/agent_factory.py`)**
  - [ ] Update `create_tools(config, ...)` to read `config.get("tool_execution_mode")`.
  - [ ] Implement conditional logic:

        ```python
        if config.get("tool_execution_mode") == "remote":
            tools["ssh"] = RemoteToolProxy("ssh", config["tool_server_url"])
        else:
            tools["ssh"] = SSH_Tool()
        ```

  - [ ] Ensure "Heavy" tools (e.g., `CodeRunnerTool`) respect this setting.
  - [ ] Ensure "Light" tools (e.g., `Calculator`) always run locally if possible, or add a split configuration (e.g., `heavy_tools_mode`).

## Phase 2: In-Process Logic Consolidation

Objective: Enable the main `pipecatapp` container to perform LLM inference and manage state locally, eliminating the need for sidecar containers on Tier 2 nodes.

- [ ] **Refactor LLM Service Initialization (`pipecatapp/app.py`)**
  - [ ] Add support for `llama-cpp-python` direct loading.
  - [ ] In `main()`, check `RUN_LOCAL_LLM` environment variable.
  - [ ] If true:
    - [ ] Import `llama_cpp`.
    - [ ] Initialize `Llama` class with model path from `nomad/models/`.
    - [ ] Wrap it in a `LocalLLMService` class that adheres to the Pipecat `LLMService` interface.
  - [ ] If false (default): Continue using `OpenAILLMService` pointing to `LLAMA_API_SERVICE_NAME`.

- [ ] **Integrate World Model**
  - [ ] Create `pipecatapp/local_world_model.py`.
  - [ ] Implement a singleton class `LocalWorldModel` that matches the API of the MQTT-based service.
  - [ ] In `app.py`, conditionally instantiate `LocalWorldModel` vs `MQTTWorldModelClient` based on `WORLD_MODEL_MODE` (local/distributed).
  - [ ] Ensure `LocalWorldModel` still publishes updates to MQTT (fire-and-forget) so external observers (Home Assistant) stay in sync, even if the app doesn't read from MQTT.

- [ ] **Deprecate "Expert" Container**
  - [ ] Update `ansible/roles/pipecatapp/tasks/main.yaml` to make the deployment of `expert-*.nomad` jobs conditional on `deploy_topology != 'monolith'`.

## Phase 3: Adaptive Service Discovery

Objective: Allow the application to seamlessly switch between finding services on `localhost` and finding them via Consul DNS, without code changes.

- [ ] **Update Service Discovery Logic (`app.py`)**
  - [ ] Modify `discover_services` function.
  - [ ] Add logic to check for "Override URLs" in environment variables first:
    - [ ] `LLAMA_API_URL_OVERRIDE`
    - [ ] `TOOL_SERVER_URL_OVERRIDE`
  - [ ] If override is present, use it directly and skip Consul lookup.
  - [ ] If override is absent, proceed with Consul `health/service/` check.

- [ ] **Configure Ansible for Tiered Deployment**
  - [ ] Update `group_vars/all.yaml` or inventory vars to define `node_tier` (edge, mid, core).
  - [ ] In `ansible/roles/pipecatapp/templates/pipecat.env.j2`:
    - [ ] If `node_tier == 'mid'` (Monolith), set `LLAMA_API_URL_OVERRIDE = "http://localhost:8080"` (or internal pointer).
    - [ ] If `node_tier == 'edge'`, set `LLAMA_API_URL_OVERRIDE` to the Core Node's address.

- [ ] **Update Bootstrap CLI (`bootstrap.sh`)**
  - [ ] Add a new flag `--tier [edge|mid|core]` to `bootstrap.sh`.
  - [ ] Pass this flag as an extra-var `node_tier` to the Ansible playbook.
  - [ ] Update the help menu to explain the new tier options.

## Phase 4: Docker Image Optimization

Objective: Create a single, flexible Docker image that can run in any of the three modes.

- [ ] **Update Python Dependencies**
  - [ ] Review `pipecatapp/requirements.txt`.
  - [ ] Ensure `llama-cpp-python` is included (or installed in the base image) but does not crash if no GPU is present (use CPU-only fallback build or conditional import).
  - [ ] Ensure `fastapi` and `uvicorn` are present for the Web UI.

- [ ] **Enhance Startup Script (`pipecatapp/start_pipecat.sh`)**
  - [ ] Add logic to `ansible/roles/pipecatapp/templates/start_pipecatapp.sh.j2` (or `pipecatapp/start_pipecat.sh`).
  - [ ] Parse `NODE_ROLE` or `DEPLOYMENT_MODE`.
  - [ ] If `MODE=monolith`, start `app.py` directly.
  - [ ] If `MODE=distributed`, ensure `consul-template` or sidecars are ready before starting.

- [ ] **Validate Build Process**
  - [ ] Run `ansible-playbook` with `pipecat_deployment_style=docker` to verify image build.
  - [ ] Verify image size impact (ensure we aren't bloating the Edge image with unused heavy libraries if possible, though a unified image is preferred for simplicity).

## Phase 5: Verification & Documentation

- [ ] **Create Architecture Test Suite**
  - [ ] Create a test for "Monolith Mode": Mock network/Consul, verify App can answer "Hello" using only local classes.
  - [ ] Create a test for "Distributed Mode": Verify App fails if Consul/Remote LLM is missing.

- [ ] **Update User Documentation**
  - [ ] Update `README.md` with "Deployment Options" section.
  - [ ] Document how to set `node_tier` in Ansible inventory.
