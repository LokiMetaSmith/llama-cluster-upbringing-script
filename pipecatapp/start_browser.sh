#!/bin/bash
export PATH="/opt/pipecat_venv/bin:$PATH"
export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
# Start a headless playwright remote server or some simple python runner exposing it
# For now, we'll start a basic python uvicorn/fastapi if we wrap it, or just sleep
# A better approach is to run a simple playwright server. Let's use playwright CLI if possible,
# or we'll wrap it later.
echo "Starting Playwright Browser Runner"
python3 -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); browser = p.chromium.launch(headless=True, args=['--remote-debugging-port=9222', '--remote-debugging-address=0.0.0.0']); print('Browser running on port 9222'); import time; time.sleep(1000000)"
