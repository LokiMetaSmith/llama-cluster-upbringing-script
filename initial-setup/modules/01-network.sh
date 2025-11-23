#!/bin/bash

log "Configuring network..."

# --- Dynamically determine the primary network interface ---
INTERFACE=$(ip route | grep '^default' | awk '{print $5}' | head -n1)
if [ -z "$INTERFACE" ]; then
    log "Could not determine primary network interface. Falling back to eth0."
    INTERFACE="eth0"
fi
log "Using network interface: $INTERFACE"

# --- Helper function to check if an element is in a bash array ---
containsElement () {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}

# --- Get current hostname ---
CURRENT_HOSTNAME=$(hostname)

# --- Derive NODE_ID for cluster network ---
# If hostname is 'devbox', use 10. Otherwise extract number and add 10.
if [ "$CURRENT_HOSTNAME" == "devbox" ]; then
    NODE_ID=10
else
    NODE_ID_SUFFIX=$(echo "$CURRENT_HOSTNAME" | tr -dc '0-9')
    if [ -z "$NODE_ID_SUFFIX" ]; then
        # Fallback if no number found, though this shouldn't happen with correct naming
        NODE_ID=11
        log "WARNING: Could not extract number from hostname $CURRENT_HOSTNAME. Defaulting to 11."
    else
        NODE_ID=$((NODE_ID_SUFFIX + 10))
    fi
fi
log "Derived Node ID: $NODE_ID (Cluster IP: ${CLUSTER_SUBNET_PREFIX}.${NODE_ID})"

# --- Configure Network Interfaces ---
# All nodes use DHCP for the primary interface (WAN) and a static alias for the cluster (LAN).

cat > /etc/network/interfaces <<EOL
# This file is managed by the llama-cluster-upbringing-script

# The loopback network interface
auto lo
iface lo inet loopback

# Primary Interface (WAN) - Gets Internet from Home Router
auto $INTERFACE
iface $INTERFACE inet dhcp

# Virtual Interface (Cluster LAN) - Private Static IP
auto $INTERFACE:0
iface $INTERFACE:0 inet static
    address ${CLUSTER_SUBNET_PREFIX}.${NODE_ID}
    netmask ${CLUSTER_NETMASK}
EOL

log "Network configuration written. WAN: DHCP, LAN: ${CLUSTER_SUBNET_PREFIX}.${NODE_ID}"


# --- Restart networking service ---
log "Restarting networking service to apply changes..."
if systemctl list-units --type=service | grep -q 'networking.service'; then
    systemctl restart networking
elif systemctl list-units --type=service | grep -q 'systemd-networkd.service'; then
    systemctl restart systemd-networkd
else
    log "Could not find networking.service or systemd-networkd.service to restart."
fi

log "Network configuration complete."
