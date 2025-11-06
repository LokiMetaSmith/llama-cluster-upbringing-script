#!/bin/bash
#
# Wrapper Script for pipecatapp
#
# This script ensures that the pipecat application is run within its
# virtual environment and that all of its output (both stdout and stderr)
# is reliably redirected to a log file for debugging.

# Exit immediately if a command exits with a non-zero status.
set -e

# Define the log file path inside the app directory
LOG_FILE="/opt/pipecatapp/pipecat.log"

# Change to the application directory first
cd /opt/pipecatapp


source /opt/pipecatapp/venv/bin/activate

# Create the log file if it doesn't exist
touch "$LOG_FILE"

echo "--- Starting pipecat-app: $(date) ---" >> "$LOG_FILE"
exec /opt/pipecatapp/venv/bin/python3 "$@" >> "$LOG_FILE" 2>&1
