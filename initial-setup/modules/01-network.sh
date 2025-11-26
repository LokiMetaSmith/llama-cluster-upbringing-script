#!/bin/bash

log "Configuring network..."

# --- Dynamically determine the primary network interface ---
INTERFACE=$(ip route | grep '^default' | awk '{print $5}' | head -n1)
if [ -z "$INTERFACE" ]; then
    log "Could not determine primary network interface. Falling back to eth0."
    INTERFACE="eth0"
fi
log "Using network interface: $INTERFACE"

# --- Get current hostname ---
CURRENT_HOSTNAME=$(hostname)

# --- Derive NODE_ID for cluster network ---
# Logic: Extract number from hostname (e.g., worker1 -> 11). Default 'devbox' -> 10.
if [ "$CURRENT_HOSTNAME" == "devbox" ]; then
    NODE_ID=10
else
    NODE_ID_SUFFIX=$(echo "$CURRENT_HOSTNAME" | tr -dc '0-9')
    if [ -z "$NODE_ID_SUFFIX" ]; then
        NODE_ID=11 # Fallback
    else
        NODE_ID=$((NODE_ID_SUFFIX + 10))
    fi
fi

CLUSTER_IP="${CLUSTER_SUBNET_PREFIX}.${NODE_ID}"
log "Configuring Dual-Stack Network on $INTERFACE..."
log "  - WAN (Home): DHCP"
log "  - LAN (Cluster): $CLUSTER_IP"

# --- Configure Interfaces ---
cat > /etc/network/interfaces <<EOL
# Managed by llama-cluster-upbringing-script

auto lo
iface lo inet loopback

# Primary Interface: DHCP from Home Router (Internet Access)
auto $INTERFACE
iface $INTERFACE inet dhcp

# Virtual Alias: Static Private IP (Cluster Traffic)
auto $INTERFACE:0
iface $INTERFACE:0 inet static
    address $CLUSTER_IP
    netmask $CLUSTER_NETMASK
EOL

log "Network configuration written."

# --- Restart networking service ---
log "Restarting networking service..."
if systemctl list-units --type=service | grep -q 'networking.service'; then
    systemctl restart networking
elif systemctl list-units --type=service | grep -q 'systemd-networkd.service'; then
    systemctl restart systemd-networkd
else
    log "Could not find networking service to restart."
fi

log "Network configuration complete."
