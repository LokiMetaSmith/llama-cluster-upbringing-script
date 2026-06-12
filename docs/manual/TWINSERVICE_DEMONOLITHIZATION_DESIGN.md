# Architectural Design: Microservice De-monolithization of TwinService

## 1. Objective
To improve the robustness, scalability, and security of the AI agent on legacy hardware by breaking down the `TwinService` monolith. Heavy, blocking, or security-sensitive tools (e.g., RAG document embedding, isolated Python code execution) will be extracted into independent microservices running as separate Nomad jobs.

## 2. Current State & Problem Statement
Currently, `TwinService` acts as the primary orchestrator, routing requests and executing workflows. While there has been progress in remote execution (e.g., `tool_server.py`), `TwinService` still carries significant overhead:
- **Resource Constraints:** Running everything in a single process or even a single tool server consumes large amounts of memory, which is problematic for low-end Tier 1 and Tier 2 legacy edge nodes.
- **Blocking Operations:** Tasks like RAG document embedding and FAISS vector search block the main execution loop if not perfectly async-isolated.
- **Security & Sandboxing:** Secure sandboxing (like the CodeRunner) requires strict isolation. Running it alongside the core router increases the blast radius if an exploit occurs.

## 3. Proposed Architecture
We will migrate to a true microservices architecture for heavy tools, leveraging the existing **Consul Service Mesh** for discovery and communication.

### 3.1. Target Services
We will split the following components into independent Nomad jobs:

1. **RAG / Vector Memory Service**
   - **Responsibilities:** Ingesting documents, running embedding models, and performing FAISS similarity searches.
   - **Nomad Job:** `rag-service.nomad`
   - **Communication:** gRPC or REST over Consul Connect.

2. **Code Execution Sandbox Service**
   - **Responsibilities:** Executing LLM-generated Python/Shell code in tightly controlled ephemeral Docker environments (dropping capabilities, read-only rootfs).
   - **Nomad Job:** `code-runner-service.nomad`
   - **Communication:** REST over Consul Connect.

### 3.2. Orchestration via Consul Service Mesh
- `TwinService` will no longer instantiate `RAG_Tool` or `CodeRunnerTool` directly with deep dependencies.
- Instead, `TwinService` will use lightweight "Proxy Tools" (e.g., `RemoteRAGTool`, `RemoteCodeRunnerTool`).
- These proxy tools will route requests to `http://rag-service.service.consul` or `http://code-runner.service.consul`.
- **Consul Connect Sidecars** will be utilized to enforce mutual TLS (mTLS) and strict access control intentions, ensuring that only `TwinService` can invoke the Code Runner.

## 4. Phased Implementation Plan

### Phase 1: Architectural Design
- Define the boundaries, communication protocols, and security models. (This document).

### Phase 2: RAG Microservice Extraction
1. Create a lightweight FastAPI wrapper around the existing FAISS/embedding logic.
2. Build the Docker image and `rag-service.nomad` job file.
3. Update `TwinService` to use a proxy tool for RAG.
4. Deploy and test via Consul Service Mesh.

### Phase 3: Code Runner Sandbox Extraction
1. Create a dedicated Nomad job (`code-runner-service.nomad`) that wraps `CodeRunnerTool`.
2. Configure Consul Connect intentions to heavily restrict access to this service.
3. Update `TwinService` to offload code execution to this microservice.

## 5. Expected Outcomes
- **Reduced Memory Footprint:** `TwinService` becomes a pure orchestration layer, fitting comfortably on 2GB/4GB RAM devices.
- **Improved Resilience:** A crash in the Code Runner or an Out-Of-Memory (OOM) error during RAG embedding will not take down the main agent.
- **Enhanced Security:** Code execution is network-isolated and authenticated via mTLS.
