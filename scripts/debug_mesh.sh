#!/bin/bash

echo "=== Network Interface Summary ==="
ip -4 a | grep -E 'eth|en|wl|tailscale'

echo -e "\n=== Tailscale Status ==="
if command -v tailscale &> /dev/null; then
    tailscale status
    echo -e "\nTailscale IP:"
    tailscale ip -4
else
    echo "Tailscale binary not found."
fi

echo -e "\n=== Headscale Status (Controller Only) ==="
if systemctl is-active --quiet headscale; then
    echo "Headscale Service: Active"
    if command -v headscale &> /dev/null; then
        echo "Nodes list:"
        headscale nodes list
    fi
else
    echo "Headscale Service: Not Active (or not installed on this node)"
fi

echo -e "\n=== Consul Members (Mesh) ==="
if command -v consul &> /dev/null; then
    consul members
else
    echo "Consul binary not found."
fi

echo -e "\n=== Nomad Members (Mesh) ==="
if command -v nomad &> /dev/null; then
    nomad server members
    echo "---"
    nomad node status
else
    echo "Nomad binary not found."
fi

echo -e "\n=== Port Bindings (Cluster IP) ==="
# Try to find the tailscale IP
MESH_IP=$(ip -4 addr show tailscale0 2>/dev/null | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
if [ -n "$MESH_IP" ]; then
    echo "Checking bindings on $MESH_IP..."
    ss -tulpn | grep "$MESH_IP"
else
    echo "No tailscale0 IP found."
fi
