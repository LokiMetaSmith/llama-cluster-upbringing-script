#!/bin/bash
set -e

# Activate virtualenv
source /opt/pipecatapp/venv/bin/activate

# Start the service
# The archivist_service.py is located in the same directory as this script (usually /opt/pipecatapp)
# or in the files directory if running from repo.
# In deployment, Ansible copies files to /opt/pipecatapp.

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

if [ -f "$SCRIPT_DIR/archivist_service.py" ]; then
    TARGET_SCRIPT="$SCRIPT_DIR/archivist_service.py"
elif [ -f "/opt/pipecatapp/archivist_service.py" ]; then
    TARGET_SCRIPT="/opt/pipecatapp/archivist_service.py"
else
    echo "Error: archivist_service.py not found."
    exit 1
fi

echo "Starting Archivist Service from $TARGET_SCRIPT"
# Use uvicorn CLI to start the service to avoid port binding issues and ensure clean signal handling
if [ -z "$ARCHIVIST_PORT" ]; then
    echo "Error: ARCHIVIST_PORT is not set."
    exit 1
fi
cd "$(dirname "$TARGET_SCRIPT")"
exec python3 archivist_service.py
