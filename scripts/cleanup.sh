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
#
# Options:
#   --scorched-earth    Aggressively wipe all caches, repo data, and infrastructure data

set -e

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BOLD='\033[1m'

SCORCHED_EARTH=0
POST_BOOTSTRAP=0

for arg in "$@"; do
    if [ "$arg" == "--scorched-earth" ]; then
        SCORCHED_EARTH=1
    elif [ "$arg" == "--post-bootstrap" ] || [ "$arg" == "--safe-mode" ]; then
        POST_BOOTSTRAP=1
    fi
done

if [ "$POST_BOOTSTRAP" -eq 1 ]; then
    echo -e "${BOLD}${CYAN}🧹 Running Post-Bootstrap Cleanup...${NC}"
    echo "This will safely prune Docker build caches, package manager caches, and temp archives."

    # Optional: Log size before cleanup
    echo -e "\n${YELLOW}Current Cache Sizes:${NC}"
    sudo du -sh /root/.cache/uv /root/.cache/pip /var/tmp/ansible_pip_build/uv_cache 2>/dev/null || echo "No UV/Pip caches found."
    if command -v docker &> /dev/null; then
        sudo docker system df | grep "Build Caches" || true
    fi
    sudo du -sh /tmp/*.zip /tmp/*.tgz /tmp/*.tar /tmp/*.sh 2>/dev/null || echo "No large temp archives found."

    # 1. Safely Prune Docker Build Cache
    if command -v docker &> /dev/null; then
        echo -e "\n${BOLD}🐳 Pruning Docker Build Cache...${NC}"
        docker builder prune --all --force
    fi

    # 2. Safely Clean UV / PIP Caches
    echo -e "\n${BOLD}🧹 Cleaning UV / PIP Caches...${NC}"
    sudo rm -rf /root/.cache/pip /var/tmp/ansible_pip_build/uv_cache 2>/dev/null || true

    # Use uv cache prune instead of deleting the directory to preserve hardlinks
    if command -v uv &> /dev/null; then
        echo "Pruning uv cache..."
        uv cache prune || sudo uv cache prune || true
    fi

    if [ -n "$SUDO_USER" ]; then
        USER_HOME=$(eval echo "~$SUDO_USER")
        sudo rm -rf "$USER_HOME/.cache/pip" 2>/dev/null || true
    else
        sudo rm -rf ~/.cache/pip 2>/dev/null || true
    fi

    # 3. Clean Bootstrap Artifacts
    echo -e "\n${BOLD}🧹 Cleaning Bootstrap Temp Archives...${NC}"
    rm -f /tmp/consul.zip
    rm -f /tmp/nomad.zip
    rm -f /tmp/cni-plugins.tgz
    rm -f /tmp/get-docker.sh
    rm -f /tmp/pipecatapp.tar
    rm -f /opt/pipecatapp.tar
    rm -rf /tmp/consul
    rm -rf /tmp/nomad

    echo -e "\n${GREEN}✨ Post-Bootstrap Cleanup Complete!${NC}"
    df -h /
    exit 0
fi

if [ "$SCORCHED_EARTH" -eq 1 ]; then
    echo -e "${BOLD}${RED}⚠️  WARNING: SCORCHED EARTH MODE ACTIVATED ⚠️${NC}"
    echo -e "${RED}This will completely wipe all local caches (pip, uv, npm, etc.),"
    echo -e "reset the repository to a fresh git clone state (removing all untracked files),"
    echo -e "and DESTROY ALL infrastructure data for Nomad, Consul, Vault, and IPFS.${NC}"
    echo ""
    read -p "Are you sure you want to scorch the earth? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cleanup aborted."
        exit 1
    fi
    echo -e "${BOLD}${RED}Executing Scorched Earth Protocol...${NC}"
else
    echo -e "${BOLD}${YELLOW}⚠️  Starting Aggressive System Cleanup...${NC}"
fi

# 1. Docker Cleanup
if command -v docker &> /dev/null; then
    echo -e "\n${BOLD}🐳 Cleaning Docker System...${NC}"
    echo "Pruning stopped containers, unused networks, and dangling images..."
    docker system prune -a --force --volumes

    echo "Pruning build cache..."
    docker builder prune --all --force

    # Optional: Remove all unused images older than 24h, not just dangling ones
    docker image prune -a --filter "until=24h" --force
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

# 5. Dedicated Cache Scripts and Deduplication
echo -e "\n${BOLD}🧹 Running Dedicated Cache and Deduplication Scripts...${NC}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

if [ -x "${SCRIPT_DIR}/clean_caches.sh" ]; then
    echo "Executing clean_caches.sh..."
    "${SCRIPT_DIR}/clean_caches.sh"
else
    echo "Warning: clean_caches.sh not found or not executable."
fi

if [ -x "${SCRIPT_DIR}/dedup_venvs.py" ]; then
    echo "Executing dedup_venvs.py..."
    python3 "${SCRIPT_DIR}/dedup_venvs.py"
else
    echo "Warning: dedup_venvs.py not found or not executable."
fi

# 6. Bootstrap Artifacts Cleanup
echo -e "\n${BOLD}🧹 Cleaning Bootstrap Artifacts...${NC}"
# Remove downloaded archives
rm -f /tmp/consul.zip
rm -f /tmp/nomad.zip
rm -f /tmp/cni-plugins.tgz
rm -f /tmp/get-docker.sh
rm -f /tmp/pipecatapp.tar
rm -f /opt/pipecatapp.tar

# Remove extracted directories
rm -rf /tmp/consul
rm -rf /tmp/nomad

# 5b. General Temporary Files Cleanup
echo -e "\n${BOLD}🧹 Cleaning Temporary Files (older than 3 days)...${NC}"
sudo find /tmp -type f -atime +3 -delete 2>/dev/null || true
sudo find /var/tmp -type f -atime +3 -delete 2>/dev/null || true

echo -e "\n${BOLD}🧹 Cleaning UV Cache...${NC}"
sudo rm -rf /var/tmp/ansible_pip_build/uv_cache 2>/dev/null || true
if command -v uv &> /dev/null; then
    uv cache prune || sudo uv cache prune || true
fi

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
if [ -d "/opt/consul/data" ] || [ "$SCORCHED_EARTH" -eq 1 ]; then
    echo "Stopping Consul service (if running)..."
    sudo systemctl stop consul 2>/dev/null || true
    echo "Removing /opt/consul/data..."
    sudo rm -rf "/opt/consul/data"
fi

# Clean up Vault state (Scorched Earth)
if [ "$SCORCHED_EARTH" -eq 1 ]; then
    echo "Stopping Vault service (if running)..."
    sudo systemctl stop vault 2>/dev/null || true
    if [ -d "/opt/vault/data" ]; then
        echo "Removing /opt/vault/data..."
        sudo rm -rf "/opt/vault/data"
    fi
fi

# Clean up IPFS state (Scorched Earth)
if [ "$SCORCHED_EARTH" -eq 1 ]; then
    echo "Stopping IPFS service (if running)..."
    sudo systemctl stop ipfs 2>/dev/null || true
    if [ -d "/opt/unified_fs/ipfs" ]; then
        echo "Removing /opt/unified_fs/ipfs..."
        sudo rm -rf "/opt/unified_fs/ipfs"
    fi
fi

# Clean up Nomad state
if [ -d "/opt/nomad" ] || [ "$SCORCHED_EARTH" -eq 1 ]; then
    echo "Stopping Nomad service (if running)..."
    sudo systemctl stop nomad 2>/dev/null || true

    echo "Unmounting any active allocations in /opt/nomad..."
    for mount in $(mount | awk '{print $3}' | grep '^/opt/nomad/' | sort -r); do
        echo "Unmounting $mount"
        sudo umount "$mount" || true
    done

    if [ "$SCORCHED_EARTH" -eq 1 ]; then
        echo "Cleaning ENTIRE /opt/nomad state (Scorched Earth)..."
        sudo rm -rf /opt/nomad
    else
        echo "Cleaning /opt/nomad state (preserving models)..."
        # Find and delete everything in /opt/nomad EXCEPT the models directory
        # -mindepth 1 prevents matching /opt/nomad itself
        # -maxdepth 1 prevents diving into subdirectories for matching
        # ! -name "models" excludes the models folder
        # -exec rm -rf {} + executes rm -rf on the matched items
        sudo find /opt/nomad -mindepth 1 -maxdepth 1 ! -name "models" -exec rm -rf {} +
    fi
fi

# 8. Force kill orphaned and running opencode processes
echo -e "\n${BOLD}🔪 Terminating all running and orphaned opencode processes...${NC}"
sudo pkill -9 -x "opencode" || sudo pkill -9 -f "bin/opencode" || true


if [ "$SCORCHED_EARTH" -eq 1 ]; then
    echo -e "\n${BOLD}🔥 Scorched Earth: Wiping Global Caches & Untracked Files...${NC}"

    # Wipe user and root caches
    echo "Wiping ~/.cache and /root/.cache for pip, uv, npm, playwright, etc..."
    sudo rm -rf /root/.cache/pip /root/.cache/uv /root/.npm /root/.cache/ms-playwright 2>/dev/null || true

    if [ -n "$SUDO_USER" ]; then
        USER_HOME=$(eval echo "~$SUDO_USER")
        sudo rm -rf "$USER_HOME/.cache/pip" "$USER_HOME/.cache/uv" "$USER_HOME/.npm" "$USER_HOME/.cache/ms-playwright" 2>/dev/null || true
    else
        sudo rm -rf ~/.cache/pip ~/.cache/uv ~/.npm ~/.cache/ms-playwright 2>/dev/null || true
    fi

    echo "Resetting git repository to a clean state (removing all untracked files)..."
    # Ensure we are in the repo root
    REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    if [ -d "$REPO_ROOT/.git" ]; then
        cd "$REPO_ROOT"
        sudo git clean -fdx
    else
        echo -e "${YELLOW}Warning: Not inside a git repository, skipping git clean.${NC}"
    fi
fi

echo -e "\n${GREEN}✨ Cleanup Complete!${NC}"
df -h /

if [ -x "${SCRIPT_DIR}/ipfs_cleanup.sh" ]; then
    # Don't run ipfs_cleanup if we already wiped the IPFS directory entirely
    if [ "$SCORCHED_EARTH" -ne 1 ]; then
        echo "Executing ipfs_cleanup.sh..."
        "${SCRIPT_DIR}/ipfs_cleanup.sh"
    fi
else
    echo "Warning: ipfs_cleanup.sh not found or not executable."
fi
