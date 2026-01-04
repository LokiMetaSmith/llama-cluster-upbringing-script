# Agent Memories

Last updated: 2025-01-01

This file serves as the canonical source of "long-term memory" for the agent. It contains architectural decisions, known gotchas, best practices, and recurring patterns found in the project.

## Ansible Patterns & Best Practices

* **Syntax & Formatting:**
  * Do not start task files with `---` (violates `.yamllint`).
  * Quote task names that contain colons.
  * Use Fully Qualified Collection Names (FQCN) like `ansible.builtin.file`.
  * `loop` keyword must be at the same indentation level as task attributes.
  * Avoid commented-out lines mixing "k=v" shorthand with YAML to prevent parser confusion.
  * Match `vars` block names to Jinja2 template variable names.

* **Variables & Conditionals:**
  * **Check Mode:** `ansible.builtin.uri` does not support check mode. Tasks managing system services/files should use `when: not ansible_check_mode` if the files aren't actually written in check mode.
  * **Conditionals:** Use `is defined` for optional variables. For `slurp`, check `'content' in registered_var`, not just `is defined`.
  * **Rescue Blocks:** Tasks in `rescue` blocks performing intermediate steps should use `ignore_errors: yes` to prevent premature failure.
  * **Undefined Vars:** Provide default values for variables dependent on inventory groups (e.g., `groups['workers']`) to prevent errors in partial inventories.

* **Modules:**
  * **URI:** To flatten a list of dictionaries from a looped `uri` result: `... | selectattr('status', 'equalto', 200) | map(attribute='content') | map('from_json') | flatten | items2dict(key_name='name')`.
  * **URI Loop Extraction:** `((... | selectattr('item', 'equalto', 'my_item') | first).content | default('{}')) | from_json`.
  * **Pip:** Use `--no-cache-dir` if tasks hang/timeout.
  * **Unarchive:** Ensure destination directory exists (`file` task) or force `check_mode: false` on the directory creation if `unarchive` is run in check mode. Use `creates` for idempotency.
  * **Docker:** Use `ansible.builtin.command` for `docker build` (with `force_source: true` semantics) to avoid python dependency issues with `community.docker` in this env.
  * **Git:** Roles compiling from source should compare remote hashes vs local version files for idempotency.
  * **Get URL:** Set a long `timeout` for large files.

* **Handlers:**
  * Use `listen: "Handler Name"` to group tasks.
  * Refactoring handlers: Preserve the `name` or `listen` string.
  * Service Restarts: Restart handlers should poll the service API until ready if a race condition is possible.
  * Systemd: Use a dedicated `daemon-reload` handler notified by file changes instead of `daemon_reload: yes` on every start task.

## Nomad & Consul Configuration

* **Networking:**
  * **Dual Network:** `advertise_ip` (DHCP) for management/UI, `cluster_ip` (Static 10.0.0.x) for internal cluster gossip/RPC.
  * **Host Mode:** `network { mode = "host" }` requires `address_mode = "host"` in health checks.
    * Remove `ports` list in Docker `config` (rely on `network` stanza).
    * Use `nc -z 127.0.0.1 <port>` for internal script checks (e.g., MQTT) to avoid routing issues with the advertised IP.
    * Use `${NOMAD_PORT_<label>}` env vars in `raw_exec` scripts.
  * **Consul Gossip:** `retry_join` must use `cluster_ip` (e.g., `{{ hostvars[...]['cluster_ip'] }}`).

* **Job Specifications (HCL):**
  * **Syntax:** Keys in `env` blocks must be unquoted (`KEY = "VAL"`).
  * **Drivers:** `exec` and `raw_exec` must be explicitly enabled in client config (v1.7.5+).
  * **Volumes:** For `raw_exec`/`exec`, define `volume` in `group` block, not `task`. Host volume paths are relative to client `data_dir`.
  * **Devices:** USB selection requires `constraint` with namespaced attribute (e.g., `usb.class_id`).
  * **Templates:** Use `template` stanza to inject secrets. Render Jinja2 templates to static files on host, then run `nomad job run` on the file.
  * **Docker Images:** For locally built images (no registry), use plain tag (e.g., `my-image:latest`) and `force_pull = false`. Do *not* prefix with `localhost/`.

* **Service Discovery & Health:**
  * Nomad HTTP checks require 2xx. Application must return non-2xx (e.g., 503) if internal state (MQTT connection, model load) is bad.
  * Add `check_restart` stanza to restart unhealthy tasks (Nomad only restarts on exit by default).
  * Services must be registered *after* Consul is ready. Playbooks should run `expert-main` job and wait for `expert-api-main` service.

* **Consul:**
  * ACLs: Include `X-Consul-Token` header.
  * KV: Central source of truth for runtime config.
  * Cleanup: When wiping Consul data, ensure process is stopped and port 8500 closed.
  * Stale Services: Use `scripts/prune_consul_services.py` if "All service checks failing" persists for old Node IDs.

## Development Workflow & Testing

* **Testing:**
  * **Unit Tests:** Path: `tests/unit/`. Invocation: `python -m unittest tests.unit.<module>`.
  * **Mocking:**
    * Mock subprocesses, hardware libs (`pyaudio`, `faster_whisper`, `playwright`).
    * Use `AsyncMock` for async functions (must be awaitable).
    * `pytest-asyncio` required for async tests.
    * `pytest-mock` required for `mocker` fixture.
  * **Tool Tests:** Insert tool directory into `sys.path` to run tool tests individually.
  * **Integration:** Requires running `pipecat` and `consul`.
  * **Scripts:** `run_tests.sh` (flags: `--unit`, `--integration`, `--e2e`, `--all`).

* **Linting:**
  * `scripts/lint.sh` runs `yamllint`, `ansible-lint`, `markdownlint-cli`, `djlint`.
  * Markdown: Use asterisks `*` for lists, blank lines around headers (MD022/032).
  * Ansible Lint: Requires role name prefix for variables.

* **Debugging:**
  * `bootstrap.sh`: Accepts `--run-local` (sets `raw_exec`), `--debug` (saves log), `--external-model-server`.
  * `debug_world_model.sh`: Builds image, checks MQTT/Mosquitto locally.
  * **Ansible:** Check existence of files (e.g., with `ls`) even if tools say missing (delete/recreate to fix). Use `jq` to parse JSON logs.
  * **Nomad:** Use `nomad job status -json`. `nomad alloc logs`. Sort allocations by `CreateTime` to find recent failures.

## Project Architecture & Components

* **Core Components:**
  * **Pipecat App:** Uvicorn server (`WEB_PORT`). `TwinService` agent logic.
  * **Tool Server:** MCP server (`ansible/roles/tool_server/app.py`). Docker build copies `tools/` library.
  * **World Model:** Centralized state via MQTT and Consul.
  * **Agents:** Defined by prompts (`ansible/roles/pipecatapp/files/prompts/`). "Router" agent in `app.py`.
  * **Experts:** Defined in `group_vars/models.yaml`. Deployed as `expert` (orchestrator) and `llamacpp-rpc` (workers).

* **Environment:**
  * **Paths:** App venv: `/opt/pipecatapp/venv`. Nomad data: `/opt/nomad`.
  * **Dependencies:** Runtime: `ansible/roles/python_deps/files/requirements.txt`. Dev: `requirements-dev.txt`.
  * **System:** `rsync` required for playbooks. `cython` before `av`. `libgl` for `open3d`.

## Troubleshooting & Gotchas

* **Filesystem:**
  * `replace_with_git_merge_diff` may fail on context match -> use `overwrite_file_with_block`.
  * Known 0-byte corrupted models: `en_US-lessac-medium.onnx`, `chat.prompt.bin`.
* **Specific Errors:**
  * `AnsibleUnicode` attribute error -> Data structure mismatch (list of strings vs objects).
  * `Waiting for cache lock` -> apt is busy.
  * Docker connection refused on `localhost/image` -> Image missing locally, Docker trying registry.
* **Refactoring:**
  * Update all callsites when changing method signatures.
  * When moving from file-based to DB persistence (e.g., FAISS), ensure order is preserved or explicitly tracked.

## Workflow

* **Bootstrap:** `bootstrap.sh` handles environment setup, arguments as extra-vars.
* **Promotion:** `promote_controller.yaml` for node promotion.
* **Remote:** Uses `mosh`, `tmux`.
* **Plan:** Always verify work. Edit source, not artifacts. Diagnose before changing environment.
