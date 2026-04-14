# TODO

## Immediate Actions

- [x] **Bootable System Installation & Auto-Configuration:**
  - **Goal:** Create a slimmed-down, bootable Debian ISO and enhance `bootstrap.sh` to auto-detect hardware resources.
  - **Tasks:**
    1. [x] Update `bootstrap.sh` to profile system resources (CPU cores, RAM).
    2. [x] Dynamically configure `--role` (controller, worker, all) and model settings based on available hardware (e.g., fallback to external models on 4GB machines).
    3. [x] Create a `live-build` configuration to generate a custom, headless Debian bootable ISO that includes the project source and dependencies.
- [x] **Migrate to Hybrid Architecture (Phase 1):**
  - **Goal:** Allow the application to choose between running tools in-process (Monolith) or via the Tool Server (Distributed).
  - Reference: `docs/TODO_Hybrid_Architecture.md`
- [x] **Implement Active Vault Workflow (Phase 1):**
  - **Goal:** Support 3D spatial properties in nodes and implement `CanvasConverter`.
  - Reference: `docs/OBSIDIAN_WORKFLOW_DESIGN.md`
- [x] **Train and Configure LLMRouter:**
  - **Goal:** Replace the heuristic PoC logic in `LLMRouterNode` with a fully trained `LLMRouter` instance.
  - **Tasks:**
    1. [x] Generate a training dataset of queries and optimal models using `LLMRouter`'s data generation tools.
    2. [x] Train the router to map queries to our specific local experts.
    3. [x] Update `LLMRouterNode` to load the trained config/model.

## Agentic Patterns Implementation

- [x] **Implement Technician Agent:**
  - Create a 3-phase agent (Plan, Execute, Reflect) in `pipecatapp/technician_agent.py`.
  - Update `SwarmTool` to support spawning technician agents.
- [x] **Swarm Orchestration (Map-Reduce):**
  - **Goal:** Implement the "Swarm Migration" pattern where a manager agent splits a large task into chunks and dispatches them to multiple Technician Agents.
  - **Tasks:**
    1. [x] Create a `ManagerAgent` or update `TechnicianAgent` to have a "Manager Mode".
    2. [x] Implement the "Map" phase: Analysis of the task and generation of sub-task definitions.
    3. [x] Implement the "Dispatch" phase: Using `SwarmTool` to spawn multiple `technician` agents.
    4. [x] Implement the "Reduce" phase: Aggregating results from the spawned workers.
- [x] **Durable Execution Integration:**
  - **Goal:** Ensure `TechnicianAgent` can resume execution after a crash or restart.
  - **Tasks:**
    1. [x] Update `TechnicianAgent` to use `pipecatapp.durable_execution.DurableExecutionEngine`.
    2. [x] Decorate the `execute_step` method with `@durable_step`.
    3. [x] Ensure state (messages list, current plan) is checkpointed.
- [x] **Skill Library (Knowledge Persistence):**
  - **Goal:** Allow agents to save successful tool usage patterns for future use.
  - **Tasks:**
    1. [x] Create a simple file-based or database-backed Skill Library service (or use the existing Memory service).
    2. [x] Add a `save_skill` tool to the agent's toolkit.
    3. [x] Add a `search_skills` tool to the agent's toolkit.
    4. [x] Update the `TechnicianAgent` reflection phase to optionally suggest saving a new skill if the task was novel and successful.

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
- [x] **Web-Based UI for Campaign Analysis:**
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

- [ ] **Convert all configuration files to templates (Recurring Review):** Any file that contains a variable should be a Jinja2 template (`.j2`). Ensure new services follow this pattern.
- [x] **Establish a clear variable hierarchy (Recurring Review):** Use `group_vars/all.yaml` for system-wide defaults and consider `host_vars/<hostname>.yaml` for machine-specific overrides. Audit periodically.

### Pre-build a Docker Image for `pipecatapp`

- [x] **Add a flag to `bootstrap.sh`:** Add a `--run-local` or similar flag to the bootstrap script to allow switching between a Docker-based deployment and the old `raw_exec` method for debugging.
- [x] **Create a `Dockerfile` for the `pipecatapp` application.**
- [x] **Build and push the image to a registry as part of the development process.**
- [x] **Simplify the Nomad job to use the `docker` driver with the pre-built image.**

## Testing and Usability

### Bolster Automated Testing

- [x] **Implement Ansible Molecule tests:** Create a Molecule test scenario for at least one critical role (e.g., `nomad` or `docker`).
- [x] **Expand end-to-end tests:** Add a new test case to `e2e-tests.yaml` that verifies a core function of the agent.
- [x] **Increase unit test coverage:** Write unit tests for the remaining Python tools in the `tools/` directory. (Completed: added tests for `archivist_tool.py` and `swarm_tool.py`)

### Improve Web UI and User Experience

- [x] **Replace ASCII art:** Create a more dynamic and expressive animated character or graphic.
- [x] **Add a "Clear Terminal" button:** Provide a simple way for the user to clear the log history in the UI.
- [x] **Improve status display:** Format the status display into a more readable table or list.
- [x] **Frontend for Real-Time Steering (UI Integration):**
  - **Goal:** Expose the `PersonalityTool` capabilities in the web interface.
  - **Tasks:**
    1. Add a "Personality" or "Brain" tab to `cluster.html` or `monitor.html`.
    2. Create sliders or controls to adjust specific axis vectors (e.g., "Assistant <-> Creative").
    3. Connect the frontend controls to the `llama.cpp` `/control-vectors` API (possibly proxied through `web_server.py`).

## Architecture 2.0 (Post 1.0 Release)

These structural suggestions are targeted for a future major release to significantly simplify deployment logic and enforce the separation of concerns between infrastructure and application lifecycle management.

- [ ] **Decouple Task Supervisor from Subprocesses:** Consider replacing raw subprocess polling in `TaskSupervisor` with Nomad API task submission or a distributed task queue (like Celery) for better cluster-native fault tolerance.

- [x] **Native Ansible Hardware Profiling:** Move the machine resource detection logic (RAM, CPU, Disk) out of `bootstrap.sh` and into a native Ansible `preflight` playbook using `setup` facts. Ansible should dynamically group hosts (e.g., using `group_by`) and execute roles conditionally based on the detected hardware tier, reducing reliance on Bash wrapper scripts.
- [ ] **Strict Infrastructure vs. Payload Separation:** Restrict Ansible playbooks to provisioning the "underlay" infrastructure (OS configuration, Docker, Consul, Nomad, network overlay). Migrate the deployment of the application payload (`pipecatapp`, `llamacpp`, AI experts) entirely to Nomad job specifications (`.nomad` files) managed via a dedicated tool (like Terraform/OpenTofu or a pure Nomad submission script) rather than using Ansible to start application services.
- [ ] **Microservice De-monolithization of `TwinService`:** To improve robustness on legacy hardware, the main `pipecatapp` (router/workflow engine) should be made as lightweight as possible. Extract heavy, blocking tools (e.g., RAG document embedding, isolated Python code execution sandboxes) into independent microservices running as separate Nomad jobs. The core agent should interact with these tools exclusively via the Consul Service Mesh.

## Future Enhancements and Backlog

### Integrate LangChain (Tandem/Hybrid Approach)

- [x] **Phase 1: Build a `LangChainToolAdapter`:**
  - Create a wrapper class in `pipecatapp/tools/` capable of ingesting any LangChain `BaseTool` and exposing it through the standard methods expected by our `ToolExecutorNode` and UI approval queue (`TwinService._request_approval`).
- [x] **Phase 2: RAG Internals Enhancement:**
  - Update `RAG_Tool.add_document()` to utilize LangChain's `DocumentLoaders` (e.g., `DirectoryLoader`, `PyMuPDFLoader`) and `RecursiveCharacterTextSplitter` internally, maintaining the tool's external API.
- [x] **Phase 3: Create LangChain Memory Wrappers:**
  - Implement `PMMChatMessageHistory` (inheriting from `BaseChatMessageHistory`) that reads/writes to our deterministic `pmm_memory.db` ledger.
  - Implement `PipecatVectorStore` (inheriting from `VectorStore`) wrapping our custom `memory.py` FAISS/SQLite setup.
- [x] **Phase 4: Build a `LangGraphNode` for the Workflow Engine:**
  - Create a custom node for `pipecatapp/workflow/nodes/` that compiles and executes a specialized LangGraph (e.g., a complex agentic research loop) as a single step within our hardware-aware, orchestrator-driven DAG.

- [x] **Implement Graceful LLM Failover:** Enhance the `llama-expert.nomad` job to include a final, lightweight fallback model.
- [ ] **Re-evaluate Consul Connect Service Mesh:** Create a new feature branch to attempt to re-enable `sidecar_service` in the Nomad job files and document the process.
- [x] **Add Pre-flight System Health Checks:** Create a new Ansible role to perform non-destructive checks at the beginning of `playbook.yaml`.
- [x] **Investigate Advanced Power Management:** Research and prototype a more advanced version that uses Wake-on-LAN.
- [x] **Implement Claude Code CLI Techniques:** Review `docs/CLAUDE_CODE_ANALYSIS.md` and implement the recommended techniques in `pipecatapp/tools/`:
  - Format Zod/Pydantic validation errors for LLMs.
  - Add robust ripgrep fallback (EAGAIN handling) to `shell_tool.py`.
  - Add transparent pagination feedback (e.g. `[Showing results with pagination...]`).
  - Implement single-pass read with metadata extraction (encoding, line endings) for file editors.
  - Implement `LRUCache` for file state to optimize `RAG_Tool` and `DocumentTool`.
  - Integrate dynamic "thinking" feature support detection based on model string.
- [x] **Expand the Model Collection:** Systematically test and add the remaining LiquidAI nano models to `group_vars/models.yaml`.
- [ ] **Security Hardening:**
  - [x] **Remove passwordless sudo:** Modify the sudoers file configuration to require a password for the `target_user`.
  - [x] **Run services as non-root users:** Audit all services and ensure they are running as dedicated, non-privileged users where possible.
- [x] **Robust Remote Node Recovery:** Add mechanism to recover remote nodes even if network stack is completely broken (possibly via serial console or IPMI automation).
- [x] **Monitoring and Observability:** Deploy a monitoring stack like Prometheus and Grafana.
- [x] Add a `wait_for` to the `home_assistant` role to ensure the `mqtt` service is running before starting the `home-assistant` service.
- [x] Create a new integration test file for home assistant.
- [x] Add the new test to `e2e-tests.yaml`.
- [x] Modify `start_services.sh` to include the home assistant job.
- [x] Investigate <https://github.com/microsoft/agent-lightning> as a possible agent improvement method.
- [ ] **Investigate RPC Provider Monitoring:** Research how to expose or scrape metrics from `llamacpp-rpc` providers to aggregate backend performance data.
- [ ] **Evaluate Ouro/LoopLM Support in llama.cpp:** In 3 months, check if the upstream `llama.cpp` project has added support for the Ouro LoopLM architecture. If so, create a plan to integrate it as a native model option.

## 4. Maintenance & Clean Up

This section tracks identified placeholder files, corrupted binaries, and code that needs to be fixed or removed.

- [x] **Remove or Implement Empty Handler:**
  - `ansible/roles/bootstrap_agent/handlers/main.yaml` is currently empty.

- [x] **Reconcile Stale Artifacts:**
  - `pipecatapp/app.py` contains code and TODOs (e.g., vision model failover). Determine if these changes should be merged or if the artifact should be regenerated.
- [x] **Vision Model Failover**: Implement failover or selection logic for vision models (see `pipecatapp/app.py`).
- [x] **Refactor Vision Role**: The `vision` role is currently minimal (only installs `libgl1`) and does not deploy Frigate as implied by the `frigate_port` variable. It needs to be refactored to actually deploy the service.
- [x] **Review Hardcoded Network References:**
  - **Goal:** Align Ansible roles with the "Provisioning Underlay" vs. "Cluster Overlay" architecture.
  - **Tasks:**
    1. [x] Audit `ansible/roles/power_manager/tasks/main.yaml` for hardcoded `10.0.0.0/24` subnet references.
    2. [x] Ensure that firewall rules (UFW/iptables) correctly handle both the provisioning underlay and the Tailscale overlay.
    3. [x] Verify that `group_vars/all.yaml` variables are consistently used instead of hardcoded IPs.

## Completed History

- [x] **Read and evaluate VLLM project findings**
- [x] **Implement LLMRouter Integration (Proof of Concept)**
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
- [x] **Real-time Steering for llama.cpp:**
  - Implemented `POST /control-vectors` endpoint in `llama.cpp`.
  - Added `PersonalityTool` for dynamic steering.
  - Included automation scripts for vector generation.

## Performance & I/O Optimization

- [ ] **Optimize Fast Path Security Redaction:** Evaluate the regex patterns in `security.py` (e.g., `_FAST_PATH_PATTERN`) under heavy concurrent load and consider implementing a Rust-based extension or a streaming redaction approach for large contexts.

- [x] **Optimize ExperimentTool Sandbox Creation:**
  - Replaced `shutil.copytree` with `tar` snapshotting to reduce syscall overhead.
- [x] **Optimize ProjectMapperTool Scanning:**
  - Implemented `git ls-files` strategy for faster file listing in git repositories.
- [x] **Review Codebase for I/O Inefficiencies:**
  - **Goal:** Identify and optimize other areas with heavy syscall usage (e.g., logging, data processing).
  - **Strategy:** Look for repeated file opens/closes in loops, inefficient directory traversals, and opportunities to batch I/O or use `tar`/`sqlite` strategies.
  - **Action:** Batched synchronous writes to `pypicat_faiss_store.json` in `memory.py` by grouping saves and adding an `atexit` handler to safely flush pending changes on shutdown.

## Security Audit

- [ ] **Audit Hardcoded Local IP Addresses:** Remove hardcoded `127.0.0.1` and `localhost` fallbacks in critical services (e.g., `app.py`, `workflow_nodes`, `web_server.py`) and replace them with robust environment-based configuration matching the cluster overlay architecture.
- [ ] **Audit Subprocess Injection Risks:** Thoroughly review all tools using `subprocess.run` (like `heretic_tool.py`, `experiment_tool.py`, `autoloop_tool.py`) for potential command injection vulnerabilities when interpolating user or LLM input into shell commands without `shlex.quote`.
- [ ] **Review Autoloop Tool Security:** The `autoloop_tool.py` executes code locally without a sandbox. Sandbox this tool or restrict its usage strictly to trusted, airgapped environments.

- [x] **Audit and remove hardcoded secrets:**
  - Audit frontend code (`pipecatapp/static/js`), workflows (`workflows/`), and tools (`pipecatapp/tools/`) for hardcoded secrets, API keys, or tokens.
  - Remove any found secrets and replace them with secure environment variable loading.
- [x] **Audit unauthenticated API endpoints:**
  - Review `pipecatapp/web_server.py` and other API definitions to ensure sensitive data endpoints are authenticated.
  - Specifically check endpoints returning user data or configuration.
- [x] **Audit WebSocket security:**
  - Verify that WebSocket connections enforce strict Origin checks to prevent Cross-Site WebSocket Hijacking (CSWSH).
  - Consider implementing authentication for WebSocket connections.
- [x] **Audit write access controls:**
  - Ensure that all state-changing endpoints (POST, PUT, PATCH) require authentication and authorization.
  - Verify that unauthenticated users cannot modify workflows or agent state.
- [x] **Audit rate limiting configuration:**
  - Review rate limiting settings in `pipecatapp/rate_limiter.py` and `pipecatapp/web_server.py`.
  - Ensure critical endpoints have stricter limits to prevent abuse.
- [x] **Audit data storage security:**
  - Check how sensitive data (e.g., in `pipecatapp/memory.py` or database integrations) is stored.
  - Ensure encryption at rest is considered or implemented for sensitive fields.

## Technical Debt & Lazy Code

- [ ] **Address Missing Tool Tests:** Create unit tests for tools lacking coverage (e.g., `atproto_tool.py`, `autoloop_tool.py`, `container_registry_tool.py`, `context_upload_tool.py`, `cq_tool.py`, `dependency_scanner_tool.py`, `document_tool.py`, `dynamic_skill_tool.py`, `openclaw_tool.py`, `save_skill_tool.py`, `scale_compute_tool.py`, `scheduler_tool.py`, `search_skills_tool.py`, `skill_builder_tool.py`, `spec_loader_tool.py`, `submit_solution_tool.py`, `update_litellm_tool.py`, `vr_tool.py`, `wol_tool.py`).
- [ ] **Fix Lazy Tests:** Address tests that contain only `pass` without actual assertions (e.g., `tests/unit/test_pipecat_app_unit.py`, `tests/test_event_bus.py`, `tests/verify_dlq.py`).
- [ ] **Decouple Subprocess Usage:** Refactor hardcoded `subprocess.run` calls in tools (like `heretic_tool.py`, `project_mapper_tool.py`, `autoresearch_tool.py`, `experiment_tool.py`, `ansible_tool.py`, etc.) to use a unified execution abstraction, enabling easier mocking and sandboxing.

- [x] Improve `test_allowlist` in `tests/test_ssrf_validation.py`
- [x] Improve `test_endpoint` in `pipecatapp/tests/test_rate_limiter.py`
- [x] Improve `test_leak` in `tests/unit/test_shell_tool_security.py`
- [x] Improve `test_main_purge_jobs` in `tests/unit/test_provisioning.py`
- [x] Improve `test_run_script_failure` in `tests/unit/test_supervisor.py`
- [x] Improve `test_validate_url_safe` in `tests/test_ssrf_validation.py`
- [x] Improve `test_validate_url_unsafe_ip` in `tests/test_ssrf_validation.py`
- [x] Improve `test_validate_url_unsafe_scheme` in `tests/test_ssrf_validation.py`
- [x] Improve `test_websocket_allows_wildcard` in `pipecatapp/tests/test_websocket_security.py`
- [x] Improve `test_websocket_default_secure_same_origin_success` in `pipecatapp/tests/test_websocket_security.py`
- [x] Improve `test_yolo_internal_process_frame_failover` in `tests/unit/test_vision_failover.py`
- [x] **Fix Lazy Tests:**
  - [x] `tests/test_emperor_node.py:test_emperor_node` (dry run with simple pass instead of validation)
  - [x] `tests/unit/test_vision_failover.py:test_yolo_internal_process_frame_failover` (relies on mock failure passing without asserts)

## Paseo Integration Ideas

This section tracks actionable ideas derived from the `docs/PASEO_ANALYSIS.md` document for integrating Paseo's orchestration concepts into our custom Pipecat architecture.

- [x] **Implement `OpenCodeProviderTool`:** Create a Python-based provider wrapper in `pipecatapp/tools/` that executes OpenCode via `NomadSandboxExecutor`, intercepts standard output streams, and standardizes them into Pipecat agent events.
- [x] **Add MCP-like Agent Management to `EmperorAgentNode`:** Expose new tools (e.g., `CreateAgentTool`, `WaitAgentTool`) to the Emperor node, allowing it to dynamically spawn and await specialized `TwinService` or Nomad worker instances (similar to Paseo's `agent-management-mcp.ts`).
- [x] **Implement Automated Verifier Loops ("Ralph Loop"):** Create a new workflow node in `pipecatapp/workflows/` that implements a worker-verifier loop (Worker -> Verifier -> Feedback) specifically for complex coding tasks, allowing automatic trial-and-error iterations before returning to the main graph.
- [x] **Enhance `MemoryStore` with an Activity Timeline:** Extend `pipecatapp/memory.py` to support a chronologically ordered "Cluster Activity Timeline" that tracks tool invocations, agent spawns, and background process exit codes to provide better distributed system context.

## Agent Reliability and Security (Future Enhancements)

- [x] **Implement State-Based Tool Gating in Workflow Nodes:**
  - **Goal:** Prevent agents from fabricating tool outputs or bypassing required tools by enforcing deterministic state transitions.
  - **Context:** Currently, `EmperorAgentNode` and similar agents operate autoregressively and can hallucinate tool outputs if they choose to bypass the actual tool execution. To solve this, an orchestration layer should intercept the execution graph. If an agent tries to transition to a "response generation" state without a verified, required tool execution payload (e.g. `call_id` and verified output) present, the transition must be explicitly blocked at the router level.
- [x] **Integrate Cryptographic Receipts for Tool Execution:**
  - **Goal:** Ensure that in a decentralized/zero-trust multi-agent system, tool outputs are genuinely executed by the designated node/enclave and not hallucinated by compromised nodes.
  - **Context:** Since forcing language models to hallucinate raw SHA-256 hashes often fails due to tokenization, the deterministic runtime executing the tool should cryptographically sign the execution trace (input parameters and output payload) with a private key. The orchestration router must then verify this signature before allowing the state machine to proceed, creating an immutable proof of execution.

## Flowise UI Integration Ideas

This section tracks actionable ideas derived from the `docs/FLOWISE_ANALYSIS.md` document for integrating visual workflow concepts into the `pipecatapp` architecture.

- [ ] **Decouple Node Handlers (Input vs Output):** In the frontend, separate the visual node UI into dedicated Input and Output handlers that dynamically adjust their height to keep connection anchors perfectly aligned when configuration controls expand/collapse.
- [ ] **Strict Visual Edge Validation:** Implement an `isValidConnection` hook on the frontend canvas that checks the backend Python/Pydantic schemas. Prevent users from visually connecting a text output port to a dictionary input port to avoid runtime crashes.
- [x] **Dynamic Variable Interpolation:** Standardize the `{{ $vars.NAME }}` syntax. Add a pre-processing step to the Python `WorkflowRunner` that resolves and injects these variables globally across all node configs before the graph execution begins.
- [x] **Expose UI Metadata from Backend:** Add a new REST API endpoint to the Python server that returns a JSON schema describing the available workflow nodes (including category, icon, accepted input types, and tooltips). Use this to dynamically construct the frontend node properties panel.
- [x] **Introduce a `PostProcessorNode`:** Implement an execution hook or a dedicated node that allows arbitrary Javascript/Python manipulation of the final output dictionary (e.g., reformatting or filtering data) before it is sent back to the client.
