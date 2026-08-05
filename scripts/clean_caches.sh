#!/bin/bash
# clean_caches.sh - Script to remove large temporary cache directories to free disk space.

echo "Starting cache cleanup..."

# Target specific user home cache directories
USER_HOME="/home/pipecatapp"

if [ -d "$USER_HOME" ]; then
    echo "Cleaning caches for $USER_HOME..."
    rm -rf "$USER_HOME/.cache/pip"
    rm -rf "$USER_HOME/.cache/uv"
    rm -rf "$USER_HOME/.npm/_cacache"
    rm -rf "$USER_HOME/.npm/_npx"

    # Keep only the most recent playwright caches if needed, or wipe all to save space
    # (Since this is an automated node, wiping old browser binaries often saves GBs)
    rm -rf "$USER_HOME/.cache/ms-playwright"
else
    echo "User home $USER_HOME not found, skipping."
fi

# Clean root caches if script is run with sudo
echo "Cleaning root caches..."
sudo rm -rf /root/.cache/pip
sudo rm -rf /root/.cache/uv
sudo rm -rf /root/.cache/ms-playwright
sudo rm -rf /root/.npm/_cacache
sudo rm -rf /root/.npm/_npx
sudo rm -rf /root/.cache/ccache
sudo rm -rf /root/.cache/node-gyp
sudo rm -rf /root/.cargo/registry
sudo rm -rf /root/.cargo/git

# Clean apt cache
echo "Cleaning apt cache..."
sudo apt-get clean

echo "Cache cleanup complete."
