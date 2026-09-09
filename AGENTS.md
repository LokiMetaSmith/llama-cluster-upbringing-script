# AGENTS.md

Welcome, Agent. This file contains the mandatory operating procedures, execution constraints, CLI cheatcodes, and playbooks for working within this repository.

This document serves a **dual target audience**: primarily Jules and autonomous AI coding agents requiring strict, deterministic guardrails and actionable CLI playbooks, but also human engineers seeking a clear reference for system operations.

You must strictly adhere to the following rules, tools, and workflows. Do not deviate, shortcut, or attempt to bypass these instructions.

---

## 💻 EXECUTION ENVIRONMENT PROFILE

Autonomous agents operating in this sandbox environment run under the following operational specifications and constraints:

* **Hardware & Virtualization:** Intel(R) Xeon(R) Processor @ 2.30GHz (4 Cores / 4 Threads, x86_64), ~7.8 GiB Total RAM, 98 GB Disk Space (OverlayFS) under KVM / Containerized setup.
* **OS & User Context:** Ubuntu 24.04 Headless running under user `jules` (uid=1001, gid=1001) with passwordless `sudo` privileges.
* **Resource Optimization Guidelines:**
  * **Build Concurrency:** Keep memory-heavy build/compilation processes single-threaded or capped at `-j2` / `-j4` to prevent Out-Of-Memory (OOM) failures on 7.8 GiB RAM.
  * **Headless Operations:** Always run tests, plotting libraries, and browser/UI engines headlessly (e.g., `export MPLBACKEND=Agg` for matplotlib, headless browser arguments for Playwright/Puppeteer).
  * **Compute Fallbacks:** Do not assume host GPU/CUDA hardware is present during agent tasks; enforce CPU fallbacks for PyTorch, ONNX, and OpenCV executions.

---

## 🚀 AGENT CHEATCODES & TRIGGER KEYWORDS

When these trigger phrases appear in prompt instructions or user requests, execute the corresponding workflow actions:

| Trigger Keyword / Phrase | Mode & Workflow Action |
| :--- | :--- |
| `"Use deep planning mode"` | **Forces explicit requirement verification**, dependency tracing, architectural analysis, and risk audits using `request_user_input` before creating or executing a plan. |
| `"Add tests in pytest / jest"` | **Prioritizes dedicated automated test coverage**. Every new feature, bug fix, or tool modification must include corresponding `pytest` or `jest`/`npm test` cases. |
| `"Run pre-commit checks"` | **Audits code quality before submission**. Runs syntax checks, linting, formatting (`scripts/agent_fast_check.sh`), dead-code detection (`vulture`), and preflight scripts (`scripts/agent_preflight.sh`). |
| `"Create an AGENTS.md guide for this repo"` | **Self-documents repository patterns**. Generates or updates local `AGENTS.md` files with directory-specific conventions, tools, and testing procedures. |

---

## 🔒 SECURITY ENFORCEMENT: Zero-Tolerance for TLS/SSL Bypasses

* **Core Rule:** You are strictly prohibited from bypassing, disabling, or ignoring TLS/SSL certificate validation to resolve connection errors or force a failing pipeline to pass.
* **Forbidden Mechanisms:** You must never use arguments such as `validate_certs: no` (Ansible), `--insecure` / `-k` (cURL), `verify=False` (Python/Requests), `NODE_TLS_REJECT_UNAUTHORIZED=0` (Node.js), or any equivalent bypass.
* **Fix the Root Cause:** If a TLS handshake fails (e.g., "invalid certificate", "unknown issuer"), you must diagnose and fix the underlying cryptographic trust infrastructure.
* **Certificate Requirements:** When troubleshooting mesh or cluster SSL errors, verify that the Root CA has the correct `basicConstraints` (`CA:TRUE`) and `keyUsage`, ensure Subject Alternative Names (SANs) include the correct mesh IPs (e.g., Tailscale `100.x.y.z`) and DNS names, and verify the CA is correctly appended to the target system's trust store.
* **No Band-Aids:** "Green" pipelines achieved by disabling security are considered critical failures. Absolute mesh security and zero-trust integrity supersede task completion speed.

---

## 📚 ARCHITECTURAL & CODING STANDARDS

* **Core Rule:** You must consult and strictly adhere to the `docs/BEST_PRACTICES.md` document. It contains the ground-truth reference for architectural boundaries, directory structures, testing requirements, and specific system memory rules (like zero-copy Rust DMA, ephemeral Tailscale keys, and `uv pip install` caching) that govern development in this repository.

### Modern Python & Ansible Tooling Protocols
* **`uv` Package Manager:** Always use `uv` for Python virtual environments and package installations (`uv venv`, `uv pip install`, `uv run`).
* **`uvx` Ephemeral Tooling:** Run CLI tools (such as Ansible playbooks and linter tools) using `uvx` to ensure isolated execution (e.g., `uvx --from ansible-core ansible-playbook`, `uvx ansible-lint`).
* **Directory Sync & State Exclusions:** In Ansible roles and deployment scripts (e.g., `ansible.posix.synchronize`), perform recursive syncs while strictly preserving runtime state files (such as SQLite DBs, `.liminal`, `chromadb/`, `holographic_memory/`, `visualizations/`, `pipecat.env`, `pw-browsers/`, and `venv/`) using rsync exclusion patterns.

---

## 🔨 EXECUTABLE ORACLES & VERIFICATION SCRIPTS

You are provided with several executable oracles to verify your work. You must use these tools to test your code before considering a task complete.

* **Pre-flight Checks:** You must run the `scripts/agent_preflight.sh` script prior to submitting any code. This wrapper runs tests, linters, and static analysis tools.
  * *Oracle Rule:* You must include the output (or a statement of its success) when you submit a task. All checks within it must pass.
* **Rapid Local Verification (Fast-Check Loop):** During rapid local development and iteration, run `scripts/agent_fast_check.sh` to quickly check code formatting, dry-run Ansible playbooks, and run Python unit tests without full bootstrap overhead.
  * *Usage:* Run `./scripts/agent_fast_check.sh` for all fast checks, or pass filters/targets directly (e.g., `./scripts/agent_fast_check.sh --tests-only tests/unit/test_safe_flatten.py`).
* **Automated Tests:** Run unit and integration tests using `pytest` (Python) or `npm run test` (JavaScript/TypeScript).
  * *Oracle Rule:* A failing test is a showstopper. You must fix the code until the test passes. Every new feature or bug fix MUST include a corresponding automated test.
* **Linters & Static Analysis:** Run `npm run lint` or `scripts/lint.sh` to check for formatting and syntax errors. Static analysis (`mypy`) and dead-code detection (`vulture`) are included.
  * *Oracle Rule:* All code must pass linting without errors or warnings. You MUST remove any orphaned code identified by `vulture`.
* **Code Runner Sandbox:** Use the `code_runner` tool to execute Python code in an isolated container sandbox.
  * *Oracle Rule:* Validate your logic in the sandbox before modifying host files.
* **Autoresearch Iteration:** Use the `autoresearch` tool for automated hypothesize-edit-evaluate loops.
  * *Oracle Rule:* The tool will evaluate your code against a test command (e.g., `pytest`). A non-zero exit code means failure, and the change will be reverted.

---

## 📋 MANDATORY PLAYBOOKS

When modifying or creating code, you must follow this linear sequence of steps. **These steps are mandatory; deviations are not allowed.**

1. **Understand the Goal:** Read the issue description, `README.md`, and use the `rag` tool to search the knowledge base for relevant context.
2. **Explore the Codebase:** Use `project_mapper` or `shell` (with `find`/`grep`) to locate the relevant source files. **Do not edit build artifacts** (e.g., `/dist`, `/build`). Trace back to the source.
3. **Hypothesize & Plan:** Formulate a plan and use the `set_plan` tool. If the task is complex, write a failing test first.
4. **Edit Source:** Modify the source code using the `file_editor` or `shell` tools.
5. **Run Executable Oracles:** Immediately run the relevant tests (`pytest`, `npm run test`) and linters (`npm run lint` / `./scripts/agent_fast_check.sh`).
6. **Analyze & Iterate:** If an oracle fails, analyze the error output (the concise counterexample or stack trace). Do not ignore the error. Fix the code and re-run the oracle.
7. **Finalize:** Only mark the step complete when all oracles pass, including `./scripts/agent_preflight.sh`.

---

## 🚫 ANTI-PATTERNS & UNCONTROLLED DEGREES OF FREEDOM

Be aware that executable oracles cannot easily measure everything. You must strictly avoid the following anti-patterns and exercise human-like judgment:

### Explicit Anti-Patterns to Avoid
* **Modifying Generated State Files / Build Artifacts:** Never edit generated files, compiled bundles (`dist/`, `build/`), or runtime database files directly. Always trace to original source files.
* **Omitting Headless Flags:** Never execute GUI tests, browser automation, or plotting libraries without explicit headless configurations (`MPLBACKEND=Agg`, headless browser flags).
* **Assuming Host GPU Availability:** Never write non-defensive GPU/CUDA code assuming host GPU presence. Always implement CPU fallback mechanisms.
* **Copying Stale Artifacts or Virtualenvs:** Never copy `.venv`, `node_modules`, or uncommitted temporary build files across node targets. Use explicit rsync exclusion rules.
* **Disabling Security / SSL:** Never use insecure TLS parameters (`validate_certs: no`, `-k`, `verify=False`, `NODE_TLS_REJECT_UNAUTHORIZED=0`).

### Code Quality Standards
* **Software Architecture:** Ensure your code is modular, readable, and follows existing design patterns. Do not paint yourself into a corner with poor architecture.
* **Duplication:** Do not write nearly-duplicate functions or excessive defensive code. Abstract properly.
* **Dead Code:** Remove code that becomes dead or unreachable as you work. Do not leave it behind. You must actively look for and delete orphaned functions and classes that you replace. Use `vulture` to assist in finding dead code.

---

## 🛠 TOOL USAGE AND QUERYABLE INTERFACES

* **`shell` (Persistent Tmux Session):**
  * *Usage:* Use this for navigating directories, running scripts, and executing git commands.
  * *Long-Running Processes:* **Warning:** Do not wait synchronously for a long-running process (like a server) that will never finish. To run a process in the background, append `&` and redirect output to a file (e.g., `npm start > app.log 2>&1 &`). Use `tail -n 50 app.log` to check the status.
  * *Timeouts:* Commands have a default timeout (usually 30s). If a command times out, it means you likely ran a blocking process without `&`.
* **`autoresearch` (Iterative Loop):**
  * *Usage:* Provide a `target_file`, a `test_command`, and `program_instructions`. The tool will automatically run the loop and commit/revert based on the `exit_code`.
* **`code_runner` (Sandbox):**
  * *Usage:* Execute snippets of Python in an isolated container.
* **`rag` (Knowledge Retrieval):**
  * *Usage:* Ask specific questions about the project architecture, design decisions, or existing APIs.

---

## ⚠️ HANDLING FAILURES

LLMs are industrious but can be lazy. If a tool fails (e.g., command not found, permission denied, missing library):

* **DO NOT** rewrite the tool from scratch.
* **DO NOT** try to bypass the sandbox or security controls.
* **DO** read the error message carefully. Install the missing dependency, fix the path, or adjust the configuration. Ask the user for help if you are truly stuck.

---

## 🔄 UPDATING LOCAL CLUSTER INFRASTRUCTURE

When updating the `bootstrap.sh` script (the primary upbringing script that manages and scales the cluster infrastructure), you MUST verify the changes using the local ROCm simulation to avoid recursive crash loops (the "Ouroboros Effect").

* **Mandatory Action:** You must run `act` locally (the local GitHub Action runner) and verify workflows pass before proposing or submitting a merge to the primary branch.
* **Pre-commit Hook:** Always ensure the custom pre-commit hook is active by running `git config core.hooksPath .githooks`. This hook provides a safety net against logic errors and missing ROCm checks.
* If the simulation fails with a 'VGPR Mismatch' or 'KFD Error', or other container crash, roll back the changes and search for recent amdgpu firmware patches or logic errors in the code. Do not bypass these local tests under any circumstances.

---

## 🧠 FIVE PRINCIPLES OF AGENT SKILLS

1. **Process over prose:** Workflows are actionable; essays are not. Use defined sequences of steps with checkpoints.
2. **Anti-rationalization tables:** Anticipate and rebut excuses for skipping workflows (e.g., "This is too simple to need a test").
3. **Verification is non-negotiable:** Every task must terminate with concrete evidence (passing tests, clean build output, etc.) rather than "seems right".
4. **Progressive disclosure:** Only load the skills and context relevant to the current phase of the task.
5. **Scope discipline:** Touch only what you are asked to touch. Avoid refactoring adjacent systems or unrelated code without explicit instruction.
