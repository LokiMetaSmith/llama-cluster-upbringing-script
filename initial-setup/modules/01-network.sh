#!/bin/bash

echo "Configuring network..."

# Check if the IP is already configured
if ip addr show "$INTERFACE" | grep -q "$STATIC_IP"; then
    echo "Static IP $STATIC_IP is already configured on $INTERFACE."
    exit 0
fi

# Backup the original interfaces file
cp /etc/network/interfaces /etc/network/interfaces.bak

# Create the new interfaces file
cat > /etc/network/interfaces <<EOL
auto $INTERFACE
iface $INTERFACE inet static
    address $STATIC_IP
    netmask $NETMASK
    gateway $GATEWAY
EOL

echo "Static IP configured. Restarting networking service..."
systemctl restart networking

echo "Network configuration complete."
