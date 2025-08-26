#!/bin/bash

log "Configuring hostname..."

# Get the current hostname
CURRENT_HOSTNAME=$(hostname)

# Safety check: If the current hostname is not a generic default (like 'debian')
# and it does not match the HOSTNAME variable in the config, then we have a
# potentially dangerous mismatch. Abort to prevent accidentally re-configuring
# an already-configured node with the wrong identity.
if [ "$CURRENT_HOSTNAME" != "debian" ] && [ "$CURRENT_HOSTNAME" != "$HOSTNAME" ]; then
    error "FATAL: Hostname mismatch detected."
    error "This machine's current hostname is '$CURRENT_HOSTNAME', but the HOSTNAME variable in 'setup.conf' is set to '$HOSTNAME'."
    error "To prevent catastrophic misconfiguration, the script has been aborted."
    error "Please edit 'setup.conf' to match the intended hostname for this machine before re-running."
    exit 1
fi

# Set hostname if it's different from the current one
if [ "$CURRENT_HOSTNAME" != "$HOSTNAME" ]; then
    log "Setting hostname to '$HOSTNAME'..."
    hostnamectl set-hostname "$HOSTNAME"
    log "Hostname has been set to '$HOSTNAME'."
else
    log "Hostname is already set to '$HOSTNAME'. No changes made."
fi
