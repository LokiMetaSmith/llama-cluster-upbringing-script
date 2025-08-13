#!/bin/bash

log "Configuring network..."

# Check if the IP is already configured
if ip addr show "$INTERFACE" | grep -q "$STATIC_IP"; then
    log "Static IP $STATIC_IP is already configured on $INTERFACE."
    return 0 # Use return instead of exit in a sourced script
fi

# Backup the original interfaces file
if [ -f /etc/network/interfaces ]; then
    cp /etc/network/interfaces /etc/network/interfaces.bak
fi

# Create the new interfaces file
cat > /etc/network/interfaces <<EOL
auto $INTERFACE
iface $INTERFACE inet static
    address $STATIC_IP
    netmask $NETMASK
    gateway $GATEWAY
EOL

log "Static IP configured. Restarting networking service..."
if systemctl list-units --type=service | grep -q 'networking.service'; then
    systemctl restart networking
elif systemctl list-units --type=service | grep -q 'systemd-networkd.service'; then
    systemctl restart systemd-networkd
else
    log "Could not find networking.service or systemd-networkd.service to restart."
fi

log "Network configuration complete."
