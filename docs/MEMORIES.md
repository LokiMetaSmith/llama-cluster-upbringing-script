# Agent Memories

Last updated: 2025-12-31

Agent memories related to the project.

* The correct Python module path for unit tests invoked via `python -m unittest` is `tests.unit.<module_name>`, matching the filesystem structure `tests/unit/`.
* When running E2E tests, the `pipecat` application and its dependencies must be running.
* When an Ansible task using the `slurp` module is skipped due to a `when` condition, the registered variable is still created but will lack the `content` key. Conditional logic should check for the key's existence (e.g., `'content' in my_variable`) rather than just if the variable is defined (`my_variable is defined`) to avoid errors.
* Unit tests that involve subprocess calls should be mocked to ensure they are isolated and do not depend on external services or file systems.
* In Nomad HCL, keys within an `env` block must not be quoted. For example, use `KEY = "value"` instead of `"KEY" = "value"`.
* Agent definition markdown files must strictly format the 'Backing LLM Model' section with a bullet point like `* **Model:** ...` to pass schema validation tests.
* `supervisor.py` depends on `health_check.yaml`, `diagnose_failure.yaml`, and `heal_job.yaml` being present in the root directory.
* When debugging, prioritize identifying the root cause of the initial error message (e.g., "Temporary failure in name resolution") before attempting complex refactoring of seemingly related code.
* The `bootstrap.sh` script accepts a `--run-local` flag, which sets the Ansible extra variable `pipecat_deployment_style=raw_exec` for local debugging.
* In the development environment, if a file is confirmed to exist via `ls` but tools like `read_file` or `replace_with_git_merge_diff` fail with a 'file not found' error, deleting and recreating the file can resolve the issue.
* The `tool_server` build process copies the shared `tools` library from `ansible/roles/pipecatapp/files/tools/` into the build context.
* In Nomad client configurations (v1.7.5+), task drivers like `exec` and `raw_exec` must be explicitly enabled using `plugin` blocks to function.
* Ansible tasks and handlers managing system services (e.g., `systemd`, `service`) should be skipped in check mode (`when: not ansible_check_mode`) if the service configuration files are not actually written.
* The project uses a centralized, data-driven approach for managing LLM 'expert' models. Configurations, including download URLs and filenames, are defined in `group_vars/models.yaml` and the list of active experts is in `group_vars/all.yaml`.
* The `tool_server` role deploys a full Model Context Protocol (MCP) server implementation (migrated from `ansible/roles/pipecatapp/files/tool_server.py`) to `ansible/roles/tool_server/app.py`.
* Always wait for explicit user approval before beginning a multi-step plan, especially one involving code modifications. Do not bundle unrequested changes with requested ones.
* When an Ansible handler restarts a service like Nomad, a race condition can occur if other tasks or handlers try to use the service's API before it is fully initialized. The restart handler should include a task that polls the service's API endpoint until it is ready.
* In Nomad HCL, to select a USB device within a `device` block, a `constraint` sub-block should be used with the `attribute` namespaced by device type (e.g., `usb.class_id`) and the `value` as the decimal class ID.
* The Ansible playbook for `pipecatapp` must explicitly run the `expert-main` Nomad job before waiting for the `expert-api-main` service in Consul, otherwise the playbook will hang.
* The `check_all_playbooks.sh` script performs a dry run (`--check`) on all Ansible playbooks, attempting to dynamically locate the `ansible-playbook` executable and using `local_inventory.ini` if present to target localhost.
* Ansible roles compiling software from git (e.g., `whisper_cpp`) should ensure idempotency by comparing remote commit hashes against a local version file before building.
* The `faster-whisper` STT provider is installed as a Python dependency via the `python_deps` role and is not managed by a dedicated Ansible role.
* The Ansible `debug` module does not accept `mode` or `become` parameters. Incorrectly adding them can cause YAML syntax errors.
* To prevent failures in Ansible `--check` mode when copying generated files, check for the source file's existence using `stat` with `check_mode: false` and condition the `copy` task on the result.
* The `scripts/lint.sh` script requires `yamllint` and `ansible-lint`, installed via pip.
* The project uses two distinct AI agent architectures: a runtime "Mixture of Experts" (MoE) and a development "Ensemble of Agents".
* The `scripts/lint.sh` script (invoked via `npm run lint`) orchestrates linters including `yamllint`, `markdownlint-cli`, `djlint`, and an Ansible-based `nomad fmt` check.
* The `nomad job run` command uses the `-var` flag to pass variables.
* The `bootstrap.sh` script is the primary entry point for running the Ansible playbook, handling environment setup and arguments.
* Mock problematic modules like `pyaudio`, `faster_whisper`, `piper.voice`, and `playwright` when running unit tests in a minimal environment.
* To flatten a JSON list of dictionaries from a looped `ansible.builtin.uri` result, use: `... | selectattr('status', 'equalto', 200) | map(attribute='content') | map('from_json') | flatten | items2dict(key_name='name')`.
* Unit tests in `tests/unit/test_pipecat_app_unit.py` focus on Python application logic, not Ansible template rendering.
* When executing `nomad` commands via Ansible, the `NOMAD_ADDR` environment variable must be set, typically to `http://{{ ansible_default_ipv4.address }}:4646`.
* The project's Python tools (e.g., `mcp_tool.py`, `ansible_tool.py`) are located in `ansible/roles/pipecatapp/files/tools/`.
* Nomad job template `world_model.nomad.j2` should use `{{ advertise_ip }}` for `MQTT_HOST`, `CONSUL_HOST`, and `NOMAD_ADDR` to align with the host's actual IP address (`hostname -I`) used by successful debug scripts.
* When fixing a bug, create a persistent test case that fails before the fix and passes after.
* The repository contains Ansible playbooks for provisioning a cluster infrastructure using services like Consul, Docker, and Nomad.
* The `expert` Nomad job registers its service in Consul as `expert-api-main`.
* The `nomad` role configuration in `group_vars/all.yaml` should define `nomad_version` (e.g., "1.7.7") and omit `nomad_zip_url` to allow the role to dynamically determine the download URL based on the version.
* To avoid YAML parser confusion, remove commented-out lines in Ansible playbooks that mix "k=v" shorthand with standard YAML.
* The `download_models` Ansible role uses `ansible.builtin.stat` to ensure idempotency by checking for existing model files.
* The error `"'ansible.parsing.yaml.objects.AnsibleUnicode object' has no attribute..."` in Ansible usually implies a data structure mismatch, such as filtering a list of strings instead of objects.
* Nomad HCL job files are sensitive to syntax errors.
* The development environment uses `pyenv` and Ansible executables are not in the default system `PATH`.
* Ansible pipelining is disabled in `ansible.cfg` (`pipelining = False`) to avoid privilege escalation issues.
* Runtime Python dependencies are in `ansible/roles/python_deps/files/requirements.txt`; dev dependencies are in `requirements-dev.txt`.
* Ensure volume mounts and configuration paths in Nomad job templates match the directory structure created by Ansible on the host.
* Async functions under test require `AsyncMock` instances to be awaitable.
* The `ShellTool` operates asynchronously using `tmux` sessions; its unit tests require `pytest-asyncio` and `AsyncMock` for `asyncio.create_subprocess_exec`.
* When refactoring an Ansible handler, preserve its `name`. Use a `block` to group actions like post-restart waiting within the existing handler.
* The `mqtt` Ansible role configures `mosquitto.conf` with both `log_dest stdout` and `log_dest stderr` to ensure comprehensive log capture during container startup and health check failures.
* Ansible task files should not begin with `---` as per `.yamllint` configuration.
* The `reflection/reflect.py` script uses live API calls to an LLM to diagnose Nomad job failures.
* The `term.everything` Ansible role requires the `podman` package to build the AppImage.
* When using Nomad's `mode = "host"` networking with the Docker driver, the `ports` list in the Docker `config` stanza should be removed to avoid binding conflicts, relying instead on the `network` stanza.
* Before starting work, enter a deep planning mode to clarify user expectations using `request_user_input` and `message_user`. Only set a plan with `set_plan` after verification.
* The `pipecat-app` application uses a Uvicorn web server, configured via the `WEB_PORT` environment variable.
* The `llama-server` application's `/health` endpoint requires a model to be successfully loaded to return healthy.
* The PXE boot process uses `pxe_os` in `group_vars/all.yaml` to select between Debian and NixOS.
* For `unarchive` tasks in Ansible to succeed in check mode, the destination directory creation task must be forced to run (`check_mode: false`) or the unarchive task must be skipped.
* To deploy a Nomad job via Ansible, render the Jinja2 template to a static file first, then run `nomad job run` on the rendered file.
* User requires comprehensive docstrings for all public code elements following language-specific style guides.
* The `ansible.builtin.uri` module does not support `--check` mode.
* The `bootstrap.sh` script supports an `--external-model-server` flag to skip model downloads/builds.
* When running executables like `ansible-playbook` via `bootstrap.sh`, use the full path to the executable to ensure the correct environment.
* Avoid `eval` in Bash scripts; use arrays to build command arguments safely.
* The `tool_server` role relies on `ansible/roles/tool_server/app.py` as the single source of truth, which is copied into the Docker image via the `Dockerfile`.
* Use `systemctl status nomad` to verify Nomad status if Ansible logs are inconclusive.
* Home Assistant's auth token is stored at `/opt/nomad/volumes/ha-config/.storage/auth_provider.homeassistant`.
* In shell scripts, check if process ID variables are set before using them with `kill` or `wait`.
* Mosquitto 2.0+ configuration in Ansible templates must use the `listener port [address]` syntax (e.g., `listener 1883 0.0.0.0`) instead of the deprecated `bind_address` directive to ensure proper binding on all interfaces in Docker host networking mode.
* Ansible's `--check` mode is unreliable for logic dependent on variable contents. Use targeted real runs with tags instead.
* Expert agents are defined by prompts in `ansible/roles/pipecatapp/files/prompts/`.
* The `world_model_service` Nomad job is configured with `network { mode = "host" }` to align with debug scripts and ensure MQTT connectivity.
* The `tool_server` role Docker image build process is updated to copy the source files (`app.py`, `Dockerfile`, `tools/`, etc.) into a dedicated build directory `/opt/tool_server` before building to ensure a clean build context.
* `AGENTS.md` documents local development setup and testing.
* Provide default values for variables dependent on inventory groups (e.g., `groups['workers']`) to prevent errors in partial inventories.
* The `tool_server` serves as a Model Context Protocol (MCP) server, exposing functionality via the `/run_tool/` endpoint.
* The project uses two Home Assistant tools: `HomeAssistantTool` (structured) and `HA_Tool` (natural language).
* The `pipecatapp` role requires the `/opt/pipecatapp` directory to exist before starting Nomad.
* When `replace_with_git_merge_diff` fails due to context matching issues, `overwrite_file_with_block` is a reliable alternative for ensuring file correctness.
* In Ansible, the `loop` keyword must be at the same indentation level as task attributes.
* `scripts/ansible_diff.sh` compares Ansible playbook `--check` runs against a baseline.
* The `jq` package is installed via the `system_deps` Ansible role.
* When configuring Nomad jobs with `network { mode = "host" }`, avoid setting `mode = "host"` explicitly if also relying on Docker bridge networking defaults; instead, remove the `mode` attribute to allow Nomad to manage port mapping correctly or use `bridge` mode explicitly if port isolation is required.
* `EVALUATOR_GENERATOR.md` is documentation, not an agent definition file.
* Shell scripts are tested using a Python `unittest` file that runs the script in a subprocess with a temporary file system.
* Creating Nomad job files requires `become: yes` to write to `/opt/nomad/jobs`.
* Add `--no-cache-dir` to Ansible `pip` tasks if they hang or time out.
* Jinja2 templates converted to JSON cannot contain comments.
* Use `listen: "Handler Name"` in Ansible handlers to group multiple tasks (e.g., restart service and wait for port) under a single notification name.
* Containers starting as root and dropping privileges (e.g., `eclipse-mosquitto`) need `SETUID` and `SETGID` capabilities in `cap_add`.
* When using ACLs with Consul in Ansible, include the `X-Consul-Token` header.
* Use `regex_findall` instead of `regex_search` in Ansible log entries for easier handling of no-match cases.
* `traffic_monitor.c` requires `<uapi/linux/in.h>` for compilation.
* The `config_manager` role stores the Home Assistant token in Consul at `config/hass/token`.
* User prefers submitting completed work even if unrelated tests fail due to environment issues.
* The `open3d` library requires `libgl1-mesa-glx`, `libgl1-mesa-dev`, and `libglu1-mesa-dev`.
* Use fully qualified collection names (FQCN) in Ansible (e.g., `ansible.builtin.file`).
* `prompt_engineering/evaluation_lib.py` contains common functions for deploying and testing code in Nomad/Consul.
* Use `ansible.builtin.shell` with `jq` to reliably parse JSONL files in Ansible, rather than `map('from_json')`.
* `ansible/roles/pipecatapp/files/app.py` uses a `TwinService` class for agent logic.
* `ansible-playbook --start-at-task` works with task names, not play names.
* The `tool_server` Docker image includes specific dependencies (`pyautogui`, `ansible`, `pipecat-ai[all]`) to support the tools library.
* `prompt_engineering/evolve.py` uses `openevolve` for prompt improvement.
* Nomad service checks should include a `check_restart` stanza to ensure the task is restarted if the application becomes unhealthy (e.g., failing HTTP/TCP checks), as Nomad otherwise only restarts on process exit.
* Command-line arguments for `bootstrap.sh` are passed as `--extra-vars` to `ansible-playbook`.
* The `group_vars/all.yaml` file unconditionally defines `cluster_ip` using the `cluster_subnet_prefix` and `node_id` (e.g., 10.0.0.x) to enforce a stable virtual subnet, avoiding fallback to DHCP addresses.
* `rsync` is a required system dependency for the main Ansible playbook.
* Use `creates` with `ansible.builtin.script` to ensure idempotency.
* `bootstrap.sh --debug` saves full Ansible output to `playbook_output.log`.
* `langchain.text_splitter` is deprecated; use `langchain-text-splitters`.
* `playbook.yaml` explicitly loads `group_vars/models.yaml`.
* Markdown documentation must use asterisks `*` for unordered lists, blank lines around headings and lists (MD022, MD032), and correct table spacing (MD060) to pass linting.
* `scripts/ci_ansible_check.sh` wrappers `ansible_diff.sh` for CI workflows.
* Nomad health checks for the MQTT service should use an internal script check (`nc -z 127.0.0.1 1883`) instead of the default advertised IP (`${NOMAD_IP_mqtt}`) to avoid host networking routing issues.
* `tests/unit/test_home_assistant_template.py` requires `hostvars` to be mocked.
* `requirements-dev.txt` contains redundant entries (e.g., `yaml`) that can break installation.
* The RAG tool (`rag_tool.py`) uses a FAISS vector index.
* The file `docker/pipecatapp/app.py` is a stale or divergent artifact that differs from the source of truth `ansible/roles/pipecatapp/files/app.py`.
* Third-party LLM expert configuration is in `group_vars/external_experts.yaml`.
* Consul KV is the central source of truth for runtime configuration.
* `pytest-mock` is required for tests using the `mocker` fixture.
* `openevolve` evaluates code performance by deploying to Nomad and running integration tests.
* To generate test coverage reports: `python -m pytest --cov=ansible --cov=supervisor --cov-report=term-missing tests/unit/`.
* The `run_tests.sh` script in the root directory executes tests using flags: `--unit`, `--integration`, `--e2e`, and `--all`.
* To detect changes with Ansible check runs, `diff` two separate `--check` output files.
* Use `creates` with `ansible.builtin.unarchive` for idempotency.
* Explicitly set `torch.backends.cuda.matmul.fp32_precision = 'high'` in `app.py` to silence TF32 warnings.
* The `scripts/debug/test_mqtt_connection.py` script diagnoses MQTT connectivity by probing port 1883 on all local interfaces to troubleshoot Nomad health check failures.
* `llama.cpp` `rpc-server` requires `-H HOST` to specify the bind address (e.g., `-H 0.0.0.0`) and `-p PORT` for the port.
* The `nomad_namespace` variable must be defined in `group_vars/all.yaml`.
* The `pipecatapp` role depends on `system_deps`, `nomad`, and `python_deps` roles running first.
* The `heal_job.yaml` playbook performs remedial actions based on `reflection/reflect.py` output.
* `playbooks/common_setup.yaml` now explicitly updates the apt cache when installing `sudo` to handle environments with stale caches.
* Nomad HCL job files are sensitive to syntax errors.
* The `tool_server` Nomad job registers the service as `tool-server-api` to match `llxprt_code` expectations.
* Nomad's `exec` and `raw_exec` drivers must be explicitly enabled in the client config.
* Nomad client configuration is managed by `ansible/roles/nomad/templates/nomad.hcl.client.j2`.
* Include `is defined` checks in Ansible `when` conditionals for optional variables.
* The `nixos_pxe_server` role uses `configuration.nix` to build a netboot environment.
* Transient "Waiting for cache lock" errors in Ansible can happen if `apt` is busy.
* Python applications in this project must explicitly exit (e.g., `os._exit(1)`) if critical background threads (like MQTT listeners) fail, to ensure Nomad restarts the allocation.
* To reliably debug Nomad deployment failures in Ansible, use `jq` to sort allocations by `CreateTime` (e.g., `sort_by(.CreateTime) | reverse | .[0].ID`) to target the most recent attempt.
* Use `select('list')` before `sum` when flattening lists in Ansible to avoid TypeErrors.
* The `download_models` role organizes STT models by provider under `/opt/nomad/models/stt/` based on `group_vars/models.yaml`.
* The `term_everything` role compares commit hashes to ensure idempotent builds.
* `ansible.builtin.uri` is used instead of `community.general.consul_kv` to avoid dependency issues.
* The repository uses a unified `tests/` directory with subdirectories: `unit`, `integration`, `e2e`, `scripts`, and `playbooks`.
* Shell scripts should include a `show_help()` function for usage information.
* The user wants an 'ensemble of agents' workflow.
* Avoid using `daemon_reload: yes` in every `systemd` service start task; instead, use a dedicated handler notified by service file changes to improve idempotency.
* Home Assistant auto-configures MQTT from `MQTT_SERVER`, conflicting with explicit `mqtt:` blocks in `configuration.yaml`.
* Install specific packages directly if `pip install -r requirements-dev.txt` times out.
* Existing 'expert routing' prompts are in `ansible/roles/pipecatapp/files/prompts/`.
* `consul` role default data directory is `/opt/consul`.
* `bootstrap.sh` should check for `nomad` installation before use.
* Use a conditional check instead of `default` when using the Ansible `combine` filter on potentially missing dictionaries.
* Split plays that contain both `roles:` and `tasks:` to ensure handlers load correctly.
* Host directories for Nomad `host_volume` mounts must be created before the service starts.
* `piper-tts` uses `PiperVoice.load()` instead of `from_files`.
* To extract an item from an Ansible loop result: `((... | selectattr('item', 'equalto', 'my_item') | first).content | default('{}')) | from_json`.
* API endpoints are in `ansible/roles/pipecatapp/files/web_server.py`.
* Explicitly set `executable: /bin/bash` for Ansible shell tasks using bash features like `set -o pipefail`.
* The `workflow.runner` module must import the `registry` instance explicitly (`from .nodes.registry import registry`) rather than the module package to avoid `AttributeError`.
* Use retry loops (`until`, `retries`) for Ansible tasks prone to transient network errors.
* When creating model-specific Nomad jobs, loop over full model objects enriched via Jinja2 filters.
* `tests/unit/test_code_runner_tool.py` requires the `docker` python package to be installed to avoid `AttributeError` when mocking `docker.from_env`.
* Agent roles include Problem Scope Framing, Architecture Review, New Task Review, Debug and Analysis, and Code Clean Up.
* The `tests/scripts/run_unit_tests.sh` script (or `run_tests.sh --unit`) runs the unit test suite.
* `prompts/router.txt` defines the Router agent's vision and tool usage.
* Install `community.general` and `ansible.posix` collections using the full pyenv path to `ansible-galaxy`.
* `supervisor.py` is a self-healing loop for system jobs.
* The `debug_world_model.sh` script requires the `world-model-service:latest` Docker image to be manually built from `ansible/roles/world_model_service/files/` before execution.
* Clustered Nomad services should have `count > 1` and configured `update`, `migrate`, and `reschedule` stanzas.
* Unit tests for tools in `ansible/roles/pipecatapp/files/tools/` must insert the tool directory into `sys.path` to support running test files individually.
* Escape inner template delimiters (e.g., `{{ '{{' }} env ... {{ '}}' }}`) in Ansible templates containing other template syntax.
* `pipecat-app` connects to `expert-api-main` via `LLAMA_API_SERVICE_NAME` defined in `pipecat.env.j2`.
* CI workflows are defined in `.github/workflows/ci.yml`.
* Use `include_tasks` to loop over a block of tasks in Ansible.
* The user wants to pre-generate Nomad job files for all experts but only run the `main` expert's job by default.
* `promote_controller.yaml` defines local handlers that can conflict with role handlers.
* Debug script documentation is maintained in `scripts/debug/README.md`.
* Project uses `pytest`. `app.py` unit tests are in `tests/unit/test_pipecat_app_unit.py`.
* `fix_yaml.sh` and `fix_markdown.sh` automate linting fixes.
* Common operational issues, such as stale Nomad service registrations, are documented in `docs/TROUBLESHOOTING.md`.
* `TwinService.get_system_prompt` constructs the system prompt from `prompts/router.txt`.
* The `world_model_service` requires an active MQTT connection to report healthy status via its `/health` endpoint (returns 503 on failure).
* `av` package requires `ffmpeg` dev libraries.
* Use `nomad job status -json` for machine-readable output in scripts.
* Create systemd service files before tasks that notify service restart handlers.
* Prompt evaluation test cases are in `prompt_engineering/evaluation_suite/`.
* Do not remove existing documentation sections during updates.
* Application virtual environment is at `/opt/pipecatapp/venv`.
* The `docker_image` Ansible module should use `force_source: true` to ensure container images are rebuilt when the build context (source files) changes.
* Use `pytest.ini` markers to skip tests requiring a graphical environment.
* Remote workflow uses `mosh` and `tmux`, documented in `REMOTE_WORKFLOW.md`.
* Avoid hardcoded user paths in scripts.
* `tests/unit/test_playbook_integration.py` fails due to missing `community.general` in the test environment.
* `PyAudio` requires `portaudio` dev libraries.
* `pipecatapp` discovers experts via Consul tags.
* `pipecat` architecture uses a `router-api` service; deployment waits for it to be healthy.
* Unit tests for `SummarizerTool` must patch `summarizer_tool.SentenceTransformer` to prevent real model downloads and authentication errors during instantiation.
* Agent definition schema tests are in `tests/unit/test_agent_definitions.py`.
* Debug Ansible roles in isolation using a temporary playbook with a `fail` task for inspection.
* Nomad host volume source paths are relative to the client's `data_dir` (default `/opt/nomad`).
* The `mosquitto.conf` generated by the `mqtt` Ansible role must include a trailing slash for the `persistence_location` path (e.g., `/mosquitto/data/`) to ensure the `eclipse-mosquitto` container starts correctly.
* Home Assistant deployment is asynchronous; `config_manager` conditionally extracts the token.
* User prefers `ansible-playbook --check` for validation over syntax check.
* When a Nomad job using the `network { mode = "host" }` configuration runs as a non-root user (e.g., `eclipse-mosquitto` user 1883), it must be granted the `NET_BIND_SERVICE` capability to bind to privileged ports. This capability should be added to the `cap_add` block within the task configuration.
* `bootstrap.sh --flush-cache` clears the torch cache.
* Scripts identifying playbooks should filter for `hosts:` to ensure correct matching.
* Install build tools like `cython` before complex Python packages like `av`.
* Home Assistant generates its Long-Lived Access Token after initial startup.
* Use a `daemon-reload` handler for systemd file changes to avoid premature restarts.
* In Ansible shell tasks, when using `ip route` to detect the default interface, use `head -n1` to ensure only the primary interface is returned if multiple default routes exist.
* Use `xvfb-run` for headless `pyautogui` tests and import the module locally within functions.
* Generated evaluators are in `prompt_engineering/generated_evaluators/`.
* Integration tests require running `pipecat` and Consul.
* Use `ansible_default_ipv4.address` in `ansible.builtin.uri` URLs to avoid IPv6 issues.
* Test environment needs `pytest` and `ansible-core` in pyenv.
* `playbook.yaml` should define `vars_files` at the top level.
* If a Nomad job using the Docker driver fails with a connection refused error trying to pull `localhost/image-name`, it indicates the image does not exist locally, causing Nomad to default to a registry pull.
* The agent uses `DesktopControlTool` and `pyautogui` for vision-based automation.
* In the `world_model_service` role, the Docker image is built using `ansible.builtin.command` directly to avoid issues with the `community.docker` module and ensure the image is available for Nomad.
* To tag a looped role inclusion, apply tags to the `include_role` task itself.
* Statically include roles with handlers in the top-level `roles:` section to ensure they are registered.
* Target fixes to the specific bug; avoid unrelated refactoring.
* Run unittest files directly: `python -m unittest path/to/test.py`.
* `llama-server` requires `--flash-attn` to be set.
* `nomad_models_dir` must be defined in `group_vars/all.yaml`.
* `playbook.yaml` uses `external_model_server` variable to conditionally skip model roles.
* Local dev setup: create venv, install from `requirements-dev.txt`.
* The `common` Ansible role configures a persistent `cluster_ip` alias (e.g., `10.0.0.x/24`) on the default interface using a systemd service (`cluster-ip-alias.service`) to ensure connectivity for Consul and Nomad across reboots.
* Python test dependencies are in `requirements-dev.txt`, `ansible/roles/python_deps/files/requirements.txt`, and `prompt_engineering/requirements-dev.txt`.
* Set `address_mode = "host"` in Nomad health checks when using `network { mode = "host" }`.
* Set a long `timeout` for `ansible.builtin.get_url` when downloading large files.
* `expert.nomad` fetches configuration from Consul based on `NOMAD_VAR_expert_name`.
* Make disruptive Ansible tasks conditional on boolean variables.
* Copy files into Docker images via `Dockerfile`, not Nomad `artifact` blocks.
* Experts can be deployed as a distributed cluster (`llamacpp-rpc`) or standalone.
* Manually run specific linters if `scripts/lint.sh` misapplies them.
* Use `check_mode: no` for setup tasks that must run during `--check`.
* The `debug_world_model.sh` script detects if MQTT (port 1883) is active and starts a temporary `eclipse-mosquitto` container if missing.
* The root-level `promote_controller.yaml` is the primary playbook for node promotion, while `playbooks/promote_to_controller.yaml` is a simplified version.
* Main `README.md` must be a complete guide for new developers.
* Kill hanging Ansible playbooks and proceed with verification if necessary.
* Use `ansible-playbook --syntax-check` for fast validation.
* Focus on the request; revert unrelated changes before submission.
* Use `add_host` to resolve undefined variable errors between plays.
* Correct Python executable path: `/home/jules/.pyenv/versions/3.12.12/bin/python`.
* `ansible-lint` is a required pip-installed dev dependency.
* `world_model_service` maintains centralized state via MQTT and Consul.
* When defining Docker images in Nomad job specs that are built locally (without a registry), do not prefix the image name with `localhost/`. This causes the Docker driver to attempt a registry pull from `localhost:80`. Use the plain image tag (e.g., `my-image:latest`) and set `force_pull = false`.
* Do not use `namespace` as a variable name in Ansible; use `nomad_namespace`.
* Verify redundancy before removing code.
* `playbook.yaml` requires `target_user` variable.
* In Ansible tasks checking Consul availability (e.g., `wait_for`, `uri`), explicitly use `{{ advertise_ip }}` as the host address instead of `127.0.0.1` or `localhost` to ensure consistent connectivity verification.
* Access original loop items in registered results via `item.item.property`.
* When Ansible error logs reference a task (e.g., "Wait for MQTT service...") that is absent from the file, assume a local modification or version mismatch and verify file integrity before debugging logic.
* Use `async` and `poll: 0` for fire-and-forget Ansible tasks.
* Refactor standalone task files into dedicated roles.
* `supervisor.py` unit tests are in `tests/unit/test_supervisor.py`.
* CI uses `actions/cache` for `ansible_run.baseline.log`.
* Nomad health checks for the MQTT service using host networking should use `nc -z 127.0.0.1 1883` instead of the advertised IP (`${NOMAD_IP_mqtt}`) to avoid routing issues.
* Tasks within an Ansible `rescue` block that perform intermediate steps (like parsing IDs for logging) should use `ignore_errors: yes` to preventing the rescue block from failing prematurely.
* Ansible `--check` mode fails on tasks dependent on skipped setup tasks.
* The `ansible-playbook` executable is located at `/home/loki/.local/bin/ansible-playbook`.
* `expert.nomad.j2` requires `job_name` and `expert_name` variables.
* `download_models` depends on `config_manager` execution.
* Evaluator generator docs are at `prompt_engineering/agents/EVALUATOR_GENERATOR.md`.
* Update all callsites when refactoring module interfaces.
* The repository contains known 0-byte corrupted model files (`en_US-lessac-medium.onnx`, `chat.prompt.bin`, `bob.prompt.bin`) and binaries (`distributed-llama-repo/dllama*`).
* `llama.cpp` role uses commit hashes for idempotency.
* Agent definitions are stored in `prompt_engineering/agents/`.
* Full `pip install` often fails due to heavy system dependencies.
* Prompt evolution scripts are in `prompt_engineering/`.
* Use `${NOMAD_PORT_<label>}` in applications running with Nomad host networking.
* Home Assistant container requires `NET_RAW` and `NET_ADMIN` capabilities.
* The `llama_cpp` Ansible role includes `benchmark_single_model.yaml` from the project root using a relative path.
* `nomad` role default data directory is `/opt/nomad`.
* Match `vars` block names to Jinja2 template variable names to avoid errors.
* Use `daemon_reload: yes` when creating systemd services with Ansible.
* Nomad HTTP health checks consider only 2xx status codes as "healthy"; application endpoints must return non-2xx codes (like 503) to signal failure.
* Local playbook handlers can override role handlers, causing 'handler not found' errors.
* Shell debug scripts (e.g., `debug_world_model.sh`) should use `hostname -I` to determine the host IP for network bindings when emulating Nomad host networking.
* Ensure destination directory exists before using `ansible.builtin.unarchive`.
* The Consul management token (SecretID) required for UI access is stored in `/etc/consul.d/management_token` on the controller node.
* `python_deps` role uses long async timeout for PyTorch installation.
* Stale Nomad service registrations in Consul, often caused by wiping Nomad's data directory without clearing Consul's state, result in 'All service checks failing' for the old Node ID; these can be removed using `scripts/prune_consul_services.py`.
* Use `default('')` for `home_assistant_token` in Nomad template to handle circular dependency.
* LLM service uses `expert.nomad.j2` orchestrator and `llamacpp-rpc.nomad.j2` workers.
* The cluster uses a "Dual Network" architecture: `advertise_ip` (DHCP) for external management/UI ("Front of House") and `cluster_ip` (Static 10.0.0.x) for internal cluster communication ("Backstage").
* Router Agent is implemented in `app.py` and configured by `router.txt`.
* `ansible-lint` requires role name prefix for variables.
* Define Nomad `volume_mount` inside the `group` block, not `task` block.
* `REMOTE_WORKFLOW.md` suggests `helix`, `yazi`, and `lazygit`.
* Do not use `force_pull = true` for locally-built Docker images in Nomad.
* The `common` Ansible role configures `ufw` to allow SSH, loopback traffic (essential for local health checks), and all traffic from the `10.0.0.0/24` cluster subnet, while enforcing a default deny policy.
* Ansible `rescue` blocks do not catch Jinja2 template parsing errors.
* Invoke `ansible-playbook` with a playbook file to avoid inventory misinterpretation.
* `openevolve` dependency is in `prompt_engineering/requirements-dev.txt`.
* Use Nomad's top-level `volume` and `volume_mount` for host volumes, not Docker driver volumes.
* Nomad `raw_exec` health status only reflects command exit code, not app health.
* For `raw_exec`/`exec`, define `volume` inside the `group` block.
* `group_vars/models.yaml` defines `expert_models`.
* `pipecatapp` role deploys Nomad jobs for the app and services.
* `nomad` role creates `/opt/nomad/jobs`.
* `ansible-lint` checks for best practices and style.
* Quote Ansible task names containing colons.
* Experts are verified by cross-referencing `expert_models` with `llama_benchmarks.jsonl`.
* `test_home_assistant_template.py` requires `pyyaml`, `pytest`, `jinja2`.
* `ansible-lint` is at `/home/jules/.pyenv/versions/3.12.12/bin/ansible-lint`.
* Shell scripts in `raw_exec` jobs must use injected env vars (e.g., `$NOMAD_PORT_http`), not `{{ env ... }}`.
* Model health checks involve starting `llama-server`, checking health, then shutting down.
* Nomad agent cannot be configured as both server and client in the same file.
* Use Ansible `template` module to inject secrets into `.nomad.j2` files.
* Relative paths in `include_tasks` resolve relative to the top-level playbook directory.
* `TODO.md` tracks project status and user alignment.
* `config_manager` role populates Consul KV.
* Use `python-consul2` instead of `python-consul`.
* `pipecat-ai` now uses `SileroVADAnalyzer` (requires `[silero]`).
* Stay focused on the user's immediate request.
* `pipecatapp` fetches config from Consul KV at startup.
* `WebBrowserTool` supports vision-based interaction.
* User wants a discrepancy report before code changes.
* Multiple packages (pytest, pyyaml, etc.) are required to run `run_unit_tests.sh`.
* Prefer using `ansible.builtin.command` to execute `docker build` for local image creation in Ansible roles, as `community.docker.docker_image` may fail silently or encounter Python dependency issues in the project environment.
* Jinja2 `do` extension is not enabled; use list concatenation instead.
* `prompt_engineering/create_evaluator.py` generates evaluator scripts.
* Model filenames in `models.yaml` must match download URL case exactly.
* Use handlers for service restarts/rebuilds triggered by config changes.
* Use full `--flash-attn` flag in `llama-server` to avoid parsing errors.
* Test complex roles using a temporary playbook with dependencies in order.
* Wrapper tools should use a Python class with `subprocess` for execution.
* `llama-server` uses `--rpc` for RPC servers.
* Ansible tasks that deploy Nomad jobs using `nomad job run` should be wrapped in a `block/rescue` structure to capture and display job status and allocation logs (`nomad alloc logs`) if the deployment fails.
* Specific TCP ports allowed through the firewall include 4646 (Nomad HTTP), 8500 (Consul HTTP), 1883 (MQTT), 9001 (MQTT Websockets), and 8080 (Traefik/Router).
* `ansible-core` must be installed in pyenv via pip.
* `pytest-asyncio` is required for async tests.
* `download_models` depends on `config_manager` execution.
* Nomad roles template job files to `/opt/nomad/jobs/` and notify a handler to run them.
* Run `pytest` on specific directories to avoid name collisions.
* Use `inventory_hostname` instead of `ansible_host` if facts are not gathered.
* The `tool_server` Nomad job mounts `/opt/cluster-infra` (for `Ansible_Tool`) and the host user's SSH keys (`/home/{{ target_user }}/.ssh`) (for `SSH_Tool`).
* Exclude `tests/` and `prompt_engineering/` when searching for project files.
* For Nomad services using `network { port ... }`, explicitly set `address_mode = "host"` in the `check` stanza to ensure health checks target the correct IP address reachable by the Nomad agent.
* Nomad batch jobs can be scheduled with `periodic`.
* The `tool_server` Nomad job mounts `/opt/mcp` for the `TermEverythingTool` and injects `HA_URL` and `HA_TOKEN` environment variables for the `HA_Tool`.
* Run long Ansible commands in background (`&`) to avoid timeouts.
* End-to-end tests are in `tests/playbooks/e2e-tests.yaml`.
* The `docker/dev_container/Dockerfile` includes `rsync` to ensure compatibility with `playbooks/common_setup.yaml`.
* Project uses `MemoryStore` and `RAG_Tool` (FAISS) for long-term memory.
* The `InputNode` in the workflow system handles `outputs` configuration as either a list of strings or dictionaries; code consuming this config must check the type.
* Unit tests for tools in `ansible/roles/pipecatapp/files/tools/` must insert the tool directory into `sys.path` to support running test files individually.
* Use process substitution for `find` loops in Bash to preserve variables.
* Launch FastAPI/Uvicorn programmatically in `app.py`.
* To reliably debug Nomad deployment failures in Ansible, use `jq` to sort allocations by `CreateTime` (e.g., `sort_by(.CreateTime) | reverse | .[0].ID`) to target the most recent attempt.
* `pipecatapp` role installs Playwright browsers using the venv path.
* `TwinService` in `app.py` runs a vision-centric agent loop.
* Do not ask clarifying questions until the task is complete.
* Flatten list of JSON strings in Ansible: `... | map('from_json') | sum(start=[])`.
* Set `gather_facts: yes` if playbook depends on host facts.
* Explicitly purge Nomad jobs to clean up locked resources.
* Pass variables for top-level play attributes as extra vars.
* Unit test suite is run via `./tests/scripts/run_unit_tests.sh`.
* Create users before performing file operations that require them.
* Global app variables are in `group_vars/all.yaml` and Consul.
* The `world_model_service` uses `network { mode = "host" }` for its Nomad job configuration, mirroring the successful configuration of the `debug_world_model.sh` script.
* Modular, containerized architecture on Nomad with MQTT, Home Assistant, Frigate, and vector DB.
* Consul `retry_join` configuration must use the target node's `cluster_ip` (e.g., `{{ hostvars[...]['cluster_ip'] }}`) to ensure gossip traffic occurs on the private network.
* When refactoring a module or class, it is crucial to also update all the code that calls it to match the new interface (e.g., constructor arguments). Failure to do so will result in runtime error
* When refactoring a persistence layer from a simple file-based JSON dump (O(N) writes) to a database like SQLite, it is critical to ensure that any auxiliary in-memory structures (like a list of keys mapping to external index offsets) are also persisted or deterministically reconstructible. For example, replacing a JSON dump of `{id: page}` with a SQLite table breaks the implicit ordering that might be used to map FAISS vector indices to Page IDs. The restoration logic must guarantee that the in-memory list matches the on-disk FAISS index order, either by persisting the list explicitly (e.g., in `state.json`) or by using a deterministic database query (e.g., `ORDER BY timestamp ASC`) if insertion order is strictly guaranteed.
* Nomad must start *after* Consul to correctly populate node attributes like `attr.consul.version`. Use `After=consul.service` and `Wants=consul.service` in Nomad's systemd unit to prevent "Constraint Mismatch" errors (e.g. `consul.version >= 1.8.0` failing).
* When purging Consul data (e.g., with `cleanup_services=true`), strictly verify that the process is stopped and port 8500 is closed before deleting data. Using `ignore_errors: yes` on the port check can lead to data deletion while the process is active, corrupting the state (e.g., "ACL not found").
