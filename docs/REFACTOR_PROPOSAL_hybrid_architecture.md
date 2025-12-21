# Refactoring Proposal: Hybrid / Cluster-Native Architecture

## 1. Objective

To refactor the current distributed, microservices-based architecture into a flexible **Hybrid / Cluster-Native** model. This new architecture will allow the system to adapt its deployment topology based on available hardware, optimizing for resource efficiency on low-end edge nodes (2-core/8GB) while maintaining scalability on high-end core nodes (32-core/64GB).

## 2. Problem Statement (Current State)

The current "Ensemble of Agents" architecture treats every component as a separate microservice orchestrated by Nomad/Docker. While scalable, this approach introduces significant overhead:

* **High RAM Usage:** Running separate Python runtimes for `pipecatapp`, `expert` (wrapper), `tool_server`, and `world_model` consumes ~500MB-1GB of redundant memory.
* **Latency:** HTTP/JSON serialization between local components adds 5-20ms per hop.
* **Complexity:** Running a full orchestration stack (Nomad+Consul) on a single edge device is overkill.

## 3. Proposed Architecture (Hybrid Model)

We propose a tiered architecture where components can be "Colocated" (Monolith) or "Distributed" based on configuration.

### Tier 1: Low-End Edge Node (2 Core, 8GB RAM)

**Role:** Frontend / Voice Interaction

* **Mode:** `Monolith-Lite`
* **Configuration:**
  * **In-Process:** `pipecatapp` (App), `STT` (Whisper), `TTS` (Piper), Lightweight Tools.
  * **Remote:** LLM Inference (via HTTP to Core Node), Heavy Tools (via HTTP to Tool Server).
* **Benefit:** Fits in 8GB RAM, fast voice response.

### Tier 2: Mid-Range Node (8 Core, 16-32GB RAM)

**Role:** Smart Edge / Standalone Dev

* **Mode:** `Full Monolith`
* **Configuration:**
  * **In-Process:** All of Tier 1 + `llama-server` (Local binding or localhost), `world_model` (Local object).
* **Benefit:** Fully autonomous, zero network dependency.

### Tier 3: High-End Core Node (32 Core, 64GB RAM)

**Role:** Cluster Brain

* **Mode:** `Distributed Service Provider`
* **Configuration:**
  * **Hosted:** Large LLM Inference Cluster, Tool Server, Persistent World Model (MQTT/DB).
* **Benefit:** Centralized compute for the cluster.

## 4. Implementation Plan

> **Note:** A detailed engineering checklist for these phases is available in [TODO_Hybrid_Architecture.md](./TODO_Hybrid_Architecture.md).

### Phase 1: Configurable Tool Factory (Local vs Remote)

* **Goal:** Allow `agent_factory.py` to instantiate tools either locally or as proxies to a remote server.
* **Files:** `ansible/roles/pipecatapp/files/agent_factory.py`
* **Action:**
    1. Update `create_tools` signature to accept a `tool_mode` config.
    2. Implement `RemoteToolProxy` class.
    3. Toggle logic: `if mode == 'remote': return RemoteToolProxy('ssh') else: return SSH_Tool()`.

### Phase 2: In-Process Logic Consolidation

* **Goal:** Eliminate "Expert" wrapper container and "Tool Server" if not needed.
* **Files:** `ansible/jobs/expert.nomad.j2`, `ansible/roles/pipecatapp/files/app.py`
* **Action:**
    1. Modify `app.py` to optionally load `llama-cpp-python` direct bindings instead of using `OpenAILLMService`.
    2. Deprecate `expert` Nomad job in favor of a `pipecatapp` config flag `RUN_LOCAL_LLM=true`.

### Phase 3: Adaptive Service Discovery

* **Goal:** Seamlessly switch between `localhost` and `consul` discovery.
* **Files:** `ansible/roles/pipecatapp/files/app.py`
* **Action:**
    1. Update `discover_services` helper.
    2. If `LLM_URL` env var is set (e.g., to `http://core-node:8080`), skip Consul discovery.

### Phase 4: Docker Image Optimization

* **Goal:** One image, multiple behaviors.
* **Files:** `docker/pipecatapp/Dockerfile`, `start_pipecat.sh`
* **Action:**
    1. Ensure all dependencies (including `llama-cpp-python`) are optional or lazily loaded.
    2. Use env vars (`NODE_ROLE=edge|core`) to control startup logic.

## 5. Relationship to Existing Architecture

This proposal modifies **Layer 3 (Orchestration)** and **Layer 4 (AI Stack)** of `docs/ARCHITECTURE.md`.

* **Layer 3:** Reduces reliance on Nomad for internal component communication on single nodes.
* **Layer 4:** Merges distinct `TwinService` satellites into a unified application runtime.

Refer to `docs/ARCHITECTURE.md` for the baseline definition of these layers.
