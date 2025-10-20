```bash
#!/bin/bash

# This script starts the necessary Nomad jobs for the AI digital twin application.
# It should be run from the user's home directory on a controller node.

#NOTE: DO NOT RUN THIS FROM AN AUTOMATED SCRIPT

set -e

echo "🚀 Starting the main Llama Expert service..."
if [ -f /opt/nomad/jobs/expert-main.nomad ]; then
    nomad job run /opt/nomad/jobs/expert-main.nomad
fi

echo "🚀 Starting the Pipecat application service..."
nomad job run /opt/nomad/jobs/pipecatapp.nomad

echo "🚀 Starting the Home Assistant service..."
if [ -f /opt/nomad/jobs/home-assistant.nomad ]; then
    nomad job run /opt/nomad/jobs/home-assistant.nomad
fi

echo "✅ All services have been submitted to Nomad."
echo "Use 'nomad status' to monitor their deployment."

nomad status
```