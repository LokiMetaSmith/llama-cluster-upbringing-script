#!/bin/bash

echo "Configuring SSH..."

# Check if ssh is installed
if ! dpkg -s openssh-server >/dev/null 2>&1; then
    echo "Installing OpenSSH server..."
    apt-get update
    apt-get install -y openssh-server
else
    echo "OpenSSH server is already installed."
fi

# Ensure the ssh service is running and enabled
systemctl is-active --quiet ssh || systemctl start ssh
systemctl is-enabled --quiet ssh || systemctl enable ssh

echo "SSH configuration complete."
