# TODO

## Prompt Engineering Enhancements
- [x] **Implement Automated Testing for `prompt_engineering`:**
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

## Harden the Core System

### Phase 4: Implement the "ComfyUI for Agents" Workflow Engine
- [ ] **Build a Visual Workflow Editor:**
    - [ ] Integrate a library like `litegraph.js` or extend the existing Cytoscape UI to allow drag-and-drop creation and modification of workflows.
    - [ ] Create a backend API endpoint (`/api/workflows/save`) to receive the new graph definition from the UI and save it as a YAML file.

### Centralize All Configuration
- [ ] **Convert all configuration files to templates:** Any file that contains a variable should be a Jinja2 template (`.j2`).
- [ ] **Establish a clear variable hierarchy:** Use `group_vars/all.yaml` for system-wide defaults and consider `host_vars/<hostname>.yaml` for machine-specific overrides.

### Pre-build a Docker Image for `pipecatapp`
- [ ] **Add a flag to `bootstrap.sh`:** Add a `--run-local` or similar flag to the bootstrap script to allow switching between a Docker-based deployment and the old `raw_exec` method for debugging.
- [ ] **Create a `Dockerfile` for the `pipecatapp` application.**
- [ ] **Build and push the image to a registry as part of the development process.**
- [ ] **Simplify the Nomad job to use the `docker` driver with the pre-built image.**

## Testing and Usability

### Bolster Automated Testing
- [ ] **Implement Ansible Molecule tests:** Create a Molecule test scenario for at least one critical role (e.g., `nomad` or `docker`).
- [x] **Expand end-to-end tests:** Add a new test case to `e2e-tests.yaml` that verifies a core function of the agent.
- [ ] **Increase unit test coverage:** Write unit tests for the remaining Python tools in the `tools/` directory. (Partially completed: added tests for `project_mapper_tool.py`)

### Improve Web UI and User Experience
- [ ] **Replace ASCII art:** Create a more dynamic and expressive animated character or graphic.
- [x] **Add a "Clear Terminal" button:** Provide a simple way for the user to clear the log history in the UI.
- [x] **Improve status display:** Format the status display into a more readable table or list.

## Future Enhancements and Backlog
- [ ] **Implement Graceful LLM Failover:** Enhance the `llama-expert.nomad` job to include a final, lightweight fallback model.
- [ ] **Re-evaluate Consul Connect Service Mesh:** Create a new feature branch to attempt to re-enable `sidecar_service` in the Nomad job files and document the process.
- [ ] **Add Pre-flight System Health Checks:** Create a new Ansible role to perform non-destructive checks at the beginning of `playbook.yaml`.
- [ ] **Investigate Advanced Power Management:** Research and prototype a more advanced version that uses Wake-on-LAN.
- [ ] **Expand the Model Collection:** Systematically test and add the remaining LiquidAI nano models to `group_vars/models.yaml`.
- [ ] **Security Hardening:**
  - **Remove passwordless sudo:** Modify the sudoers file configuration to require a password for the `target_user`.
  - **Run services as non-root users:** Audit all services and ensure they are running as dedicated, non-privileged users where possible.
- [ ] **Robust Remote Node Recovery:** Add mechanism to recover remote nodes even if network stack is completely broken (possibly via serial console or IPMI automation).
- [ ] **Monitoring and Observability:** Deploy a monitoring stack like Prometheus and Grafana.
- [ ] Add a `wait_for` to the `home_assistant` role to ensure the `mqtt` service is running before starting the `home-assistant` service.
- [ ] Create a new integration test file for home assistant.
- [ ] Add the new test to `e2e-tests.yaml`.
- [ ] Modify `start_services.sh` to include the home assistant job.
- [ ] Investigate https://github.com/microsoft/agent-lightning as a possible agent improvement method.
- [ ] **Vision Model Failover**: Implement failover or selection logic for vision models (see `ansible/roles/pipecatapp/files/app.py`).

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
