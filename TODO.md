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

- [ ] **Automated Bootstrap Script (`bootstrap.sh`) Verification:**
  - [x] Integrated automated troubleshooting report generation on bootstrap failures in `bootstrap.sh`.
  - [x] Audited and fixed IPFS Nomad job and Ansible task permissions (`ansible/roles/ipfs/tasks/main.yaml` ownership by `target_user`, Multiaddr strings in `ipfs.nomad.j2`, and 30x retries with 5s delay on gateway readiness).
  - [ ] Verify local ROCm simulation via `act` to ensure kernel/driver sanity before cluster deployments.
- [x] **Nomad & Consul Service Mesh Sanity:**
  - [x] Ensure Raft quorum forms automatically across controller nodes using dynamic `bootstrap_expect` (verified in `consul.hcl.j2` and `nomad.hcl.server.j2`).
  - [x] Confirm Consul ACL bootstrap reset flow operates reliably on transient network splits (verified recovery flow in `ansible/roles/consul/tasks/acl.yaml`).
  - [x] Validate that all cluster nodes populate `retry_join` with complete controller node IPs (verified in server and client templates).
- [ ] **Deploy & Verify Core Pipecat Nomad Job:**
  - [ ] Run `pipecatapp` Nomad job on active cluster and verify it reaches stable `running` state.
  - [ ] Confirm `/api/status` returns 200 OK without flapping or triggering Nomad task restarts.
  - [ ] Verify zero OOM kills under the 300MB baseline memory ceiling.

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

- [ ] **Offload Heavy Tools to `tool_server`:**
  - [x] Hardened `tool_server.py` with dynamic `_safe_import_and_init` fallbacks, unauthenticated `/health` check, and full `/run_tool/` test verification.
  - [x] Eliminated background thread leakage and filesystem scan deadlocks in `RAG_Tool` (`auto_index=False` default, lazy model encoder initialization).
  - [x] Implemented strict request timeouts and circuit breakers for external tool RPCs (`TOOL_RPC_TIMEOUT` in `RemoteToolProxy`).
  - [ ] Migrate heavy tool workloads (RAG document parsing, Docker sandbox code execution, WASM plugins) out-of-process in production deployment.
  - [ ] Ensure `pipecatapp` core process only communicates with heavy tools via HTTP/Consul service mesh.
- [ ] **Memory & Resource Profiling:**
  - [ ] Benchmark memory consumption of `pipecatapp` under multi-turn conversations.
  - [ ] Guarantee background processes remain capped at `-j2` / `-j4` to honor 7.8 GiB hardware limits.

---

## 🤖 Phase 3: Autonomous Workflow Engine & Agents (P3 - Enhancement)

- [ ] **Technician Agent 3-Phase Execution:**
  - [x] Validate Plan, Execute, and Reflect phases in `pipecatapp/technician_agent.py`.
  - [x] Ensure `@durable_step` checkpointing functions reliably with cached idempotency (verified 0 network calls on cached steps).
- [ ] **Tangle UI & Visual Workflow Integration:**
  - [ ] Complete KFP-style `ComponentSpec` parser in `pipecatapp/workflow/`.
  - [ ] Connect lightweight API adapter (`/api/components`, `/api/pipeline_runs`) to Consul state layer.
- [ ] **Swarm Orchestration (Map-Reduce):**
  - [x] Verify `SwarmTool` worker dispatch and task result reduction across worker nodes (verified `test_manager_agent_map_reduce`).
  - [ ] Validate Thompson-sampling load routing in `moe_gateway`.

---

## 🔬 Phase 4: Extended Roadmap & Research Previews (Backlog / Speculative)

- [ ] **Authentik Identity Provider Job:**
  - [ ] Resolve 'progress deadline' deployment issue in `ansible/jobs/authentik.nomad.j2`.
  - [ ] Automate M2M OAuth2 service account provisioning during bootstrap.
- [ ] **HelixDB Unified Graph-Vector Memory:**
  - [ ] Review `docs/analysis/HELIXDB_EVALUATION.md` and prototype HelixDB PoC.
- [ ] **TML Interaction Models Research Preview:**
  - [ ] Review `moshi/rust` continuous audio/video streaming architecture.
  - [ ] Replace placeholder `thinkingmachines/interaction-runtime:preview` with verified build.
- [ ] **Trained LLMRouter Deployment:**
  - [ ] Replace heuristic routing in `LLMRouterNode` with trained model weights and evaluation dataset.
- [ ] **P2P Model Pinning via IPFS:**
  - [ ] Automate P2P pinning and weight distribution for `.gguf` files across nodes.
- [ ] **Type Safety & Static Analysis Cleanliness:**
  - [ ] Progressively resolve `mypy` typing warnings in `pipecatapp/core/` and `pipecatapp/workflow/`.

---

## 📜 Completed History (Reference Archive)

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
