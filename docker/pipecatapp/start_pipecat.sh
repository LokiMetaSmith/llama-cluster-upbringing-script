#!/bin/bash
#
# Wrapper Script for pipecatapp inside a Docker container
#
# This script ensures that the pipecat application is run within its
# virtual environment.

# Exit immediately if a command exits with a non-zero status.
set -e

# Activate the virtual environment
source /opt/pipecatapp/venv/bin/activate

# Execute the Python application.
# The 'exec' command replaces the shell process with the python process.
echo "--- Starting pipecat-app: $(date) ---"
exec /opt/pipecatapp/venv/bin/python3 /opt/pipecatapp/app.py