#!/bin/bash
# ==============================================================================
# 00-usb-imprint.sh - Cluster Credential & Keychain Auto-Enrollment Module
# ==============================================================================
# Checks for cluster credentials either pre-bundled in /opt/cluster_keys or
# located on a FAT32 USB partition labeled 'CONFIGS'.
# Automatically imports mTLS certificates, enrolls in Tailscale/Headscale mesh,
# installs operator SSH keys, and configures Consul & Nomad clients.
# ==============================================================================

echo "[INFO] Checking for Cluster Credential Imprints & Keychains..."

# Ensure clock sync is stepped immediately to avoid TLS / GPG expiration issues
if command -v chronyc &>/dev/null; then
    echo "[INFO] Stepping system clock via Chrony..."
    chronyc makestep 2>/dev/null || true
fi

SOURCE_DIR=""
MNT_DIR=""

# 1. Check for pre-bundled ISO keys
if [ -d "/opt/cluster_keys" ] && [ -f "/opt/cluster_keys/mesh_auth_key" ]; then
    echo "[INFO] Found pre-bundled credentials in /opt/cluster_keys"
    SOURCE_DIR="/opt/cluster_keys"
fi

# 2. Check for USB CONFIGS partition
if [ -z "$SOURCE_DIR" ]; then
    CONFIGS_PART=$(blkid -L CONFIGS 2>/dev/null || true)
    if [ -n "$CONFIGS_PART" ]; then
        echo "[INFO] Found CONFIGS partition at $CONFIGS_PART"
        MNT_DIR=$(mktemp -d)
        if mount "$CONFIGS_PART" "$MNT_DIR" 2>/dev/null; then
            echo "[INFO] Mounted CONFIGS partition at $MNT_DIR"
            SOURCE_DIR="$MNT_DIR"
        else
            echo "[WARN] Failed to mount CONFIGS partition."
        fi
    fi
fi

if [ -n "$SOURCE_DIR" ]; then
    echo "[INFO] Importing cluster credentials from $SOURCE_DIR..."

    # 1. Controller IP & Headscale Endpoint
    if [ -f "$SOURCE_DIR/controller_ip" ]; then
        CONTROLLER_IP=$(cat "$SOURCE_DIR/controller_ip" | tr -d ' \n\r')
        if [ -n "$CONTROLLER_IP" ]; then
            echo "[INFO] Found Controller IP: $CONTROLLER_IP"
            echo "$CONTROLLER_IP" > /etc/pipecat_controller_ip
            if [ -f "$CONFIG_FILE" ]; then
                if grep -q "^CONTROL_NODE_IP=" "$CONFIG_FILE"; then
                    sed -i "s/^CONTROL_NODE_IP=.*/CONTROL_NODE_IP=\"$CONTROLLER_IP\"/" "$CONFIG_FILE"
                else
                    echo "CONTROL_NODE_IP=\"$CONTROLLER_IP\"" >> "$CONFIG_FILE"
                fi
            fi
            export CONTROL_NODE_IP="$CONTROLLER_IP"
        fi
    fi

    # 2. Authorized SSH Public Keys
    USER_HOME="/home/${USERNAME:-pipecatapp}"
    SSH_DIR="$USER_HOME/.ssh"
    mkdir -p "$SSH_DIR"
    chmod 700 "$SSH_DIR"

    if [ -f "$SOURCE_DIR/authorized_keys" ]; then
        echo "[INFO] Applying authorized SSH keys..."
        cat "$SOURCE_DIR/authorized_keys" >> "$SSH_DIR/authorized_keys"
    fi
    if [ -f "$SOURCE_DIR/fido_authorized_keys" ]; then
        echo "[INFO] Applying FIDO SSH keys..."
        cat "$SOURCE_DIR/fido_authorized_keys" >> "$SSH_DIR/authorized_keys"
    fi

    if [ -f "$SSH_DIR/authorized_keys" ]; then
        sort -u "$SSH_DIR/authorized_keys" -o "$SSH_DIR/authorized_keys"
        chown -R "${USERNAME:-pipecatapp}:${USERNAME:-pipecatapp}" "$SSH_DIR"
        chmod 600 "$SSH_DIR/authorized_keys"
        echo "[INFO] Configured SSH keys for ${USERNAME:-pipecatapp}."
    fi

    # 3. Headscale Auth Key & Mesh Joining
    if [ -f "$SOURCE_DIR/mesh_auth_key" ]; then
        echo "[INFO] Found Headscale Auth Key."
        cp "$SOURCE_DIR/mesh_auth_key" /etc/pipecat_mesh_auth_key
        chmod 600 /etc/pipecat_mesh_auth_key

        HEADSCALE_URL="https://headscale.local.mesh"
        if [ -f "$SOURCE_DIR/headscale_url" ]; then
            HEADSCALE_URL=$(cat "$SOURCE_DIR/headscale_url" | tr -d ' \n\r')
            cp "$SOURCE_DIR/headscale_url" /etc/pipecat_headscale_url
            chmod 600 /etc/pipecat_headscale_url
        fi

        if command -v tailscale &>/dev/null; then
            echo "[INFO] Activating Tailscale mesh connection to ${HEADSCALE_URL}..."
            tailscale up --login-server="${HEADSCALE_URL}" --authkey="$(cat /etc/pipecat_mesh_auth_key)" --accept-routes --reset || true
        else
            echo "[INFO] Tailscale not yet installed. Auth key staged at /etc/pipecat_mesh_auth_key for bootstrap."
        fi
    fi

    # 4. Nomad Mutual TLS Certificates & Trust Store
    if [ -f "$SOURCE_DIR/nomad_ca.pem" ]; then
        echo "[INFO] Installing Nomad mTLS certificates..."
        mkdir -p /etc/nomad.d/tls /usr/local/share/ca-certificates
        cp "$SOURCE_DIR/nomad_ca.pem" /etc/nomad.d/tls/ca.pem
        chmod 644 /etc/nomad.d/tls/ca.pem

        cp "$SOURCE_DIR/nomad_ca.pem" /usr/local/share/ca-certificates/nomad-ca.crt
        update-ca-certificates >/dev/null 2>&1 || true

        if [ -f "$SOURCE_DIR/nomad_cli.cert.pem" ]; then
            cp "$SOURCE_DIR/nomad_cli.cert.pem" /etc/nomad.d/tls/cli.cert.pem
            chmod 644 /etc/nomad.d/tls/cli.cert.pem
        fi
        if [ -f "$SOURCE_DIR/nomad_cli.key.pem" ]; then
            cp "$SOURCE_DIR/nomad_cli.key.pem" /etc/nomad.d/tls/cli.key.pem
            chmod 644 /etc/nomad.d/tls/cli.key.pem
        fi
        if [ -f "$SOURCE_DIR/nomad_node.cert.pem" ]; then
            cp "$SOURCE_DIR/nomad_node.cert.pem" /etc/nomad.d/tls/cert.pem
            chmod 644 /etc/nomad.d/tls/cert.pem
        fi
        if [ -f "$SOURCE_DIR/nomad_node.key.pem" ]; then
            cp "$SOURCE_DIR/nomad_node.key.pem" /etc/nomad.d/tls/key.pem
            chmod 600 /etc/nomad.d/tls/key.pem
        fi

        # Install profile environment
        cat > /etc/profile.d/nomad.sh << 'EOF'
#!/bin/sh
export NOMAD_ADDR="${NOMAD_ADDR:-https://100.64.0.1:4646}"
export NOMAD_CACERT="/etc/nomad.d/tls/ca.pem"
export NOMAD_CLIENT_CERT="/etc/nomad.d/tls/cli.cert.pem"
export NOMAD_CLIENT_KEY="/etc/nomad.d/tls/cli.key.pem"
EOF
        chmod +x /etc/profile.d/nomad.sh
        echo "[INFO] Nomad mTLS credentials and CLI profile installed."
    fi

    # 5. Consul Root CA & ACL Token
    if [ -f "$SOURCE_DIR/consul_ca.pem" ]; then
        echo "[INFO] Installing Consul CA..."
        mkdir -p /etc/consul.d
        cp "$SOURCE_DIR/consul_ca.pem" /etc/consul.d/ca.pem
        chmod 644 /etc/consul.d/ca.pem

        cp "$SOURCE_DIR/consul_ca.pem" /usr/local/share/ca-certificates/consul-ca.crt
        update-ca-certificates >/dev/null 2>&1 || true
    fi

    if [ -f "$SOURCE_DIR/consul_token" ]; then
        echo "[INFO] Staging Consul ACL token..."
        mkdir -p /etc/consul.d
        echo "CONSUL_HTTP_TOKEN=$(cat "$SOURCE_DIR/consul_token" | tr -d ' \n\r')" > /etc/consul.d/consul.env
        chmod 600 /etc/consul.d/consul.env
    fi

    # Unmount if we mounted a USB partition
    if [ -n "$MNT_DIR" ]; then
        umount "$MNT_DIR" 2>/dev/null || true
        rm -rf "$MNT_DIR"
    fi

    echo "[INFO] Credential auto-enrollment completed successfully."
else
    echo "[INFO] No cluster credential bundle or CONFIGS partition found. Proceeding with standard setup."
fi
