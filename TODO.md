# TODO

This document outlines the major refactoring, feature enhancement, and maintenance tasks for the project.

**Status Update:** The critical refactoring work outlined in Phase 1 is complete. The core deployment process is now significantly more stable and idempotent. The next priorities focus on containerizing the application and centralizing configuration.

-----

# Completed Tasks

---
## Phase 1: Solidify Core Deployment & Service Management

**Goal:** Eliminate the race conditions and conflicting entry points that have caused the cascading failures. Make the system's state fully managed by Ansible in a declarative way.

- [x] **Create `heal_cluster.yaml`:**
    - A new playbook `heal_cluster.yaml` was created to ensure core services are running.

- [x] **Make `llama_cpp` and `bootstrap_agent` Roles Idempotent:**
    - The `nomad job run` task for `llamacpp-rpc` was made idempotent.
    - The compilation tasks in the `llama_cpp` role are skipped if the binaries already exist.

- [x] **Refactor the Main Playbook (`playbook.yaml`):**
    - The role execution order was corrected, and health checks are now in place before the `pipecatapp` is deployed.

- [x] **Remove Conflicting Startup Logic:**
    - The conflicting `systemd` service for `pipecatapp` was removed.

- [x] **State Export/Import**: Allowing tasks to be saved and resumed.
- [x] **Interactive approval of actions**: For enhanced safety and user control.
- [x] **Enhanced Debugging Modes**: For better transparency.
- [x] **WebBrowserTool**: For browsing the web.

-----

# Next Priorities

---

## 1. Pre-build a Docker Image for `pipecatapp`

**Goal:** Decouple the application build process from the deployment process. This is the most effective way to eliminate dependency and environment-related errors.

- [ ] **Create a comprehensive `Dockerfile`:** This file will be the blueprint for the `pipecatapp` image. It should:
  1. Start from a base Python image (e.g., `python:3.12-slim`).
  2. Install all necessary system-level dependencies (`build-essential`, `portaudio19-dev`, etc.) using `apt-get`.
  3. Copy the `requirements.txt` file and run `pip install` to create a self-contained Python environment.
  4. Copy the entire application directory (`app.py`, `tools/`, `prompts/`, etc.) into the image.
  5. Set the `CMD` to run the `start_pipecat.sh` script.
- [ ] **Add a build stage to `bootstrap.sh`:** Before running `ansible-playbook`, the bootstrap script should build the Docker image locally (e.g., `docker build -t pipecat-app:latest .`).
- [ ] **Refactor the `pipecatapp.nomad` job:** Change the task driver from `raw_exec` to `docker`. The configuration will become much simpler, just needing to specify the image name (`pipecat-app:latest`).
- [ ] **Update the Ansible Role:** The `pipecatapp` Ansible role will be simplified. It will no longer need to install Python dependencies or copy application files; its main job will be to deploy the Nomad job file.
- [ ] **Add a flag to `bootstrap.sh`:** Add a `--run-local` or similar flag to the bootstrap script to allow switching between the new Docker-based deployment and the old `raw_exec` method for debugging purposes.

## 2. Centralize All Configuration

**Goal:** Create a single source of truth for all configuration variables to simplify management and reduce the risk of inconsistencies.

- [ ] **Migrate hardcoded variables to `group_vars`:** Search the entire codebase for hardcoded values (e.g., paths, usernames, ports, service names) and replace them with Ansible variables defined in `group_vars/all.yaml`.
- [ ] **Convert all configuration files to templates:** Any file that contains a variable should be a Jinja2 template (`.j2`). This includes all Nomad job files (`*.nomad`), the `start_pipecat.sh` script, and systemd service files.
- [ ] **Establish a clear variable hierarchy:** Use `group_vars/all.yaml` for system-wide defaults and consider `host_vars/<hostname>.yaml` for machine-specific overrides.

## 3. High-Priority Feature: Create OpenAI-Compatible API Gateway

**Goal:** Expose the cluster's Mixture of Experts (MoE) routing capabilities to external applications through a standard, OpenAI-compatible REST API. This will transform the cluster from a standalone agent into a private, powerful AI cloud.

-   [ ] **Create a New "MoE Gateway" Service:**
    -   Develop a lightweight FastAPI application that will run as a new, dedicated Nomad job.
    -   This service's sole responsibility will be to act as a secure entry point to the cluster.
-   [ ] **Implement an OpenAI-Compatible Endpoint:**
    -   The gateway must expose a `/v1/chat/completions` endpoint that mirrors the official OpenAI API specification.
    -   It should handle API key authentication for external clients.
-   [ ] **Integrate with the `pipecat` Pipeline:**
    -   When the gateway receives a request, it will transform the payload into a text message and inject this message into the `pipecatapp`'s existing `text_message_queue`.
-   [ ] **Handle the Response Path:**
    -   A mechanism needs to be created to capture the final text response from `pipecatapp` and route it back to the originating API call in the gateway service.

## 4. Documentation and Cleanup

**Goal:** Finalize the project by cleaning up obsolete files and creating clear documentation for the new features.

- [ ] **Remove Obsolete Scripts:**
    - Delete the entire `debian_service/` directory and its contents.
    - Review the `initial-setup/` scripts and migrate any remaining essential logic into the main Ansible roles, then remove the scripts.
- [ ] **Create API Documentation:**
    - Create a new file, `API_USAGE.md`, in the root directory explaining how to use the new OpenAI-compatible endpoint.

-----

# Future Enhancements and Backlog

## Testing and Usability

- [ ] **Bolster Automated Testing:**
    - Implement Ansible Molecule tests for critical roles.
    - Expand end-to-end tests to cover more critical paths.
    - Increase unit test coverage for Python tools.
- [ ] **Improve Web UI and User Experience:**
    - Replace the placeholder ASCII art with a more expressive animated character or graphic.
    - Add a "Clear Terminal" button to the UI.
    - Improve the status display to be more readable than a JSON dump.

## System Enhancements

- [ ] **Implement Graceful LLM Failover:**
  - Enhance the `prima-expert.nomad` job to fall back to a lightweight model if larger models fail to load.
- [ ] **Re-evaluate Consul Connect Service Mesh:**
  - Once the core system is stable, attempt to re-enable `sidecar_service` in the Nomad job files.
- [ ] **Add Pre-flight System Health Checks:**
  - Create a new Ansible role to perform checks for disk space, network connectivity, etc., before a playbook run.
- [ ] **Investigate Advanced Power Management:**
  - Research and prototype using Wake-on-LAN for a more advanced power management system.
- [ ] **Expand the Model Collection:**
  - Systematically test and add the remaining LiquidAI nano models to `group_vars/models.yaml`.
- [ ] **Security Hardening:**
  - Remove passwordless sudo and ensure services run as non-root users.
- [ ] **Monitoring and Observability:**
  - Deploy a monitoring stack like Prometheus and Grafana.

## For Future Review

- [ ] Review `llama.cpp` optimization guide for server performance tuning: <https://blog.steelph0enix.dev/posts/llama-cpp-guide/#llamacpp-server-settings>
- [ ] Consolidate all AI models (LLM, Whisper, Vision) into a single, unified directory to avoid duplication.
- [ ] Add the remaining LiquidAI nano models from the collection: <https://huggingface.co/collections/LiquidAI/liquid-nanos-68b98d898414dd94d4d5f99a>