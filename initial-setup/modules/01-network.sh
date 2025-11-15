#!/bin/bash
#
# Manages network configuration for controller and worker nodes.
# It identifies the primary network interface and configures a static IP
# for controller nodes to ensure stable communication.

# --- Configuration ---
# All configuration is now sourced from setup.conf to centralize settings.

# --- Script Logic ---
echo "[INFO] Configuring network..."

# Load configuration safely
source "$(dirname "$0")/../setup.conf"

# --- Functions ---
get_primary_interface() {
    # Get the interface associated with the default route
    ip route | grep '^default' | awk '{print $5}' | head -n1
}

# --- Main Execution ---
PRIMARY_INTERFACE=$(get_primary_interface)

if [ -z "$PRIMARY_INTERFACE" ]; then
    echo "[ERROR] Could not determine the primary network interface. Exiting."
    exit 1
fi

echo "[INFO] Detected primary network interface: $PRIMARY_INTERFACE"

if [ "$NODE_TYPE" = "controller" ]; then
    echo "[INFO] Node '$HOSTNAME' is a controller. Configuring static IP: $CONTROLLER_STATIC_IP..."

    # Create Netplan configuration for a static IP on the primary interface
    # This overwrites any existing config for the interface to ensure consistency.
    cat > /etc/netplan/01-static.yaml <<- EOM
network:
  version: 2
  ethernets:
    $PRIMARY_INTERFACE:
      dhcp4: no
      addresses:
        - $CONTROLLER_STATIC_IP/24
      routes:
        - to: default
          via: $GATEWAY_IP
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
EOM

    echo "[INFO] Netplan configuration written for $PRIMARY_INTERFACE."
    echo "[INFO] Applying Netplan configuration..."
    netplan apply

    # Verify the IP address was set
    if ip addr show "$PRIMARY_INTERFACE" | grep -q "$CONTROLLER_STATIC_IP"; then
        echo "[INFO] Successfully set static IP on $PRIMARY_INTERFACE."
    else
        echo "[ERROR] Failed to set static IP on $PRIMARY_INTERFACE. Please check Netplan configuration and logs."
        exit 1
    fi

elif [ "$NODE_TYPE" = "worker" ]; then
    echo "[INFO] Node '$HOSTNAME' is a worker. Ensuring it uses DHCP..."

    # Create a simple DHCP configuration for the primary interface.
    # This ensures workers get their IP from the network's DHCP server.
    cat > /etc/netplan/01-dhcp.yaml <<- EOM
network:
  version: 2
  ethernets:
    $PRIMARY_INTERFACE:
      dhcp4: yes
EOM
    echo "[INFO] Netplan DHCP configuration written for $PRIMARY_INTERFACE."
    echo "[INFO] Applying Netplan configuration..."
    netplan apply
else
    echo "[WARNING] NODE_TYPE is not set to 'controller' or 'worker'. Skipping network configuration."
fi

echo "[INFO] Network configuration complete."
