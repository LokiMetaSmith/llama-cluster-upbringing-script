#!/bin/bash
set -e
cd /opt/pipecatapp
source /opt/pipecatapp/venv/bin/activate
echo "--- Starting pipecat-app: $(date) ---"
exec /opt/pipecatapp/venv/bin/python3 /opt/pipecatapp/app.py
