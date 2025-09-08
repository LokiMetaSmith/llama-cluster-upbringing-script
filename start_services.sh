#!/bin/bash

# This script starts the necessary Nomad jobs for the AI digital twin application.
# It should be run from the user's home directory on a controller node.

set -e

echo "🚀 Starting the distributed Llama C++ RPC service..."
nomad job run /opt/cluster-infra/ansible/jobs/llamacpp-rpc.nomad

echo "🚀 Starting the Pipecat application service..."
nomad job run /opt/cluster-infra/ansible/jobs/pipecatapp.nomad

echo "✅ All services have been submitted to Nomad."
echo "Use 'nomad status' to monitor their deployment."

nomad status
