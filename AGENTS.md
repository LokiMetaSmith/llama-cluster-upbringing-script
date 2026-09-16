# AGENTS.md

## Project overview

This document contains the mandatory operating procedures, execution constraints, CLI cheatcodes, and playbooks for working within this repository. It serves a **dual target audience**: primarily Jules and autonomous AI coding agents requiring strict, deterministic guardrails, but also human engineers seeking a clear reference for system operations.

The repository is a Distributed Conversational AI Pipeline: A stateful, embodied AI agent pipeline on a cluster of legacy computers, powered by Ansible, Nomad, Consul, and Pipecat. You must consult and strictly adhere to the `docs/BEST_PRACTICES.md` document. It contains the ground-truth reference for architectural boundaries, directory structures, testing requirements, and specific system memory rules (like zero-copy Rust DMA, ephemeral Tailscale keys, and `uv pip install` caching) that govern development in this repository.

## Project structure

- `ansible/` - Contains all Ansible playbooks, roles, and templates for provisioning and deploying the entire system.
  - `ansible/roles/` - Individual, reusable components (e.g., `nomad`, `consul`, `pipecatapp`).
  - `ansible/roles/pipecatapp/files/` - The core Python source code for the conversational agent (e.g., `app.py`, `memory.py`, `tools/`).
- `pipecatapp/workflows/` - YAML definitions for the agent's behavior and thought processes.
- `verification/` - Scripts and tools for verifying the system's frontend and functionality.
- `prompt_engineering/` - Scripts and tools for evaluating and improving the AI's prompts.
- `reflection/` - Scripts related to the agent's self-reflection and self-healing capabilities.
- `scripts/` - Utility and linting scripts for maintaining code quality.
- `testing/` - Contains unit and integration tests for the various components of the project.
- `group_vars/` - Ansible configuration files that apply to all hosts, such as `all.yaml` and `models.yaml`.

## Setup & build

```bash
uv venv                # Create virtual environment
uv pip install -r ...  # Install dependencies
```

- **Execution Environment Profile**: You operate in an Ubuntu 24.04 Headless environment under user `jules` (uid=1001, gid=1001) with passwordless `sudo` privileges. Hardware is limited (~7.8 GiB Total RAM, 98 GB Disk Space under KVM / Containerized setup).
- **Build Concurrency**: Keep memory-heavy build/compilation processes single-threaded or capped at `-j2` / `-j4` to prevent Out-Of-Memory (OOM) failures.
- **`uv` Package Manager**: Always use `uv` for Python virtual environments and package installations (`uv venv`, `uv pip install`, `uv run`).
- **`uvx` Ephemeral Tooling**: Run CLI tools (such as Ansible playbooks and linter tools) using `uvx` to ensure isolated execution (e.g., `uvx --from ansible-core ansible-playbook`, `uvx ansible-lint`).
- **Directory Sync & State Exclusions**: In Ansible roles and deployment scripts (e.g., `ansible.posix.synchronize`), perform recursive syncs while strictly preserving runtime state files (such as SQLite DBs, `.liminal`, `chromadb/`, `holographic_memory/`, `visualizations/`, `pipecat.env`, `pw-browsers/`, and `venv/`) using rsync exclusion patterns.

## Testing

```bash
./scripts/agent_preflight.sh     # Pre-flight Checks wrapper runs tests, linters, and static analysis tools.
./scripts/agent_fast_check.sh    # Rapid Local Verification loop.
pytest                           # Python unit/integration tests
npm run test                     # JavaScript/TypeScript tests
```

- Run the full suite before committing (`scripts/agent_preflight.sh`). All checks within it must pass. You must include the output (or a statement of its success) when you submit a task.
- While iterating, run the single test closest to your change, or use `scripts/agent_fast_check.sh`.
- Never delete, weaken, or rewrite a test to make a change pass.
- Do not claim that an interrupted or timed-out run passed.
- A failing test is a showstopper. You must fix the code until the test passes. Every new feature or bug fix MUST include a corresponding automated test.
- Validate your logic in the sandbox before modifying host files (use `code_runner` or `autoresearch`).
- **Updating local cluster infrastructure**: When updating the `bootstrap.sh` script, you MUST verify the changes using the local ROCm simulation via `act` locally (the local GitHub Action runner) to avoid recursive crash loops (the "Ouroboros Effect"). If the simulation fails with a 'VGPR Mismatch' or 'KFD Error', or other container crash, roll back the changes. Do not bypass these local tests under any circumstances.

## Code style

- Formatter/Linter: `npm run lint` or `scripts/lint.sh`. Run them; do not hand-format.
- Static analysis (`mypy`) and dead-code detection (`vulture`) are included in linting.
- Follow the patterns already in neighboring files.
- Do not add comments that restate the code.
- Do not reformat code you are not otherwise changing.
- All code must pass linting without errors or warnings. You MUST remove any orphaned code identified by `vulture`.
- **Software Architecture**: Ensure your code is modular, readable, and follows existing design patterns. Do not write nearly-duplicate functions or excessive defensive code. Abstract properly.

## Git workflow

- **Mandatory Playbooks**: You must follow this sequence: 1) Understand the Goal. 2) Explore the Codebase (trace to source, do not edit build artifacts). 3) Hypothesize & Plan (`set_plan`). 4) Edit Source. 5) Run Executable Oracles. 6) Analyze & Iterate. 7) Finalize (only when `./scripts/agent_preflight.sh` passes).
- **Pre-commit Hook**: Always ensure the custom pre-commit hook is active by running `git config core.hooksPath .githooks`. This hook provides a safety net against logic errors and missing ROCm checks.
- Never commit, push, or open a PR unless asked.
- All CI checks must pass before merge.

## Boundaries

- Do not modify unrelated files or widen scope beyond the request.
- Do not add dependencies without asking.
- Never commit secrets, API keys, or .env files.
- If a command fails, report the failure. Do not guess or present assumptions as confirmed results.
- **SECURITY ENFORCEMENT: Zero-Tolerance for TLS/SSL Bypasses**: You are strictly prohibited from bypassing, disabling, or ignoring TLS/SSL certificate validation. You must never use arguments such as `validate_certs: no`, `--insecure` / `-k`, `verify=False`, `NODE_TLS_REJECT_UNAUTHORIZED=0`. If a TLS handshake fails, you must diagnose and fix the underlying cryptographic trust infrastructure.
  - Certificate Requirements: When troubleshooting mesh or cluster SSL errors, verify that the Root CA has the correct `basicConstraints` (`CA:TRUE`) and `keyUsage`, ensure Subject Alternative Names (SANs) include the correct mesh IPs (e.g., Tailscale `100.x.y.z`) and DNS names, and verify the CA is correctly appended to the target system's trust store.
- **Explicit Anti-Patterns to Avoid**:
  - Never edit generated files, compiled bundles (`dist/`, `build/`), or runtime database files directly. Always trace to original source files.
  - Never execute GUI tests, browser automation, or plotting libraries without explicit headless configurations (`MPLBACKEND=Agg`, headless browser flags).
  - Never write non-defensive GPU/CUDA code assuming host GPU presence. Always implement CPU fallback mechanisms.
  - Never copy `.venv`, `node_modules`, or uncommitted temporary build files across node targets. Use explicit rsync exclusion rules.
- **Handling Failures**: If a tool fails (e.g., command not found, permission denied), DO NOT rewrite the tool from scratch. DO NOT try to bypass the sandbox or security controls. DO read the error message carefully and fix the underlying issue.
- **Tool Usage & Queryable Interfaces**:
  - `shell` (Persistent Tmux Session): Use this for navigating directories, running scripts, and executing git commands. **Warning:** Do not wait synchronously for a long-running process (like a server) that will never finish. To run a process in the background, append `&` and redirect output to a file (e.g., `npm start > app.log 2>&1 &`). Use `tail -n 50 app.log` to check the status. Commands have a default timeout (usually 30s). If a command times out, it means you likely ran a blocking process without `&`.
  - `autoresearch` (Iterative Loop): Provide a `target_file`, a `test_command`, and `program_instructions`. The tool will automatically run the loop and commit/revert based on the `exit_code`.
  - `code_runner` (Sandbox): Execute snippets of Python in an isolated container.
  - `rag` (Knowledge Retrieval): Ask specific questions about the project architecture, design decisions, or existing APIs.
- **Five Principles of Agent Skills**:
  1. Process over prose: Workflows are actionable; essays are not. Use defined sequences of steps with checkpoints.
  2. Anti-rationalization tables: Anticipate and rebut excuses for skipping workflows.
  3. Verification is non-negotiable: Every task must terminate with concrete evidence (passing tests, clean build output, etc.) rather than "seems right".
  4. Progressive disclosure: Only load the skills and context relevant to the current phase of the task.
  5. Scope discipline: Touch only what you are asked to touch. Avoid refactoring adjacent systems or unrelated code without explicit instruction.
- **Agent Cheatcodes & Trigger Keywords**:
  - `"Use deep planning mode"`: Forces explicit requirement verification, dependency tracing, architectural analysis, and risk audits using `request_user_input` before creating or executing a plan.
  - `"Add tests in pytest / jest"`: Prioritizes dedicated automated test coverage.
  - `"Run pre-commit checks"`: Audits code quality before submission (runs `scripts/agent_preflight.sh`).
  - `"Create an AGENTS.md guide for this repo"`: Self-documents repository patterns (generates or updates local `AGENTS.md`).
