# AGENTS.md

Welcome, Agent. This file contains the mandatory operating procedures and playbooks for working within this repository.

As per the philosophy of "Zero-Degree-of-Freedom LLM Coding using Executable Oracles," you must strictly adhere to the following rules, tools, and workflows. Do not deviate, shortcut, or attempt to bypass these instructions.

## 1. Executable Oracles

You are provided with several executable oracles to verify your work. You must use these tools to test your code before considering a task complete.

* **Tests:** Run unit and integration tests using `pytest` (Python) or `npm run test` (JavaScript/TypeScript).
  * *Oracle Rule:* A failing test is a showstopper. You must fix the code until the test passes.
* **Linters:** Run `npm run lint` or `scripts/lint.sh` to check for formatting and syntax errors.
  * *Oracle Rule:* All code must pass linting without errors or warnings.
* **Code Runner Sandbox:** Use the `code_runner` tool to execute Python code in an isolated Docker/Nomad container.
  * *Oracle Rule:* Validate your logic in the sandbox before modifying host files.
* **Autoresearch Iteration:** Use the `autoresearch` tool for automated hypothesize-edit-evaluate loops.
  * *Oracle Rule:* The tool will evaluate your code against a test command (e.g., `pytest`). A non-zero exit code means failure, and the change will be reverted.

## 2. Mandatory Playbooks

When modifying or creating code, you must follow this linear sequence of steps. **These steps are mandatory; deviations are not allowed.**

1. **Understand the Goal:** Read the issue description, `README.md`, and use the `rag` tool to search the knowledge base for relevant context.
2. **Explore the Codebase:** Use `project_mapper` or `shell` (with `find`/`grep`) to locate the relevant source files. **Do not edit build artifacts** (e.g., `/dist`, `/build`). Trace back to the source.
3. **Hypothesize & Plan:** Formulate a plan and use the `set_plan` tool. If the task is complex, write a failing test first.
4. **Edit Source:** Modify the source code using the `file_editor` or `shell` tools.
5. **Run Executable Oracles:** Immediately run the relevant tests (`pytest`, `npm run test`) and linters (`npm run lint`).
6. **Analyze & Iterate:** If an oracle fails, analyze the error output (the concise counterexample or stack trace). Do not ignore the error. Fix the code and re-run the oracle.
7. **Finalize:** Only mark the step complete when all oracles pass.

## 3. Tool Usage and "Queryable" Interfaces

Your tools are designed to have clear, queryable interfaces.

* **`shell` (Persistent Tmux Session):**
  * *Usage:* Use this for navigating directories, running scripts, and executing git commands.
  * *Long-Running Processes:* **Warning:** Do not wait synchronously for a long-running process (like a server) that will never finish. To run a process in the background, append `&` and redirect output to a file (e.g., `npm start > app.log 2>&1 &`). Use `tail -n 50 app.log` to check the status.
  * *Timeouts:* Commands have a default timeout (usually 30s). If a command times out, it means you likely ran a blocking process without `&`.
* **`autoresearch` (Iterative Loop):**
  * *Usage:* Provide a `target_file`, a `test_command`, and `program_instructions`. The tool will automatically run the loop and commit/revert based on the `exit_code`.
  * *Robustness:* You cannot game this metric. The evaluation happens in an isolated sandbox. You must write code that genuinely passes the test.
* **`code_runner` (Sandbox):**
  * *Usage:* Execute snippets of Python.
  * *Dependencies:* If you need external libraries, specify them in the `libraries` argument. The tool will check dependencies against a vulnerability scanner (OSV database).
* **`rag` (Knowledge Retrieval):**
  * *Usage:* Ask specific questions about the project architecture, design decisions, or existing APIs. The tool embeds project documents into a FAISS index.

## 4. Uncontrolled Degrees of Freedom

Be aware that executable oracles cannot easily measure everything. You must exercise human-like judgment for:

* **Software Architecture:** Ensure your code is modular, readable, and follows the existing design patterns. Do not paint yourself into a corner with poor architecture.
* **Duplication:** Do not write nearly-duplicate functions or excessive defensive code. Abstract properly.
* **Dead Code:** Remove code that becomes dead or unreachable as you work. Do not leave it behind.

## 5. Handling Failures

LLMs are industrious but can be lazy. If a tool fails (e.g., command not found, permission denied, missing library):

* **DO NOT** rewrite the tool from scratch.
* **DO NOT** try to bypass the sandbox or security controls.
* **DO** read the error message carefully. Install the missing dependency, fix the path, or adjust the configuration. Ask the user for help if you are truly stuck.

## 6. Updating the Local Cluster Infrastructure

When updating the `bootstrap.sh` script (the primary upbringing script that manages and scales the cluster infrastructure), you MUST verify the changes using the local ROCm simulation to avoid recursive crash loops (the "Ouroboros Effect").

* **Mandatory Action:** You must run `act` locally (the local GitHub Action runner) and verify workflows pass before proposing or submitting a merge to the primary branch.
* **Pre-commit Hook:** Always ensure the custom pre-commit hook is active by running `git config core.hooksPath .githooks`. This hook provides a safety net against logic errors and missing ROCm checks.
* If the simulation fails with a 'VGPR Mismatch' or 'KFD Error', or other container crash, roll back the changes and search for recent amdgpu firmware patches or logic errors in the code. Do not bypass these local tests under any circumstances.

## 7. Five Principles of Agent Skills

Lifted from Addy Osmani's Agent Skills, these are the core principles for agent behavior:

1. **Process over prose:** Workflows are actionable; essays are not. Use defined sequences of steps with checkpoints.
2. **Anti-rationalization tables:** Anticipate and rebut excuses for skipping workflows (e.g., "This is too simple to need a test").
3. **Verification is non-negotiable:** Every task must terminate with concrete evidence (passing tests, clean build output, etc.) rather than "seems right".
4. **Progressive disclosure:** Only load the skills and context relevant to the current phase of the task.
5. **Scope discipline:** Touch only what you are asked to touch. Avoid refactoring adjacent systems or unrelated code without explicit instruction.
