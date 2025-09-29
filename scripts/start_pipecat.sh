#!/bin/bash
#
# Wrapper Script for pipecat-app
#
# This script ensures that the pipecat application is run within its
# virtual environment and that all of its output (both stdout and stderr)
# is reliably redirected to a log file for debugging.

# Exit immediately if a command exits with a non-zero status.
set -e

# Define the log file path
LOG_FILE="/tmp/pipecat.log"

# Activate the virtual environment
source /opt/pipecatapp/venv/bin/activate

# Execute the Python application, redirecting all output to the log file.
# The 'exec' command replaces the shell process with the python process.
echo "--- Starting pipecat-app: $(date) ---" > "$LOG_FILE"
exec /opt/pipecatapp/venv/bin/python3 /opt/pipecatapp/app.py &>> "$LOG_FILE"