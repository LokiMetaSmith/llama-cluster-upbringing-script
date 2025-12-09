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
             # Note: +ipv4.addresses works for adding.
             nmcli connection modify "$CON_NAME" +ipv4.addresses "$CLUSTER_IP/$CLUSTER_NETMASK"

             # Reapply the connection to take effect (might briefly drop connection, but safer than restarting service)
             # However, bringing up the connection again might be disruptive.
             # Let's try to just bring it up which re-applies changes.
             nmcli connection up "$CON_NAME"
             log "Secondary IP $CLUSTER_IP added to connection '$CON_NAME'."
        else
             log "IP $CLUSTER_IP already configured on '$CON_NAME'."
        fi
    else
        log "No active NetworkManager connection found for $INTERFACE. Attempting runtime configuration..."
        ip addr add "$CLUSTER_IP/$CLUSTER_NETMASK" dev "$INTERFACE" || log "Failed to add IP address."
    fi

elif [ -d "/etc/network/interfaces.d" ] || [ -f "/etc/network/interfaces" ]; then
    # Fallback to ifupdown ONLY if we are sure it's safe.
    # If the interface looks like wireless (wl*), overwriting /etc/network/interfaces with a simple 'dhcp' stanza
    # will break WPA authentication unless wpa-conf is handled.

    if [[ "$INTERFACE" == wl* ]]; then
        log "Wireless interface detected ($INTERFACE). Skipping /etc/network/interfaces overwrite to prevent breaking WiFi."
        log "Adding runtime IP alias instead..."
        ip addr add "$CLUSTER_IP/$CLUSTER_NETMASK" dev "$INTERFACE" || true
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

        log "Restarting networking service..."
        if systemctl list-units --type=service | grep -q 'networking.service'; then
            systemctl restart networking
        else
            log "networking.service not found. You may need to manually restart networking."
        fi
    fi
else
    # Universal fallback
    log "No supported network manager detected (NetworkManager or ifupdown). Using runtime configuration."
    ip addr add "$CLUSTER_IP/$CLUSTER_NETMASK" dev "$INTERFACE" || true
fi

log "Network configuration complete."
