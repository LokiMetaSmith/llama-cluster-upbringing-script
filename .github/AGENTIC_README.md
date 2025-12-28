# Agentic Validation Loop Architecture

This repository uses a "Validation Loop" to bridge AI agents with local workstation hardware via isolated containers.

## The Loop
- **Implementation:** Jules (Agent) pushes code and a **successor task** in `ISSUES/`.
- **Remote Verification:** `remote-verify.yml` triggers on the **Self-Hosted Runner**.
- **Execution:** Hardware runs `./bootstrap.sh --container --debug`, generating native `playbook_output.log`.
- **Log Evaluation:** `jules-queue.yml` inspects logs for Ansible failures (`failed=1` or `unreachable=1`).
- **Continuous Motion:** `auto-merge.yml` blocks merges unless a new task definition is detected in the PR diff.
