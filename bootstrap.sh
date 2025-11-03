#!/bin/bash
#
# Easy Bootstrap Script for Single-Node Setup
#
# This script simplifies the process of bootstrapping the system on a single
# server for development or as the initial control node for a new cluster.
# It runs the main Ansible playbook using a local inventory file.

# --- Initialize flags ---
CLEAN_REPO=false
DEBUG_MODE=false
EXTERNAL_MODEL_SERVER=false
PURGE_JOBS=false
CONTINUE_RUN=false
ANSIBLE_ARGS=""
LOG_FILE="playbook_output.log"
STATE_FILE=".bootstrap_state"

# --- Parse command-line arguments ---
for arg in "$@"
do
    case $arg in
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
        --external-model-server)
        EXTERNAL_MODEL_SERVER=true
        shift
        ;;
        --continue)
        CONTINUE_RUN=true
        shift
        ;;
    esac
done

# --- Move to the script's directory ---
cd "$(dirname "$0")"

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
ANSIBLE_ARGS="--extra-vars=target_user=loki"

if [ "$DEBUG_MODE" = true ]; then
    echo "🔍 --debug flag detected. Ansible output will be saved to '$LOG_FILE'."
    ANSIBLE_ARGS="$ANSIBLE_ARGS -vvvv"
fi

if [ "$EXTERNAL_MODEL_SERVER" = true ]; then
    echo "⚡️ --external-model-server flag detected. Skipping large model downloads and builds."
    ANSIBLE_ARGS="$ANSIBLE_ARGS --extra-vars=external_model_server=true"
fi

# --- Find Ansible Playbook executable ---
find_executable() {
    local executable_name=$1
    # 1. Check PATH first
    if command -v "$executable_name" &> /dev/null; then
        command -v "$executable_name"
        return 0
    fi

    # 2. Check pyenv shims and versions
    if [ -d "$HOME/.pyenv" ]; then
        local pyenv_path
        pyenv_path=$(find "$HOME/.pyenv/versions" -type f -name "$executable_name" | head -n 1)
        if [ -n "$pyenv_path" ] && [ -x "$pyenv_path" ]; then
            echo "$pyenv_path"
            return 0
        fi
    fi

    return 1
}

ANSIBLE_PLAYBOOK=$(find_executable "ansible-playbook")
if [ -z "$ANSIBLE_PLAYBOOK" ]; then
    echo "Error: ansible-playbook could not be found."
    echo "Please install Ansible before running this script."
    echo "On Debian/Ubuntu: sudo apt update && sudo apt install ansible"
    exit 1
fi

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

PLAYBOOKS=(
    "playbooks/common_setup.yaml"
    "playbooks/services/core_infra.yaml"
    "playbooks/services/app_services.yaml"
    "playbooks/services/model_services.yaml"
    "playbooks/services/core_ai_services.yaml"
    "playbooks/services/ai_experts.yaml"
    "playbooks/services/final_verification.yaml"
)

for i in "${!PLAYBOOKS[@]}"; do
    playbook="${PLAYBOOKS[$i]}"

    if [ "$i" -lt "$start_index" ]; then
        echo "--------------------------------------------------"
        echo "⏭️  Skipping already completed playbook: $playbook"
        echo "--------------------------------------------------"
        continue
    fi

    echo "--------------------------------------------------"
    echo "🚀 Running playbook ($((i+1))/${#PLAYBOOKS[@]}): $playbook"
    echo "--------------------------------------------------"

    if [ "$DEBUG_MODE" = true ]; then
        # Execute with verbose logging and append to file
        time "$ANSIBLE_PLAYBOOK" -i local_inventory.ini "$playbook" $ANSIBLE_ARGS >> "$LOG_FILE" 2>&1
        playbook_exit_code=$?
    else
        # Execute normally
        time "$ANSIBLE_PLAYBOOK" -i local_inventory.ini "$playbook" $ANSIBLE_ARGS
        playbook_exit_code=$?
    fi

    if [ $playbook_exit_code -ne 0 ]; then
        echo "❌ Playbook '$playbook' failed. Aborting script."
        echo "To resume from the next playbook, run this script again with the --continue flag."
        if [ "$DEBUG_MODE" = true ]; then
            echo "View the detailed log in '$LOG_FILE'."
        fi
        exit $playbook_exit_code
    fi

    # Save the index of the successfully completed playbook
    echo "$i" > "$STATE_FILE"
    echo "✅ Playbook '$playbook' completed successfully."
done

echo "--------------------------------------------------"
echo "✅ All playbooks completed successfully."
echo "Bootstrap complete."
