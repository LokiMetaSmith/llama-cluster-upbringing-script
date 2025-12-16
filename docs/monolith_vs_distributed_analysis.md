# Monolith vs. Distributed Architecture Analysis

## Executive Summary

This document analyzes the theoretical resource overhead of the current containerized, distributed architecture ("Ensemble of Agents") compared to a hypothetical single-process monolithic application running on bare metal.

**Conclusion:** The current architecture introduces significant overhead, primarily in **Memory (RAM)** usage due to duplicated Python runtimes and **Latency** due to HTTP/JSON serialization between components. Transitioning to a monolith could save approximately **500MB - 1GB of RAM** and reduce request latency by **5-20ms per hop**, while simplifying the operational stack.

---

## 1. Architecture Comparison

### Current State (Distributed / Microservices)
The system currently operates as a cluster of independent services orchestrated by Nomad:

*   **Orchestration:** Nomad Agent, Consul Agent, Docker Daemon.
*   **Main Application (`pipecatapp`):** A Docker container running the core logic, STT (Faster-Whisper), and TTS (Piper).
*   **Expert/LLM Service (`expert`):** A separate Docker container (running `pipecatapp:local`) acting as an API gateway to the inference engine.
*   **Inference Backend (`rpc-server`):** A bare-metal process (`raw_exec`) running `llama.cpp`'s `rpc-server`.
*   **Tool Server (`tool_server`):** A separate Docker container running a FastAPI wrapper around python tools.
*   **World Model (`world_model_service`):** A separate service syncing state via MQTT.
*   **Communication:** Components communicate via HTTP (REST) and MQTT (Pub/Sub) over the loopback or local network interface.

### Proposed State (Monolith)
A single Python process running on bare metal:

*   **Orchestration:** None (Systemd unit or simple script).
*   **Main Application:** Imports all logic directly.
*   **LLM:** Uses `llama-cpp-python` direct bindings to load models and execute inference in-process (or in a thread).
*   **Tools:** Imported as standard Python modules.
*   **World Model:** A shared in-memory dictionary or singleton class.
*   **Communication:** Direct function calls and shared memory.

---

## 2. Resource Overhead Analysis

### A. Memory (RAM) Overhead

This is the most significant source of waste in the current architecture.

1.  **Python Runtime Duplication:**
    *   **Current:** `pipecatapp` (Main), `expert` (Python wrapper), `tool_server`, and `world_model_service` each require their own Python interpreter instance.
    *   **Cost:** A base Python process with libraries like `torch`, `fastapi`, and `numpy` loaded can easily consume **100MB - 200MB** just for the runtime environment.
    *   **Monolith:** One runtime. Libraries are loaded once. Shared objects (`.so` files) are mapped once by the OS, but private heaps are consolidated.
    *   **Savings:** ~300MB - 500MB.

2.  **Container Overhead:**
    *   **Current:** Each Docker container requires a `containerd-shim` process and kernel structures for cgroups/namespaces.
    *   **Cost:** ~5-10MB per container. With 4+ containers (Main, Expert, Tool Server, World Model), this adds up.
    *   **Monolith:** Zero.
    *   **Savings:** ~40MB.

3.  **Orchestration Agents:**
    *   **Current:**
        *   `nomad`: ~50-100MB RAM.
        *   `consul`: ~50-100MB RAM.
    *   **Monolith:** Removed.
    *   **Savings:** ~100MB - 200MB.

**Total Estimated RAM Savings:** **~0.5 GB - 1.0 GB**

### B. Compute (CPU) Overhead

1.  **Serialization/Deserialization:**
    *   **Current:** Every interaction between the App and the LLM, or the App and Tools, involves:
        1.  Python Dict -> JSON string (Serialize).
        2.  JSON string -> HTTP Packet (Network Stack).
        3.  HTTP Packet -> JSON string (Receive).
        4.  JSON string -> Python Dict (Deserialize).
    *   **Monolith:** Zero. Data is passed as pointers/references.
    *   **Impact:** Noticeable during high-frequency token streaming or large prompt transfers, consuming CPU cycles that could be used for inference.

2.  **Context Switching:**
    *   **Current:** The OS scheduler must constantly switch between the Application process, the HTTP server process, the Docker daemon, and the networking stack.
    *   **Monolith:** Reduced context switching, improving CPU cache locality.

### C. Latency

1.  **Network Hops:**
    *   **Current:** Localhost HTTP requests typically take **1-5ms**. While small, this adds up in multi-step "Agentic" workflows (e.g., Thought -> Tool -> Observation -> Thought) which can involve dozens of round-trips per user request.
    *   **Monolith:** Function calls take **nanoseconds**.

2.  **Inference Latency:**
    *   **Current:** The `expert` job adds an extra hop: `App -> Expert (HTTP) -> RPC Server (TCP)`.
    *   **Monolith:** `App -> LLM (C Binding)`. Removing the "Expert" proxy and the RPC layer (if running on a single GPU) reduces "Time to First Token" (TTFT).

---

## 3. Specific Component Deep Dive

### LLM Inference
*   **Current:** Uses `llama.cpp`'s `rpc-server` + a Python "Expert" proxy. This is designed for *distributed* inference (splitting one model across multiple machines). On a single machine, this is purely overhead.
*   **Monolith:** Direct C++ bindings (`llama-cpp-python`) allow the Python app to talk directly to the GPU memory. This eliminates the need to copy tensor data into network buffers.

### Tool Server
*   **Current:** The `tool_server` exposes tools via HTTP.
*   **Monolith:** Tools are just classes. The security isolation provided by the container is lost (unless using Firejail/Sandbox), but the overhead of serializing arguments and results is eliminated.

### World Model
*   **Current:** State is synced via MQTT. This allows other devices (like Home Assistant) to subscribe, but for internal app state, it's slow.
*   **Monolith:** The "World Model" becomes a class instance. External syncing can still happen via a background thread publishing to MQTT, but the app itself doesn't need to wait for the network to read its own state.

---

## Summary of Trade-offs

| Feature | Distributed (Current) | Monolith (Proposed) |
| :--- | :--- | :--- |
| **Resource Efficiency** | Low (High RAM/CPU overhead) | **High** (Maximized for hardware) |
| **Latency** | Medium (Network hops) | **Low** (Direct calls) |
| **Simplicity** | Low (Complex orchestration) | **High** (Single script/service) |
| **Scalability** | **High** (Add nodes easily) | Low (Vertical scaling only) |
| **Resilience** | **High** (Restart individual crashes) | Low (App crash kills everything) |
| **Isolation** | **High** (Tools can't crash App) | Low (Segfault in tool kills App) |

**Recommendation:** If the goal is running on resource-constrained edge hardware (e.g., NVIDIA Jetson, Consumer PC), the **Monolith** approach is vastly superior. The Distributed architecture is only beneficial if you intend to span the application across multiple physical machines.
