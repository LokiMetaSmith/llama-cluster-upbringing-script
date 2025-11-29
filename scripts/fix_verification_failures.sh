#!/bin/bash
# Scripts to help remediate failures reported by verify_components.py

echo "Starting remediation of component failures..."

# 1. Fix llxprt_code
if ! command -v llxprt &> /dev/null; then
    echo "Attempting to install llxprt-code globally..."
    if [ -d "/opt/llxprt-code" ]; then
        cd /opt/llxprt-code && npm install -g .
    else
        echo "Warning: /opt/llxprt-code does not exist. Cloning repo..."
        sudo git clone https://github.com/vybestack/llxprt-code.git /opt/llxprt-code
        cd /opt/llxprt-code && sudo npm install && sudo npm install -g .
    fi
else
    echo "llxprt is already installed."
fi

# 2. Fix claude_clone
if [ ! -d "/opt/claude_clone" ]; then
    echo "Cloning Claude_Clone..."
    sudo git clone https://github.com/LokiMetaSmith/Claude_Clone.git /opt/claude_clone
    cd /opt/claude_clone && sudo npm install && sudo npm run build
elif [ ! -f "/opt/claude_clone/package.json" ]; then
     echo "Repopulating Claude_Clone..."
     sudo git clone https://github.com/LokiMetaSmith/Claude_Clone.git /tmp/cc_temp
     sudo mv /tmp/cc_temp/* /opt/claude_clone/
     sudo rm -rf /tmp/cc_temp
     cd /opt/claude_clone && sudo npm install && sudo npm run build
fi

# 3. Fix moe_gateway
if [ ! -f "/opt/pipecatapp/moe_gateway/gateway.py" ]; then
    echo "Restoring moe_gateway/gateway.py..."
    # Assuming we are in the repo root when running this, or we can fetch it.
    # We will try to copy from the local repo if available
    REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")
    SRC="$REPO_ROOT/ansible/roles/moe_gateway/files/gateway.py"
    if [ -f "$SRC" ]; then
        sudo mkdir -p /opt/pipecatapp/moe_gateway
        sudo cp "$SRC" /opt/pipecatapp/moe_gateway/gateway.py
        echo "Restored gateway.py from local repo."
    else
        echo "Error: Could not find source gateway.py in $SRC"
    fi
fi

# 4. Power Manager
echo "Checking power-agent service..."
if systemctl is-active --quiet power-agent; then
    echo "power-agent is running."
else
    echo "power-agent is not running. Attempting restart..."
    sudo systemctl restart power-agent
fi

# 5. Nomad Connectivity
echo "------------------------------------------------"
echo "NOTE regarding Nomad 'no route to host' errors:"
echo "Ensure your NOMAD_ADDR environment variable is set correctly."
echo "Current value: $NOMAD_ADDR"
echo "If you are running this locally and Nomad is on localhost, try:"
echo "export NOMAD_ADDR=http://localhost:4646"
echo "If Nomad is on a remote node, ensure VPN or network routing is active."
echo "------------------------------------------------"

echo "Remediation attempts complete. Please run verify_components.py again."
