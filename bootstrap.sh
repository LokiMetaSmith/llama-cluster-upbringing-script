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
ANSIBLE_ARGS=""
LOG_FILE="playbook_output.log"

# --- Parse command-line arguments ---
for arg in "$@"
do
    case $arg in
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
    ANSIBLE_ARGS="$ANSIBLE_ARGS -vvv"
fi

if [ "$EXTERNAL_MODEL_SERVER" = true ]; then
    echo "⚡️ --external-model-server flag detected. Skipping large model downloads and builds."
    ANSIBLE_ARGS="$ANSIBLE_ARGS --extra-vars=external_model_server=true"
fi

# --- Main script logic ---

# Check if ansible-playbook is installed
if ! command -v ansible-playbook &> /dev/null
then
    echo "Error: ansible-playbook could not be found."
    echo "Please install Ansible before running this script."
    echo "On Debian/Ubuntu: sudo apt update && sudo apt install ansible"
    exit 1
fi



echo "Forcefully terminating any orphaned application processes to prevent memory leaks..."
pkill -f dllama-api || true
pkill -f "/opt/pipecatapp/venv/bin/python3 /opt/pipecatapp/app.py" || true
echo "Process cleanup complete."

# Display system memory
free -h

# Run the Ansible playbook with the local inventory
echo "Running the Ansible playbook for local setup..."
echo "You will be prompted for your sudo password."

if [ "$DEBUG_MODE" = true ]; then
    # Execute with verbose logging and redirect to file
    time ansible-playbook -i local_inventory.ini playbook.yaml $ANSIBLE_ARGS > "$LOG_FILE" 2>&1 &
    playbook_exit_code=$?
    echo "✅ Playbook run complete. View the detailed log in '$LOG_FILE'."
else
    # Execute normally
    ansible-playbook -i local_inventory.ini playbook.yaml $ANSIBLE_ARGS &
    playbook_exit_code=$?
fi

if [ $playbook_exit_code -ne 0 ]; then
    echo "❌ Ansible playbook failed. Aborting script."
    exit $playbook_exit_code
fi


echo "Bootstrap complete."

# The main playbook handles the deployment of all necessary services.
# No further action is needed.
echo "✅ Standalone server setup is complete."
