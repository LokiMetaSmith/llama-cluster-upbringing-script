# Evaluation of REA (Reverse Engineer Anything) for Cluster Inclusion

## 1. Executive Summary

This report evaluates **REA (Reverse Engineer Anything)**—an MCP (Model Context Protocol) server designed to enable AI agents to perform deep reverse engineering across applications, native binaries, and runtime environments—for integration into our local `pipecatapp` cluster.
REA provides a comprehensive toolkit for analyzing Javascript/Electron apps, websites, Android APKs, network captures, and native binaries (via Ghidra, Hopper, or IDA). Given our ongoing work with AI agents that require software diagnostic and decompilation capabilities, REA is highly relevant.

### Key Recommendations

1. **Integrate via `tool-server` Containerization**: REA is a Node.js (v22+) application. It should be deployed as a distinct unprivileged containerized service (e.g., inside our existing `tool-server` architecture under a `reverse_engineering` role), rather than directly coupling it to the core Python `pipecatapp` Workflow Engine.
2. **Prioritize Ghidra Headless Integration**: Our cluster nodes lack GUI environments. For native binary analysis, REA must be configured to use a headless installation of Ghidra over local Hopper or IDA Pro. Ghidra operates well on CPU-bound legacy nodes (Core 2 Duo) and natively supports headless analysis via Java bridges, perfectly aligning with our resource-constrained Nomad jobs.
3. **Sandbox Analysis Targets**: Reverse engineering inherently involves executing or parsing untrusted data (e.g., malware, buggy software). REA's backend providers must run within tightly bounded `docker` containers orchestrated by Nomad, ensuring malicious artifacts do not escape the filesystem namespace or consume unbounded cluster memory (8GB limits).
4. **Expose as a Custom Pipecat Tool**: The REA MCP interface must be wrapped into a standard `pipecatapp` tool (implementing `get_component_spec()`) to allow the legacy LLM orchestrators and multi-agent systems to seamlessly call it.

---

## 2. Architecture & Viability on Legacy Hardware

Our cluster consists primarily of **Intel Core 2 Duo nodes with 8GB RAM**, orchestrated via Nomad. REA's architecture relies on Node.js and a modular "Provider Layer" that spawns child processes for deep analysis.

### 2.1 CPU & Memory Footprint

* **Node.js MCP Server**: Lightweight. The base REA server uses a low amount of RAM and minimal CPU when idle.
* **Javascript/Static Analysis**: Artifact unpacking and ASAR analysis perform adequately on legacy CPUs.
* **Native Analysis (Ghidra/Hopper)**: Ghidra is Java-based and highly memory intensive. While a headless Ghidra instance can boot on 8GB RAM, concurrent analysis of large binaries *will* exhaust memory and trigger OOM (Out Of Memory) kills if not bounded.
**Recommendation**: When running REA within Nomad, we must set strict task limits (`memory = 4096`) and configure Ghidra's JVM max heap (`-Xmx3G`) to prevent it from destabilizing the host node. Furthermore, we must utilize `REA_GHIDRA_STARTUP_TIMEOUT_MS` to account for slow boot times on older Core 2 Duo CPUs.

### 2.2 Security and Sandboxing

REA supports evaluating untrusted native binaries and PCAPs.
Our cluster requires strict adherence to security rules:

* The tool must run as an unprivileged user (e.g., `pipecatapp`).
* Network isolation: Analyzing malicious web pages or performing PTY process captures must not leak into the trusted `tailscale0` mesh network. Any dynamic runtime captures should execute inside ephemeral Nomad jobs without network access to the primary cluster services.

---

## 3. Integration Strategy

REA uses the **Model Context Protocol (MCP)**, which is natively understood by modern agents (like Claude Code) via JSON-RPC. Our `pipecatapp` platform relies on custom Pydantic V2 tool wrappers.

### 3.1 Containerization within `tool-server`

Currently, `tool-server` handles `core`, `browser`, and `vision` microservices. We propose adding a fourth image: **`Dockerfile.rea`**.
This container would:

1. Base off an Ubuntu/Debian image with Node.js 22 installed.
2. Install headless Java (`default-jre`) and download the Ghidra zip archive.
3. Install REA globally via `npm install --global rea-agents`.
4. Run an entrypoint that starts `rea` bound to a local HTTP/TCP transport, allowing the `pipecatapp` Workflow Engine to interact with it securely.

### 3.2 Python Pipecat Wrapper

Within the `pipecatapp` repository, we will create `pipecatapp/tools/reverse_engineer_tool.py`.
This class will act as an MCP client bridge, implementing the `get_component_spec()` interface.
Example interaction:

1. The Pipecat agent decides to analyze an unknown `.exe` file.
2. It invokes the `reverse_engineer_tool` with the file path.
3. The Python wrapper forwards the request (via JSON-RPC) to the Node.js `tool-server` running REA.
4. REA orchestrates Ghidra, performs analysis, and returns the generated pseudocode/AST to the Python wrapper, which yields it back to the agent.

---

## 4. Conclusion & Action Plan

REA is an exceptionally powerful addition that empowers our AI agents to debug and decompile external systems. Its modular architecture is well-designed but requires careful integration to avoid resource exhaustion on our constrained hardware.

### Concrete Actions

1. **Dockerfile Extension**: Create `Dockerfile.rea` under `docker/` that includes Node.js 22, Ghidra (headless), and `rea-agents`.
2. **Nomad Job Update**: Add a `rea-server` task to the standard `ansible/jobs/` configurations.
3. **Pipecat Tool Creation**: Implement `pipecatapp/tools/rea_tool.py` as an MCP client wrapper, exposing standard JSON schema inputs for the legacy orchestration engine.
4. **Documentation**: Add a brief guide on dropping binaries into a shared Btrfs volume for the REA agent to analyze securely.

## 5. Implementation Status

**Completed:** The integration steps outlined above have been successfully implemented.

* **Docker Container**: A new `Dockerfile.rea` was created inside the `tool_server` role to build an unprivileged Node.js 22 container encompassing headless Ghidra and the `rea-agents` global NPM package. A lightweight FastAPI wrapper (`app_rea.py`) serves as the bridge.
* **Nomad Orchestration**: The `tool_server.nomad.j2` job specification was updated to include the `tool-server-rea` group, with strict memory limits (4096MB) and extended startup grace periods to accommodate Ghidra's JVM boot times.
* **Workflow Engine Tool**: The `ReverseEngineerTool` was added to `pipecatapp/tools/reverse_engineer_tool.py`, exposing a standard KFP-style component spec to the agents, bridging network calls seamlessly via Consul Service Discovery.
