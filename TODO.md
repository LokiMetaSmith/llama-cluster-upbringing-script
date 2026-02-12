# TODO

## Immediate Actions

- [x] **Read and evaluate VLLM project findings:**
  - Read `docs/VLLM_PROJECT_EVALUATION.md` to understand the potential of Semantic Router, GuideLLM, and vLLM Omni.
  - Decide on the implementation timeline for `semantic_router` and `guidellm`.
- [x] **Implement LLMRouter Integration (Proof of Concept):**
  - **Goal:** Replace static "tiered" routing in `SimpleLLMNode` with dynamic, semantic routing using `LLMRouter`.
  - **Tasks:**
    1. Add `llmrouter` to `ansible/roles/python_deps/files/requirements.txt`.
    2. Create a new `LLMRouterNode` class in `workflow/nodes/llm_nodes.py` (see `docs/EVALUATION_LLMROUTER.md` for design).
    3. Implement a basic mapping config to route between at least two local experts (e.g., `llamacpp-rpc-main` vs. `llamacpp-rpc-coding`).
    4. Update a test workflow to use this new node.
- [ ] **Train and Configure LLMRouter:**
  - **Goal:** Replace the heuristic PoC logic in `LLMRouterNode` with a fully trained `LLMRouter` instance.
  - **Tasks:**
    1. Generate a training dataset of queries and optimal models using `LLMRouter`'s data generation tools.
    2. Train the router to map queries to our specific local experts.
    3. Update `LLMRouterNode` to load the trained config/model.

## Agentic Patterns Implementation

- [x] **Implement Technician Agent:**
  - Create a 3-phase agent (Plan, Execute, Reflect) in `pipecatapp/technician_agent.py`.
  - Update `SwarmTool` to support spawning technician agents.
- [ ] **Swarm Orchestration (Map-Reduce):**
  - **Goal:** Implement the "Swarm Migration" pattern where a manager agent splits a large task into chunks and dispatches them to multiple Technician Agents.
  - **Tasks:**
    1. Create a `ManagerAgent` or update `TechnicianAgent` to have a "Manager Mode".
    2. Implement the "Map" phase: Analysis of the task and generation of sub-task definitions.
    3. Implement the "Dispatch" phase: Using `SwarmTool` to spawn multiple `technician` agents.
    4. Implement the "Reduce" phase: Aggregating results from the spawned workers.
- [ ] **Durable Execution Integration:**
  - **Goal:** Ensure `TechnicianAgent` can resume execution after a crash or restart.
  - **Tasks:**
    1. Update `TechnicianAgent` to use `pipecatapp.durable_execution.DurableExecutionEngine`.
    2. Decorate the `execute_step` method with `@durable_step`.
    3. Ensure state (messages list, current plan) is checkpointed.
- [ ] **Skill Library (Knowledge Persistence):**
  - **Goal:** Allow agents to save successful tool usage patterns for future use.
  - **Tasks:**
    1. Create a simple file-based or database-backed Skill Library service (or use the existing Memory service).
    2. Add a `save_skill` tool to the agent's toolkit.
    3. Add a `search_skills` tool to the agent's toolkit.
    4. Update the `TechnicianAgent` reflection phase to optionally suggest saving a new skill if the task was novel and successful.

## Prompt Engineering Enhancements

- [x] **Implement Automated Testing for `prompt_engineering`:**
  - Create a new test suite (e.g., `tests/unit/test_prompt_engineering.py`).
  - Add unit tests for the core logic in `run_campaign.py`, `visualize_archive.py`, and `promote_agent.py`.
  - Mock the `subprocess` calls to `evolve.py` to test the campaign loop without running the full, slow evolution process.
  - Create a small, temporary mock archive to test the analysis, visualization, and promotion scripts against a known, controlled dataset.
- [x] **Improve Parent Selection Algorithm:**
  - Research alternative selection strategies from evolutionary computation (e.g., tournament selection, novelty search).
  - Add a new command-line argument to `evolve.py` to allow the user to choose the selection strategy (e.g., `--selection-method tournament`).
  - Implement the new selection logic in the `select_parent_from_archive` function.
- [ ] **Web-Based UI for Campaign Analysis:**
  - Create a new script `archive_server.py` using a lightweight web framework like Flask or FastAPI.
  - The server should have an endpoint that reads the entire `archive/` directory and constructs a JSON representation of the evolutionary tree.
  - Create a simple, single-page HTML/JavaScript frontend that fetches this JSON and uses a library (like D3.js or vis.js) to render an interactive evolutionary tree.
  - The UI should allow clicking on a node to display the agent's full details (code, rationale, fitness, parent) in a side panel.

## Harden the Core System

### Phase 4: Implement the "ComfyUI for Agents" Workflow Engine

- [x] **Build a Visual Workflow Editor:**
  - [x] Integrate a library like `litegraph.js` or extend the existing Cytoscape UI to allow drag-and-drop creation and modification of workflows.
  - [x] Create a backend API endpoint (`/api/workflows/save`) to receive the new graph definition from the UI and save it as a YAML file.

### Centralize All Configuration

- [ ] **Convert all configuration files to templates:** Any file that contains a variable should be a Jinja2 template (`.j2`).
- [ ] **Establish a clear variable hierarchy:** Use `group_vars/all.yaml` for system-wide defaults and consider `host_vars/<hostname>.yaml` for machine-specific overrides.

### Pre-build a Docker Image for `pipecatapp`

- [x] **Add a flag to `bootstrap.sh`:** Add a `--run-local` or similar flag to the bootstrap script to allow switching between a Docker-based deployment and the old `raw_exec` method for debugging.
- [x] **Create a `Dockerfile` for the `pipecatapp` application.**
- [ ] **Build and push the image to a registry as part of the development process.**
- [x] **Simplify the Nomad job to use the `docker` driver with the pre-built image.**

## Testing and Usability

### Bolster Automated Testing

- [x] **Implement Ansible Molecule tests:** Create a Molecule test scenario for at least one critical role (e.g., `nomad` or `docker`).
- [x] **Expand end-to-end tests:** Add a new test case to `e2e-tests.yaml` that verifies a core function of the agent.
- [x] **Increase unit test coverage:** Write unit tests for the remaining Python tools in the `tools/` directory. (Completed: added tests for `archivist_tool.py` and `swarm_tool.py`)

### Improve Web UI and User Experience

- [ ] **Replace ASCII art:** Create a more dynamic and expressive animated character or graphic.
- [x] **Add a "Clear Terminal" button:** Provide a simple way for the user to clear the log history in the UI.
- [x] **Improve status display:** Format the status display into a more readable table or list.

## Future Enhancements and Backlog

- [x] **Implement Graceful LLM Failover:** Enhance the `llama-expert.nomad` job to include a final, lightweight fallback model.
- [ ] **Re-evaluate Consul Connect Service Mesh:** Create a new feature branch to attempt to re-enable `sidecar_service` in the Nomad job files and document the process.
- [x] **Add Pre-flight System Health Checks:** Create a new Ansible role to perform non-destructive checks at the beginning of `playbook.yaml`.
- [ ] **Investigate Advanced Power Management:** Research and prototype a more advanced version that uses Wake-on-LAN.
- [ ] **Expand the Model Collection:** Systematically test and add the remaining LiquidAI nano models to `group_vars/models.yaml`.
- [ ] **Security Hardening:**
  - **Remove passwordless sudo:** Modify the sudoers file configuration to require a password for the `target_user`.
  - **Run services as non-root users:** Audit all services and ensure they are running as dedicated, non-privileged users where possible.
- [ ] **Robust Remote Node Recovery:** Add mechanism to recover remote nodes even if network stack is completely broken (possibly via serial console or IPMI automation).
- [x] **Monitoring and Observability:** Deploy a monitoring stack like Prometheus and Grafana.
- [x] Add a `wait_for` to the `home_assistant` role to ensure the `mqtt` service is running before starting the `home-assistant` service.
- [x] Create a new integration test file for home assistant.
- [x] Add the new test to `e2e-tests.yaml`.
- [x] Modify `start_services.sh` to include the home assistant job.
- [ ] Investigate <https://github.com/microsoft/agent-lightning> as a possible agent improvement method.
- [ ] **Investigate RPC Provider Monitoring:** Research how to expose or scrape metrics from `llamacpp-rpc` providers to aggregate backend performance data.

## 4. Maintenance & Clean Up

This section tracks identified placeholder files, corrupted binaries, and code that needs to be fixed or removed.

- [x] **Remove or Implement Empty Handler:**
  - `ansible/roles/bootstrap_agent/handlers/main.yaml` is currently empty.

- [ ] **Reconcile Stale Artifacts:**
  - `pipecatapp/app.py` contains code and TODOs (e.g., vision model failover). Determine if these changes should be merged or if the artifact should be regenerated.
- [x] **Vision Model Failover**: Implement failover or selection logic for vision models (see `pipecatapp/app.py`).
- [ ] **Refactor Vision Role**: The `vision` role is currently minimal (only installs `libgl1`) and does not deploy Frigate as implied by the `frigate_port` variable. It needs to be refactored to actually deploy the service.
- [ ] **Review Hardcoded Network References:**
  - **Goal:** Align Ansible roles with the "Provisioning Underlay" vs. "Cluster Overlay" architecture.
  - **Tasks:**
    1. Audit `ansible/roles/power_manager/tasks/main.yaml` for hardcoded `10.0.0.0/24` subnet references.
    2. Ensure that firewall rules (UFW/iptables) correctly handle both the provisioning underlay and the Tailscale overlay.
    3. Verify that `group_vars/all.yaml` variables are consistently used instead of hardcoded IPs.

## Completed History

- [x] Fix Memory Service networking (Port 8000 conflict).
- [x] Implement real LLM calls in `worker_agent.py` (replace mock).
- [x] Connect `PlannerTool` to real LLM for robust plan generation.
- [x] Refactor `pipecatapp` role to use Docker image for memory service in production.
- [x] Frontier Agent Roadmap Phase 1-4.
- [x] Add `frontend_verification_instructions` for UI changes.
- [x] Implement SEAL-Inspired Self-Adaptation Loop.
- [x] Phase 2: Implement the OpenAI-Compatible MoE Gateway.
- [x] Harden the Core System: Phase 3 Documentation and Cleanup.
- [x] Harden the Core System: Phase 4 Workflow Engine (Steps 1-3).
- [x] Refactor for Strict Idempotency in Ansible.
- [x] Maintenance & Clean Up (Empty Handler, Corrupted Files, etc.).

## Performance & I/O Optimization

- [x] **Optimize ExperimentTool Sandbox Creation:**
  - Replaced `shutil.copytree` with `tar` snapshotting to reduce syscall overhead.
- [x] **Optimize ProjectMapperTool Scanning:**
  - Implemented `git ls-files` strategy for faster file listing in git repositories.
- [ ] **Review Codebase for I/O Inefficiencies:**
  - **Goal:** Identify and optimize other areas with heavy syscall usage (e.g., logging, data processing).
  - **Strategy:** Look for repeated file opens/closes in loops, inefficient directory traversals, and opportunities to batch I/O or use `tar`/`sqlite` strategies.

## Security Audit

- [x] **Audit and remove hardcoded secrets:**
  - Audit frontend code (`pipecatapp/static/js`), workflows (`workflows/`), and tools (`pipecatapp/tools/`) for hardcoded secrets, API keys, or tokens.
  - Remove any found secrets and replace them with secure environment variable loading.
- [ ] **Audit unauthenticated API endpoints:**
  - Review `pipecatapp/web_server.py` and other API definitions to ensure sensitive data endpoints are authenticated.
  - Specifically check endpoints returning user data or configuration.
- [ ] **Audit WebSocket security:**
  - Verify that WebSocket connections enforce strict Origin checks to prevent Cross-Site WebSocket Hijacking (CSWSH).
  - Consider implementing authentication for WebSocket connections.
- [ ] **Audit write access controls:**
  - Ensure that all state-changing endpoints (POST, PUT, PATCH) require authentication and authorization.
  - Verify that unauthenticated users cannot modify workflows or agent state.
- [ ] **Audit rate limiting configuration:**
  - Review rate limiting settings in `pipecatapp/rate_limiter.py` and `pipecatapp/web_server.py`.
  - Ensure critical endpoints have stricter limits to prevent abuse.
- [ ] **Audit data storage security:**
  - Check how sensitive data (e.g., in `pipecatapp/memory.py` or database integrations) is stored.
  - Ensure encryption at rest is considered or implemented for sensitive fields.
