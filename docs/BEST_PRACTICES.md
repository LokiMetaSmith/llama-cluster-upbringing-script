# Best Practices and Development Guidelines

This document serves as the ground-truth reference for architectural boundaries, structural conventions, and specific development rules across the repository. It is primarily designed to guide autonomous agents and human developers, ensuring consistency and preventing regressions across complex, multi-language cluster deployments.

---

## 1. Project Structure

The repository is a hybrid monorepo consisting of Ansible playbooks, Rust systems programming, Python backends, and cluster configuration. Key directories include:

*   **/ansible:** Contains playbooks, roles, and templates for cluster provisioning (Nomad, Consul, Docker, networking).
    *   *Rule:* All application port assignments must be centrally defined in `group_vars/all.yaml` (e.g., `pipecat_port: 8007`) to prevent collisions. Nomad job network stanzas must explicitly use these variables with `static = {{ port_var }}`.
*   **/pipecatapp:** The core Python service orchestrating the AI workflow engine (`TwinService`).
    *   *Rule:* When adding new Python modules or subdirectories here, explicitly append them to the `ansible.builtin.copy` tasks list in `ansible/roles/pipecatapp/tasks/main.yaml` (omitting tests).
*   **/colibri_io_uring:** The Rust-based prototype for high-performance SSD-to-VRAM streaming and `StreamingMoeLayer`.
    *   *Rule:* Project-specific task tracking for the Colibri prototype is maintained in `colibri_io_uring/TODO.md` rather than the repository root.
*   **/scripts:** Utility scripts for cluster management, cleanup (`cleanup.sh`, `clean_caches.sh`), cache deduplication (`dedup_venvs.py`), and pre-flight agent checks.
*   **/command_deck:** Contains clients and benchmarks for interaction, such as the `personaplex_client.py` websocket client for real-time audio capture and latency benchmarking.
*   **/tests:** Standardized unit tests (`tests/unit/`).

---

## 2. Core Architectural Principles

*   **Workflow Autonomy:** In the `pipecatapp` workflow engine, tools are managed dynamically. The `ToolExecutorNode` supports per-node configuration of tool autonomy via `autonomous_tools` and `requires_approval_tools` in workflow YAMLs.
*   **Routing and Escalation:** `DynamicSupervisorNode` handles dynamic routing by evaluating sub-agent execution against prompts, directing to `pass_route` or `escalate_route` based on an LLM judge.
*   **Hardware Agnosticism (Rust):** To support direct NVMe-to-VRAM streaming across vendors (NVIDIA, AMD, Intel), use a hardware-agnostic trait abstraction (e.g., `DirectVramStreamer`).
*   **Zero-Copy Memory (Rust):** For Rust-based I/O streaming engines (`colibri_io_uring`), utilize `posix_memalign` with `O_DIRECT` to achieve zero-copy kernel DMA into page-aligned host buffers. When bridging tensors via `candle_core` from raw `&[u8]` buffers, safely use `unsafe { buf.align_to::<T>() }` for zero-copy transmutation.
*   **PersonaPlex Integration:** Relies on `state_adapter.py` to translate structured XML/JSON simulation states into natural language.
*   **Rust Dependency Management:** Prefer `edition = "2021"` or avoid overly restrictive edge versioning in `Cargo.toml` to prevent dependency hallucination build issues. Ensure `moshi-core` and `colibri_io_uring` compile together without debugging unrelated third-party trait bound conflicts (e.g., `axum-server`).
*   **Python Execution:** When executing workflows via `WorkflowRunner`, use `runner.run(global_inputs)`, NOT `runner.run_async()`.

---

## 3. Security Guidelines

*   **Zero-Tolerance for TLS/SSL Bypasses:** Agents must never use arguments like `validate_certs: no` (Ansible), `--insecure` / `-k` (cURL), `verify=False` (Python/Requests), or `NODE_TLS_REJECT_UNAUTHORIZED=0` (Node.js). Fix the root cause (trust infrastructure, SANs).
*   **Defense in Depth:** Web applications (e.g., Uvicorn) must natively serve HTTPS at the application layer using internal CA certificates (injected via Nomad `template` blocks), rather than relying solely on network-level encryption like WireGuard. Python scripts must explicitly trust the internal CA.
*   **Tailscale / Headscale Mesh Security:** All automated (Ansible) and day-to-day Headscale pre-auth keys must be **ephemeral (single-use)** and dynamically generated. Static, cluster-wide reusable keys are strictly forbidden to prevent lateral movement.
*   **USB Break-Glass Key:** Maintained via `scripts/imprint_usb_keychain.sh`, generated with `tag:usb-bootstrap`, monitored via `scripts/alert_usb_bootstrap_usage.sh`, and revocable.
*   **Secrets Evaluation:** The `PostProcessorNode` securely evaluates Python expressions (including f-strings).

---

## 4. Development & Testing Practices

*   **Environment Setup:** Initialize virtual environments with `uv venv` and install via `uv pip install -r pipecatapp/requirements.txt`. System dependencies (e.g., `portaudio19-dev` for `pyaudio`) must be installed first.
*   **Test Location & Imports:** Unit tests must reside in `tests/unit/`. Run internal package tests using PYTHONPATH correctly (e.g., `PYTHONPATH=$(pwd):$(pwd)/pipecatapp uv run pytest <test_file>`).
*   **Mocking:** Use standard library `unittest.mock.patch` (`AsyncMock` or `MagicMock`). Do NOT introduce external libraries like `pytest-httpx` or `pytest-mock`.
*   **Mocking `asyncio.wait_for`:** When mocking functions wrapped inside `asyncio.wait_for`, mock `asyncio.wait_for` to return the target directly and mock the inner function as a synchronous `MagicMock` to prevent `RuntimeWarning`.
*   **Pre-flight Checks:** Always run `scripts/agent_preflight.sh` or `scripts/agent_fast_check.sh` before submission. `AGENTS.md` mandates that all linters (`npm run lint`), `vulture` dead-code scans, and tests (`pytest`) must pass.
*   **Local Configuration:** Ensure `~/.config/pipecat/` exists when running tests like `test_app_hybrid.py`.
*   **LLM Configuration:** Passed dynamically via `--llm-config` command-line argument as JSON strings in reflection pipelines.

---

## 5. Infrastructure & Deployment Rules

*   **Nomad/Consul Raft Quorum:** Dynamically set `bootstrap_expect` to `{{ groups['controller_nodes'] | length }}`.
*   **Mesh Node Discovery:** Nomad/Consul configurations must populate their `retry_join` lists with ALL controller node IPs using `groups['controller_nodes']` (not just a single primary).
*   **Consul Retries (Ansible):** Wrap write operations (e.g., PUT requests to Consul) with retry logic (`retries: 6`, `delay: 10`) to handle 500 'No cluster leader' errors during early Raft leader elections.
*   **Parsing Consul Errors:** Always combine `stdout` and `stderr` when parsing errors in Ansible. If 'ACL bootstrap no longer allowed' occurs, dynamically extract the reset index from logs, write to `acl-bootstrap-reset`, and restart Consul before retrying.
*   **Ansible `uv pip install`:** Explicitly set `UV_CACHE_DIR` to a managed temp directory (e.g., `/var/tmp/ansible_pip_build/uv_cache`) to prevent 'No space left on device' errors in constrained home directories.
*   **Systemd Services:** When using `ansible.builtin.systemd` to start/enable a service immediately after copying a unit file, ALWAYS include `daemon_reload: yes` to prevent EBUSY errors. When forceful termination is needed, ensure the `.service` file is removed/disabled and `daemon-reload` is executed before `pkill`ing the process to prevent instant respawning.
*   **IPFS Caching & Cleanup:** If tasks like 'Warm up IPFS gateway cache' fail with 504 Gateway Timeout, increase `retries` (e.g., to 30). For cleanup, explicitly run `scripts/ipfs_cleanup.sh` to unpin orphaned objects since `ipfs repo gc` alone is insufficient.
*   **System Cleanup:** `--system-cleanup` in `bootstrap.sh` heavily relies on `scripts/cleanup.sh`, `scripts/clean_caches.sh` (clears large caches like `~/.cache/pip`, `~/.npm/_cacache`), and `scripts/dedup_venvs.py` (hardlinking `.so` files across venvs).
*   **FastAPI & Uvicorn:** Preferred stack for backend HTTP services in the cluster.
*   **Git Integrations:** When adding large external repositories (e.g., `moshi`), remove the internal `.git` folder and use a whitelist `.gitignore` approach (e.g., ignoring `moshi/*` but allowing `!moshi/rust/`) to avoid tracking artifacts.
*   **Local Backend Debugging:** The `ARCHIVIST_PORT` defaults to `8008` in bash scripts and Python services for local testing without Nomad's dynamic port allocation.