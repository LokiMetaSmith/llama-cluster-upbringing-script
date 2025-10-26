Agent memories related to the project. 

The Ansible playbook's --check mode can fail on tasks that depend on state created by other tasks (e.g., a service task failing because the task that creates the service file was skipped), as many setup tasks do not run in check mode. This is a known issue.



The check_all_playbooks.sh script is used to perform a dry run (--check) on all Ansible playbooks. It dynamically locates the ansible-playbook executable by searching the system PATH first, then looking in ~/.pyenv, to ensure portability.



Hardcoded, user-specific paths (e.g., /home/jules/...) in scripts are not acceptable. Scripts should dynamically find required executables or rely on the user's PATH.



The term_everything Ansible role ensures idempotent builds by comparing the latest remote git commit hash with a locally stored version hash in /usr/local/etc/term.everything.version. Recompilation is skipped if the hashes match.



The scripts/lint.sh script requires yamllint and ansible-lint, which can be installed via pip install yamllint ansible-lint.



When fixing a bug, a new, persistent test case must be created that fails before the fix and passes after. Temporary verification files are not sufficient.



A testing pattern for shell scripts in this repository is to use a Python unittest file that creates a temporary file system, runs the script as a subprocess, and asserts on its output.



Fixes must be targeted to the identified bug. Do not include unrelated changes like style fixes or refactoring in the same submission.



Ansible plays that template variables depending on host facts (e.g., ansible_memtotal_mb) may fail if facts are not gathered. Explicitly setting gather_facts: yes in the play is the required fix, even if it should be the default behavior.



The development environment can be fragile. Ansible executables like ansible-playbook are not in the default system PATH and depend on a specific pyenv or virtual environment that may require manual setup or activation.



To determine 'verified experts', the Ansible playbook cross-references the list of an expert's models (from expert_models in group_vars/models.yaml) with the list of successfully benchmarked model filenames (from /var/log/llama_benchmarks.jsonl). An expert is verified if there is an intersection between these two lists.



The project uses a centralized, data-driven approach for managing LLM 'expert' models. Configurations, including download URLs and filenames, are defined in group_vars/models.yaml and the list of active experts is in group_vars/all.yaml. This data is used by the download_models Ansible role and various Nomad job templates to ensure consistency.



The llama-server application's /health endpoint only becomes available after a model is successfully loaded. An http health check in a Nomad service is appropriate, but a failure may indicate a model loading issue rather than a missing endpoint.



Model filenames are case-sensitive. When configuring models in group_vars/models.yaml, the filename value must exactly match the case of the file from the download URL to prevent 'file not found' errors during model loading.



In Bash scripts, avoid using eval to construct commands with arguments. Instead, use an array to build the list of arguments and expand it safely with "${array[@]}".



Comparing the output of an ansible-playbook run with --check to the output of a run without it is unreliable for change detection. The correct approach is to diff the outputs of two separate --check runs against each other (e.g., a baseline --check run vs. a current --check run).



The Ansible playbook requires at least the community.general and ansible.posix collections. They must be installed with ansible-galaxy collection install <collection_name> before running the playbook.



To reliably identify top-level Ansible playbooks, scripts should filter for files containing ^\s*-\s*hosts: to correctly match playbooks that are structured as YAML lists.



Ansible tasks that create directories or perform other setup required by subsequent tasks may be skipped in --check mode, causing failures. Such tasks can be forced to run by adding check_mode: no.



To maintain atomicity, changes should be focused on the user's request. Unrelated fixes, even if necessary for local testing, should be reverted before submission and handled separately in a subsequent commit.



When searching for project files to operate on, the testing/ and prompt_engineering/ directories should generally be excluded.



In Bash, when piping from find to a while loop, the loop runs in a subshell, preventing variable changes from persisting. Use process substitution (while ...; do ...; done < <(find ...))) to avoid this.



When validating Ansible playbooks, the user prefers a full dry-run using ansible-playbook --check rather than a simple ansible-playbook --syntax-check.



To prevent 'undefined variable' errors in Ansible when conditionals that check dictionary keys or variables that may not exist for all hosts, always include an is defined check (e.g., when: my_var is defined and my_var == 'value').



To resolve 'undefined variable' errors in Ansible when a hosts directive in a later play depends on a variable from an earlier play (e.g., from vars_prompt), use the add_host module in the first play to dynamically add the target host to an in-memory group. The subsequent play can then target this dynamic group.



In Ansible, the unarchive module requires the dest directory to exist before execution. A file task with state: directory should precede the unarchive task to ensure the destination path is present.



Ansible may misinterpret a YAML inventory file as a playbook if ansible-playbook is invoked without a specific playbook file, causing a 'playbook must be a list of plays' error. Ensure invocations are correct and that inventory file extensions (.yaml, .ini) match their content format to allow the correct inventory plugin to be used.



In Ansible, ansible_host is a gathered fact and is unavailable if gather_facts: no is set. Use inventory_hostname instead, as it is always available from the inventory.



When an Ansible task fails due to a 'user not found' error during a file operation like chown, ensure that the user creation task is executed before the file operation task. User creation should be handled in the appropriate role or playbook, and variables like target_user should be passed correctly to the roles that need them.



To run a syntax check on the main playbook, use the command ansible-playbook -i local_inventory.ini playbook.yaml --syntax-check --extra-vars="target_user=jules". The specific executable path might need to be found using which ansible-playbook.



In a Nomad job file using the raw_exec driver, shell scripts cannot use Nomad's env template function (e.g., {{ env "NOMAD_PORT_http" }}). They must access allocated ports and other runtime variables through standard environment variables that Nomad injects into the execution environment (e.g., $NOMAD_PORT_http).



To selectively run an Ansible role that is included via a loop on an include_role task, the --tags flag must match a tags: key applied directly to the include_role task itself.



The main playbook (playbook.yaml) uses the external_model_server boolean variable to conditionally skip model-dependent roles (like download_models and llama_cpp) by checking when: not external_model_server.



The Python testing environment has numerous unlisted dependencies. To successfully run the ./testing/run_unit_tests.sh script, the following packages must be installed via pip: pytest, pytest-mock, pytest-asyncio, httpx, openevolve, numpy, requests, ultralytics, faiss-cpu, pipecat-ai, sentence-transformers, websockets, python-consul2, fastapi, paramiko, and uvicorn.



The pipecat-app connects to the main LLM orchestrator service, expert-api-main, via the LLAMA_API_SERVICE_NAME environment variable set in the ansible/roles/pipecatapp/templates/pipecat.env.j2 template.



The LLM service architecture consists of an orchestrator job (expert.nomad.j2) that exposes the expert-api-main service, which in turn uses a pool of llamacpp-rpc-pool-provider worker services defined in llamacpp-rpc.nomad.j2.



The Ansible playbook can hang on the 'Run mqtt job' task. If this occurs after relevant changes have been applied, killing the playbook and proceeding with verification is a valid strategy.



Global application variables, such as llama_api_service_name, are defined as the source of truth in group_vars/all.yaml and propagated to the application via the config_manager role writing to Consul.



The unit tests in testing/unit_tests/test_pipecat_app.py focus on the Python application logic and do not cover the rendering of associated Ansible configuration templates.



The pipecat architecture includes a dedicated 'router' Nomad job, which provides a router-api service registered in Consul. The pipecat-app is configured via the LLAMA_API_SERVICE_NAME environment variable to use this service, and the Ansible deployment playbook waits for the router-api service to be healthy before starting the application.



The expert Nomad job, defined in ansible/jobs/expert.nomad.j2, registers its service in Consul with the name expert-api-main.



The pipecat-app application, which is started via app.py, uses a Uvicorn web server and its listening port is configurable through the WEB_PORT environment variable.



When a Nomad job uses network { mode = "host" }, the application code must not use a hardcoded port. Instead, it should read the port from the ${NOMAD_PORT_<label>} environment variable, which is passed from the Nomad job file.



The health status of a Nomad job using the raw_exec driver only indicates if the initial command ran successfully, not if the underlying application started by the command is healthy or responsive.



The Ansible playbook for pipecatapp must explicitly run the expert-main Nomad job before waiting for the expert-api-main service in Consul, otherwise the playbook will hang and time out.



Expert services can be deployed in two modes: as a distributed cluster using llamacpp-rpc for scalability, or as a single standalone llamacpp instance.



Nomad host volumes, when specified with a relative source path in the job file, are resolved relative to the data_dir configured for the Nomad client (defaulting to /opt/nomad). For example, a volume source of world_model_storage resolves to /opt/nomad/volumes/world_model_storage.



To run a long-running command in Ansible without blocking the playbook (e.g., submitting a Nomad job), use the async and poll: 0 directives. This makes the task 'fire and forget'.



For Python packages with complex C-extension build dependencies like av, ensuring build tools like cython are installed in a separate, preceding step can resolve compilation failures and race conditions during pip install.



If the Ansible pip task hangs or times out, adding the --no-cache-dir flag to the task's extra_args can resolve issues related to a corrupted package cache.



The ansible-lint package is a required development dependency for checking Ansible code and must be installed via pip.



The python_deps Ansible role installs large, time-consuming Python packages (e.g., torch, torchvision, torchaudio) from a custom PyTorch index URL. The pip installation task uses a long async timeout (1200 seconds) to accommodate this.



To idempotently manage changes to systemd service files in Ansible without causing premature service restarts, create a dedicated handler that only performs a daemon-reload. The task that templates the service file should notify this daemon-reload handler. Handlers that restart the service can then be notified by subsequent configuration tasks.



When using Ansible's ansible.builtin.uri module for service health checks, it may fail on hosts with IPv6 enabled due to malformed URLs. To ensure reliability, explicitly use ansible_default_ipv4.address in the URL.



The project utilizes two distinct AI agent architectures, both documented in AGENTS.md: 1. A runtime "Mixture of Experts" (MoE) where a Router agent delegates to specialized Experts. 2. A development "Ensemble of Agents" (e.g., Problem Scope Framing, Code Clean Up) for workflow automation.



The requirements-dev.txt file contains incorrect or redundant entries (e.g., yaml in addition to the correct pyyaml) that can break dependency installation.



Installing all dependencies from requirements-dev.txt can time out due to large packages like torch. If only a subset of tools is needed for a task, installing the specific package directly is an effective workaround.



When updating documentation, do not remove existing sections like configuration or usage guides, as this is considered a regression.



The scripts/lint.sh script can misapply linters; for example, it may run yamllint on Markdown files. Manually running the correct linter for a specific file (e.g., npx markdownlint-cli AGENTS.md) is a valid workaround.



A script at scripts/ansible_diff.sh exists to compare Ansible playbook --check runs against a stored baseline to detect potential changes.



A CI-friendly wrapper script, scripts/ci_ansible_check.sh, provides pass/fail exit codes based on the output of ansible_diff.sh for use in automated workflows.



The repository has a GitHub Actions CI workflow in .github/workflows/ci.yml that runs jobs for linting, unit testing, and Ansible change detection.



The Ansible change detection job in the CI workflow uses actions/cache to persist the ansible_run.baseline.log file between runs, ensuring stateful comparisons.



In Ansible, the task that creates a systemd service file must be executed before any tasks that notify a handler to restart that service. Otherwise, the handler may be called before the service unit exists, causing a 'service not found' error.



When using the ansible.builtin.systemd module to manage a service for the first time in a playbook run, it is crucial to include daemon_reload: yes to ensure systemd registers the new service unit file before attempting to start or enable it.



The bootstrap.sh script can be run with the --debug flag to save the full Ansible playbook output to playbook_output.log.



Ansible roles that compile software from a git repository (e.g., whisper_cpp) should ensure idempotency by fetching the latest commit hash from the remote, comparing it to a version stored locally on the target machine (e.g., in /usr/local/etc/), and only performing the build if the hashes differ.



To ensure idempotency for Ansible tasks using the ansible.builtin.script module, the creates argument should be used to specify a path that, if it exists, will cause the task to be skipped.



In Ansible playbooks, potentially disruptive or long-running tasks (like purging Nomad jobs or running benchmarks) should be made conditional on boolean variables (e.g., when: run_benchmarks) to prevent them from running on every execution.



The Nomad service is configured to bind to the host's advertise_ip (defined in group_vars/all.yaml), not localhost. Ansible tasks checking the Nomad API must use this variable.



Command-line arguments for bootstrap.sh (e.g., --flush-cache, --external-model-server) are parsed and passed as --extra-vars to the underlying ansible-playbook command, rather than being handled directly by the shell script itself.



The bootstrap.sh script can be run with the --flush-cache flag, which passes a flush_cache=true variable to the Ansible playbook to handle the deletion of the ~/.cache/torch directory.



The command to run the unit test suite is python -m unittest discover testing/unit_tests.



The project's Python dependencies for testing are spread across multiple files: requirements-dev.txt (root), ansible/roles/python_deps/files/requirements.txt, and prompt_engineering/requirements-dev.txt.



When an ansible.builtin.shell task uses bash-specific features like set -o pipefail, it may fail with an "Illegal option" error if the default shell is /bin/sh. The fix is to explicitly set executable: /bin/bash on the task.



When parsing JSONL files in Ansible, Jinja2's map('from_json') filter is brittle as it fails the entire task on the first invalid line. A more robust method is to use an ansible.builtin.shell task to iterate through each line, validate it with a tool like jq, and only process the valid JSON lines.



Ansible's rescue blocks do not catch Jinja2 template parsing errors, as they occur before the task executes. A failing from_json filter within a template will prevent the task's rescue path from being triggered.



The faster-whisper STT provider is installed as a Python dependency via the python_deps role (from ansible/roles/python_deps/files/requirements.txt) and is not managed by a dedicated Ansible role.



The project is refactoring Ansible logic from standalone task files (like setup_whisper_cpp.yaml) into dedicated, self-contained roles (like the whisper_cpp role).



To ensure Ansible's unarchive module is idempotent, use the creates parameter to specify a file that, if it exists, will cause the task to be skipped. For example, when unarchiving CNI plugins, creates: /opt/cni/bin/bridge prevents re-extraction.



In Ansible, combining a 'roles:' section and a 'tasks:' section within the same play can prevent handlers from being loaded correctly. The correct solution is to split the single play into two distinct plays: one exclusively for the 'roles:' section and a second for the 'tasks:' section.



Local handlers defined within an Ansible playbook (e.g., promote_controller.yaml) can override handlers with the same name that are defined within an included role. This can cause 'handler not found' errors if a notification is intended for the role's handler but is instead caught by a conflicting local handler.



The promote_controller.yaml playbook defines its own local handlers, including one for restarting Nomad, which can conflict with the handler defined in the nomad role.



When Ansible playbook logs are truncated or inconclusive, the status of the target service (e.g., systemctl status nomad) can be used as a reliable alternative to verify a successful run.



In Ansible, handlers defined in roles that are loaded dynamically within a task loop (using include_role) are not registered at the play level and cannot be notified. To ensure handlers are available, roles with handlers must be included statically in the top-level roles: section of the play.



When debugging, prioritize identifying the root cause of the initial error message (e.g., "Temporary failure in name resolution") before attempting complex refactoring of seemingly related code.



When Ansible tasks fail with transient network errors like 'Temporary failure in name resolution', the preferred solution is to make the task resilient by adding a retry loop (until, retries, delay) rather than altering unrelated playbook structures.



The primary source for runtime Python dependencies is ansible/roles/python_deps/files/requirements.txt. Development dependencies are in requirements-dev.txt.



User requires comprehensive docstrings for all public code elements (functions, classes, methods) following language-specific style guides (e.g., Google Style for Python).



AGENTS.md provides essential instructions for local development setup and testing procedures.



User has indicated a preference for submitting completed work even if unrelated tests are failing due to environment issues, rather than spending excessive time on debugging the environment.



To set up a local development environment, create a Python virtual environment and install dependencies from requirements-dev.txt. Runtime dependencies are in ansible/roles/python_deps/files/requirements.txt.



User requires the main README.md to be a complete and up-to-date guide for new developers.



User instruction: Do not ask clarifying questions until the assigned task is fully completed.



In Nomad HCL, to select a USB device within a device block, a constraint sub-block should be used. The attribute must be namespaced with the device type (e.g., usb.class_id), and the value should be the class ID in decimal format.



The av Python package requires the ffmpeg development libraries (e.g., libavdevice-dev on Debian/Ubuntu) to be installed on the system for successful compilation.



The PyAudio Python package requires the portaudio development libraries (e.g., portaudio19-dev on Debian/Ubuntu) to be installed on the system for successful compilation.



The openevolve Python package, a dependency for some tests, is defined in prompt_engineering/requirements-dev.txt.



To run the unit test suite in a minimal environment, problematic modules like pyaudio, faster_whisper, piper.voice, and playwright must be mocked to bypass ImportError issues.



To generate a test coverage report for the ansible and supervisor directories, run the command python -m pytest --cov=ansible --cov=supervisor --cov-report=term-missing testing/unit_tests/ within the activated virtual environment.



The testing environment is difficult to set up due to Python packages with heavy system-level dependencies (e.g., pyaudio, av, playwright). A full pip install of all requirements often fails.



The RAG tool, located at ansible/roles/pipecatapp/files/tools/rag_tool.py, uses a FAISS vector index for its knowledge base search.



The test suite has a known, unrelated failing test: test_playbook_integration_syntax_check. This failure should be ignored unless the task is specifically to fix it.



In the development environment, if a file is confirmed to exist via ls but tools like read_file or replace_with_git_merge_diff fail with a 'file not found' error, deleting and recreating the file can resolve the issue.



In Nomad HCL, the volume_mount block must be defined inside the group block, not the task block. Placing it incorrectly can lead to misleading parsing errors like "Unsupported argument".



When an Ansible handler restarts a service like Nomad, a race condition can occur if other tasks or handlers try to use the service's API before it is fully initialized. To prevent this, the restart handler itself should include a task that polls the service's API endpoint until it receives a successful response, ensuring the service is ready before the playbook continues.



When refactoring an Ansible handler, its name must be preserved to avoid breaking existing notify directives. To add logic like a post-restart wait task, use a block to group the actions within the existing named handler.



When an Ansible task using the slurp module is skipped due to a when condition, the registered variable is still created but will lack the content key. Conditional logic should check for the key's existence (e.g., 'content' in my_variable) rather than just if the variable is defined (my_variable is defined) to avoid errors.



In Nomad HCL, keys within an env block must not be quoted. For example, use KEY = "value" instead of "KEY" = "value".



The bootstrap.sh script may fail to find executables installed via pyenv because it does not use the pyenv execution environment. To work around this, run executables like ansible-playbook directly using their full path.



To run the main playbook directly, use the command: /home/jules/.pyenv/versions/3.12.12/bin/ansible-playbook -i local_inventory.ini playbook.yaml --extra-vars="target_user=jules". To speed up execution, add external_model_server=true to the extra vars.



The Ansible playbook execution can time out in the interactive environment due to long-running tasks like pip install or cmake --build. Running the playbook command in the background (&) is a valid workaround.



The llama.cpp Ansible role ensures idempotent builds by comparing the latest remote git commit hash with a locally stored version hash in /usr/local/etc/llama-cpp.version. Recompilation is skipped if the hashes match.



When executing nomad commands via Ansible, the NOMAD_ADDR environment variable must be set, typically to http://{{ ansible_default_ipv4.address }}:4646.



Ansible roles that deploy Nomad services follow a pattern: a task in tasks/main.yaml templates the Nomad job file to /opt/nomad/jobs/ and notifies a handler. The handler, defined in handlers/main.yaml, then executes nomad job run to apply the changes.



The advertise_ip variable, defined in group_vars/all.yaml, should be used in service templates (e.g., Nomad jobs) for the host's IP address, particularly for connecting to host services like Consul.



The Home Assistant deployment is configured to be asynchronous. The Ansible home_assistant role uses async: 300 and poll: 0 to run the Nomad job without waiting for it to become healthy. The config_manager role uses a non-blocking stat check to conditionally extract the auth token if/when it becomes available.



The Home Assistant Nomad job template (home_assistant.nomad.j2) has a circular dependency where it requires home_assistant_token, a variable which is only generated after Home Assistant starts. This is resolved by using a Jinja2 default('') filter to provide an empty string for the token on the initial run.



Jinja2 templates that are converted to JSON cannot contain comments, as this will cause a templating error during the conversion.



The unit test testing/unit_tests/test_home_assistant_template.py is fragile and will fail when run outside a full Ansible execution context because it depends on the hostvars variable. The test needs to be skipped or have hostvars mocked to pass.



To run Ansible commands, ansible-core must be installed in the pyenv environment via pip.



The unit test suite is executed by running the ./testing/run_unit_tests.sh script.



Nomad job files are written in HCL, not YAML. Unit tests that validate rendered Nomad templates should use string assertions rather than attempting to parse the file as YAML.



Home Assistant's authentication data, including the Long-Lived Access Token, is stored on the host machine at /opt/nomad/volumes/ha-config/.storage/auth_provider.homeassistant.



The Home Assistant Long-Lived Access Token is not pre-configured; it is generated by Home Assistant after its initial startup.



The project utilizes two distinct Home Assistant tools: HomeAssistantTool provides structured methods like call_service and get_state, while HA_Tool uses a natural language-based call_ai_task method. Both are necessary to maintain full feature parity.



The Home Assistant tools (HomeAssistantTool and HA_Tool) require a Long-Lived Access Token. Ansible's config_manager role stores this in Consul at config/hass/token, which is then loaded into the application configuration under the key ha_token.



Do not remove code that appears redundant without first verifying that it will not cause a feature regression. Some components may have overlapping but distinct purposes.



The pipecat-ai library has updated its VAD implementation. The previously used pipecat_whisker.WhiskerObserver has been replaced by pipecat.audio.vad.silero.SileroVADAnalyzer, which requires the [silero] extra.



The world_model_service is a core component of the "home brain" architecture, responsible for maintaining a centralized state representation of the home environment by listening to MQTT messages and querying other services like Consul.



The project contains two distinct long-term memory systems: a MemoryStore for conversational history and a RAG_Tool for documentation Q&A. Both were originally implemented with local FAISS indexes.



When building a Docker image with Ansible, ensure the application files are copied into the image via the Dockerfile. Do not use redundant artifact blocks in the corresponding Nomad job file to load the same files.



When refactoring a module or class, it is critical to also update all the code that calls it to match the new interface (e.g., constructor arguments). Failure to do so will result in runtime errors.



In Nomad job files for locally-built Docker images, do not use force_pull = true, as it may cause failures by trying to pull from a remote registry. Rely on specific image tags for updates.



When configuring Nomad jobs with host volumes, it's crucial to use Nomad's top-level volume and volume_mount directives as the single source of truth. Avoid using the Docker driver's volumes directive simultaneously, as it can lead to conflicts and unpredictable behavior.



When a Nomad job's service fails to start, a common cause is a mismatch between the directory structure created by Ansible on the host and the paths expected by the service inside the container. It's crucial to ensure that volume mounts and configuration file paths are consistent between the Ansible role and the Nomad job template.



To ensure Nomad services start correctly, any host directories required for host_volume mounts must be created before the Nomad service is started or restarted by Ansible.



The nomad Ansible role is responsible for creating the /opt/nomad/jobs directory, which is required for other roles to template their job files.



A Nomad agent cannot be configured as both a server and a client in the same configuration file (nomad.hcl.client.j2). The server block should be removed from client configurations.



The .yamllint configuration forbids the use of --- to start a document (document-start: present: false). Ansible task files should not begin with ---.



The project architecture is a modular, containerized system on a Nomad cluster, communicating via MQTT. Key components include Home Assistant, a conversational AI pipeline (pipecat), Frigate for computer vision, and a vector database for memory.



The ansible-lint executable is located at /home/jules/.pyenv/versions/3.12.12/bin/ansible-lint and should be run from there if the pyenv shim is not available.



The langchain.text_splitter module has been deprecated and its contents moved to the langchain-text-splitters package.



It is crucial to stay focused on the user's immediate request and not implement larger, unrequested features from previous architectural discussions.



To validate an Ansible playbook's syntax and role dependencies without running it, use ansible-playbook --syntax-check. This is more suitable for integration unit tests than ansible-lint, which also checks for stylistic issues.



In Ansible, the loop keyword must be at the same indentation level as the task attributes (e.g., name, register), not indented under them.



Use a pytest.ini file with a custom marker (e.g., requires_display) and addopts = -m "not requires_display" to cleanly skip tests that need a graphical environment. This is preferable to using @pytest.mark.skip on individual tests.



The open3d library requires system-level dependencies libgl1-mesa-glx, libgl1-mesa-dev, and libglu1-mesa-dev to be installed.



When using pyautogui in a headless environment, tests must be run with xvfb-run to provide a virtual display. To avoid import errors during test collection, pyautogui should be imported within the functions that use it, rather than at the module level.



The Python testing environment is managed with pyenv and the correct Python executable path is /home/jules/.pyenv/versions/3.12.12/bin/python.



To address PyTorch UserWarnings about deprecated TF32 settings, explicitly set the new precision flags (e.g., torch.backends.cuda.matmul.fp32_precision = 'high') in the application's entry point (app.py) after importing torch. This ensures future compatibility and silences the warning.



In Ansible, to handle potential TypeError when flattening a list of lists with the sum filter, use the select('list') filter first. This ensures that only list elements are passed to sum, preventing errors if the data contains non-list items.



The Ansible combine filter does not accept a default argument. When combining dictionaries that might not exist, a conditional check should be used to provide a default empty dictionary ({}) to the filter.



The download_models Ansible role is designed to handle STT models from different providers (e.g., whisper-cpp, faster-whisper) by organizing them into provider-specific subdirectories under /opt/nomad/models/stt/. The model structure is defined in group_vars/models.yaml under the stt_models key.



The term.everything Ansible role requires the podman package to be installed to build the AppImage.



The bootstrap.sh script should check if nomad is installed before attempting to use it to prevent errors on a fresh setup.



Configuration for third-party LLM experts is stored in group_vars/external_experts.yaml.



The main playbook playbook.yaml should define vars_files at the top level of the playbook to avoid redundancy and ensure all plays have access to the same variables.



In Ansible, the variable namespace is a reserved keyword for a special Jinja2 Namespace object and should not be used as a variable name for strings. A different name, such as nomad_namespace, must be used to avoid template rendering errors. A vars block within a task can also shadow global variables, causing this issue.



The remote development workflow uses mosh for stable connections and tmux for persistent sessions. This is documented in REMOTE_WORKFLOW.md.



The REMOTE_WORKFLOW.md file recommends using helix, yazi, and lazygit as optional tools to enhance the development experience, with provided configurations.



The Ansible debug module does not accept mode or become parameters. Incorrectly adding them can cause YAML syntax errors.



In Ansible, a task name with a colon requires quotes to avoid YAML parsing errors.



The project has automated linting scripts, fix_yaml.sh and fix_markdown.sh, in the scripts/ directory to automatically fix common linting errors.



Always wait for explicit user approval before beginning a multi-step plan, especially one involving code modifications. Do not bundle unrequested changes with requested ones.



Expert agents (main, coding, math, extract) are defined by prompt files in ansible/roles/pipecatapp/files/prompts/ and their models are configured in group_vars/models.yaml.



The Router Agent is the only agent with access to tools. It is implemented in ansible/roles/pipecatapp/files/app.py and configured by ansible/roles/pipecatapp/files/prompts/router.txt.



When using loop in Ansible, it is not possible to use it directly on a block of tasks. The include_tasks module should be used instead to loop over a separate file containing the tasks.



The ansible-lint tool enforces that variables defined within a role are prefixed with the role's name.



The EVALUATOR_GENERATOR.md file is documentation and should not be treated as an agent definition file during testing.



When creating a log entry in Ansible, it's better to use regex_findall instead of regex_search as it returns an empty list instead of None when no match is found, which is easier to handle. Additionally, including comprehensive details like a timestamp, return code, stdout, and stderr in the log entry is a good practice for easier debugging.



Ansible's include_tasks with a relative path resolves the file path relative to the directory where the top-level playbook is being executed, not relative to the role's tasks directory where the include_tasks statement is located.



The Ansible task to create Nomad job files requires become: yes to have permission to write to the /opt/nomad/jobs directory.



The nomad_namespace variable must be globally available to all Ansible roles. Defining it in group_vars/all.yaml is the correct approach to ensure it's accessible during template rendering.



The user wants to pre-generate all Nomad job files for all experts at deployment time, but only run the main expert's job. The other experts will be started on-demand by the application.



The TODO.md file serves as the primary document for tracking the project's status and synchronizing understanding between the user and the agent.



The user wants to be shown a discrepancy report for review before any changes are made to the codebase.



The project uses npm run lint to execute a scripts/lint.sh script that runs multiple linters, including yamllint, markdownlint-cli, and djlint.



The consul Ansible role defines its default data directory as /opt/consul in roles/consul/defaults/main.yaml.



The nomad Ansible role defines its default data directory as /opt/nomad in roles/nomad/defaults/main.yaml.



The API endpoints are defined in ansible/roles/pipecatapp/files/web_server.py using the FastAPI framework.



The project uses pytest as its testing framework. Unit tests for app.py are in testing/unit_tests/test_pipecat_app.py.



The expert.nomad.j2 template requires both job_name and expert_name variables to be defined in the calling Ansible task.



The bootstrap.sh script can be run with the --external-model-server flag to skip large model downloads and builds.



The rpc-server executable from llama.cpp uses short-form arguments -H for host and -p for port, not the long-form --host and --port which can cause parsing errors.



The intended architecture for model health checks is to start the llama-server for each model, verify it's healthy, and then immediately shut it down to conserve resources, rather than keeping all models running.



The llama-server command-line argument for specifying RPC servers is --rpc, not --rpc-server.



In shell scripts, especially within Nomad job files, always check if a process ID variable (e.g., $server_pid) is set and not empty ([ -n "$server_pid" ]) before using it with commands like kill or wait. This prevents script failures if the process fails to start and the PID variable is not assigned.



A reusable library, prompt_engineering/evaluation_lib.py, contains common functions for deploying and testing code in a Nomad/Consul environment.



The openevolve workflow evaluates the performance of generated code (specifically app.py), not just text prompts. It does this by deploying the code in a Nomad environment and running integration tests.



Generated evaluator scripts are stored in the prompt_engineering/generated_evaluators/ directory, which is ignored by git.



Agent-facing documentation for generating evaluators is located at prompt_engineering/agents/EVALUATOR_GENERATOR.md.



A generator script, prompt_engineering/create_evaluator.py, exists to create new, specific evaluator scripts from a template, based on provided parameters.



The pytest-asyncio package is required to run tests that use async functions with pytest.



The llama-server command-line argument -fa is a shorthand for --flash-attn. Using the shorthand with a value can cause parsing errors.



To use a host_volume in a Nomad job with the raw_exec or exec drivers, the volume block must be defined inside the group block, not at the top level of the job.



The pytest-mock library is a development dependency and is required for tests that use the mocker fixture.



The main agent prompt, prompts/router.txt, instructs the LLM to analyze screenshots and use coordinate-based tools (click_at, type_text_at) for desktop and web interactions.



The agent possesses a vision-based desktop automation capability. It uses a DesktopControlTool with the pyautogui library to take screenshots, and perform coordinate-based clicks and keyboard typing.



The agent's web browser tool, WebBrowserTool, has been enhanced with vision-based interaction methods (get_screenshot, click_at, type_text_at) to complement its existing selector-based methods.



The TwinService in app.py operates in a vision-centric loop (run_agent_loop). It repeatedly captures the screen, calls a vision-capable LLM with the image and conversation history, and executes the returned tool call.



Nomad's exec and raw_exec drivers must be explicitly enabled in the client configuration to allow jobs to use them.



When an Ansible template file (e.g., a .j2 file) contains template syntax for another engine (like Nomad's {{ env "..." }}), the inner template delimiters must be escaped using Jinja2's syntax (e.g., {{ '{{' }} env "..." {{ '}}' }}) to prevent Ansible from interpreting them.



The nomad client configuration requires the nomad_models_dir variable to be defined in group_vars/all.yaml to properly configure the models host volume.



When registering the result of an Ansible loop with the register keyword, each item in the resulting list is an object containing the original item nested inside it. To access the original properties, use item.item.property.



The pipecatapp Python application fetches its configuration from Consul KV at startup.



The bootstrap.sh script is the primary entry point for running the Ansible playbook. It handles environment setup, including checking for the ansible-playbook executable and passing necessary arguments.



The PXE boot process can be configured to use either Debian or NixOS as the host operating system, selectable via the pxe_os variable in group_vars/all.yaml.



Ansible roles should use fully qualified collection names (FQCN) for modules (e.g., ansible.builtin.file instead of file) to avoid ambiguity and improve clarity.



The nixos_pxe_server Ansible role uses a declarative configuration.nix file to configure DHCP, TFTP, and Nginx for PXE booting, and to build a minimal NixOS netboot environment.



The ansible-lint tool is used to check Ansible code for best practices, style issues, and potential errors.



Ansible handlers should be used to trigger actions like service restarts or system rebuilds only when configuration files change, making playbooks more efficient and idempotent.



The playbook.yaml file explicitly loads variables from group_vars/models.yaml.



The Ansible community.general.consul_kv module has been replaced with ansible.builtin.uri to interact with the Consul API directly, avoiding Python dependency conflicts.



The group_vars/all.yaml file defines a list of expert names under the experts variable.



The group_vars/models.yaml file defines the expert_models dictionary, which contains model configurations for different experts (e.g., main, coding).



The config_manager role in Ansible is responsible for populating Consul KV with model and application configurations.



When running Ansible playbooks that require variables for top-level attributes like remote_user, those variables must be passed as extra vars (-e) on the command line, as vars_files are processed after these attributes are evaluated.



The nomad job run command uses the -var flag to pass variables, not -meta.



The download_models Ansible role uses the ansible.builtin.stat module to check for the existence of model files before downloading them, ensuring idempotency.



The Python virtual environment for the application is located at /opt/pipecatapp/venv.



The expert.nomad job dynamically fetches its model configuration from Consul KV based on the NOMAD_VAR_expert_name environment variable.



In Ansible, when a variable's definition depends on an inventory group (e.g., expected_cluster_size: "{{ groups['workers'] | length }}"), it's crucial to provide a default value using a conditional check like groups['workers'] | length if 'workers' in groups else 1. This makes the playbook more robust by preventing 'undefined variable' errors when running with inventories that do not define that specific group. The default() filter is insufficient if the parent dictionary (groups) itself might not contain the key (workers).



The project uses Consul KV as the central source of truth for runtime configuration.



The pipecatapp application discovers available expert services by querying Consul for services with the expert tag.



The download_models Ansible role queries the Consul KV store to determine which models to download.



The python-consul library is outdated and incompatible with Python 3.12+; python-consul2 should be used instead as a drop-in replacement.



The reflection/reflect.py script makes live API calls to an LLM to diagnose Nomad job failures and can use tools to gather more information.



The heal_job.yaml playbook can perform 'restart' and 'increase_memory' actions based on the output of the reflection/reflect.py script.



Unit tests that involve subprocess calls should be mocked to ensure they are isolated and do not depend on external services or file systems.



The pipecatapp role requires the directory /opt/pipecatapp to exist before the nomad service starts, as it is configured as a required host volume.



The pipecatapp role's main.yaml contains a task to install Playwright browsers, which must use the correct path to the Python virtual environment.



The pipecatapp Ansible role is responsible for deploying Nomad jobs, including the main application and other related services.



Nomad job templates (.nomad.j2) can be used with Ansible's template module to inject secrets and other variables, such as OPENAI_API_KEY, into the job definition.



Nomad batch jobs can be scheduled to run periodically using the periodic block within the job file.



The project has an existing 'expert routing' system defined by prompts in ansible/roles/pipecatapp/files/prompts, which is distinct from the development workflow agents.



Unit tests for agent definition markdown files are located in testing/unit_tests/test_agent_definitions.py and validate the schema of the files.



Async functions under test require their mocks to be AsyncMock instances to be awaitable.



The app.py file in ansible/roles/pipecatapp/files/ uses a TwinService class to manage the main agent logic.



The prompt_engineering/evolve.py script uses the openevolve library to iteratively improve prompts.



The TwinService's get_system_prompt method constructs the main system prompt, starting with a base prompt from prompts/router.txt.



Prompt performance is evaluated using test cases defined in YAML files within the prompt_engineering/evaluation_suite/ directory.



The prompt evolution workflow is managed by scripts in the prompt_engineering/ directory.



The user wants to structure the workflow around an 'ensemble of agents' concept, where each agent has a specific role.



The agent roles are: Problem Scope Framing, Architecture Review, New Task Review, Debug and Analysis, and Code Clean Up.



Agent definitions, including their roles and backing LLM models, are to be stored in markdown files within the prompt_engineering/agents/ directory.



The jq package is a system dependency and is installed via the system_deps Ansible role.



The llama-server requires the --flash-attn flag to have a value (on, off, or auto).



The project's integration tests (testing/integration_tests/) require a running instance of the pipecat application and its dependencies, including the Consul service, to pass.



The project contains multiple test files with the same name in different directories (e.g., in ansible/ vs docker/, and testing/unit_tests vs testing/integration_tests). To avoid import file mismatch errors, pytest should be run on specific directories rather than on the root.



The supervisor.py script is the core of a self-healing loop that uses Ansible playbooks to check, diagnose, and heal failed system jobs.



Unit tests for supervisor.py are located in testing/unit_tests/test_supervisor.py.



When running E2E tests, the pipecat application and its dependencies must be running.



The project's Python tools (e.g., mcp_tool.py, ansible_tool.py) are located in ansible/roles/pipecatapp/files/tools/.



Ansible pipelining is disabled in ansible.cfg (pipelining = False) to avoid privilege escalation issues.



The main Ansible playbook (playbook.yaml) requires the target_user variable to be defined.



End-to-end tests are defined in the e2e-tests.yaml Ansible playbook.



