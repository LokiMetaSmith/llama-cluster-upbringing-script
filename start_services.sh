#!/bin/bash

# This script is a legacy utility for manually starting services.
# ⚠️  DEPRECATED: Please use Ansible to deploy services to ensure consistency.
# Example: ansible-playbook playbook.yaml --tags ai-experts

echo "⚠️  WARNING: This script is deprecated and may not reflect the latest deployment logic."
echo "Use at your own risk. For proper deployment, run:"
echo "  ansible-playbook playbook.yaml --tags ai-experts,app-services"
echo ""
echo "Press output any key to continue or Ctrl+C to abort..."
read -r -n 1 -s

# Legacy logic below (best effort)
set -e

echo "🚀 Starting the main Llama Expert service..."
if [ -f /opt/nomad/jobs/expert-main.nomad ]; then
    nomad job run /opt/nomad/jobs/expert-main.nomad
fi

echo "🚀 Starting the Pipecat application service..."
if [ -f /opt/nomad/jobs/pipecatapp.nomad ]; then
    nomad job run /opt/nomad/jobs/pipecatapp.nomad
fi

echo "🚀 Starting the Home Assistant service..."
if [ -f /opt/nomad/jobs/home-assistant.nomad ]; then
    nomad job run /opt/nomad/jobs/home-assistant.nomad
fi

echo "✅ All services have been submitted to Nomad."
echo "Use 'nomad status' to monitor their deployment."

nomad status
