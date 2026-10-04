#!/bin/bash
export PATH="/opt/pipecat_venv/bin:$PATH"
export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
CHROME_BIN=$(find /opt/pw-browsers -name chrome -type f -perm /111 2>/dev/null | head -n 1)
if [ -z "$CHROME_BIN" ]; then
    CHROME_BIN=$(find /opt/pw-browsers -name "chrome-headless-shell" -type f -perm /111 2>/dev/null | head -n 1)
fi

echo "Found Chrome binary at: $CHROME_BIN"
echo "Starting Chromium on port 9222..."
exec "$CHROME_BIN" \
    --headless \
    --no-sandbox \
    --disable-gpu \
    --disable-dev-shm-usage \
    --remote-debugging-port=9222 \
    --remote-debugging-address=0.0.0.0 \
    --user-data-dir=/tmp/chromium-profile \
    "about:blank"

