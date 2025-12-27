#!/bin/bash

# Ensure CONFIG_FILE is defined (fallback if run standalone)
if [ -z "${CONFIG_FILE:-}" ]; then
    CONFIG_FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/setup.conf"
fi

# Source config if available
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
fi

# --- Helper Functions (Standalone Safety) ---

if ! command -v log &> /dev/null; then
    log() { echo "[INFO] $1"; }
fi

if ! command -v error &> /dev/null; then
    error() { echo "[ERROR] $1" >&2; exit 1; }
fi

check_ip_availability() {
    local target_ip="$1"
    # Ping the IP directly to avoid DNS dependencies during bootstrap.
    if ping -c 1 -W 1 "$target_ip" &>/dev/null; then
        return 1 # Taken (ping success)
    else
        return 0 # Available (ping failed)
    fi
}

update_setup_conf() {
    local new_hostname="$1"
    local config_file="$2"

    if grep -q "^HOSTNAME=" "$config_file"; then
        sed -i "s/^HOSTNAME=.*/HOSTNAME=\"$new_hostname\"/" "$config_file"
    else
        echo "HOSTNAME=\"$new_hostname\"" >> "$config_file"
    fi
}

calculate_ip() {
    local id="$1"
    local role="$2"
    local offset

    if [ "$role" == "controller" ]; then
        offset=10
    else
        offset=50
    fi

    local node_id=$((id + offset))
    echo "${CLUSTER_SUBNET_PREFIX}.${node_id}"
}

# --- Main Logic ---

log "Configuring hostname..."
CURRENT_HOSTNAME=$(hostname)

# Check if a valid hostname is already set in the config (e.g. from a previous run)
if [ -n "${HOSTNAME:-}" ] && [ "$HOSTNAME" != "debian" ] && [ "$HOSTNAME" != "localhost" ]; then
    # Double check if it matches dynamic pattern or is a manual override
    log "Hostname '$HOSTNAME' is defined in setup.conf. Verifying..."
    if [ "$CURRENT_HOSTNAME" == "$HOSTNAME" ]; then
        log "Hostname is already set to '$HOSTNAME'. No changes made."
        exit 0
    else
        log "Applying pre-defined hostname '$HOSTNAME'..."
        hostnamectl set-hostname "$HOSTNAME"
        exit 0
    fi
fi

log "Determining dynamic hostname..."

FOUND_HOSTNAME=""

# 1. Try to become a Controller
log "Checking controller slots (1 to $MAX_CONTROLLERS)..."
for ((i=1; i<=MAX_CONTROLLERS; i++)); do
    CANDIDATE="${BASE_HOSTNAME}-${i}-controller"
    CANDIDATE_IP=$(calculate_ip "$i" "controller")

    # Check self
    if [ "$CURRENT_HOSTNAME" == "$CANDIDATE" ]; then
        FOUND_HOSTNAME="$CANDIDATE"
        break
    fi

    # Check IP availability
    if check_ip_availability "$CANDIDATE_IP"; then
        log "Slot available: $CANDIDATE (IP: $CANDIDATE_IP)"
        FOUND_HOSTNAME="$CANDIDATE"
        break
    else
        log "Slot taken: $CANDIDATE (IP: $CANDIDATE_IP)"
    fi
done

# 2. If no controller slot, become a Worker
if [ -z "$FOUND_HOSTNAME" ]; then
    log "All controller slots taken. Checking worker slots..."
    i=1
    while true; do
        CANDIDATE="${BASE_HOSTNAME}-${i}-worker"
        CANDIDATE_IP=$(calculate_ip "$i" "worker")

        if [ "$CURRENT_HOSTNAME" == "$CANDIDATE" ]; then
            FOUND_HOSTNAME="$CANDIDATE"
            break
        fi

        if check_ip_availability "$CANDIDATE_IP"; then
            log "Slot available: $CANDIDATE (IP: $CANDIDATE_IP)"
            FOUND_HOSTNAME="$CANDIDATE"
            break
        else
            log "Slot taken: $CANDIDATE (IP: $CANDIDATE_IP)"
            ((i++))
        fi

        if [ $i -gt 100 ]; then
            error "Could not find a free worker slot after 100 attempts. Aborting."
        fi
    done
fi

# --- Apply Changes ---

if [ -n "$FOUND_HOSTNAME" ]; then
    log "Selected hostname: $FOUND_HOSTNAME"

    if [ "$CURRENT_HOSTNAME" != "$FOUND_HOSTNAME" ]; then
        log "Setting hostname to '$FOUND_HOSTNAME'..."
        hostnamectl set-hostname "$FOUND_HOSTNAME"
        log "Hostname has been set."
    else
        log "Hostname is already correct."
    fi

    log "Updating setup.conf with HOSTNAME..."
    update_setup_conf "$FOUND_HOSTNAME" "$CONFIG_FILE"

    # Reload config in current shell
    HOSTNAME="$FOUND_HOSTNAME"
else
    error "Failed to determine a hostname."
fi
