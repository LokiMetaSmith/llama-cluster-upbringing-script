#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -euo pipefail

# --- Configuration ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
CONFIG_FILE="$SCRIPT_DIR/setup.conf"
MODULE_DIR="$SCRIPT_DIR/modules"

# --- Functions ---
log() {
    echo "[INFO] $1"
}

error() {
    echo "[ERROR] $1" >&2
    exit 1
}

# --- Main Script ---
log "Starting initial machine setup..."

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    error "This script must be run as root."
fi

# Source the configuration file
if [ -f "$CONFIG_FILE" ]; then
    log "Loading configuration from $CONFIG_FILE"
    source "$CONFIG_FILE"
else
    error "Configuration file not found: $CONFIG_FILE"
fi

# Run modules
for module in "$MODULE_DIR"/*.sh; do
    if [ -f "$module" ]; then
        log "Running module: $(basename "$module")"
        source "$module"
        log "Finished module: $(basename "$module")"
    fi
done

log "Generating dynamic inventory..."
bash "$SCRIPT_DIR/update_inventory.sh"

# Ensure repository ownership is restored to the non-root user
TARGET_REPO_USER="${SUDO_USER:-${USERNAME:-}}"
if [ -n "$TARGET_REPO_USER" ] && id "$TARGET_REPO_USER" &>/dev/null; then
    REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
    log "Restoring repository ownership in $REPO_ROOT for $TARGET_REPO_USER..."
    chown -R "$TARGET_REPO_USER":"$TARGET_REPO_USER" "$REPO_ROOT" 2>/dev/null || true
fi

log "Initial machine setup complete."
log "Please reboot the machine for all changes to take effect."
