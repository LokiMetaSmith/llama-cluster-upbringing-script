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

# Helper function to add runtime IP safely
add_runtime_ip() {
    local ip_cidr="$1"
    local dev="$2"
    log "Attempting runtime configuration: ip addr add $ip_cidr dev $dev"
    if ip addr show dev "$dev" | grep -q "$CLUSTER_IP"; then
         log "IP $CLUSTER_IP is already assigned to $dev."
    else
         ip addr add "$ip_cidr" dev "$dev" || log "Warning: Failed to add IP address."
    fi
}

# Check if NetworkManager is active
if command -v nmcli >/dev/null && nmcli general status | grep -q "connected"; then
    log "NetworkManager detected. Using nmcli to configure secondary IP..."

    # Find the active connection for the interface
    CON_NAME=$(nmcli -t -f NAME,DEVICE connection show --active | grep ":$INTERFACE" | cut -d: -f1 | head -n1)

    if [ -n "$CON_NAME" ]; then
        log "Active connection found: '$CON_NAME'. Adding alias IP if missing..."

        # Check if IP is already added to avoid duplication
        CURRENT_IPV4=$(nmcli -g ipv4.addresses connection show "$CON_NAME")
        if [[ "$CURRENT_IPV4" != *"$CLUSTER_IP"* ]]; then
             # We want to ADD the IP, not replace.
             nmcli connection modify "$CON_NAME" +ipv4.addresses "$CLUSTER_IP/$CLUSTER_NETMASK"

             # Reapply the connection
             nmcli connection up "$CON_NAME"
             log "Secondary IP $CLUSTER_IP added to connection '$CON_NAME'."
        else
             log "IP $CLUSTER_IP already configured on '$CON_NAME'."
        fi
    else
        log "No active NetworkManager connection found for $INTERFACE."
        add_runtime_ip "$CLUSTER_IP/$CLUSTER_NETMASK" "$INTERFACE"
    fi

elif [ -d "/etc/network/interfaces.d" ] || [ -f "/etc/network/interfaces" ]; then
    # Fallback to ifupdown ONLY if we are sure it's safe.
    # If the interface looks like wireless (wl*), overwriting /etc/network/interfaces with a simple 'dhcp' stanza
    # will break WPA authentication unless wpa-conf is handled.

    if [[ "$INTERFACE" == wl* ]]; then
        log "Wireless interface detected ($INTERFACE). Skipping /etc/network/interfaces overwrite to prevent breaking WiFi."
        add_runtime_ip "$CLUSTER_IP/$CLUSTER_NETMASK" "$INTERFACE"
    else
        log "Configuring /etc/network/interfaces for wired interface..."
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
        log "Network configuration written to /etc/network/interfaces."

        # We wrote to a config file, so we really should try to restart the service to apply it.
        # But we only do this in the 'ifupdown' block.
        log "Restarting networking service..."
        if systemctl list-units --type=service | grep -q 'networking.service'; then
            systemctl restart networking
        else
            log "networking.service not found. Manual restart may be required."
        fi
    fi
else
    # Universal fallback (NixOS, or others)
    log "No supported network manager detected (NetworkManager or ifupdown). Using runtime configuration."
    add_runtime_ip "$CLUSTER_IP/$CLUSTER_NETMASK" "$INTERFACE"
fi

# --- Final Service Restart Attempt (Generic) ---
# This ensures that if we made changes (or if the system state is inconsistent),
# we try to poke relevant services, ignoring failures if they don't exist.
log "Ensuring network services are in consistent state..."
for service in networking NetworkManager systemd-networkd; do
    if systemctl is-active --quiet "$service"; then
        log "Restarting active service: $service"
        systemctl restart "$service" || true
    fi
done

log "Network configuration complete."
