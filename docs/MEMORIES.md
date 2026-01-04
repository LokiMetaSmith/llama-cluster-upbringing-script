# Agent Memories

Last updated: 2026-01-04

Agent memories related to the project.

## Ansible Patterns & Best Practices

* When an Ansible task using the `slurp` module is skipped due to a `when` condition, the registered variable is still created but will lack the `content` key. Conditional logic should check for the key's existence (e.g., `'content' in my_variable`) rather than just if the variable is defined (`my_variable is defined`) to avoid errors.
* Ansible tasks and handlers managing system services (e.g., `systemd`, `service`) should be skipped in check mode (`when: not ansible_check_mode`) if the service configuration files are not actually written.
* Always wait for explicit user approval before beginning a multi-step plan, especially one involving code modifications. Do not bundle unrequested changes with requested ones.
* When an Ansible handler restarts a service like Nomad, a race condition can occur if other tasks or handlers try to use the service's API before it is fully initialized. The restart handler should include a task that polls the service's API endpoint until it is ready.
* Ansible roles compiling software from git (e.g., `whisper_cpp`) should ensure idempotency by comparing remote commit hashes against a local version file before building.
* The Ansible `debug` module does not accept `mode` or `become` parameters. Incorrectly adding them can cause YAML syntax errors.
* To prevent failures in Ansible `--check` mode when copying generated files, check for the source file's existence using `stat` with `check_mode: false` and condition the `copy` task on the result.
* To flatten a JSON list of dictionaries from a looped `ansible.builtin.uri` result, use: `... | selectattr('status', 'equalto', 200) | map(attribute='content') | map('from_json') | flatten | items2dict(key_name='name')`.
* To avoid YAML parser confusion, remove commented-out lines in Ansible playbooks that mix "k=v" shorthand with standard YAML.
* The error `"'ansible.parsing.yaml.objects.AnsibleUnicode object' has no attribute..."` in Ansible usually implies a data structure mismatch, such as filtering a list of strings instead of objects.
* Ansible pipelining is disabled in `ansible.cfg` (`pipelining = False`) to avoid privilege escalation issues.
* When refactoring an Ansible handler, preserve its `name`. Use a `block` to group actions like post-restart waiting within the existing handler.
* Ansible task files should not begin with `---` as per `.yamllint` configuration.
* For `unarchive` tasks in Ansible to succeed in check mode, the destination directory creation task must be forced to run (`check_mode: false`) or the unarchive task must be skipped.
* The `ansible.builtin.uri` module does not support `--check` mode.
* Provide default values for variables dependent on inventory groups (e.g., `groups['workers']`) to prevent errors in partial inventories.
* When `replace_with_git_merge_diff` fails due to context matching issues, `overwrite_file_with_block` is a reliable alternative for ensuring file correctness.
* In Ansible, the `loop` keyword must be at the same indentation level as task attributes.
* Use `listen: "Handler Name"` in Ansible handlers to group multiple tasks (e.g., restart service and wait for port) under a single notification name.
* Use `regex_findall` instead of `regex_search` in Ansible log entries for easier handling of no-match cases.
* Use fully qualified collection names (FQCN) in Ansible (e.g., `ansible.builtin.file`).
* Use `ansible.builtin.shell` with `jq` to reliably parse JSONL files in Ansible, rather than `map('from_json')`.
* `ansible-playbook --start-at-task` works with task names, not play names.
* Command-line arguments for `bootstrap.sh` are passed as `--extra-vars` to `ansible-playbook`.
* Use `creates` with `ansible.builtin.script` to ensure idempotency.
* Use `creates` with `ansible.builtin.unarchive` for idempotency.
* Include `is defined` checks in Ansible `when` conditionals for optional variables.
* Transient "Waiting for cache lock" errors in Ansible can happen if `apt` is busy.
* Use `select('list')` before `sum` when flattening lists in Ansible to avoid TypeErrors.
* `ansible.builtin.uri` is used instead of `community.general.consul_kv` to avoid dependency issues.
* Avoid using `daemon_reload: yes` in every `systemd` service start task; instead, use a dedicated handler notified by service file changes to improve idempotency.
* Use a conditional check instead of `default` when using the Ansible `combine` filter on potentially missing dictionaries.
* Split plays that contain both `roles:` and `tasks:` to ensure handlers load correctly.
* To extract an item from an Ansible loop result: `((... | selectattr('item', 'equalto', 'my_item') | first).content | default('{}')) | from_json`.
* Explicitly set `executable: /bin/bash` for Ansible shell tasks using bash features like `set -o pipefail`.
* Use retry loops (`until`, `retries`) for Ansible tasks prone to transient network errors.
* Use `include_tasks` to loop over a block of tasks in Ansible.
* The `docker_image` Ansible module should use `force_source: true` to ensure container images are rebuilt when the build context (source files) changes.
* Debug Ansible roles in isolation using a temporary playbook with a `fail` task for inspection.
* User prefers `ansible-playbook --check` for validation over syntax check.
* Scripts identifying playbooks should filter for `hosts:` to ensure correct matching.
* Use a `daemon-reload` handler for systemd file changes to avoid premature restarts.
* Use `ansible_default_ipv4.address` in `ansible.builtin.uri` URLs to avoid IPv6 issues.
* To tag a looped role inclusion, apply tags to the `include_role` task itself.
* Statically include roles with handlers in the top-level `roles:` section to ensure they are registered.
* Set a long `timeout` for `ansible.builtin.get_url` when downloading large files.
* Make disruptive Ansible tasks conditional on boolean variables.
* Use `check_mode: no` for setup tasks that must run during `--check`.
* Kill hanging Ansible playbooks and proceed with verification if necessary.
* Use `ansible-playbook --syntax-check` for fast validation.
* Use `add_host` to resolve undefined variable errors between plays.
* `ansible-lint` is a required pip-installed dev dependency.
* Do not use `namespace` as a variable name in Ansible; use `nomad_namespace`.
* Access original loop items in registered results via `item.item.property`.
* When Ansible error logs reference a task (e.g., "Wait for MQTT service...") that is absent from the file, assume a local modification or version mismatch and verify file integrity before debugging logic.
* Use `async` and `poll: 0` for fire-and-forget Ansible tasks.
* Refactor standalone task files into dedicated roles.
* Tasks within an Ansible `rescue` block that perform intermediate steps (like parsing IDs for logging) should use `ignore_errors: yes` to preventing the rescue block from failing prematurely.
* Ansible `--check` mode fails on tasks dependent on skipped setup tasks.
* `download_models` depends on `config_manager` execution.
* Full `pip install` often fails due to heavy system dependencies.
* Match `vars` block names to Jinja2 template variable names to avoid errors.
* Use `daemon_reload: yes` when creating systemd services with Ansible.
* Local playbook handlers can override role handlers, causing 'handler not found' errors.
* Ensure destination directory exists before using `ansible.builtin.unarchive`.
* `python_deps` role uses long async timeout for PyTorch installation.
* `ansible-lint` requires role name prefix for variables.
* Ansible `rescue` blocks do not catch Jinja2 template parsing errors.
* Invoke `ansible-playbook` with a playbook file to avoid inventory misinterpretation.
* `ansible-lint` checks for best practices and style.
* Quote Ansible task names containing colons.
* `ansible-lint` is at `/home/jules/.pyenv/versions/3.12.12/bin/ansible-lint`.
* Use Ansible `template` module to inject secrets into `.nomad.j2` files.
* Relative paths in `include_tasks` resolve relative to the top-level playbook directory.
* Prefer using `ansible.builtin.command` to execute `docker build` for local image creation in Ansible roles, as `community.docker.docker_image` may fail silently or encounter Python dependency issues in the project environment.
* Jinja2 `do` extension is not enabled; use list concatenation instead.
* Use handlers for service restarts/rebuilds triggered by config changes.
* Test complex roles using a temporary playbook with dependencies in order.
* Ansible tasks that deploy Nomad jobs using `nomad job run` should be wrapped in a `block/rescue` structure to capture and display job status and allocation logs (`nomad alloc logs`) if the deployment fails.
* `ansible-core` must be installed in pyenv via pip.
* Use `inventory_hostname` instead of `ansible_host` if facts are not gathered.
* Run long Ansible commands in background (`&`) to avoid timeouts.
* Flatten list of JSON strings in Ansible: `... | map('from_json') | sum(start=[])`.
* Set `gather_facts: yes` if playbook depends on host facts.
* Pass variables for top-level play attributes as extra vars.
* Create users before performing file operations that require them.
* Global app variables are in `group_vars/all.yaml` and Consul.

## Nomad & Consul Configuration

* In Nomad HCL, keys within an `env` block must not be quoted. For example, use `KEY = "value"` instead of `"KEY" = "value"`.
* In Nomad client configurations (v1.7.5+), task drivers like `exec` and `raw_exec` must be explicitly enabled using `plugin` blocks to function.
* The project uses a centralized, data-driven approach for managing LLM 'expert' models. Configurations, including download URLs and filenames, are defined in `group_vars/models.yaml` and the list of active experts is in `group_vars/all.yaml`.
* In Nomad HCL, to select a USB device within a `device` block, a `constraint` sub-block should be used with the `attribute` namespaced by device type (e.g., `usb.class_id`) and the `value` as the decimal class ID.
* The Ansible playbook for `pipecatapp` must explicitly run the `expert-main` Nomad job before waiting for the `expert-api-main` service in Consul, otherwise the playbook will hang.
* The `nomad job run` command uses the `-var` flag to pass variables.
* When executing `nomad` commands via Ansible, the `NOMAD_ADDR` environment variable must be set, typically to `http://{{ ansible_default_ipv4.address }}:4646`.
* Nomad job template `world_model.nomad.j2` should use `{{ advertise_ip }}` for `MQTT_HOST`, `CONSUL_HOST`, and `NOMAD_ADDR` to align with the host's actual IP address (`hostname -I`) used by successful debug scripts.
* The `expert` Nomad job registers its service in Consul as `expert-api-main`.
* The `nomad` role configuration in `group_vars/all.yaml` should define `nomad_version` (e.g., "1.7.7") and omit `nomad_zip_url` to allow the role to dynamically determine the download URL based on the version.
* Nomad HCL job files are sensitive to syntax errors.
* Ensure volume mounts and configuration paths in Nomad job templates match the directory structure created by Ansible on the host.
* When using Nomad's `mode = "host"` networking with the Docker driver, the `ports` list in the Docker `config` stanza should be removed to avoid binding conflicts, relying instead on the `network` stanza.
* To deploy a Nomad job via Ansible, render the Jinja2 template to a static file first, then run `nomad job run` on the rendered file.
* Use `systemctl status nomad` to verify Nomad status if Ansible logs are inconclusive.
* Mosquitto 2.0+ configuration in Ansible templates must use the `listener port [address]` syntax (e.g., `listener 1883 0.0.0.0`) instead of the deprecated `bind_address` directive to ensure proper binding on all interfaces in Docker host networking mode.
* The `world_model_service` Nomad job is configured with `network { mode = "host" }` to align with debug scripts and ensure MQTT connectivity.
* When configuring Nomad jobs with `network { mode = "host" }`, avoid setting `mode = "host"` explicitly if also relying on Docker bridge networking defaults; instead, remove the `mode` attribute to allow Nomad to manage port mapping correctly or use `bridge` mode explicitly if port isolation is required.
* Creating Nomad job files requires `become: yes` to write to `/opt/nomad/jobs`.
* Containers starting as root and dropping privileges (e.g., `eclipse-mosquitto`) need `SETUID` and `SETGID` capabilities in `cap_add`.
* When using ACLs with Consul in Ansible, include the `X-Consul-Token` header.
* The `config_manager` role stores the Home Assistant token in Consul at `config/hass/token`.
* Nomad service checks should include a `check_restart` stanza to ensure the task is restarted if the application becomes unhealthy (e.g., failing HTTP/TCP checks), as Nomad otherwise only restarts on process exit.
* The `group_vars/all.yaml` file unconditionally defines `cluster_ip` using the `cluster_subnet_prefix` and `node_id` (e.g., 10.0.0.x) to enforce a stable virtual subnet, avoiding fallback to DHCP addresses.
* Nomad health checks for the MQTT service should use an internal script check (`nc -z 127.0.0.1 1883`) instead of the default advertised IP (`${NOMAD_IP_mqtt}`) to avoid host networking routing issues.
* Third-party LLM expert configuration is in `group_vars/external_experts.yaml`.
* Consul KV is the central source of truth for runtime configuration.
* The `nomad_namespace` variable must be defined in `group_vars/all.yaml`.
* Nomad HCL job files are sensitive to syntax errors.
* The `tool_server` Nomad job registers the service as `tool-server-api` to match `llxprt_code` expectations.
* Nomad's `exec` and `raw_exec` drivers must be explicitly enabled in the client config.
* Nomad client configuration is managed by `ansible/roles/nomad/templates/nomad.hcl.client.j2`.
* Python applications in this project must explicitly exit (e.g., `os._exit(1)`) if critical background threads (like MQTT listeners) fail, to ensure Nomad restarts the allocation.
* To reliably debug Nomad deployment failures in Ansible, use `jq` to sort allocations by `CreateTime` (e.g., `sort_by(.CreateTime) | reverse | .[0].ID`) to target the most recent attempt.
* The `download_models` role organizes STT models by provider under `/opt/nomad/models/stt/` based on `group_vars/models.yaml`.
* `consul` role default data directory is `/opt/consul`.
* Host directories for Nomad `host_volume` mounts must be created before the service starts.
* When creating model-specific Nomad jobs, loop over full model objects enriched via Jinja2 filters.
* Clustered Nomad services should have `count > 1` and configured `update`, `migrate`, and `reschedule` stanzas.
* Escape inner template delimiters (e.g., `{{ '{{' }} env ... {{ '}}' }}`) in Ansible templates containing other template syntax.
* The user wants to pre-generate Nomad job files for all experts but only run the `main` expert's job by default.
* The `world_model_service` requires an active MQTT connection to report healthy status via its `/health` endpoint (returns 503 on failure).
* Use `nomad job status -json` for machine-readable output in scripts.
* `pipecatapp` discovers experts via Consul tags.
* Nomad host volume source paths are relative to the client's `data_dir` (default `/opt/nomad`).
* When a Nomad job using the `network { mode = "host" }` configuration runs as a non-root user (e.g., `eclipse-mosquitto` user 1883), it must be granted the `NET_BIND_SERVICE` capability to bind to privileged ports. This capability should be added to the `cap_add` block within the task configuration.
* If a Nomad job using the Docker driver fails with a connection refused error trying to pull `localhost/image-name`, it indicates the image does not exist locally, causing Nomad to default to a registry pull.
* In the `world_model_service` role, the Docker image is built using `ansible.builtin.command` directly to avoid issues with the `community.docker` module and ensure the image is available for Nomad.
* `nomad_models_dir` must be defined in `group_vars/all.yaml`.
* The `common` Ansible role configures a persistent `cluster_ip` alias (e.g., `10.0.0.x/24`) on the default interface using a systemd service (`cluster-ip-alias.service`) to ensure connectivity for Consul and Nomad across reboots.
* Set `address_mode = "host"` in Nomad health checks when using `network { mode = "host" }`.
* `expert.nomad` fetches configuration from Consul based on `NOMAD_VAR_expert_name`.
* Copy files into Docker images via `Dockerfile`, not Nomad `artifact` blocks.
* Experts can be deployed as a distributed cluster (`llamacpp-rpc`) or standalone.
* `world_model_service` maintains centralized state via MQTT and Consul.
* When defining Docker images in Nomad job specs that are built locally (without a registry), do not prefix the image name with `localhost/`. This causes the Docker driver to attempt a registry pull from `localhost:80`. Use the plain image tag (e.g., `my-image:latest`) and set `force_pull = false`.
* Do not use `force_pull = true` for locally-built Docker images in Nomad.
* In Ansible tasks checking Consul availability (e.g., `wait_for`, `uri`), explicitly use `{{ advertise_ip }}` as the host address instead of `127.0.0.1` or `localhost` to ensure consistent connectivity verification.
* Nomad health checks for the MQTT service using host networking should use `nc -z 127.0.0.1 1883` instead of the advertised IP (`${NOMAD_IP_mqtt}`) to avoid routing issues.
* The `expert.nomad.j2` requires `job_name` and `expert_name` variables.
* Use `${NOMAD_PORT_<label>}` in applications running with Nomad host networking.
* `nomad` role default data directory is `/opt/nomad`.
* Nomad HTTP health checks consider only 2xx status codes as "healthy"; application endpoints must return non-2xx codes (like 503) to signal failure.
* The Consul management token (SecretID) required for UI access is stored in `/etc/consul.d/management_token` on the controller node.
* Stale Nomad service registrations in Consul, often caused by wiping Nomad's data directory without clearing Consul's state, result in 'All service checks failing' for the old Node ID; these can be removed using `scripts/prune_consul_services.py`.
* Use `default('')` for `home_assistant_token` in Nomad template to handle circular dependency.
* LLM service uses `expert.nomad.j2` orchestrator and `llamacpp-rpc.nomad.j2` workers.
* The cluster uses a "Dual Network" architecture: `advertise_ip` (DHCP) for external management/UI ("Front of House") and `cluster_ip` (Static 10.0.0.x) for internal cluster communication ("Backstage").
* Define Nomad `volume_mount` inside the `group` block, not `task` block.
* Use Nomad's top-level `volume` and `volume_mount` for host volumes, not Docker driver volumes.
* Nomad `raw_exec` health status only reflects command exit code, not app health.
* For `raw_exec`/`exec`, define `volume` inside the `group` block.
* `pipecatapp` role deploys Nomad jobs for the app and services.
* `nomad` role creates `/opt/nomad/jobs`.
* Shell scripts in `raw_exec` jobs must use injected env vars (e.g., `$NOMAD_PORT_http`), not `{{ env ... }}`.
* Model health checks involve starting `llama-server`, checking health, then shutting down.
* Nomad agent cannot be configured as both server and client in the same file.
* `config_manager` role populates Consul KV.
* Use `python-consul2` instead of `python-consul`.
* `pipecatapp` fetches config from Consul KV at startup.
* Model filenames in `models.yaml` must match download URL case exactly.
* Use full `--flash-attn` flag in `llama-server` to avoid parsing errors.
* `llama-server` uses `--rpc` for RPC servers.
* Specific TCP ports allowed through the firewall include 4646 (Nomad HTTP), 8500 (Consul HTTP), 1883 (MQTT), 9001 (MQTT Websockets), and 8080 (Traefik/Router).
* Nomad roles template job files to `/opt/nomad/jobs/` and notify a handler to run them.
* The `tool_server` Nomad job mounts `/opt/cluster-infra` (for `Ansible_Tool`) and the host user's SSH keys (`/home/{{ target_user }}/.ssh`) (for `SSH_Tool`).
* For Nomad services using `network { port ... }`, explicitly set `address_mode = "host"` in the `check` stanza to ensure health checks target the correct IP address reachable by the Nomad agent.
* Nomad batch jobs can be scheduled with `periodic`.
* The `tool_server` Nomad job mounts `/opt/mcp` for the `TermEverythingTool` and injects `HA_URL` and `HA_TOKEN` environment variables for the `HA_Tool`.
* Explicitly purge Nomad jobs to clean up locked resources.
* The `world_model_service` uses `network { mode = "host" }` for its Nomad job configuration, mirroring the successful configuration of the `debug_world_model.sh` script.
* Modular, containerized architecture on Nomad with MQTT, Home Assistant, Frigate, and vector DB.
* Consul `retry_join` configuration must use the target node's `cluster_ip` (e.g., `{{ hostvars[...]['cluster_ip'] }}`) to ensure gossip traffic occurs on the private network.
* Nomad must start *after* Consul to correctly populate node attributes like `attr.consul.version`. Use `After=consul.service` and `Wants=consul.service` in Nomad's systemd unit to prevent "Constraint Mismatch" errors (e.g. `consul.version >= 1.8.0` failing).
* When purging Consul data (e.g., with `cleanup_services=true`), strictly verify that the process is stopped and port 8500 is closed before deleting data. Using `ignore_errors: yes` on the port check can lead to data deletion while the process is active, corrupting the state (e.g., "ACL not found").

## Development Workflow & Testing

* The correct Python module path for unit tests invoked via `python -m unittest` is `tests.unit.<module_name>`, matching the filesystem structure `tests/unit/`.
* When running E2E tests, the `pipecat` application and its dependencies must be running.
* Unit tests that involve subprocess calls should be mocked to ensure they are isolated and do not depend on external services or file systems.
* Agent definition markdown files must strictly format the 'Backing LLM Model' section with a bullet point like `* **Model:** ...` to pass schema validation tests.
* When debugging, prioritize identifying the root cause of the initial error message (e.g., "Temporary failure in name resolution") before attempting complex refactoring of seemingly related code.
* The `bootstrap.sh` script accepts a `--run-local` flag, which sets the Ansible extra variable `pipecat_deployment_style=raw_exec` for local debugging.
* In the development environment, if a file is confirmed to exist via `ls` but tools like `read_file` or `replace_with_git_merge_diff` fail with a 'file not found' error, deleting and recreating the file can resolve the issue.
* The `check_all_playbooks.sh` script performs a dry run (`--check`) on all Ansible playbooks, attempting to dynamically locate the `ansible-playbook` executable and using `local_inventory.ini` if present to target localhost.
* The `faster-whisper` STT provider is installed as a Python dependency via the `python_deps` role and is not managed by a dedicated Ansible role.
* The `scripts/lint.sh` script requires `yamllint` and `ansible-lint`, installed via pip.
* The `scripts/lint.sh` script (invoked via `npm run lint`) orchestrates linters including `yamllint`, `markdownlint-cli`, `djlint`, and an Ansible-based `nomad fmt` check.
* The `bootstrap.sh` script is the primary entry point for running the Ansible playbook, handling environment setup and arguments.
* Mock problematic modules like `pyaudio`, `faster_whisper`, `piper.voice`, and `playwright` when running unit tests in a minimal environment.
* Unit tests in `tests/unit/test_pipecat_app_unit.py` focus on Python application logic, not Ansible template rendering.
* When fixing a bug, create a persistent test case that fails before the fix and passes after.
* The development environment uses `pyenv` and Ansible executables are not in the default system `PATH`.
* Async functions under test require `AsyncMock` instances to be awaitable.
* The `ShellTool` operates asynchronously using `tmux` sessions; its unit tests require `pytest-asyncio` and `AsyncMock` for `asyncio.create_subprocess_exec`.
* The `reflection/reflect.py` script uses live API calls to an LLM to diagnose Nomad job failures.
* Before starting work, enter a deep planning mode to clarify user expectations using `request_user_input` and `message_user`. Only set a plan with `set_plan` after verification.
* The `bootstrap.sh` script supports an `--external-model-server` flag to skip model downloads/builds.
* When running executables like `ansible-playbook` via `bootstrap.sh`, use the full path to the executable to ensure the correct environment.
* Avoid `eval` in Bash scripts; use arrays to build command arguments safely.
* In shell scripts, check if process ID variables are set before using them with `kill` or `wait`.
* Ansible's `--check` mode is unreliable for logic dependent on variable contents. Use targeted real runs with tags instead.
* `AGENTS.md` documents local development setup and testing.
* `scripts/ansible_diff.sh` compares Ansible playbook `--check` runs against a baseline.
* `EVALUATOR_GENERATOR.md` is documentation, not an agent definition file.
* Shell scripts are tested using a Python `unittest` file that runs the script in a subprocess with a temporary file system.
* Add `--no-cache-dir` to Ansible `pip` tasks if they hang or time out.
* User prefers submitting completed work even if unrelated tests fail due to environment issues.
* `prompt_engineering/evaluation_lib.py` contains common functions for deploying and testing code in Nomad/Consul.
* `prompt_engineering/evolve.py` uses `openevolve` for prompt improvement.
* `bootstrap.sh --debug` saves full Ansible output to `playbook_output.log`.
* Markdown documentation must use asterisks `*` for unordered lists, blank lines around headings and lists (MD022, MD032), and correct table spacing (MD060) to pass linting.
* `scripts/ci_ansible_check.sh` wrappers `ansible_diff.sh` for CI workflows.
* `tests/unit/test_home_assistant_template.py` requires `hostvars` to be mocked.
* `requirements-dev.txt` contains redundant entries (e.g., `yaml`) that can break installation.
* `pytest-mock` is required for tests using the `mocker` fixture.
* `openevolve` evaluates code performance by deploying to Nomad and running integration tests.
* To generate test coverage reports: `python -m pytest --cov=ansible --cov=supervisor --cov-report=term-missing tests/unit/`.
* The `run_tests.sh` script in the root directory executes tests using flags: `--unit`, `--integration`, `--e2e`, and `--all`.
* To detect changes with Ansible check runs, `diff` two separate `--check` output files.
* The `scripts/debug/test_mqtt_connection.py` script diagnoses MQTT connectivity by probing port 1883 on all local interfaces to troubleshoot Nomad health check failures.
* The `heal_job.yaml` playbook performs remedial actions based on `reflection/reflect.py` output.
* `playbooks/common_setup.yaml` now explicitly updates the apt cache when installing `sudo` to handle environments with stale caches.
* The repository uses a unified `tests/` directory with subdirectories: `unit`, `integration`, `e2e`, `scripts`, and `playbooks`.
* Shell scripts should include a `show_help()` function for usage information.
* Install specific packages directly if `pip install -r requirements-dev.txt` times out.
* `bootstrap.sh` should check for `nomad` installation before use.
* `tests/unit/test_code_runner_tool.py` requires the `docker` python package to be installed to avoid `AttributeError` when mocking `docker.from_env`.
* The `tests/scripts/run_unit_tests.sh` script (or `run_tests.sh --unit`) runs the unit test suite.
* Install `community.general` and `ansible.posix` collections using the full pyenv path to `ansible-galaxy`.
* The `debug_world_model.sh` script requires the `world-model-service:latest` Docker image to be manually built from `ansible/roles/world_model_service/files/` before execution.
* Unit tests for tools in `ansible/roles/pipecatapp/files/tools/` must insert the tool directory into `sys.path` to support running test files individually.
* CI workflows are defined in `.github/workflows/ci.yml`.
* Debug script documentation is maintained in `scripts/debug/README.md`.
* Project uses `pytest`. `app.py` unit tests are in `tests/unit/test_pipecat_app_unit.py`.
* `fix_yaml.sh` and `fix_markdown.sh` automate linting fixes.
* Common operational issues, such as stale Nomad service registrations, are documented in `docs/TROUBLESHOOTING.md`.
* Use `nomad job status -json` for machine-readable output in scripts.
* Prompt evaluation test cases are in `prompt_engineering/evaluation_suite/`.
* Do not remove existing documentation sections during updates.
* Use `pytest.ini` markers to skip tests requiring a graphical environment.
* Remote workflow uses `mosh` and `tmux`, documented in `REMOTE_WORKFLOW.md`.
* Avoid hardcoded user paths in scripts.
* `tests/unit/test_playbook_integration.py` fails due to missing `community.general` in the test environment.
* Unit tests for `SummarizerTool` must patch `summarizer_tool.SentenceTransformer` to prevent real model downloads and authentication errors during instantiation.
* Agent definition schema tests are in `tests/unit/test_agent_definitions.py`.
* Home Assistant deployment is asynchronous; `config_manager` conditionally extracts the token.
* `bootstrap.sh --flush-cache` clears the torch cache.
* Install build tools like `cython` before complex Python packages like `av`.
* Use `xvfb-run` for headless `pyautogui` tests and import the module locally within functions.
* Generated evaluators are in `prompt_engineering/generated_evaluators/`.
* Integration tests require running `pipecat` and Consul.
* Test environment needs `pytest` and `ansible-core` in pyenv.
* Target fixes to the specific bug; avoid unrelated refactoring.
* Run unittest files directly: `python -m unittest path/to/test.py`.
* Local dev setup: create venv, install from `requirements-dev.txt`.
* Python test dependencies are in `requirements-dev.txt`, `ansible/roles/python_deps/files/requirements.txt`, and `prompt_engineering/requirements-dev.txt`.
* Manually run specific linters if `scripts/lint.sh` misapplies them.
* The `debug_world_model.sh` script detects if MQTT (port 1883) is active and starts a temporary `eclipse-mosquitto` container if missing.
* Main `README.md` must be a complete guide for new developers.
* Focus on the request; revert unrelated changes before submission.
* Correct Python executable path: `/home/jules/.pyenv/versions/3.12.12/bin/python`.
* CI uses `actions/cache` for `ansible_run.baseline.log`.
* The `ansible-playbook` executable is located at `/home/loki/.local/bin/ansible-playbook`.
* Evaluator generator docs are at `prompt_engineering/agents/EVALUATOR_GENERATOR.md`.
* Agent definitions are stored in `prompt_engineering/agents/`.
* Prompt evolution scripts are in `prompt_engineering/`.
* Shell debug scripts (e.g., `debug_world_model.sh`) should use `hostname -I` to determine the host IP for network bindings when emulating Nomad host networking.
* `REMOTE_WORKFLOW.md` suggests `helix`, `yazi`, and `lazygit`.
* `openevolve` dependency is in `prompt_engineering/requirements-dev.txt`.
* `test_home_assistant_template.py` requires `pyyaml`, `pytest`, `jinja2`.
* `TODO.md` tracks project status and user alignment.
* Stay focused on the user's immediate request.
* User wants a discrepancy report before code changes.
* Multiple packages (pytest, pyyaml, etc.) are required to run `run_unit_tests.sh`.
* `prompt_engineering/create_evaluator.py` generates evaluator scripts.
* Wrapper tools should use a Python class with `subprocess` for execution.
* `pytest-asyncio` is required for async tests.
* Run `pytest` on specific directories to avoid name collisions.
* Exclude `tests/` and `prompt_engineering/` when searching for project files.
* End-to-end tests are in `tests/playbooks/e2e-tests.yaml`.
* The `docker/dev_container/Dockerfile` includes `rsync` to ensure compatibility with `playbooks/common_setup.yaml`.
* Unit tests for tools in `ansible/roles/pipecatapp/files/tools/` must insert the tool directory into `sys.path` to support running test files individually.
* Use process substitution for `find` loops in Bash to preserve variables.
* To reliably debug Nomad deployment failures in Ansible, use `jq` to sort allocations by `CreateTime` (e.g., `sort_by(.CreateTime) | reverse | .[0].ID`) to target the most recent attempt.
* Do not ask clarifying questions until the task is complete.
* Unit test suite is run via `./tests/scripts/run_unit_tests.sh`.
* When refactoring a module or class, it is crucial to also update all the code that calls it to match the new interface (e.g., constructor arguments). Failure to do so will result in runtime error

## Project Architecture & Components

* `supervisor.py` depends on `health_check.yaml`, `diagnose_failure.yaml`, and `heal_job.yaml` being present in the root directory.
* The `tool_server` build process copies the shared `tools` library from `ansible/roles/pipecatapp/files/tools/` into the build context.
* The `tool_server` role deploys a full Model Context Protocol (MCP) server implementation (migrated from `ansible/roles/pipecatapp/files/tool_server.py`) to `ansible/roles/tool_server/app.py`.
* The project uses two distinct AI agent architectures: a runtime "Mixture of Experts" (MoE) and a development "Ensemble of Agents".
* The project's Python tools (e.g., `mcp_tool.py`, `ansible_tool.py`) are located in `ansible/roles/pipecatapp/files/tools/`.
* The repository contains Ansible playbooks for provisioning a cluster infrastructure using services like Consul, Docker, and Nomad.
* Runtime Python dependencies are in `ansible/roles/python_deps/files/requirements.txt`; dev dependencies are in `requirements-dev.txt`.
* The `mqtt` Ansible role configures `mosquitto.conf` with both `log_dest stdout` and `log_dest stderr` to ensure comprehensive log capture during container startup and health check failures.
* The `term.everything` Ansible role requires the `podman` package to build the AppImage.
* The `pipecat-app` application uses a Uvicorn web server, configured via the `WEB_PORT` environment variable.
* The `llama-server` application's `/health` endpoint requires a model to be successfully loaded to return healthy.
* The PXE boot process uses `pxe_os` in `group_vars/all.yaml` to select between Debian and NixOS.
* The `tool_server` role relies on `ansible/roles/tool_server/app.py` as the single source of truth, which is copied into the Docker image via the `Dockerfile`.
* Home Assistant's auth token is stored at `/opt/nomad/volumes/ha-config/.storage/auth_provider.homeassistant`.
* Expert agents are defined by prompts in `ansible/roles/pipecatapp/files/prompts/`.
* The `tool_server` role Docker image build process is updated to copy the source files (`app.py`, `Dockerfile`, `tools/`, etc.) into a dedicated build directory `/opt/tool_server` before building to ensure a clean build context.
* The `tool_server` serves as a Model Context Protocol (MCP) server, exposing functionality via the `/run_tool/` endpoint.
* The project uses two Home Assistant tools: `HomeAssistantTool` (structured) and `HA_Tool` (natural language).
* The `pipecatapp` role requires the `/opt/pipecatapp` directory to exist before starting Nomad.
* The `jq` package is installed via the `system_deps` Ansible role.
* `traffic_monitor.c` requires `<uapi/linux/in.h>` for compilation.
* The `open3d` library requires `libgl1-mesa-glx`, `libgl1-mesa-dev`, and `libglu1-mesa-dev`.
* `ansible/roles/pipecatapp/files/app.py` uses a `TwinService` class for agent logic.
* The `tool_server` Docker image includes specific dependencies (`pyautogui`, `ansible`, `pipecat-ai[all]`) to support the tools library.
* `rsync` is a required system dependency for the main Ansible playbook.
* `langchain.text_splitter` is deprecated; use `langchain-text-splitters`.
* `playbook.yaml` explicitly loads `group_vars/models.yaml`.
* The RAG tool (`rag_tool.py`) uses a FAISS vector index.
* The file `docker/pipecatapp/app.py` is a stale or divergent artifact that differs from the source of truth `ansible/roles/pipecatapp/files/app.py`.
* Explicitly set `torch.backends.cuda.matmul.fp32_precision = 'high'` in `app.py` to silence TF32 warnings.
* `llama.cpp` `rpc-server` requires `-H HOST` to specify the bind address (e.g., `-H 0.0.0.0`) and `-p PORT` for the port.
* The `pipecatapp` role depends on `system_deps`, `nomad`, and `python_deps` roles running first.
* The `nixos_pxe_server` role uses `configuration.nix` to build a netboot environment.
* The `term_everything` role compares commit hashes to ensure idempotent builds.
* The user wants an 'ensemble of agents' workflow.
* Home Assistant auto-configures MQTT from `MQTT_SERVER`, conflicting with explicit `mqtt:` blocks in `configuration.yaml`.
* Existing 'expert routing' prompts are in `ansible/roles/pipecatapp/files/prompts/`.
* `piper-tts` uses `PiperVoice.load()` instead of `from_files`.
* API endpoints are in `ansible/roles/pipecatapp/files/web_server.py`.
* The `workflow.runner` module must import the `registry` instance explicitly (`from .nodes.registry import registry`) rather than the module package to avoid `AttributeError`.
* Agent roles include Problem Scope Framing, Architecture Review, New Task Review, Debug and Analysis, and Code Clean Up.
* `prompts/router.txt` defines the Router agent's vision and tool usage.
* `supervisor.py` is a self-healing loop for system jobs.
* `pipecat-app` connects to `expert-api-main` via `LLAMA_API_SERVICE_NAME` defined in `pipecat.env.j2`.
* `promote_controller.yaml` defines local handlers that can conflict with role handlers.
* `TwinService.get_system_prompt` constructs the system prompt from `prompts/router.txt`.
* `av` package requires `ffmpeg` dev libraries.
* Application virtual environment is at `/opt/pipecatapp/venv`.
* `PyAudio` requires `portaudio` dev libraries.
* `pipecat` architecture uses a `router-api` service; deployment waits for it to be healthy.
* Home Assistant generates its Long-Lived Access Token after initial startup.
* The agent uses `DesktopControlTool` and `pyautogui` for vision-based automation.
* `llama-server` requires `--flash-attn` to be set.
* `playbook.yaml` uses `external_model_server` variable to conditionally skip model roles.
* `expert.nomad` fetches configuration from Consul based on `NOMAD_VAR_expert_name`.
* The root-level `promote_controller.yaml` is the primary playbook for node promotion, while `playbooks/promote_to_controller.yaml` is a simplified version.
* `world_model_service` maintains centralized state via MQTT and Consul.
* `playbook.yaml` requires `target_user` variable.
* `expert.nomad.j2` requires `job_name` and `expert_name` variables.
* The repository contains known 0-byte corrupted model files (`en_US-lessac-medium.onnx`, `chat.prompt.bin`, `bob.prompt.bin`) and binaries (`distributed-llama-repo/dllama*`).
* `llama.cpp` role uses commit hashes for idempotency.
* Home Assistant container requires `NET_RAW` and `NET_ADMIN` capabilities.
* The `llama_cpp` Ansible role includes `benchmark_single_model.yaml` from the project root using a relative path.
* Router Agent is implemented in `app.py` and configured by `router.txt`.
* `group_vars/models.yaml` defines `expert_models`.
* Experts are verified by cross-referencing `expert_models` with `llama_benchmarks.jsonl`.
* `pipecat-ai` now uses `SileroVADAnalyzer` (requires `[silero]`).
* `WebBrowserTool` supports vision-based interaction.
* Project uses `MemoryStore` and `RAG_Tool` (FAISS) for long-term memory.
* The `InputNode` in the workflow system handles `outputs` configuration as either a list of strings or dictionaries; code consuming this config must check the type.
* Launch FastAPI/Uvicorn programmatically in `app.py`.
* `pipecatapp` role installs Playwright browsers using the venv path.
* `TwinService` in `app.py` runs a vision-centric agent loop.
* When refactoring a persistence layer from a simple file-based JSON dump (O(N) writes) to a database like SQLite, it is critical to ensure that any auxiliary in-memory structures (like a list of keys mapping to external index offsets) are also persisted or deterministically reconstructible. For example, replacing a JSON dump of `{id: page}` with a SQLite table breaks the implicit ordering that might be used to map FAISS vector indices to Page IDs. The restoration logic must guarantee that the in-memory list matches the on-disk FAISS index order, either by persisting the list explicitly (e.g., in `state.json`) or by using a deterministic database query (e.g., `ORDER BY timestamp ASC`) if insertion order is strictly guaranteed.
* When purging Consul data (e.g., with `cleanup_services=true`), strictly verify that the process is stopped and port 8500 is closed before deleting data. Using `ignore_errors: yes` on the port check can lead to data deletion while the process is active, corrupting the state (e.g., "ACL not found").

## Troubleshooting & Gotchas

* In the development environment, if a file is confirmed to exist via `ls` but tools like `read_file` or `replace_with_git_merge_diff` fail with a 'file not found' error, deleting and recreating the file can resolve the issue.
* The error `"'ansible.parsing.yaml.objects.AnsibleUnicode object' has no attribute..."` in Ansible usually implies a data structure mismatch, such as filtering a list of strings instead of objects.
* `replace_with_git_merge_diff` may fail on context match -> use `overwrite_file_with_block`.
* `AnsibleUnicode` attribute error -> Data structure mismatch (list of strings vs objects).
* `Waiting for cache lock` -> apt is busy.
* Docker connection refused on `localhost/image` -> Image missing locally, Docker trying registry.
* Update all callsites when changing method signatures.
* When moving from file-based to DB persistence (e.g., FAISS), ensure order is preserved or explicitly tracked.
* Transient "Waiting for cache lock" errors in Ansible can happen if `apt` is busy.
* If a Nomad job using the Docker driver fails with a connection refused error trying to pull `localhost/image-name`, it indicates the image does not exist locally, causing Nomad to default to a registry pull.
* Local playbook handlers can override role handlers, causing 'handler not found' errors.
* When refactoring a module or class, it is crucial to also update all the code that calls it to match the new interface (e.g., constructor arguments). Failure to do so will result in runtime error
* When purging Consul data (e.g., with `cleanup_services=true`), strictly verify that the process is stopped and port 8500 is closed before deleting data. Using `ignore_errors: yes` on the port check can lead to data deletion while the process is active, corrupting the state (e.g., "ACL not found").
