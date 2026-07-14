# Automated Ansible Exception Handler & Git PR Loop (Jules)

The **Automated Ansible Exception Handler & Git PR Loop** (referred to as **Jules Triage Operator**) is an autonomous infrastructure triage engine. When an Ansible playbook or task deployment fails in your CI/CD pipeline or local runner, this tool isolates the failure, reproduces/replicates it inside a local sandbox, dynamically troubleshoots and applies upstream reverse-compiled edits, validates the edits using linters/checks, and opens a verified Git-based Pull Request.

---

## 🛠️ Architecture Overview

The system consists of three decoupled components:

1. **The Standalone CLI Core (`scripts/ansible_exception_handler.py`):**
   A self-contained Python command-line utility. It runs independently of `pipecatapp` and its extensive dependencies (FastAPI, WebSockets, Audio/LLM pipelines), allowing you to debug and repair Ansible files even when the main agent platform is down.

2. **The Pipecat Agent Tool (`pipecatapp/tools/ansible_exception_handler_tool.py`):**
   An asynchronous agent tool (registered as `ansible_exception_handler`) that exposes the triage and fix loop to the online conversational agent.

3. **Core Exception Engine (`pipecatapp/utils/ansible_triage.py`):**
   The underlying state machine that coordinates:
   - Failure Context Parsing.
   - Self-Hosted/Local LLM Triage (with cloud fallback).
   - Reverse-Compilation & Upstream Synchronization.
   - Iterative Linting & Sandbox Health Verification.
   - Opengist Remote Git Push & Local Bundle Fallback.

---

## 📂 Context Directory Structure

The CLI and the Agent tool accept a `--context-dir` containing the exact failure dump:

```text
failure-context/
├── failure_log.txt       # Raw stderr and Ansible task failure output logs
├── failing_task.yml       # The exact Ansible task file that triggered the crash
├── host_vars.json         # Active facts, variables, and ports of the target node
└── rendered_artifacts/    # Configs/scripts (e.g., .yml, .j2, .hcl) compiled before crash
```

---

## 🚀 Standalone CLI Usage

The CLI script is located at `scripts/ansible_exception_handler.py`.

### Prerequisites
Make sure your Python dependencies are installed:
```bash
uv pip install -r requirements-dev.txt
```

### Basic Command
Execute the handler directly on the host machine:
```bash
./scripts/ansible_exception_handler.py \
  --context-dir /path/to/failure-context \
  --task-id "nginx-proxy-pass-v2"
```

### Return Codes
- `0`: Triage complete, patches applied, and syntax verification succeeded.
- `1`: Fatal error (e.g., invalid context directory, LLM API failure, or unexpected exception).
- `2`: Triage finished, but sandbox checks or linter validation failed.

---

## 💬 Online Agent Tool Usage

The tool is integrated into the Pipecat App framework. The conversational agent can invoke it via:

```json
{
  "name": "ansible_exception_handler",
  "arguments": {
    "context_dir": "/opt/pipecatapp/failure_context_123",
    "task_id": "nomad-job-unquoted-key"
  }
}
```

---

## 🔧 LLM Provider Resolution & Configuration

To prioritize enterprise privacy and resilience, Jules **prioritizes self-hosted LLM endpoints** before falling back to cloud providers. It resolves endpoints in this order:

1. **Local LLM Endpoint (Prioritized):**
   Checks environment variables `LOCAL_LLM_URL`, `LLAMA_API_BASE_URL`, `LLM_API_BASE_URL`, or `OPENAI_API_BASE_URL`.
   *Example:* `export LOCAL_LLM_URL="http://localhost:8000/v1"`
   *API Key:* `LOCAL_LLM_API_KEY` (defaults to `dummy-local-key`).

2. **OpenRouter Fallback:**
   If no local URL is defined, checks for `OPENROUTER_API_KEY` and targets `https://openrouter.ai/api/v1` with model `openrouter/auto`.

3. **OpenAI Fallback:**
   Checks for `OPENAI_API_KEY` and targets `https://api.openai.com/v1` with model `gpt-4o`.

*Note: If local backends are expected but unreachable, the script fails cleanly and logs the timeout instead of silently succeeding with stale configurations.*

---

## 🧪 Iterative Linting & Sandbox Checks

A successful triage run must verify the applied patches cleanly:
1. **Iterative Linting:** Runs `yamllint` and `ansible-lint` on the modified files dynamically.
2. **Playbook Syntax Check:** Runs `ansible-playbook -i local_inventory.ini playbook.yaml --syntax-check`.
3. **Playbook Dry-Run (Check-Mode):** Executes `--check` against local inventory to ensure deterministic deployment cleanly exits with code `0`.
4. **Dynamic Health Verification:** Automatically extracts target service ports and verification curl/netcat/bash commands directly from `host_vars.json` or `failing_task.yml` and executes them to verify initialization.

---

## 📦 Git Automation & Local Fallback (Opengist)

### 1. Git Branch Isolation
The moment a triage session starts, Jules isolates changes by cutting and switching to a dedicated branch:
```bash
fix/agent-ansible-<task_id>
```

### 2. Opengist Remote Push
Jules attempts to dynamically discover the lightweight `opengist` patch/gist server via Consul DNS (`opengist-http.service.consul:6157`) or HTTP Catalog. If reachable, it adds it as a git remote and pushes:
```bash
git push opengist fix/agent-ansible-<task_id> --force
```

### 3. Local Offline Fallback
If Opengist is offline, unreachable, or running in host-only environment:
1. A **Git bundle** is automatically saved: `fix-agent-ansible-<task_id>.bundle`.
2. A **structured Pull Request Markdown Summary** is written to: `pull_request_summary.md`.

This ensures you always get a rich, detailed record of the changes (Problem, Root Cause Analysis, Changes Applied, Verification Log) even in fully isolated offline networks!

---

## 🔬 Running Tests

To verify the exception handler tool and triage logic, run pytest:
```bash
PYTHONPATH=.:pipecatapp /home/jules/.pyenv/versions/3.12.13/bin/pytest tests/unit/test_ansible_exception_handler.py
```
