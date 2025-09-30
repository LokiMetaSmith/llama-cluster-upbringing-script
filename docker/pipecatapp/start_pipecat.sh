#!/bin/bash
set -e

# Activate the virtual environment
source /opt/pipecatapp/venv/bin/activate

# Start the application
exec python /opt/pipecatapp/app.py