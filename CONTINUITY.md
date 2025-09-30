# Continuity Document: Flexible Pipecat Deployment

## 1. Objective

The user wants the ability to deploy the `pipecatapp` application using one of two methods:
1.  **`raw_exec`**: The original method, where Ansible sets up the environment directly on the target machine. This is ideal for debugging.
2.  **`docker`**: A containerized deployment for robustness and predictability.

The choice of deployment method should be controlled by a `--pipecat-docker` command-line flag in the `bootstrap.sh` script.

## 2. Current Status

The current environment is unstable, preventing progress. The workspace should be considered to be in its original state, before any containerization work was attempted. The previous strategy of complex conditional logic within a single Ansible role has been abandoned in favor of a cleaner, flag-based approach suggested by the user.

## 3. High-Level Plan

The agreed-upon plan is as follows:

1.  **Create Docker Artifacts**: Re-create the `Dockerfile` and all related build files for the containerized version of `pipecatapp`.
2.  **Create Separate Nomad Job Files**: Maintain two distinct Nomad job files, one for each deployment method (`pipecatapp.raw_exec.nomad` and `pipecatapp.docker.nomad`).
3.  **Update `bootstrap.sh`**: Add a `--pipecat-docker` flag to the script to capture the user's deployment choice.
4.  **Update Ansible Logic**: Modify the main Ansible playbook to pass the flag's value to the `pipecatapp` role, which will then execute the appropriate deployment tasks and use the correct Nomad job file.

## 4. Detailed Steps for Next Instance

Here are the specific steps to be taken to complete the task:

### Step 1: Create Docker Build Artifacts

1.  **Create Build Context Directory**:
    ```bash
    mkdir -p docker/pipecatapp
    ```
2.  **Copy Application Source**: Manually read the contents of each file and directory from `ansible/roles/pipecatapp/files/` and recreate them inside `docker/pipecatapp/`. This includes:
    - `app.py`
    - `memory.py`
    - `moondream_detector.py`
    - `web_server.py`
    - The `tools/` directory and all its contents.
    - The `static/` directory and all its contents.
    - The `prompts/` directory and all its contents.
3.  **Copy Requirements File**: Recreate `ansible/roles/python_deps/files/requirements.txt` at `docker/pipecatapp/requirements.txt`.
4.  **Create `start_pipecat.sh`**: Create a simple startup script at `docker/pipecatapp/start_pipecat.sh` to be the container's entrypoint.
5.  **Create `Dockerfile`**: Create a `Dockerfile` at `docker/pipecatapp/Dockerfile` that:
    - Starts from a `python:3.10-slim` base image.
    - Installs all necessary system dependencies from the original `pipecatapp` Ansible role.
    - Creates and uses a Python virtual environment.
    - Installs all Python packages from `requirements.txt`.
    - Installs Playwright browsers.
    - Copies the application code into the image.
    - Sets `start_pipecat.sh` as the `ENTRYPOINT`.

### Step 2: Create and Segregate Nomad Job Files

1.  **Rename Original Job File**: Rename `ansible/jobs/pipecatapp.nomad` to `ansible/jobs/pipecatapp.raw_exec.nomad`.
2.  **Create Docker Job File**: Create a new file, `ansible/jobs/pipecatapp.docker.nomad`, that is configured to use the `docker` driver and run the `pipecatapp:latest` image.

### Step 3: Update `bootstrap.sh`

1.  **Add Argument Parsing**: Modify the argument parsing logic in `bootstrap.sh` to recognize a `--pipecat-docker` flag.
2.  **Pass to Ansible**: If the flag is present, pass an extra variable to the `ansible-playbook` command, for example: `--extra-vars "pipecat_docker=true"`.

### Step 4: Update the `pipecatapp` Ansible Role

1.  **Make Role Conditional**: Modify `ansible/roles/pipecatapp/tasks/main.yaml`.
2.  **`raw_exec` Block**: Wrap all the existing tasks (installing dependencies, copying files, etc.) in a `block` with the condition: `when: not pipecat_docker|default(false)`.
3.  **Template Deployment**: Modify the task that deploys the Nomad job to use a variable in its `src` path, like so: `src: ../../jobs/pipecatapp.{{ 'docker' if pipecat_docker|default(false) else 'raw_exec' }}.nomad`.

### Step 5: Finalize

1.  **Verify**: Run `bootstrap.sh` both with and without the `--pipecat-docker` flag to ensure both deployment methods work correctly.
2.  **Review**: Request a code review.
3.  **Submit**: Submit the final, working solution.