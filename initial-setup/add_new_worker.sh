#!/bin/bash
#
# Script to manually provision a new worker node for the cluster.
# This script automates the process of initial setup, SSH key exchange,
# inventory update, and Ansible provisioning.

set -e

# --- Configuration ---
REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
INVENTORY_FILE="$REPO_ROOT/inventory.yaml"
WORKER_SETUP_SCRIPT="$REPO_ROOT/initial-setup/worker-setup/setup.sh"

# --- Usage ---
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <new_worker_hostname> <new_worker_ip> <new_worker_user> <new_worker_password>"
    exit 1
fi

NEW_HOSTNAME=$1
NEW_IP=$2
NEW_USER=$3
NEW_PASS=$4

echo "--- Starting provisioning for new worker: $NEW_HOSTNAME ($NEW_IP) ---"

# --- Step 1: Run Initial Setup on the New Worker ---
echo "--> Running initial setup script on the new worker..."
sshpass -p "$NEW_PASS" ssh -o StrictHostKeyChecking=no "${NEW_USER}@${NEW_IP}" 'bash -s' < "$WORKER_SETUP_SCRIPT"

echo "--> Initial setup script completed."

# --- Step 2: Copy SSH Key for Passwordless Access ---
echo "--> Copying SSH key to the new worker for passwordless access..."
sshpass -p "$NEW_PASS" ssh-copy-id "${NEW_USER}@${NEW_IP}"

echo "--> SSH key copied."

# --- Step 3: Update the Ansible Inventory File ---
echo "--> Adding new worker to the inventory file: $INVENTORY_FILE"
# This command uses yq to safely add a new host to the workers group.
# It checks if the host already exists before adding it.
if ! yq e ".all.children.workers.hosts | has(\"$NEW_HOSTNAME\")" "$INVENTORY_FILE" | grep -q "true"; then
    yq e ".all.children.workers.hosts += {\"$NEW_HOSTNAME\": {\"ansible_host\": \"$NEW_IP\"}}" -i "$INVENTORY_FILE"
    echo "--> $NEW_HOSTNAME added to inventory."
else
    echo "--> $NEW_HOSTNAME already exists in inventory. Skipping."
fi

# --- Step 4: Run the Ansible Playbook ---
echo "--> Running Ansible playbook to provision the new worker..."
echo "--> You may be prompted for your sudo password for the Ansible run."
ansible-playbook -i "$INVENTORY_FILE" playbook.yaml --limit "$NEW_HOSTNAME" --ask-become-pass

echo "---"
echo "✅ Provisioning complete for worker: $NEW_HOSTNAME"
echo "---"
