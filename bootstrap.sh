#!/bin/bash
#
# Easy Bootstrap Script for Single-Node Setup
#
# This script simplifies the process of bootstrapping the system on a single
# server for development or as the initial control node for a new cluster.
# It runs the main Ansible playbook using a local inventory file.

# Move to the script's directory to ensure paths are correct
cd "$(dirname "$0")"

# Check if ansible-playbook is installed
if ! command -v ansible-playbook &> /dev/null
then
    echo "Error: ansible-playbook could not be found."
    echo "Please install Ansible before running this script."
    echo "On Debian/Ubuntu: sudo apt update && sudo apt install ansible"
    exit 1
fi

# --- ADDED SECTION ---
# Purge any existing jobs to ensure a clean deployment.
echo "Purging any old Nomad jobs that will be deployed..."

# The '|| true' part ensures that the script won't stop with an error
# if the jobs don't exist yet (e.g., on a brand new setup).
nomad job stop -purge prima-expert-main || true
nomad job stop -purge pipecat-app || true

echo "Purge complete."
# --- END ADDED SECTION ---

# Run the Ansible playbook with the local inventory
echo "Running the Ansible playbook for local setup..."
echo "You will be prompted for your sudo password."

ansible-playbook -i local_inventory.ini playbook.yaml --ask-become-pass

echo "Bootstrap complete."
