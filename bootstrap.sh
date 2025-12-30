#!/bin/bash
#
# Easy Bootstrap Script for Single-Node Setup
#
# This script simplifies the process of bootstrapping the system on a single
# server for development or as the initial control node for a new cluster.
# It runs the main Ansible playbook using a local inventory file.

# --- Help Menu ---
show_help() {
    echo "Usage: $0 [options]"
    echo ""
    echo "This script runs the main Ansible playbook to bootstrap the system."
    echo ""
    echo "Options:"
    echo "  --role <role>                Specify the role for this node (all, controller, worker). Default: all."
    echo "  --controller-ip <ip>         Required if --role is 'worker'. IP address of the controller node."
    echo "  --tags <tags>                Comma-separated list of Ansible tags to run."
    echo "  --user <user>                Specify the target user for Ansible. Default: pipecatapp."
    echo "  --purge-jobs                 Stop and purge all running Nomad jobs before starting."
    echo "  --clean                      Clean the repository of all untracked files (interactive prompt)."
    echo "  --debug                      Enable verbose Ansible output and log to playbook_output.log."
    echo "  --leave-services-running     Do not clean up Nomad and Consul data on startup."
    echo "  --external-model-server      Skip large model downloads and builds, assuming an external server."
    echo "  --continue                   Resume from the last successfully completed playbook."
    echo "  --benchmark                  Run benchmark tests."
    echo "  --deploy-docker              Deploy the pipecat application using Docker (Default)."
    echo "  --run-local                  Deploy the pipecat application using local raw_exec (for debugging)."
    echo "  --home-assistant-debug       Enable debug mode for Home Assistant."
    echo "  --container                  Run the entire infrastructure inside a single large container."
    echo "  --watch <target>             Pause for inspection after the specified target (task/role) completes."
    echo "  -h, --help                   Display this help message and exit."
}

# --- Initialize flags ---
USE_CONTAINER=false
CLEAN_REPO=false
DEBUG_MODE=false
EXTERNAL_MODEL_SERVER=false
LEAVE_SERVICES_RUNNING=false
PURGE_JOBS=false
CONTINUE_RUN=false
ROLE="all" # Default role
CONTROLLER_IP=""
ANSIBLE_ARGS=() # Use an array for Ansible arguments
LOG_FILE="playbook_output.log"
STATE_FILE=".bootstrap_state"

# --- Parse command-line arguments ---
ORIGINAL_ARGS=("$@")
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --role)
        ROLE="$2"
        shift
        shift
        ;;
        --controller-ip)
        CONTROLLER_IP="$2"
        shift
        shift
        ;;
        --tags)
        ANSIBLE_TAGS="$2"
        shift
        shift
        ;;
        --purge-jobs)
        PURGE_JOBS=true
        shift
        ;;
        --clean)
        CLEAN_REPO=true
        shift
        ;;
        --debug)
        DEBUG_MODE=true
        shift
        ;;
        --leave-services-running)
        LEAVE_SERVICES_RUNNING=true
        shift
        ;;
        --external-model-server)
        EXTERNAL_MODEL_SERVER=true
        shift
        ;;
        --continue)
        CONTINUE_RUN=true
        shift
        ;;
        --user)
        TARGET_USER="$2"
        shift
        shift
        ;;
        --benchmark)
        BENCHMARK_MODE=true
        shift
        ;;
        --deploy-docker)
        ANSIBLE_ARGS+=(--extra-vars "pipecat_deployment_style=docker")
        shift
        ;;
        --run-local)
        ANSIBLE_ARGS+=(--extra-vars "pipecat_deployment_style=raw_exec")
        shift
        ;;
        --home-assistant-debug)
        ANSIBLE_ARGS+=(--extra-vars "home_assistant_debug_mode=true")
        shift
        ;;
        --container)
        USE_CONTAINER=true
        shift
        ;;
        --watch)
        WATCH_TARGET="$2"
        ANSIBLE_ARGS+=(--extra-vars "watch_target=$WATCH_TARGET")
        shift
        shift
        ;;
        -h|--help)
        show_help
        exit 0
        ;;
        *)
        echo "Unknown option: $1"
        show_help
        exit 1
        ;;
    esac
done

# --- Validate Arguments ---
if [ "$ROLE" = "worker" ] && [ -z "$CONTROLLER_IP" ]; then
    echo "Error: --controller-ip is required when using --role=worker"
    exit 1
fi

# --- Move to the script's directory ---
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR"

# --- Container Mode ---
if [ "$USE_CONTAINER" = true ]; then
    echo "--- Running in Container Mode ---"

    # --- Host-side Cluster Detection ---
    check_for_existing_cluster() {
        echo "--- Checking for existing cluster on host ---"
        CLUSTER_EXISTS=false
        if nc -z localhost 4646 2>/dev/null || nc -z localhost 8500 2>/dev/null; then
            echo "✅ Detected existing Nomad/Consul service on the host."
            CLUSTER_EXISTS=true
        else
            echo "ℹ️  No existing cluster detected on the host. Will start a new one."
        fi
    }

    # Check if we are already inside the container
    if [ -f "/.dockerenv" ] && [ "$(hostname)" = "pipecat-dev-runner" ]; then
        echo "✅ Already inside the container. Proceeding with bootstrap..."
    else
        IMAGE_NAME="pipecat-dev-container"
        CONTAINER_NAME="pipecat-dev-runner" # Keep original name to avoid regression

        check_for_existing_cluster

        echo "Building container image: $IMAGE_NAME..."
        if ! docker build -t "$IMAGE_NAME" docker/dev_container/; then
            echo "❌ Failed to build container image."
            exit 1
        fi

        echo "Checking for existing container..."
        if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
            echo "Removing existing container..."
            docker rm -f "$CONTAINER_NAME"
        fi

        # --- Dynamically configure and start container ---
        HOST_IP=$(hostname -I | awk '{print $1}')
        if [ -z "$HOST_IP" ]; then
            echo "❌ Error: Could not determine host IP address."
            exit 1
        fi

        DOCKER_RUN_CMD=(docker run -d --privileged --name "$CONTAINER_NAME" \
            --hostname "$CONTAINER_NAME" \
            -v /sys/fs/cgroup:/sys/fs/cgroup:rw --cgroupns=host \
            -v "$SCRIPT_DIR":/opt/cluster-infra -e "HOST_IP=$HOST_IP")

        if [ "$CLUSTER_EXISTS" = true ]; then
            echo "Configuring container as a WORKER to join the existing cluster."
            CONTAINER_ROLE="worker"
            CONTAINER_CONTROLLER_IP="$HOST_IP"
            # No port mappings needed for a worker node
        else
            echo "Configuring container as a new CONTROLLER."
            CONTAINER_ROLE="all"
            CONTAINER_CONTROLLER_IP="" # This will be set inside the container
            DOCKER_RUN_CMD+=(-p 4646:4646 -p 8500:8500 -p 8080:8080 -p 8000:8000)
        fi

        DOCKER_RUN_CMD+=("$IMAGE_NAME")

        echo "Starting container with role: $CONTAINER_ROLE..."
        if ! "${DOCKER_RUN_CMD[@]}"; then
            echo "❌ Failed to start container."
            exit 1
        fi

        echo "Waiting for container to initialize..."
        sleep 5

        echo "Executing bootstrap inside the container..."
        ARGS_WITHOUT_CONTAINER=()
        for arg in "${ORIGINAL_ARGS[@]}"; do
            if [[ "$arg" != "--container" && "$arg" != "--role" && "$arg" != "--controller-ip" ]]; then
                # Filter out container-specific or now-determined args
                ARGS_WITHOUT_CONTAINER+=("$arg")
            fi
        done

        # Explicitly pass the determined role and controller IP to the script inside the container
        docker exec -it "$CONTAINER_NAME" /bin/bash -c "cd /opt/cluster-infra && ./bootstrap.sh --role ${CONTAINER_ROLE} --controller-ip ${CONTAINER_CONTROLLER_IP} ${ARGS_WITHOUT_CONTAINER[*]}"
        EXIT_CODE=$?

        echo "Container bootstrap finished with exit code: $EXIT_CODE"
        echo "You can access the container using: docker exec -it $CONTAINER_NAME /bin/bash"
        echo "To stop and remove the container: docker rm -f $CONTAINER_NAME"

        exit $EXIT_CODE
    fi
fi

# --- Run Initial Machine Setup based on Role ---
# This script handles pre-Ansible configuration like network and hostname.
# It's run for all roles, and the script itself determines what to do based on the config.
echo "--- Running Initial Machine Setup ---"
# Skip setup.sh if running inside the dev container
if [ -f "initial-setup/setup.sh" ]; then
    if [ -f "/.dockerenv" ] && [ "$(hostname)" = "pipecat-dev-runner" ]; then
         echo "🐳 Container environment detected. Skipping initial machine setup (setup.sh)."
    else
        echo "You may be prompted for your sudo password to run the initial setup script."
        sudo bash "initial-setup/setup.sh"
        echo "✅ Initial machine setup complete."
    fi
else
    echo "⚠️  Warning: initial-setup/setup.sh not found. Skipping pre-configuration."
fi


# --- Handle the --clean option ---
if [ "$CLEAN_REPO" = true ]; then
    echo "⚠️  --clean flag detected. This will permanently delete all untracked files."
    echo "This includes logs, temporary files, and build artifacts."
    echo ""
    echo "Performing a dry run to show what will be deleted:"
    echo "--------------------------------------------------"
    git clean -ndx
    echo "--------------------------------------------------"
    
    read -p "Are you sure you want to permanently delete all files and directories listed above? [y/N] " -n 1 -r
    echo # Move to a new line
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Cleaning repository..."
        git clean -fdx
        echo "✅ Repository cleaned to a pristine state."
    else
        echo "Cleanup cancelled by user. Exiting script."
        exit 1
    fi
fi

# --- Build Ansible arguments ---
if [ -n "$TARGET_USER" ]; then
    echo "Using target user from --user flag: $TARGET_USER"
    ANSIBLE_ARGS+=(--extra-vars "target_user=$TARGET_USER")
else
    echo "Using default target user: pipecatapp"
    ANSIBLE_ARGS+=(--extra-vars "target_user=pipecatapp")
fi

# FIXED: Correct 'if' statement spacing
if [ "$BENCHMARK_MODE" = true ]; then
    echo "--benchmark flag detected, running benchmarks"
    ANSIBLE_ARGS+=(--extra-vars "run_benchmarks=true")
fi

# FIXED: Updated to use ANSIBLE_ARGS array directly
if [ "$EXTERNAL_MODEL_SERVER" = true ]; then
    echo "⚡️ --external-model-server flag detected. Skipping large model downloads and builds."
    ANSIBLE_ARGS+=(--extra-vars "external_model_server=true")
fi

if [ "$PURGE_JOBS" = true ]; then
    ANSIBLE_ARGS+=(--extra-vars "purge_jobs=true")
fi

if [ "$LEAVE_SERVICES_RUNNING" = true ]; then
    echo "✅ --leave-services-running detected. Nomad and Consul data will not be cleaned up."
    ANSIBLE_ARGS+=(--extra-vars "cleanup_services=false")
else
    echo "🧹 Nomad and Consul data will be cleaned up by default. Use --leave-services-running to prevent this."
    ANSIBLE_ARGS+=(--extra-vars "cleanup_services=true")
fi
# --- Now you can use the ANSIBLE_ARGS array ---
echo "---"
echo "Running Ansible with the following arguments:"
# This 'printf' is a safe way to show the final command
printf "ansible-playbook ... %s \n" "${ANSIBLE_ARGS[@]}"

# ANSIBLE_ARGS+=(--extra-vars "$EXTRA_VARS")

if [ "$DEBUG_MODE" = true ]; then
    echo "🔍 --debug flag detected. Ansible output will be saved to '$LOG_FILE'."
    ANSIBLE_ARGS+=("-vvvv")
fi

# --- Install Python dependencies (Virtual Environment) ---
echo "Setting up Python virtual environment..."
VENV_DIR="$SCRIPT_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

# Activate venv for this script execution
source "$VENV_DIR/bin/activate"

# Upgrade pip
pip install --upgrade pip

echo "Installing Python dependencies from requirements-dev.txt..."
if [ -f "requirements-dev.txt" ]; then
    pip install --no-cache-dir -r requirements-dev.txt
    echo "✅ Python dependencies installed."
else
    echo "⚠️  Warning: requirements-dev.txt not found. Skipping dependency installation."
fi

echo "Installing essential Ansible dependencies..."
pip install ansible-core
echo "✅ Ansible dependencies installed."

# --- Find Ansible Playbook executable ---
# Since we are in a venv, these are guaranteed to be in the path
ANSIBLE_PLAYBOOK_EXEC="$(which ansible-playbook)"
ANSIBLE_GALAXY_EXEC="$(which ansible-galaxy)"

if [ -z "$ANSIBLE_PLAYBOOK_EXEC" ] || [ -z "$ANSIBLE_GALAXY_EXEC" ]; then
     echo "Error: Ansible executables not found in virtual environment." >&2
     exit 1
fi

echo "Found ansible-playbook: $ANSIBLE_PLAYBOOK_EXEC"
echo "Found ansible-galaxy: $ANSIBLE_GALAXY_EXEC"

# Install Ansible collections
echo "Installing Ansible and collections..."

# Ensure ansible-galaxy is executable
if [ ! -x "$ANSIBLE_GALAXY_EXEC" ]; then
    echo "Error: ansible-galaxy is not executable at $ANSIBLE_GALAXY_EXEC" >&2
    exit 1
fi

# Install collections to a system-wide path to ensure they are available to the root user (via become)
if ! sudo "$ANSIBLE_GALAXY_EXEC" collection install community.general ansible.posix community.docker --collections-path /usr/share/ansible/collections; then
    echo "Error: Failed to install Ansible collections." >&2
    exit 1
fi
echo "✅ Ansible collections installed successfully."

# --- Handle Nomad job purge ---
if [ "$PURGE_JOBS" = true ]; then
    if command -v nomad &> /dev/null; then
        echo "🔥 --purge-jobs flag detected. Stopping and purging all Nomad jobs..."
        # Get all job IDs, filter out the header and any 'No jobs' messages
        job_ids=$(nomad job status | awk 'NR>1 {print $1}')

        if [ -n "$job_ids" ]; then
            echo "$job_ids" | while read -r job_id; do
                if [ -n "$job_id" ]; then
                    echo "Stopping and purging job: $job_id"
                    nomad job stop -purge "$job_id" >/dev/null
                fi
            done
            echo "✅ All Nomad jobs have been purged."
        else
            echo "No running Nomad jobs found to purge."
        fi
    else
        echo "⚠️  Warning: 'nomad' command not found. Cannot purge jobs. Skipping."
    fi
fi

echo "Forcefully terminating any orphaned application processes to prevent memory leaks..."
pkill -f dllama-api || true
pkill -f "/opt/pipecatapp/venv/bin/python3 /opt/pipecatapp/app.py" || true
echo "Process cleanup complete."

# Display system memory
free -h

# --- Run Ansible Playbooks ---
echo "Running Ansible playbooks for local setup..."
echo "You may be prompted for your sudo password."

# --- State Management ---
start_index=0
if [ "$CONTINUE_RUN" = true ]; then
    if [ "$DEBUG_MODE" = true ] && [ -f "$LOG_FILE" ]; then
        echo "🔄 --continue and --debug flags detected. Saving previous log to ${LOG_FILE}.before_changes"
        mv "$LOG_FILE" "${LOG_FILE}.before_changes"
    fi
    if [ -f "$STATE_FILE" ]; then
        last_completed_index=$(cat "$STATE_FILE")
        start_index=$((last_completed_index + 1))
        echo "🔄 --continue flag detected. Resuming from playbook at index $start_index."
    else
        echo "ℹ️  --continue flag detected, but no state file found. Starting from the beginning."
    fi
else
    # Not a continued run, so remove the state file to ensure a fresh start
    if [ -f "$STATE_FILE" ]; then
        rm "$STATE_FILE"
    fi
fi

# Clear the log file if debug mode is on and we are not continuing a run
if [ "$DEBUG_MODE" = true ] && [ "$CONTINUE_RUN" = false ]; then
    > "$LOG_FILE"
fi

# --- Define Role-Specific Playbooks ---
ALL_PLAYBOOKS=(
    "playbooks/preflight/checks.yaml"
    "playbooks/common_setup.yaml"
    "playbooks/services/core_infra.yaml"
    "playbooks/services/consul.yaml"
    "playbooks/services/docker.yaml"
    "playbooks/services/nomad.yaml"
    "playbooks/services/app_services.yaml"
    "playbooks/services/model_services.yaml"
    "playbooks/services/core_ai_services.yaml"
    "playbooks/services/ai_experts.yaml"
    "playbooks/services/final_verification.yaml"
)

CONTROLLER_PLAYBOOKS=(
    "playbooks/preflight/checks.yaml"
    "playbooks/common_setup.yaml"
    "playbooks/services/core_infra.yaml"
    "playbooks/services/consul.yaml"
    "playbooks/services/docker.yaml"
    "playbooks/services/nomad.yaml"
)

WORKER_PLAYBOOKS=(
    "playbooks/worker.yaml"
)

# --- Select Playbooks based on Role ---
if [ -n "$ANSIBLE_TAGS" ]; then
    ANSIBLE_ARGS+=(--tags "$ANSIBLE_TAGS")
fi
case "$ROLE" in
    "all")
        PLAYBOOKS=("${ALL_PLAYBOOKS[@]}")
        ;;
    "controller")
        PLAYBOOKS=("${CONTROLLER_PLAYBOOKS[@]}")
        ;;
    "worker")
        PLAYBOOKS=("${WORKER_PLAYBOOKS[@]}")
        ANSIBLE_ARGS+=(--extra-vars "controller_ip=$CONTROLLER_IP")
        ;;
    *)
        echo "Error: Invalid role '$ROLE' specified."
        exit 1
        ;;
esac


for i in "${!PLAYBOOKS[@]}"; do
    playbook_path="$SCRIPT_DIR/${PLAYBOOKS[$i]}"

    if [ "$i" -lt "$start_index" ]; then
        echo "--------------------------------------------------"
        echo "⏭️  Skipping already completed playbook: $playbook_path"
        echo "--------------------------------------------------"
        continue
    fi

    echo "--------------------------------------------------"
    echo "🚀 Running playbook ($((i+1))/${#PLAYBOOKS[@]}): $playbook_path"
    echo "--------------------------------------------------"

    # Add a delay before running app_services.yaml to avoid port conflicts
    if [[ "$playbook_path" == *"app_services.yaml"* ]]; then
        echo "Sleeping for 10 seconds before running app_services.yaml to avoid port conflicts..."
        sleep 10
    fi

    # --- Resource Management: Cleanup between Model Services and Core AI Services ---
    if [[ "$playbook_path" == *"core_ai_services.yaml"* ]]; then
        echo "🧹 Performing pre-Core AI Services cleanup to free RAM..."

        # Stop llamacpp-rpc jobs left over from model_services.yaml (benchmarking/speedtest)
        if command -v nomad &> /dev/null; then
            echo "Stopping any running llamacpp-rpc jobs..."
            # Using raw Nomad command to target wildcard jobs if possible, or iterating
            # Since wildcard stop isn't standard in all Nomad versions, we list and stop.
            nomad job status | awk '/llamacpp-rpc/ {print $1}' | while read -r job_id; do
                if [ -n "$job_id" ]; then
                    echo "Stopping job: $job_id"
                    nomad job stop -purge "$job_id" >/dev/null
                fi
            done
        fi

        # Drop filesystem caches to free reclaimable memory
        echo "Dropping filesystem caches..."
        sync
        echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null

        echo "RAM status after cleanup:"
        free -h
    fi

    COMMAND=("$ANSIBLE_PLAYBOOK_EXEC" -i local_inventory.ini "$playbook_path" "${ANSIBLE_ARGS[@]}")

    if [ "$DEBUG_MODE" = true ]; then
        # Execute with verbose logging and append to file
        time "${COMMAND[@]}" >> "$LOG_FILE" 2>&1
        playbook_exit_code=$?
    else
        # Execute normally
        time "${COMMAND[@]}"

        playbook_exit_code=$?
    fi

    if [ $playbook_exit_code -ne 0 ]; then
        echo "❌ Playbook '$playbook_path' failed. Aborting script."
        echo "To resume from the next playbook, run this script again with the --continue flag."
        if [ "$DEBUG_MODE" = true ]; then
            echo "View the detailed log in '$LOG_FILE'."
        fi
        exit $playbook_exit_code
    fi

    # Save the index of the successfully completed playbook
    echo "$i" > "$STATE_FILE"
    echo "✅ Playbook '$playbook_path' completed successfully."
done

echo "--------------------------------------------------"
echo "✅ All playbooks completed successfully."
echo "Bootstrap complete."
