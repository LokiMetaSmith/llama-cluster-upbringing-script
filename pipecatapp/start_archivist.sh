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

echo "DEBUG: HOST_IP=${HOST_IP:-0.0.0.0}"
echo "DEBUG: ARCHIVIST_PORT=$ARCHIVIST_PORT"

# Check if port is in use and kill the process
if command -v lsof >/dev/null 2>&1; then
    PORT_PID=$(lsof -t -i :$ARCHIVIST_PORT || true)
    if [ -n "$PORT_PID" ]; then
        echo "WARNING: Port $ARCHIVIST_PORT is in use by PID(s) $PORT_PID. Killing..."
        kill -9 $PORT_PID || true
        sleep 2
    else
        echo "Port $ARCHIVIST_PORT is free."
    fi
else
    echo "WARNING: lsof not found. Cannot check for port usage by PID."
fi

cd "$(dirname "$TARGET_SCRIPT")"
HOST_IP=${HOST_IP:-0.0.0.0}
exec uvicorn archivist_service:app --host "$HOST_IP" --port "$ARCHIVIST_PORT"
