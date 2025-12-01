# Report on YAML Files in Root Directory

## Overview

This report analyzes the `*.yaml` files located in the root directory of the repository. It describes their purpose, identifies dependencies, and provides recommendations on whether they should remain in the root or be relocated.

## Analysis

### Core Infrastructure

| File | Purpose | Dependencies / Usage | Recommendation |
| :--- | :--- | :--- | :--- |
| `playbook.yaml` | The main entry point for the Ansible automation. It imports playbooks from the `playbooks/` directory to orchestrate the entire deployment. | Used by `bootstrap.sh`, `check_all_playbooks.sh`, and general Ansible workflows. | **Keep.** Standard convention for Ansible projects. |
| `inventory.yaml` | The Ansible inventory file defining hosts and groups (worker/controller nodes). | Used by all Ansible operations. Dynamically updated by `promote_controller.yaml`. | **Keep.** Standard convention. |

### Operational & Deployment Tools

| File | Purpose | Dependencies / Usage | Recommendation |
| :--- | :--- | :--- | :--- |
| `deploy_app.yaml` | Standalone playbook to deploy the `pipecatapp` role and restart services. | Referenced in `check_all_playbooks.sh`. | **Move to `playbooks/ops/`**. Update `check_all_playbooks.sh` reference. |
| `deploy_expert.yaml` | Renders and runs the `expert-main` Nomad job. | Referenced in `README.md` as a manual tool for users. | **Keep (or Move with Doc Update).** Moving it requires updating documentation that directs users to run it from root. |
| `redeploy_pipecat.yaml` | Similar to `deploy_app.yaml`, likely an alternative or older version. | No active references found in scripts. | **Remove or Merge** with `deploy_app.yaml`. |
| `deploy_prompt_evolution.yaml` | Deploys the `evolve-prompt.nomad` job. | No active references found. | **Move to `playbooks/ops/`**. |
| `promote_controller.yaml` | Automates promoting a worker node to a controller (updates inventory, reconfigures services). | Referenced in `check_all_playbooks.sh`. Note: A simpler version exists at `playbooks/promote_to_controller.yaml`. | **Move to `playbooks/ops/`**. The root version handles inventory updates and is more robust than the one in `playbooks/`. |
| `run_config_manager.yaml` | Runs the `config_manager` role. | No active references. | **Move to `playbooks/roles_wrappers/`** or remove. |
| `run_consul.yaml` | Runs the `consul` role. | No active references. | **Move to `playbooks/roles_wrappers/`** or remove. |

### Self-Healing & Diagnostics (Supervisor Dependencies)

These files are critical for the `supervisor.py` script which runs in the root.

| File | Purpose | Dependencies / Usage | Recommendation |
| :--- | :--- | :--- | :--- |
| `health_check.yaml` | Checks the health of Nomad jobs. | **Required by `supervisor.py`**. The script calls it by filename assuming it is in the CWD. | **Keep** (unless `supervisor.py` is refactored). |
| `diagnose_failure.yaml` | Diagnoses failed jobs by fetching logs/allocations. | **Required by `supervisor.py`**. | **Keep** (unless `supervisor.py` is refactored). |
| `heal_job.yaml` | Restarts or scales jobs based on diagnostic output. | **Required by `supervisor.py`**. Also referenced in `ARCHITECTURE.md`, `MEMORIES.md`, `tests/unit/test_supervisor.py`. | **Keep** (unless `supervisor.py` is refactored). |

### Diagnostics (Stand-alone)

| File | Purpose | Dependencies / Usage | Recommendation |
| :--- | :--- | :--- | :--- |
| `diagnose_and_log_home_assistant.yaml` | Detailed HA diagnostics logging to file. | Imported by `run_ha_diag.yaml`. | **Move to `playbooks/diagnostics/`**. |
| `diagnose_home_assistant.yaml` | HA diagnostics logging to stdout. | No active references. | **Move to `playbooks/diagnostics/`**. |
| `run_ha_diag.yaml` | Wrapper for HA diagnostics. | No active references. | **Move to `playbooks/diagnostics/`**. |
| `run_health_check.yaml` | Deploys a `health-check.nomad` job (different from `health_check.yaml` which queries API). | No active references. | **Move to `playbooks/diagnostics/`**. |

### Development & Maintenance

| File | Purpose | Dependencies / Usage | Recommendation |
| :--- | :--- | :--- | :--- |
| `benchmark_single_model.yaml` | Runs benchmarks for a model. | **Hard Dependency**: Included by `ansible/roles/llama_cpp/tasks/main.yaml` via relative path `../../../benchmark_single_model.yaml`. | **Keep**. Moving it breaks the `llama_cpp` role unless the include path is updated. |
| `debug_template.yaml` | Renders Nomad templates for debugging. | No active references. | **Move to `playbooks/dev/`**. |
| `fix_cluster.yaml` | Disaster recovery playbook (re-selects controllers, wipes data). | No active references. | **Move to `playbooks/ops/`**. |
| `heal_cluster.yaml` | Ensures core services are running. | No active references. | **Move to `playbooks/ops/`**. |
| `pxe_setup.yaml` | Sets up PXE server. | No active references. | **Move to `playbooks/infra/`**. |
| `status-check.yaml` | Checks host status and WoL. | No active references. | **Move to `playbooks/infra/`**. |
| `wake.yaml` | Sends WoL to all hosts. | No active references. | **Move to `playbooks/infra/`**. |

## Summary

*   **Essential in Root**: `playbook.yaml`, `inventory.yaml`.
*   **Locked by Code Dependencies**: `health_check.yaml`, `diagnose_failure.yaml`, `heal_job.yaml` (supervisor.py), `benchmark_single_model.yaml` (llama_cpp role).
*   **Locked by Documentation**: `deploy_expert.yaml` (README.md).
*   **Candidates for Move**: All other files (approx. 13 files) can be moved to subdirectories within `playbooks/` to declutter the root, provided that `check_all_playbooks.sh` and any manual documentation are updated.
