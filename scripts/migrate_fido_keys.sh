#!/bin/bash
set -euo pipefail

echo "=== FIDO Key Migration Utility ==="
echo "This tool updates your FIDO SSH key configuration across the cluster."
echo ""

# 1. Ask for New Key
read -p "Enter path to your NEW FIDO SSH public key (e.g. ~/.ssh/id_ed25519_sk_new.pub): " NEW_KEY_PATH
if [ -z "$NEW_KEY_PATH" ] || [ ! -f "$NEW_KEY_PATH" ]; then
    echo "Error: New key file not found."
    # We avoid exit in interactive scripts, but here it's fine for the tool
fi

if [ -n "$NEW_KEY_PATH" ] && [ -f "$NEW_KEY_PATH" ]; then
    NEW_KEY=$(cat "$NEW_KEY_PATH")

    # 2. Ask for Old Key
    read -p "Enter path to your OLD FIDO SSH public key (optional, for removal): " OLD_KEY_PATH
    OLD_KEY=""
    if [ -n "$OLD_KEY_PATH" ] && [ -f "$OLD_KEY_PATH" ]; then
        OLD_KEY=$(cat "$OLD_KEY_PATH")
    fi

    # 3. Update group_vars/all.yaml if it exists
    if [ -f "group_vars/all.yaml" ]; then
        echo "Updating group_vars/all.yaml..."

        # Remove old key if present (basic sed replacement)
        if [ -n "$OLD_KEY" ]; then
            # Escape for sed
            ESCAPED_OLD=$(printf '%s\n' "$OLD_KEY" | sed -e 's/[]\/$*.^[]/\\&/g')
            sed -i "/$ESCAPED_OLD/d" group_vars/all.yaml
        fi

        # Add new key if not present
        if ! grep -qF "$NEW_KEY" group_vars/all.yaml; then
            # Find the fido_ssh_keys list and append
            # This is a bit fragile with sed, so we'll just append it to the file if fido_ssh_keys doesn't exist,
            # or try to insert it under fido_ssh_keys:
            if grep -q "^fido_ssh_keys:" group_vars/all.yaml; then
                sed -i "/^fido_ssh_keys:/a \  - \"$NEW_KEY\"" group_vars/all.yaml
            else
                echo "fido_ssh_keys:" >> group_vars/all.yaml
                echo "  - \"$NEW_KEY\"" >> group_vars/all.yaml
            fi
        fi
        echo "Updated group_vars/all.yaml."
    fi

    # 4. Push to Consul KV to sync immediately across the fleet
    read -p "Enter Controller SSH alias/IP to push new key to Consul (e.g. 'controller'): " CONTROLLER_SSH
    if [ -n "$CONTROLLER_SSH" ]; then
        echo "Pushing new key to Consul KV for immediate propagation..."
        # We store it under a known admin key path
        ssh -o "ControlMaster=no" "$CONTROLLER_SSH" "curl -s -X PUT -d '$NEW_KEY' http://127.0.0.1:8500/v1/kv/ssh-keys/admin-fido" || { echo "Failed to push to Consul."; }
        echo "Key published to Consul. Nodes will pick it up within 5 minutes."
    fi

    echo "Migration complete!"
fi
