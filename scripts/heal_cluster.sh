#!/bin/bash
#
# Wrapper script to run the cluster healing playbook.
# This ensures core infrastructure (LlamaRPC, Pipecat App) is running.

set -e

# --- Configuration ---
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
PLAYBOOK="$REPO_ROOT/playbooks/heal_cluster.yaml"

# Determine default target user (avoid root)
CURRENT_USER="$(whoami)"
if [ "$CURRENT_USER" = "root" ]; then
    TARGET_USER="pipecatapp"
else
    TARGET_USER="${CURRENT_USER:-pipecatapp}"
fi

# --- Help ---
show_help() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Runs the heal_cluster.yaml playbook to restore core services."
    echo ""
    echo "Options:"
    echo "  -u, --user <user>   Specify target user (default: $TARGET_USER)"
    echo "  -h, --help          Show this help message"
}

# --- Parse Args ---
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -u|--user) TARGET_USER="$2"; shift ;;
        -h|--help) show_help; exit 0 ;;
        *) echo "Unknown parameter passed: $1"; show_help; exit 1 ;;
    esac
    shift
done

# --- Execution ---
echo "🚀 Starting Cluster Healing..."
echo "Playbook: $PLAYBOOK"
echo "Target User: $TARGET_USER"
echo ""

if [ ! -f "$PLAYBOOK" ]; then
    echo "❌ Error: Playbook not found at $PLAYBOOK"
    exit 1
fi

# Ensure Ansible is available
if ! command -v ansible-playbook &> /dev/null; then
    echo "❌ Error: ansible-playbook not found. Please install Ansible first."
    exit 1
fi

# Run the playbook
ansible-playbook "$PLAYBOOK" \
    -e "target_user=$TARGET_USER" \
    -e "ansible_python_interpreter=$(which python3)"

echo ""
echo "✅ Healing complete."
