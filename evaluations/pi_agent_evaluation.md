# Pi Agent Harness Evaluation & Integration Plan

## 1. Executive Summary

This document evaluates [Pi](https://pi.dev/), a minimal agent harness, for inclusion into the `pipecatapp` ecosystem. Pi is designed to be highly extensible through skills, extensions, prompt templates, and themes, focusing heavily on TUI (Terminal User Interface) interactions and customizability via JavaScript/TypeScript.

Our current system is a robust, distributed pipeline built heavily on Python, Ansible, Nomad, and Consul. It already features complex workflow orchestration (`pipecatapp/workflows/`), dynamic routing, multi-agent swarming (`swarm_tool.py`), and sandbox code execution (`smol_agent_tool.py` and `code_runner_tool.py`).

While Pi and our system overlap in the broad goal of "executing agentic workflows," they do so in different paradigms. Pi excels at minimal, fast, single-user CLI-based harness extensions, whereas our system excels at distributed backend orchestration. Incorporating Pi as an orchestrated module/node within our workflow engine allows us to leverage its rich CLI/TUI generation and minimal Javascript/TypeScript extension ecosystem.

## 2. Feature Comparison: Pi vs. Current System

| Feature Area | Pi (`@earendil-works/pi-coding-agent`) | Current System (`pipecatapp`) | Notes |
| :--- | :--- | :--- | :--- |
| **Core Architecture** | Node.js / TypeScript. Single-process harness. | Python. Distributed, containerized via Nomad. | Pi acts as a fast, local executable, while our system is a distributed backend cluster. |
| **Primary Interface** | Advanced TUI, JSON output, RPC. | Web UI, Gemini CLI extension, API. | Pi's TUI and print modes are strong, interactive alternatives to our `Term Everything` tool. |
| **Workflow Definition** | JavaScript/TypeScript Extensions and "Skills" (packages). | Declarative YAML graphs (`pipecatapp/workflows/`). | We can run Pi *inside* a YAML workflow node to execute specific Javascript-based skills. |
| **Extensibility** | npm packages, GitHub repos, dynamic context injection. | Python tools (`pipecatapp/tools/`), external API routing. | Pi offers a large ecosystem of front-end and simple CLI tools that we currently lack. |
| **Sandboxing & Execution** | Relies on third-party extensions or local shell. | Built-in Pyodide/Deno sandbox (`smol_agent_tool.py`), Docker. | Our execution environment is more heavily sandboxed out-of-the-box. |

## 3. Architectural Fit & Workflow Integration

The user request specifies adding Pi as a "module" or "worksheet addition" (which maps to our YAML workflows).

**How it fits:**
Pi should *not* replace our main router or orchestrator. Instead, it should be integrated as a specialized execution node within our workflow engine. Because Pi operates in Javascript/TypeScript and is installable via `npm`/`bun`, it fits perfectly as an execution layer for tasks that require deep TUI interaction, JS-ecosystem tooling, or specific Pi "skills" that are difficult to replicate in Python.

We can define a new `PiAgentNode` (in `pipecatapp/workflow/nodes/`) that:
1. Accepts an input prompt from the workflow.
2. Invokes Pi in `--mode json` or `print` mode (e.g., `pi -p "query"`).
3. Captures the output and streams it to the next node in the YAML workflow.

## 4. Implementation Options

We evaluated the following paths for implementation:

### Option A: `PiAgentNode` Workflow Node (Recommended)
Create a native Python node in the workflow engine (`pipecatapp/workflow/nodes/pi_node.py`). This node will spawn a local `pi` subprocess, pass it the necessary context, and return the output.
- **Pros:** Native integration with existing `.yaml` worksheets. Direct data flow between `Pi` and our LLMs.
- **Cons:** Requires ensuring Node.js/npm and Pi are installed on the worker machines executing the workflow.

### Option B: Nomad Job / RPC Server
Deploy Pi as a persistent background service in Nomad, communicating via its built-in RPC mode over stdin/stdout or wrapped in an HTTP server.
- **Pros:** Perfect isolation. Doesn't pollute the Python environment.
- **Cons:** High overhead for a CLI tool. Pi is designed to be spun up dynamically.

### Option C: Python Tool (`pipecatapp/tools/pi_tool.py`)
Wrap Pi as a standard tool (like `smol_agent_tool.py`) that the main LLM can call to execute specific Javascript skills.
- **Pros:** Easy to implement.
- **Cons:** Constrains Pi to the context window of the main agent, rather than letting it run as its own step in the workflow graph.

**Conclusion:** We will proceed with **Option A** (supported by **Option C** under the hood if necessary), creating a `PiAgentNode` to act as a worksheet/workflow node.

## 5. To-Do List for Integration (Proof-of-Concept)

To successfully implement the Pi agent into our system, the following steps must be completed:

- [x] **Environment Provisioning (Ansible):**
   - Updated `ansible/roles/pipecatapp/tasks/main.yaml` to globally install Pi via `npm install -g --ignore-scripts @earendil-works/pi-coding-agent`.

- [x] **Core Workflow Node Implementation:**
   - Created `pipecatapp/workflow/nodes/pi_node.py`.
   - Implemented the `PiAgentNode` class inheriting from the base node class.
   - Configured the node to construct the `pi` CLI command, utilizing print (`-p`) mode to interact programmatically via `subprocess`.

- [x] **Workflow Registration:**
   - Registered `PiAgentNode` in the workflow node registry (`__init__.py`) so it can be parsed from YAML files.

- [x] **Example YAML Workflow:**
   - Created `pipecatapp/workflows/pi_integration_test.yaml`.
   - Defined a flow that takes an `InputNode`, passes it to the `PiAgentNode` (instructing Pi to use a specific skill), and outputs via `OutputNode`.

- [x] **Testing & Verification:**
   - Added unit tests for `pi_node.py` mocking the `subprocess` call to the Pi CLI, ensuring graceful handling of timeouts and missing binaries.
