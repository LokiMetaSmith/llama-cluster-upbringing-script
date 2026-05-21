# AI Governance & Architecture Plan

Last updated: 2026-03-27

This document outlines the current state and future roadmap for the Agentic Governance of our Distributed Conversational AI Pipeline. It maps our existing multi-layered architecture onto industry-standard frameworks for autonomous multi-agent systems, specifically focusing on orchestration, security, and regulatory compliance.

---

## 1. KPMG TACO Agent Taxonomy

To effectively govern our multi-agent system, we classify our existing AI services and tools according to the KPMG TACO (Taskers, Automators, Collaborators, Orchestrators) taxonomy.

### Current State Mapping

* **Taskers (Single function, discrete tasks):**
  * **Tools:** `shell`, `file_editor`, `git`, `code_runner` (executes sandboxed Python), `desktop_control`, `vision`, `ha` (Home Assistant), `power` (Power management).
  * **LLM Experts:** Specialized backends like the `coding-expert` or `math-expert` (deployed via `llama-expert.nomad`).
* **Automators (Multi-step, rule-based or linear workflows):**
  * **Tools:** `ansible` (runs infrastructure playbooks), `rag` (retrieval-augmented generation loop), `project_mapper`, `dependency_scanner`.
  * **Pipelines:** The `provisioning_api` handling node bootstrap sequences.
* **Collaborators (Agents that interact with users or other agents to synthesize information):**
  * **Services:** `TwinService` (the core conversational agent processing user input via `app.py`).
  * **Tools:** `council` (convenes multiple AI experts for deliberation), `archivist` (deep research on long-term memory).
* **Orchestrators (High-level planners that delegate tasks and manage resources):**
  * **Services:** The overarching `WorkflowRunner` executing complex DAGs defined in YAML (e.g., `default_agent_loop.yaml`).
  * **Tools:** `orchestrator` (dispatches complex jobs to the cluster), `planner` (creates sub-task plans), `swarm` (spawns multiple parallel worker agents), `mcp` (Master Control Program for agent introspection).
  * **Adaptation:** The Layer 7 Self-Adaptation Loop (SEAL) acting as a meta-orchestrator that detects failures and mutates code (`supervisor.py` -> `reflection` -> `evolve.py`).

### Future Recommendations

* **Explicit Role Definitions:** Formally codify these TACO roles within the `TwinService` workflow definitions (YAML) to ensure agents do not overstep their bounds (e.g., a Tasker should not spontaneously invoke the Orchestrator's `swarm` tool).
* **Role-Based Access Control (RBAC):** Bind specific Nomad/Consul tokens to specific TACO roles, rather than granting all agents broad access.

---

## 2. The Five Pillars of Agentic Governance

This framework addresses the operational and security lifecycle of autonomous agents.

### 1. Inventory

* **Current State:**
  * Services are dynamically registered and discovered via HashiCorp Consul (Layer 3).
  * The `Master Control Program (mcp)` tool provides real-time introspection into active pipeline tasks (`get_status` endpoint in `web_server.py`).
* **Future Recommendations:**
  * Implement a centralized, immutable ledger of all deployed agent versions, their specialized prompts (`prompts/router.txt`, `models.yaml`), and their allowed toolsets.
  * Regularly audit the Consul catalog against this ledger.

### 2. Identity

* **Current State:**
  * The `moe_gateway` validates incoming external requests with API keys.
  * WebSocket connections validate origin headers and optional API key tokens (`web_server.py`).
* **Future Recommendations:**
  * Implement **Agent Name Service (ANS)** (see Section 3).
  * Assign unique, cryptographically verifiable identities (e.g., SPIFFE/SPIRE) to every Nomad allocation (agent worker), replacing shared or generic API keys.

### 3. Least Privilege

* **Current State:**
  * The system uses some sandboxing (e.g., `code_runner` uses Docker).
  * However, core tools like `shell`, `ansible`, and `desktop_control` operate with dangerously high privileges on the host nodes (Ansible requires `become: yes` for many tasks).
  * Layer 7 Self-Adaptation can autonomously mutate core logic.
* **Future Recommendations:**
  * **Mandatory Human-in-the-Loop (HITL):** Enforce strict HITL approval gates via the web UI for any action that mutates the host state (`ansible`), executes arbitrary code (`shell`), or alters the core agent logic (Layer 7 Adaptation).
  * Transition all host-level execution tools to run within heavily restricted, unprivileged containers.

### 4. Observ-ability

* **Current State:**
  * OpenTelemetry is instrumented for FastAPI and HTTPX in `web_server.py`.
  * Prometheus metrics (CPU/Mem) are scraped from Nomad clients.
  * Conversation logs and pipeline states are streamed via WebSockets to the UI.
* **Future Recommendations:**
  * Expand OpenTelemetry to trace the entire execution graph of the `WorkflowRunner` and individual tool invocations.
  * Capture full, tamper-evident audit logs of every prompt sent to an LLM and the exact response received, explicitly linking decisions to actions.

### 5. Continuous Compliance

* **Current State:**
  * System includes a `dependency_scanner` (OSV database) tool.
  * Enforces "Executable Oracles" (tests, linters) before code submission.
* **Future Recommendations:**
  * Integrate automated regulatory compliance checks into the CI/CD pipeline and the Layer 7 Self-Adaptation Loop.
  * Ensure any autonomously generated code (via `autoresearch` or `evolve.py`) is scanned for security vulnerabilities *before* execution, not just functional correctness.

---

## 3. Protocols & Standards

### 1. Model Context Protocol (MCP)

* **Current State:** We have a proprietary `mcp` tool that allows the agent to inspect its own running tasks.
* **Future Recommendations:** Standardize tool interfaces to align with the open Model Context Protocol specification. This will decouple our specific tools (`file_editor`, `shell`) from the `TwinService`, allowing us to easily swap in compliant third-party tools or use our tools with external LLMs.

### 2. Agent-to-Agent Protocol (A2A)

* **Current State:** Agents communicate internally via the `InternalChatRequest` mechanism over HTTP/REST (e.g., `/internal/chat` in `web_server.py`), and the gateway routes requests.
* **Future Recommendations:** Adopt a formal A2A protocol (like FIPA ACL or a modern equivalent) to handle complex negotiations, delegation, and state synchronization between the Orchestrators and Taskers, moving beyond simple REST payloads.

### 3. Agent Name Service (ANS)

* **Current State:** We rely entirely on Consul for service discovery (e.g., searching for `llama-api-` prefixes).
* **Future Recommendations:** Layer an ANS over Consul. This service would map human-readable agent roles (e.g., `agent://cluster/orchestrator/main`) to their cryptographic identities and current network locations, enabling secure, verifiable routing.

### 4. Zero Trust Agent Task Framework (ATF)

* **Current State:** The network perimeter is secured (API keys, CORS), but internal agent-to-agent and agent-to-tool trust is implicitly high.
* **Future Recommendations:** Implement Zero Trust ATF. Every time an agent invokes a tool (especially Automators or Taskers), the request must be authenticated and authorized based on the agent's identity, its current context, and the tool's required privileges.

---

## 4. Immediate TODO List for Review

1. [x] **HITL Enforcement:** Implement a mandatory `HumanApprovalNode` in the `WorkflowRunner` for any workflow utilizing `shell`, `ansible`, `desktop_control`, or `autoresearch`.
2. [x] **Audit Logging:** Upgrade `TwinService` to output tamper-evident JSON logs for every tool invocation, including the exact prompt, response, and action taken.
3. [ ] **Identity PoC:** Research integrating SPIFFE/SPIRE with our existing Nomad/Consul cluster to provide cryptographic identities to individual agent allocations.
4. [x] **MCP Migration:** Review our current `pipecatapp/tools/` directory and draft a plan to refactor them to comply with the open Model Context Protocol.
5. [ ] **Review Layer 7 Risks:** Conduct a dedicated security review of the `prompt_engineering/evolve.py` self-adaptation loop to ensure mutated code cannot bypass security sandboxes.
