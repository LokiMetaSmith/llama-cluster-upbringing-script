# Project Roadmap & Task Tracking

## 📊 Executive Status & Stability Retrospective

### Recently Completed (Core Stability & Anti-Looping Fixes)

- [x] **Universal Python Syntax Audit:** Fixed nested double-quote f-strings across `pipecatapp` (`code_runner_tool.py`, `pmm_memory_client.py`, `archivist_tool.py`, `get_nomad_job.py`, `open_workers_tool.py`, `opencode_provider_tool.py`, `planner_tool.py`, `swarm_tool.py`, `emperor_nodes.py`, `ralph_nodes.py`). Zero syntax errors verified via `python -m compileall`.
- [x] **De-monolithized Agent Factory (Lazy Tool Loading):** Replaced 89 eager top-level imports in `pipecatapp/agent_factory.py` with dynamic `TOOL_CLASS_MAP` and `_safe_create` loader. Prevents OOM crashes and dependency avalanches at startup.
- [x] **Fault-Tolerant Optional Dependencies:** Added safe fallback handlers for optional libraries (`faiss`, `sentence_transformers`, `minisweagent`, `docker`, `jupyter_client`).
- [x] **Health Check & Auth Decoupling:** Removed `api_key` security requirement from `/api/status` in `pipecatapp/web_server.py`. Nomad and Consul HTTP health checks can now probe health without 401 Unauthorized errors.
- [x] **Startup Fault Recovery:**
  - Added Consul KV connection retry loop with backoff and default configuration fallback in `pipecatapp/app.py`.
  - Added audio STT fallback (graceful degradation to text mode if whisper/wyoming models are unavailable).
  - Removed forbidden `verify=False` from Consul client in `pipecatapp/core/config.py`.
- [x] **Nomad Job Specification Resilience:** Updated `ansible/roles/pipecatapp/templates/pipecatapp.nomad.j2` to use dynamic container driver (`docker` / `containerd`) and increased health check grace period to 120s.
- [x] **Architectural Guardrails (Hierarchy of Stability):** Documented Level 0–3 system layers in `AGENTS.md` and `docs/BEST_PRACTICES.md` to prevent autonomous agents from breaking mesh infrastructure (Consul, Nomad, IPFS, TLS) to solve application-level issues.

---

## 🎯 Phase 0: Core Infrastructure & Bootstrap Verification (P0 - Immediate Focus)

- [x] **Fix Tests:**
  - [x] Fix `test_dispatch_job_failure` in `tests/unit/test_orchestrator_tool.py` as it fails due to incorrect mocking.

- [x] **Automated Bootstrap Script (`bootstrap.sh`) Verification:**
  - [x] Integrated automated troubleshooting report generation on bootstrap failures in `bootstrap.sh`.
  - [x] Audited and fixed IPFS Nomad job and Ansible task permissions (`ansible/roles/ipfs/tasks/main.yaml` ownership by `target_user`, Multiaddr strings in `ipfs.nomad.j2`, and 30x retries with 5s delay on gateway readiness).
  - [x] Verify local ROCm simulation via `act` to ensure kernel/driver sanity before cluster deployments.
- [x] **Nomad & Consul Service Mesh Sanity:**
  - [x] Ensure Raft quorum forms automatically across controller nodes using dynamic `bootstrap_expect` (verified in `consul.hcl.j2` and `nomad.hcl.server.j2`).
  - [x] Confirm Consul ACL bootstrap reset flow operates reliably on transient network splits (verified recovery flow in `ansible/roles/consul/tasks/acl.yaml`).
  - [x] Validate that all cluster nodes populate `retry_join` with complete controller node IPs (verified in server and client templates).
- [x] **Deploy & Verify Core Pipecat Nomad Job:**
  - [x] Run `pipecatapp` Nomad job on active cluster and verify it reaches stable `running` state.
  - [x] Confirm `/api/status` returns 200 OK without flapping or triggering Nomad task restarts.
  - [x] Verify zero OOM kills under the 300MB baseline memory ceiling.

---

## 🧠 Phase 1: Memory & State Consolidation (P1 - High Priority)

- [x] **Unify Disparate Memory Implementations:**
  - [x] Consolidate legacy memory stores (`pipecatapp/memory_legacy.py`, `pipecatapp/memory.py`, and `pipecatapp/pmm_memory_client.py`) via unified `MemoryStore`.
  - [x] Standardize on `PMMMemory` / SQLite deterministic ledger backend as primary persistent storage (`pipecatapp/memory_backends_impl/pmm_backend.py`).
  - [x] Clean up deprecated ChromaDB and orphaned storage references (made ChromaDB optional with null-safe fallbacks in `rag_tool.py`, added native text-chunking fallbacks without LangChain requirement).
- [x] **State Preservation Across Syncs:**
  - [x] Verify `ansible.posix.synchronize` tasks strictly preserve `.liminal`, SQLite DBs, and runtime state (verified in `pipecatapp/tasks/main.yaml` and hardened `deploy_expert_wrapper.yaml`).
  - [x] Audit cache deduplication (`scripts/dedup_venvs.py`) to ensure no corruption of shared libraries (added explicit exclusions for `.db`, `.sqlite`, `.wal`, `.sock`, `.lock`, `.pid`).

---

## ⚙️ Phase 2: Hybrid Distributed Tool Architecture (P2 - Medium Priority)

- [x] **Offload Heavy Tools to `tool_server`:**
  - [x] Hardened `tool_server.py` with dynamic `_safe_import_and_init` fallbacks, unauthenticated `/health` check, and full `/run_tool/` test verification.
  - [x] Eliminated background thread leakage and filesystem scan deadlocks in `RAG_Tool` (`auto_index=False` default, lazy model encoder initialization).
  - [x] Implemented strict request timeouts and circuit breakers for external tool RPCs (`TOOL_RPC_TIMEOUT` in `RemoteToolProxy`).
  - [x] Migrate heavy tool workloads (RAG document parsing, Docker sandbox code execution, WASM plugins) out-of-process in production deployment.
  - [x] Ensure `pipecatapp` core process only communicates with heavy tools via HTTP/Consul service mesh.
- [x] **Memory & Resource Profiling:**
  - [x] Benchmark memory consumption of `pipecatapp` under multi-turn conversations.
  - [x] Guarantee background processes remain capped at `-j2` / `-j4` to honor 7.8 GiB hardware limits.

---

## 🤖 Phase 3: Autonomous Workflow Engine & Agents (P3 - Enhancement)

- [x] **Technician Agent 3-Phase Execution:**
  - [x] Validate Plan, Execute, and Reflect phases in `pipecatapp/technician_agent.py`.
  - [x] Ensure `@durable_step` checkpointing functions reliably with cached idempotency (verified 0 network calls on cached steps).
- [x] **Tangle UI & Visual Workflow Integration:**
  - [x] Complete KFP-style `ComponentSpec` parser in `pipecatapp/workflow/`.
  - [x] Connect lightweight API adapter (`/api/components`, `/api/pipeline_runs`) to Consul state layer.
- [x] **Swarm Orchestration (Map-Reduce):**
  - [x] Verify `SwarmTool` worker dispatch and task result reduction across worker nodes (verified `test_manager_agent_map_reduce`).
  - [x] Validate Thompson-sampling load routing in `moe_gateway`.

---

## 🌳 Phase 4: BanyanCode Features Integration (P3 - Feature Roadmap)

- [ ] **Tree-Sitter / Symbol Graph Tooling (`code_graph_tool.py`):**
  - [ ] Implement Tree-sitter / AST indexing service for Python, JS, and TS workspaces in `pipecatapp/tools/code_graph_tool.py` and `tool_server.py`.
  - [ ] Expose `blast_radius` tool: calculate direct and transitive caller/dependent call-sites and risk score.
  - [ ] Expose `preflight` tool: return pre-edit summary including caller lists, unit test mappings, documentation references, and HTTP routes.
  - [ ] Expose `repository_trace` tool: trace symbol call hierarchies outward to a configurable depth.
- [ ] **Memory Candidate Promotion Pipeline:**
  - [ ] Implement intermediate staging zone / candidate lifecycle for `pmm_datalog_memory.db`.
  - [ ] Create `memory_candidate_emit` tool for subagents to propose durable memory entries during execution.
  - [ ] Add session completion / orchestrator evaluation hooks to promote high-value candidates to main persistent memory storage.
- [ ] **Preflight Edit Verification in Code Runners:**
  - [ ] Hook `FileEditorTool` and code modification nodes into `code_graph_tool` preflight checks.
  - [ ] Require verification of connected test suites (`repository_tests`) before executing diffs.
- [ ] **Keyless Web Researcher Fallback:**
  - [ ] Implement keyless DuckDuckGo HTML web search subagent tool as fallback when primary web search APIs are unavailable or rate-limited.

---

## 🔬 Phase 5: Extended Roadmap & Research Previews (Backlog / Speculative)

- [x] **Strix Halo APU Cluster Bring-up & Verification:**
  - **Goal:** Implement the "Brain vs. Body" cluster topology using the Strix Halo APU as the control node and primary inference tier.
  - **Tasks:**
    1. [x] Create `scripts/halo_pxe_bringup.sh` to configure PXE booting for 64GB-128GB Strix Halo machines.
    2. [x] Define `halo-inference.nomad.j2` with strict memory guardrails (`--ctx-size` cap + cgroup memory caps) ensuring 15-25GB system RAM remains unclaimed.
    3. [x] Define `halo-agent.nomad.j2` to deploy the orchestrator/gateway alongside the inference job.
    4. [x] Point the SEAL loop at the APU deployment task to run iterative deterministic verification (`git apply --check` -> `build` -> test).

- [x] **Playnet / REA Ledger Architectural Resolutions:**
  - **Goal:** Address open design questions surfaced during the Agent-as-Ledger-Clerk implementation of the EISPP prototype.
  - **Tasks:**
    1. [x] **Ledger Reconciliation:** Define a conflict resolution/reconciliation rule for a multi-writer append-only ledger across the federation.
    2. [x] **Non-Transferable Clerk Identity:** Implement sybil-resistant, non-transferable identity (e.g. soulbound keys) for agents signing REA events.
    3. [x] **Multi-Agent Commit Concurrency:** Solve simultaneous commit conflicts (where two agents append modify events to the same resource).
    4. [x] **Value Flows / Price Oracles:** Bridge pure UI preference commits to the Playnet REA value ledger with explicit resource costs.

- [x] **Reverse Engineer Anything (REA) Integration:**
  - **Goal:** Integrate `morluto/rea` (Node.js MCP server with headless Ghidra) into the cluster via `tool-server` and wrap it as a Pipecat tool to enable AI agents to perform deep application reverse engineering.
  - **Tasks:**
    1. [x] Create `docker/Dockerfile.rea` for Node.js 22, Headless Ghidra, and `rea-agents`.
    2. [x] Update `ansible/roles/tool_server/defaults/main.yaml` to include the new REA container component.
    3. [x] Implement `pipecatapp/tools/reverse_engineer_tool.py` as a Python MCP wrapper that exposes REA to the workflow engine.

- [x] **Strata Feature Replication (Tiered MoE Expert Caching):**
  - **Goal:** Replicate Strata's hybrid GPU/RAM MoE offloading features directly into existing inference engines (vLLM/llama.cpp) instead of deploying the standalone Strata app.
  - **Tasks:**
    1. [x] Document Strata's speculative decoding and expert caching heuristics from `docs/analysis/STRATA_EVALUATION.md` as reference architecture.
    2. [x] Explore adding expert-aware LRU eviction policies or tiered offloading to our existing `llama.cpp` / `vLLM` implementations.
    3. [x] Research network-distributed MoE expert routing using `llama.cpp` RPC or tensor parallelism over local disk swapping to utilize horizontally scaled cluster RAM.

- [x] **Authentik Identity Provider Job:**
  - [x] Resolve 'progress deadline' deployment issue in `ansible/jobs/authentik.nomad.j2`.
  - [x] Automate M2M OAuth2 service account provisioning during bootstrap.
- [x] **HelixDB Unified Graph-Vector Memory:**
  - [x] Review `docs/analysis/HELIXDB_EVALUATION.md` and prototype HelixDB PoC.
- [x] **TML Interaction Models Research Preview:**
  - [x] Review `moshi/rust` continuous audio/video streaming architecture.
  - [x] Replace placeholder `thinkingmachines/interaction-runtime:preview` with verified build.
- [x] **Trained LLMRouter Deployment:**
  - [x] Replace heuristic routing in `LLMRouterNode` with trained model weights and evaluation dataset.
- [x] **P2P Model Pinning via IPFS:**
  - [x] Automate P2P pinning and weight distribution for `.gguf` files across nodes.
- [x] **Type Safety & Static Analysis Cleanliness:**
  - [x] Progressively resolve `mypy` typing warnings in `pipecatapp/core/` and `pipecatapp/workflow/`.

---

## 📜 Completed History (Reference Archive)

- [x] Consider refactoring `.github/workflows/unblocked-issues.yml` to support different target branches or configurable settings.
- [x] Refactor unblocked-issues workflow to use configurable trusted users list (`vars.TRUSTED_USERS`).
- [x] Read and evaluate VLLM project findings.
- [x] Fix Memory Service networking (Port 8000 conflict).
- [x] Implement real LLM calls in `worker_agent.py` (replace mock).
- [x] Connect `PlannerTool` to real LLM for robust plan generation.
- [x] Frontier Agent Roadmap Phase 1-4.
- [x] Add `frontend_verification_instructions` for UI changes.
- [x] Implement SEAL-Inspired Self-Adaptation Loop.
- [x] Phase 2: Implement the OpenAI-Compatible MoE Gateway.
- [x] Real-time Steering for llama.cpp (`POST /control-vectors` and `PersonalityTool`).
- [x] Fast path security redaction LRU caching in `security.py`.
- [x] Subprocess injection audit and `shlex.quote` escaping across critical tools.
- [x] Zero-tolerance TLS/SSL bypass enforcement across playbooks and services.
