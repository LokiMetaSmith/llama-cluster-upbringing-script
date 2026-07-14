#!/bin/bash
#
# Cleanup script to free up disk space on the host machine.
# This script aggressively cleans Docker resources, Apt cache, and temporary files.
# It is intended to be run with sudo privileges.
#
# Usage:
#   sudo ./scripts/cleanup.sh
#   OR via bootstrap:
#   ./bootstrap.sh --system-cleanup

set -e

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${BOLD}${YELLOW}⚠️  Starting Aggressive System Cleanup...${NC}"

# 1. Docker Cleanup
if command -v docker &> /dev/null; then
    echo -e "\n${BOLD}🐳 Cleaning Docker System...${NC}"
    echo "Pruning stopped containers, unused networks, and dangling images..."
    docker system prune --force

    echo "Pruning build cache..."
    docker builder prune --force

    # Optional: Remove all unused images, not just dangling ones
    # docker image prune --all --force
else
    echo "Docker not found, skipping Docker cleanup."
fi

# 2. Apt Cleanup (Debian/Ubuntu)
if command -v apt-get &> /dev/null; then
    echo -e "\n${BOLD}📦 Cleaning Apt Cache...${NC}"
    sudo apt-get clean
    sudo apt-get autoremove -y

    # Remove proxy config if it exists so next apt-get runs without hanging on a dead proxy container
    if [ -f "/etc/apt/apt.conf.d/01proxy" ]; then
        echo "Removing stale apt proxy configuration..."
        sudo rm -f /etc/apt/apt.conf.d/01proxy
    fi
else
    echo "Apt not found, skipping Apt cleanup."
fi

# 3. Playwright Cleanup (Optional)
# This directory can be very large. Uncomment if you want to force re-download of browsers.
PLAYWRIGHT_CACHE="/root/.cache/ms-playwright"
if [ -d "$PLAYWRIGHT_CACHE" ]; then
   echo -e "\n${BOLD}🎭 Cleaning Playwright Cache...${NC}"
   echo "Removing $PLAYWRIGHT_CACHE..."
   sudo rm -rf "$PLAYWRIGHT_CACHE"
fi

# 4. Snap Cleanup (if applicable)
# Snap keeps older versions of packages which can consume significant space.
if command -v snap &> /dev/null; then
    echo -e "\n${BOLD}🫰 Cleaning Snap Cache...${NC}"
    # Removes disabled snaps (older versions)
    sudo snap list --all | awk '/disabled/{print $1, $3}' |
        while read snapname revision; do
            sudo snap remove "$snapname" --revision="$revision"
        done
fi

# 5. Bootstrap Artifacts Cleanup
echo -e "\n${BOLD}🧹 Cleaning Bootstrap Artifacts...${NC}"
# Remove downloaded archives
rm -f /tmp/consul.zip
rm -f /tmp/nomad.zip
rm -f /tmp/cni-plugins.tgz
rm -f /tmp/get-docker.sh
rm -f /tmp/pipecatapp.tar

# Remove extracted directories
rm -rf /tmp/consul
rm -rf /tmp/nomad

# 6. Log Files
echo -e "\n${BOLD}📝 Cleaning Log Files...${NC}"
# Truncate large system logs instead of deleting them to avoid open file handle issues
if [ -f "/var/log/syslog" ]; then
    sudo truncate -s 0 /var/log/syslog
fi
if [ -f "/var/log/journal" ]; then
    # Retain only the last 100M of journals
    sudo journalctl --vacuum-size=100M
fi

# Local project logs
if [ -f "playbook_output.log" ]; then
    rm -f playbook_output.log
fi

# 7. Application State and Config Cleanup
echo -e "\n${BOLD}🧹 Cleaning Application State in /opt...${NC}"

# Define directories that should be completely wiped to ensure a pristine state
APP_DIRS=(
    "/opt/pipecatapp"
    "/opt/tool_server"
    "/opt/paperless"
    "/opt/claude_clone"
    "/opt/llmfit"
    "/opt/llxprt-code"
    "/opt/opengravity-build"
    "/opt/exo"
    "/opt/exo_build"
    "/opt/mcp"
    "/opt/cni"
    "/opt/cluster-infra"
    "/opt/openclaw"
    "/opt/power_manager"
    "/opt/provisioning_api"
    "/opt/world_model_service"
    "/opt/heretic_tool"
)

for dir in "${APP_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "Removing $dir..."
        sudo rm -rf "$dir"
    fi
done

# Clean up Consul state
if [ -d "/opt/consul/data" ]; then
    echo "Stopping Consul service (if running)..."
    sudo systemctl stop consul 2>/dev/null || true
    echo "Removing /opt/consul/data..."
    sudo rm -rf "/opt/consul/data"
fi

# Clean up Nomad state safely (preserve /opt/nomad/models)
if [ -d "/opt/nomad" ]; then
    echo "Stopping Nomad service (if running)..."
    sudo systemctl stop nomad 2>/dev/null || true

    echo "Unmounting any active allocations in /opt/nomad..."
    for mount in $(mount | awk '{print $3}' | grep '^/opt/nomad/' | sort -r); do
        echo "Unmounting $mount"
        sudo umount "$mount" || true
    done

    echo "Cleaning /opt/nomad state (preserving models)..."
    # Find and delete everything in /opt/nomad EXCEPT the models directory
    # -mindepth 1 prevents matching /opt/nomad itself
    # -maxdepth 1 prevents diving into subdirectories for matching
    # ! -name "models" excludes the models folder
    # -exec rm -rf {} + executes rm -rf on the matched items
    sudo find /opt/nomad -mindepth 1 -maxdepth 1 ! -name "models" -exec rm -rf {} +
fi

# 8. Force kill orphaned and running opencode processes
echo -e "\n${BOLD}🔪 Terminating all running and orphaned opencode processes...${NC}"
sudo pkill -9 -x "opencode" || sudo pkill -9 -f "bin/opencode" || true


echo -e "\n${GREEN}✨ Cleanup Complete!${NC}"
df -h /
