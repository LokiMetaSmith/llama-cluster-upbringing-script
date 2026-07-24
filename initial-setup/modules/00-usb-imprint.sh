#!/bin/bash
echo "[INFO] Checking for USB Keychain Imprints..."

# The os-image/build_iso.sh creates a FAT32 partition labeled CONFIGS.
# Let's try to find it and mount it.

CONFIGS_PART=$(blkid -L CONFIGS || true)

if [ -n "$CONFIGS_PART" ]; then
    echo "[INFO] Found CONFIGS partition at $CONFIGS_PART"
    MNT_DIR=$(mktemp -d)

    if mount "$CONFIGS_PART" "$MNT_DIR"; then
        echo "[INFO] Mounted CONFIGS partition."

        # 1. Controller IP Imprint
        if [ -f "$MNT_DIR/controller_ip" ]; then
            CONTROLLER_IP=$(cat "$MNT_DIR/controller_ip" | tr -d ' \n\r')
            if [ -n "$CONTROLLER_IP" ]; then
                echo "[INFO] Found imprinted Controller IP: $CONTROLLER_IP"
                # Update setup.conf if present, else just export it or create a file
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

        # 2. FIDO SSH Keys Imprint
        if [ -f "$MNT_DIR/fido_authorized_keys" ]; then
            echo "[INFO] Found imprinted FIDO SSH Keys."
            USER_HOME="/home/${USERNAME:-pipecatapp}"
            SSH_DIR="$USER_HOME/.ssh"
            mkdir -p "$SSH_DIR"
            cat "$MNT_DIR/fido_authorized_keys" >> "$SSH_DIR/authorized_keys"
            chown -R "${USERNAME:-pipecatapp}:${USERNAME:-pipecatapp}" "$SSH_DIR"
            chmod 700 "$SSH_DIR"
            chmod 600 "$SSH_DIR/authorized_keys"
            echo "[INFO] Applied FIDO SSH keys to $SSH_DIR/authorized_keys"
        fi

        # 3. Headscale Auth Key Imprint (Used by ansible later)
        # We can store this in /etc/pipecat_mesh_auth so Ansible tailscale role can pick it up,
        # OR we can execute tailscale up here if tailscale is already installed (it's not).
        # We'll save it to a well known location.
        if [ -f "$MNT_DIR/mesh_auth_key" ]; then
            echo "[INFO] Found imprinted Headscale Auth Key."
            cp "$MNT_DIR/mesh_auth_key" /etc/pipecat_mesh_auth_key
            chmod 600 /etc/pipecat_mesh_auth_key
            if [ -f "$MNT_DIR/headscale_url" ]; then
                cp "$MNT_DIR/headscale_url" /etc/pipecat_headscale_url
                chmod 600 /etc/pipecat_headscale_url
            fi
        fi

        umount "$MNT_DIR"
        rm -rf "$MNT_DIR"
    else
        echo "[INFO] Failed to mount CONFIGS partition."
    fi
else
    echo "[INFO] No CONFIGS partition found. Proceeding with standard setup."
fi
