#!/bin/bash

log "Configuring network..."

# --- Helper function to check if an element is in a bash array ---
containsElement () {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}

# --- Get current hostname ---
CURRENT_HOSTNAME=$(hostname)

# --- Determine node type and configure network ---
if containsElement "$CURRENT_HOSTNAME" "${CONTROLLER_HOSTNAMES[@]}"; then
    # This is a CONTROLLER node, configure a static IP.
    log "Node '$CURRENT_HOSTNAME' is a controller. Configuring static IP: $STATIC_IP..."

    # Check if the IP is already configured
    if ip addr show "$INTERFACE" | grep -q "$STATIC_IP"; then
        log "Static IP $STATIC_IP is already configured on $INTERFACE."
        return 0
    fi

    cat > /etc/network/interfaces <<EOL
# This file is managed by the llama-cluster-upbringing-script
auto $INTERFACE
iface $INTERFACE inet static
    address $STATIC_IP
    netmask $NETMASK
    gateway $GATEWAY
EOL
    log "Static IP configuration written for $INTERFACE."

else
    # This is a WORKER node, configure DHCP.
    log "Node '$CURRENT_HOSTNAME' is a worker. Configuring DHCP..."

    # Check if DHCP is already configured
    if grep -q "iface $INTERFACE inet dhcp" /etc/network/interfaces; then
        log "DHCP is already configured on $INTERFACE."
        return 0
    fi

    cat > /etc/network/interfaces <<EOL
# This file is managed by the llama-cluster-upbringing-script
auto $INTERFACE
iface $INTERFACE inet dhcp
EOL
    log "DHCP configuration written for $INTERFACE."
fi


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
