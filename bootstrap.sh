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
    echo "  --deploy-docker              Deploy the pipecat application using Docker."
    echo "  --home-assistant-debug       Enable debug mode for Home Assistant."
    echo "  -h, --help                   Display this help message and exit."
}

# --- Initialize flags ---
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
        --home-assistant-debug)
        ANSIBLE_ARGS+=(--extra-vars "home_assistant_debug_mode=true")
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

# --- Run Initial Machine Setup based on Role ---
# This script handles pre-Ansible configuration like network and hostname.
# It's run for all roles, and the script itself determines what to do based on the config.
echo "--- Running Initial Machine Setup ---"
if [ -f "initial-setup/setup.sh" ]; then
    echo "You may be prompted for your sudo password to run the initial setup script."
    sudo bash "initial-setup/setup.sh"
    echo "✅ Initial machine setup complete."
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

# --- Install Python dependencies ---
echo "Installing Python dependencies from requirements-dev.txt..."
if [ -f "requirements-dev.txt" ]; then
    pip install -r requirements-dev.txt
    echo "✅ Python dependencies installed."
else
    echo "⚠️  Warning: requirements-dev.txt not found. Skipping dependency installation."
fi

# --- Find Ansible Playbook executable ---
# JULES: The original find_executable function was unreliable. This new approach
# dynamically finds the active python interpreter's bin directory, making it
# portable across different environments (system, venv, pyenv).

# Find the directory containing the active python executable
PYTHON_EXEC=$(command -v python || command -v python3)
if [ -z "$PYTHON_EXEC" ]; then
    echo "Error: Could not find 'python' or 'python3' in the PATH." >&2
    exit 1
fi
PYTHON_BIN_DIR=$(dirname "$PYTHON_EXEC")

ANSIBLE_PLAYBOOK_EXEC="$PYTHON_BIN_DIR/ansible-playbook"
ANSIBLE_GALAXY_EXEC="$PYTHON_BIN_DIR/ansible-galaxy"

# Check if Ansible executables exist, if not, install ansible-core
if [ ! -x "$ANSIBLE_PLAYBOOK_EXEC" ] || [ ! -x "$ANSIBLE_GALAXY_EXEC" ]; then
    echo "Ansible executables not found. Attempting to install ansible-core..."
    pip install ansible-core
    # Verify after installation
    if [ ! -x "$ANSIBLE_PLAYBOOK_EXEC" ] || [ ! -x "$ANSIBLE_GALAXY_EXEC" ]; then
        echo "Error: Failed to locate Ansible executables even after pip install." >&2
        echo "Looked for: $ANSIBLE_PLAYBOOK_EXEC"
        exit 1
    fi
fi

echo "Found ansible-playbook: $ANSIBLE_PLAYBOOK_EXEC"
echo "Found ansible-galaxy: $ANSIBLE_GALAXY_EXEC"

# Install Ansible collections
echo "Installing Ansible and collections..."
# Define the collections path
COLLECTIONS_PATH="$HOME/.ansible/collections"
mkdir -p "$COLLECTIONS_PATH"

# Install collections to the specified path
if ! "$ANSIBLE_GALAXY_EXEC" collection install community.general ansible.posix community.docker -p "$COLLECTIONS_PATH"; then
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
