#!/bin/bash

log "Configuring user..."

# Create user if it doesn't exist
if ! /usr/bin/id -u "$USERNAME" >/dev/null 2>&1; then
    log "User $USERNAME does not exist. Creating user..."
    /usr/sbin/useradd -m -s /bin/bash "$USERNAME"
    log "User $USERNAME created."
fi

# Check if the user is already in the sudo group
if /usr/bin/groups "$USERNAME" | grep -q '\bsudo\b'; then
    log "User $USERNAME is already in the sudo group."
else
    log "Adding user $USERNAME to the sudo group..."
    /usr/sbin/usermod -aG sudo "$USERNAME"
    log "User $USERNAME added to the sudo group."
fi

log "User configuration complete."
