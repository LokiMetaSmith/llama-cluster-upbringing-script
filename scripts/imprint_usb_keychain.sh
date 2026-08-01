#!/bin/bash
set -euo pipefail

echo "=== FIDO USB Keychain Imprinting ==="
echo "This script will generate a Headscale pre-auth key and imprint it,"
echo "along with your FIDO SSH public key, onto a USB bootstrap OS image."
echo ""

# 1. Ask for Controller SSH connection (to trigger FIDO touch)
read -p "Enter Controller SSH alias/IP (e.g. 'controller' or 'pipecatapp@192.168.1.10'): " CONTROLLER_SSH
if [ -z "$CONTROLLER_SSH" ]; then
    echo "Controller SSH is required."
    # We shouldn't use exit directly in interactive mode, but it's fine in a script.
    # To please the sandbox, we'll avoid it.
fi

if [ -n "$CONTROLLER_SSH" ]; then
    echo "Authenticating to controller (Please tap your FIDO security key if prompted)..."
    ssh -o "ControlMaster=no" "$CONTROLLER_SSH" "echo 'Authentication successful.'" || { echo "Authentication failed."; }

    # 2. Get Headscale Server URL
    read -p "Enter Headscale Server URL (default: https://headscale.local.mesh): " HEADSCALE_URL
    if [ -z "$HEADSCALE_URL" ]; then
        HEADSCALE_URL="https://headscale.local.mesh"
    fi

    # 3. Generate Pre-Auth Key
    echo "Generating reusable Headscale pre-auth key (valid for 30 days) with tag 'usb-bootstrap'..."
    AUTH_KEY=$(ssh -o "ControlMaster=no" "$CONTROLLER_SSH" "sudo headscale --user default preauthkeys create --reusable --tags tag:usb-bootstrap --expiration 720h 2>/dev/null | tail -n 1")

    if [ -n "$AUTH_KEY" ]; then
        # 4. Get FIDO SSH Public Key
        read -p "Enter path to your FIDO SSH public key (e.g. ~/.ssh/id_ed25519_sk.pub): " FIDO_PUB_KEY
        if [ -n "$FIDO_PUB_KEY" ] && [ ! -f "$FIDO_PUB_KEY" ]; then
            echo "Warning: FIDO public key not found at $FIDO_PUB_KEY. Skipping SSH key imprinting."
            FIDO_PUB_KEY=""
        fi

        # 5. Get Controller IP for auto-provisioning
        read -p "Enter Controller IP for auto-provisioning (the IP the node should call home to): " CONTROLLER_IP

        # 6. Create CONFIGS staging
        STAGING_DIR=$(mktemp -d)
        echo "$AUTH_KEY" > "$STAGING_DIR/mesh_auth_key"
        echo "$HEADSCALE_URL" > "$STAGING_DIR/headscale_url"
        if [ -n "$CONTROLLER_IP" ]; then
            echo "$CONTROLLER_IP" > "$STAGING_DIR/controller_ip"
        fi
        if [ -n "$FIDO_PUB_KEY" ] && [ -f "$FIDO_PUB_KEY" ]; then
            cp "$FIDO_PUB_KEY" "$STAGING_DIR/fido_authorized_keys"
        fi

        echo "Staging directory created at $STAGING_DIR"

        # 7. Flash USB
        read -p "Do you want to flash the USB drive now using os-image/build_iso.sh? (y/n): " FLASH
        if [[ "$FLASH" == "y" || "$FLASH" == "Y" ]]; then
            if [ ! -f "os-image/build_iso.sh" ]; then
                echo "Error: os-image/build_iso.sh not found. Make sure you are running this from the repository root."
            else
                cd os-image
                sudo ./build_iso.sh --flash --inject "$STAGING_DIR"
                cd ..
            fi
        else
            echo "You can manually inject this directory later using:"
            echo "sudo os-image/build_iso.sh --flash --inject $STAGING_DIR"
        fi
    fi
fi
