#!/bin/bash

# This script starts the necessary Nomad jobs for the AI digital twin application.
# It should be run from the user's home directory on a controller node.

set -e

echo "🚀 Starting the Prima Expert main service..."
# Note: The file is prima-expert.nomad, but the job name inside is prima-expert-main
nomad job run /opt/nomad/jobs/prima-expert.nomad

echo "🚀 Starting the Pipecat application service..."
nomad job run /opt/nomad/jobs/pipecatapp.nomad

echo "✅ All services have been submitted to Nomad."
echo "Use 'nomad status' to monitor their deployment."

nomad status
