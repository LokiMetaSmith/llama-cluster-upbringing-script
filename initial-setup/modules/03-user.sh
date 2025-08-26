#!/bin/bash

log "Configuring user..."

# Create user if it doesn't exist
if ! id -u "$USERNAME" >/dev/null 2>&1; then
    log "User $USERNAME does not exist. Creating user..."
    useradd -m -s /bin/bash "$USERNAME"
    log "User $USERNAME created."
fi

# Check if usermod command exists
if ! command -v usermod >/dev/null 2>&1; then
    log "usermod command not found. Installing passwd package..."
    apt-get update
    apt-get install -y passwd
fi

# Check if the user is already in the sudo group
if groups "$USERNAME" | grep -q '\bsudo\b'; then
    log "User $USERNAME is already in the sudo group."
else
    log "Adding user $USERNAME to the sudo group..."
    /usr/sbin/usermod -aG sudo "$USERNAME"
    log "User $USERNAME added to the sudo group."
fi

log "User configuration complete."
