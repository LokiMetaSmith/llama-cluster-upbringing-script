#!/bin/bash
set -x
exec >> /tmp/start_services.log 2>&1
echo "--- Starting services: $(date) ---"
ls -l /opt/nomad/jobs/
echo "🚀 Starting the main Prima Expert service..."
nomad job run /opt/nomad/jobs/prima-expert.nomad
echo "🚀 Starting the Pipecat application service..."
nomad job run /opt/nomad/jobs/pipecatapp.nomad
echo "✅ All services have been submitted to Nomad."
echo "Use 'nomad status' to monitor their deployment."
nomad status