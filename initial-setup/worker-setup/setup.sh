#!/bin/bash

# This script performs the absolute minimal setup required for a new
# Debian machine to be provisioned by the Ansible controller.

# --- Pre-requisites ---
# 1. A minimal Debian 12 (Bookworm) installation is complete.
# 2. This script is run as the root user (or with sudo).
# 3. The machine has a basic internet connection.

set -e
echo "--- Starting Worker Node Initial Setup ---"

# 1. Update package cache
echo "--> Updating apt package cache..."
apt-get update

# 2. Install essential packages
# openssh-server is required for Ansible to connect.
# python3 is required for Ansible modules to run.
# sudo is required for privilege escalation.
echo "--> Installing essential packages (openssh-server, python3, sudo)..."
apt-get install -y openssh-server python3 sudo

# 3. Add the standard user to the sudo group
# Replace 'user' with the actual username of the non-root user you created
# during Debian installation. This user will be the ansible_user.
echo "--> Adding the 'user' to the sudo group..."
usermod -aG sudo user

echo "--- Manual Steps Required ---"
echo "This script has installed the necessary packages. You must now manually"
echo "configure the networking for this node."
echo ""
echo "1. Set a static IP address for this machine."
echo "   - Example for /etc/network/interfaces:"
echo "     auto enp3s0"
echo "     iface enp3s0 inet static"
echo "        address 192.168.1.XX"
echo "        netmask 255.255.255.0"
echo "        gateway 192.168.1.1"
echo ""
echo "2. Set the hostname for this machine."
echo "   - Edit /etc/hostname and /etc/hosts."
echo ""
echo "3. REBOOT the machine after making networking changes."
echo ""
echo "4. After rebooting, ensure the Ansible controller's SSH key is"
echo "   copied to this machine's 'user' account using:"
echo "   ssh-copy-id user@<this_machine_ip>"
echo ""
echo "--- Initial Setup Complete ---"
echo "This node is now ready to be added to the Ansible inventory and provisioned."
