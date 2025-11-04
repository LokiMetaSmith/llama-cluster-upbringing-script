#!/bin/bash

set -e

PLAYBOOKS=(
    "playbook.yaml"
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

# Run the tests
for playbook in "${PLAYBOOKS[@]}"; do
    echo "Testing playbook: $playbook"
    ./scripts/ansible_diff.sh "$playbook"
done

echo "All playbooks tested successfully!"
