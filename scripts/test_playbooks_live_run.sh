#!/bin/bash

set -e

PLAYBOOKS=(
    "e2e-tests.yaml"
    "heal_job.yaml"
    "promote_controller.yaml"
)

# Find the ansible-playbook executable
if ! command -v ansible-playbook &> /dev/null
then
    echo "ansible-playbook could not be found"
    exit 1
fi

for playbook in "${PLAYBOOKS[@]}"; do
    echo "Running playbook: $playbook"
    ansible-playbook -i local_inventory.ini "$playbook" --extra-vars="target_user=jules"
done

echo "All playbooks run successfully!"
