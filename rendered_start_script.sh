#!/bin/bash
set -e

LOG_FILE="/opt/pipecatapp/pipecat.log"

# Step 1: Create log file
echo "--- Script started: $(date) ---" > "$LOG_FILE"

# Step 2: Activate virtual environment
echo "--- Activating venv ---" >> "$LOG_FILE"
source /opt/pipecatapp/venv/bin/activate >> "$LOG_FILE" 2>&1

# Step 3: Run simple python command
echo "--- Running python test ---" >> "$LOG_FILE"
/opt/pipecatapp/venv/bin/python3 -c "import sys; print(f'Python version: {sys.version}')" >> "$LOG_FILE" 2>&1

# Step 4: Original command
echo "--- Starting pipecat-app: $(date) ---" >> "$LOG_FILE"
exec /opt/pipecatapp/venv/bin/python3 /opt/pipecatapp/app.py >> "$LOG_FILE" 2>&1
