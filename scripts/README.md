# `scripts/` Directory Overview

This directory contains various utility scripts for managing the lifecycle, testing, debugging, and quality assurance of the `pipecatapp` ecosystem.

## Table of Contents

- [1. Core Lifecycle & Infrastructure](#1-core-lifecycle--infrastructure)
- [2. Testing & Verification](#2-testing--verification)
- [3. Agent & Workflow (Jules)](#3-agent--workflow-jules)
- [4. Debugging & Diagnostics](#4-debugging--diagnostics)
- [5. Linting & Code Quality](#5-linting--code-quality)

---

## 1. Core Lifecycle & Infrastructure

These scripts manage the setup, teardown, and maintenance of the environment.

### `cleanup.sh`

**Usage:** `sudo ./scripts/cleanup.sh`
Aggressively cleans up system resources to free disk space. Target areas include:

- Docker (prunes system, build cache, and containers).
- Apt cache (autoremove).
- Playwright browsers (optional).
- Snap revisions (removes old disabled snaps).
- Temporary bootstrap artifacts in `/tmp`.
- Large system logs (`/var/log/syslog`, `journalctl`).

### `uninstall.sh`

**Usage:** `./scripts/uninstall.sh`
Completely removes the application and its infrastructure components. It stops services, cleans up directories, and removes configuration files.

### `provisioning.py`

**Usage:** *Internal (Called by `bootstrap.sh`)*
The Python backend for the main `bootstrap.sh` script. It handles complex logic for provisioning the environment, running Ansible playbooks, and managing dependencies. It uses `argparse` to parse arguments passed from the bootstrap wrapper.

### `start_services.sh` (⚠️ DEPRECATED)

**Usage:** `./scripts/start_services.sh`
Legacy script for manually starting services via `nomad job run`.
**Recommendation:** Use Ansible tags (e.g., `ansible-playbook playbook.yaml --tags "app,ai-experts"`) for reliable service deployment.

### `heal_cluster.sh`

**Usage:** `./scripts/heal_cluster.sh [--user <user>]`
Wrapper for the `playbooks/heal_cluster.yaml` Ansible playbook. It ensures that core infrastructure components (like `llamacpp-rpc` and `pipecat-app`) are running on the primary controller. Use this if services appear to be down or missing.

### `fix_verification_failures.sh`

**Usage:** `./scripts/fix_verification_failures.sh`
A remediation script that attempts to fix common environment issues reported by verification tools. It handles:

- Installing/Fixing `llxprt-code` (global npm package).
- Cloning/Building `Claude_Clone`.
- Restoring `moe_gateway/gateway.py`.
- Restarting the `power-agent` service.

---

## 2. Testing & Verification

Scripts to ensure the system is correct and functional.

### `run_tests.sh`

**Usage:** `./scripts/run_tests.sh [--unit|--integration|--e2e|--all]`
A unified test runner wrapper.

- `--unit`: Runs unit tests in `tests/unit/`.
- `--integration`: Runs integration tests in `tests/integration/`.
- `--e2e`: Runs end-to-end tests in `tests/e2e/`.
- `--all`: Runs all test suites sequentially.
Generates JUnit XML reports (`report_*.xml`) in the root directory.

### `check_all_playbooks.sh`

**Usage:** `./scripts/check_all_playbooks.sh [--log]`
recursively finds all Ansible playbooks (files ending in `.yaml` or `.yml` containing `- hosts:`) and runs `ansible-playbook --check` on them. This validates syntax and variable references without applying changes.

- `--log`: Saves output to `playbook_check.log`.

### `test_playbooks_dry_run.sh` / `test_playbooks_live_run.sh`

Helpers to run specific playbooks in dry-run (check) or live mode. Useful for quick validation during development.

### `check_deps.py`

**Usage:** `python3 scripts/check_deps.py`
Verifies Python dependencies by attempting a dry-run install against a temporary requirements list. Generates a `report.json` with resolution details.

---

## 3. Agent & Workflow (Jules)

Tools related to the "Agentic Workflow" and AI capabilities.

### `agentic_workflow.sh`

**Usage:** `./scripts/agentic_workflow.sh [options]`
The main entry point for managing the "Jules" agent workflow.

- `--setup`: Installs GitHub Actions workflows and local hooks.
- `--ignite`: Creates the first issue to trigger the agent loop.
- `--status`: Checks the current status of the agent queue and hardware runner.
- `--uninstall`: Removes all workflow files and labels.

### `healer.py` (🧪 EXPERIMENTAL)

**Usage:** `python3 scripts/healer.py --local-mode --log <log> --target <file>`
A self-healing agent prototype. It can:

1. Read a crash log and source code.
2. Generate a reproduction test case using an LLM.
3. Attempt to fix the code to pass the test.

### `run_quibbler.sh` (🧪 EXPERIMENTAL)

**Usage:** `./scripts/run_quibbler.sh <instructions> <plan>`
Wrapper for the `quibbler` tool to perform automated code review on agent plans.

---

## 4. Debugging & Diagnostics

Tools to help troubleshoot issues in the running cluster.

### `analyze_nomad_allocs.py`

**Usage:** `python3 scripts/analyze_nomad_allocs.py <json_dump>`
Parses a JSON dump of Nomad allocations (e.g., from `nomad alloc status -json`) and provides a human-readable summary of failures, task states, and recent events.

### `debug_expert.sh`

**Usage:** `./scripts/debug_expert.sh`
Deploys the "Expert" service in debug mode (using `ansible/jobs/expert-debug.nomad`). Useful for interactive troubleshooting or attaching debuggers.

### `profile_resources.sh` / `memory_audit.py`

Tools for profiling system resource usage (CPU, Memory) of the running services.

---

## 5. Linting & Code Quality

Scripts to enforce code style and detect regressions.

### `lint.sh`

**Usage:** `npm run lint` or `./scripts/lint.sh`
Runs all project linters:

- `yamllint` for YAML files.
- `markdownlint` for Markdown documentation.
- `nomad-fmt` (if available) for Nomad HCL.
- `djlint` for Jinja2 templates.
Reads exclusions from `scripts/lint_exclude.txt`.

### `fix_markdown.sh` / `fix_yaml.sh`

Auto-fix scripts that attempt to automatically resolve linting errors for Markdown and YAML files respectively.

### `ansible_diff.sh`

**Usage:** `./scripts/ansible_diff.sh [--update-baseline]`
Detects unintended changes in Ansible playbooks by comparing a "dry run" against a known "baseline".

#### How it Works

1. **Baseline Creation:** The first run (or with `--update-baseline`) saves the output of a check-mode run to `ansible_run.baseline.log`.
2. **Comparison:** Subsequent runs compare the current check-mode output against the baseline.
3. **Reporting:** Differences are logged to `ansible_diff.log`.

This is automatically run in CI via `ci_ansible_check.sh` to prevent regressions.
