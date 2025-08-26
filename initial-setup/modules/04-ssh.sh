#!/bin/bash

log "Configuring advanced SSH and key distribution..."

# Ensure necessary tools are installed
apt-get update
apt-get install -y openssh-server jq curl

# Ensure the ssh service is running and enabled
systemctl is-active --quiet ssh || systemctl start ssh
systemctl is-enabled --quiet ssh || systemctl enable ssh

# --- User SSH Key Generation ---
# The USERNAME is loaded from setup.conf by the main setup.sh script
USER_HOME="/home/$USERNAME"
SSH_DIR="$USER_HOME/.ssh"
PRIVATE_KEY="$SSH_DIR/id_rsa"
PUBLIC_KEY="$SSH_DIR/id_rsa.pub"

# Create .ssh directory if it doesn't exist, and set permissions
if [ ! -d "$SSH_DIR" ]; then
    log "Creating .ssh directory for user $USERNAME"
    mkdir -p "$SSH_DIR"
    chown "$USERNAME":"$USERNAME" "$USER_HOME"
    chown "$USERNAME":"$USERNAME" "$SSH_DIR"
    chmod 700 "$SSH_DIR"
fi

# Generate SSH key if it doesn't exist
if [ ! -f "$PRIVATE_KEY" ]; then
    log "Generating SSH key for user '$USERNAME'..."
    sudo -u "$USERNAME" ssh-keygen -t rsa -b 4096 -f "$PRIVATE_KEY" -N ""
    log "SSH key generated for user '$USERNAME'."
else
    log "SSH key for user '$USERNAME' already exists."
fi

# --- Consul Integration ---
# Publish public key to Consul KV store
HOSTNAME=$(hostname)
PUB_KEY_CONTENT=$(cat "$PUBLIC_KEY")

log "Waiting for Consul agent to be available..."
# Wait for up to 2 minutes for Consul to become available
for i in {1..24}; do
    if curl -s "http://127.0.0.1:8500/v1/status/leader" &> /dev/null; then
        log "Consul agent is up."
        break
    fi
    sleep 5
done

log "Publishing public key to Consul for host: $HOSTNAME"
curl -s -X PUT -d "$PUB_KEY_CONTENT" "http://127.0.0.1:8500/v1/kv/ssh-keys/$HOSTNAME"

# --- Create Authorized Keys Sync Script ---
SYNC_SCRIPT_PATH="/usr/local/bin/update-ssh-authorized-keys.sh"
cat > "$SYNC_SCRIPT_PATH" << EOF
#!/bin/bash
# This script syncs SSH public keys from the Consul KV store to the user's authorized_keys file.

# The USERNAME is set in /etc/environment by a previous script, but we can default to 'user'
if [ -z "\$USERNAME" ]; then
    USERNAME="user"
fi

USER_HOME="/home/\$USERNAME"
AUTHORIZED_KEYS_FILE="\$USER_HOME/.ssh/authorized_keys"
TEMP_KEYS_FILE=\$(mktemp)

# Ensure the .ssh directory exists
mkdir -p "\$USER_HOME/.ssh"
chown "\$USERNAME":"\$USERNAME" "\$USER_HOME/.ssh"
chmod 700 "\$USER_HOME/.ssh"

# Fetch all keys from Consul. The response is JSON.
# jq is used to extract the 'Value' field, which is base64 encoded.
# The -r flag removes quotes, and the .[] iterates over the array.
# The base64 decode and append dance ensures keys are correctly formatted.
curl -s "http://127.0.0.1:8500/v1/kv/ssh-keys?recurse" | jq -r '.[].Value' | while read -r val; do
    echo "\$val" | base64 -d >> "\$TEMP_KEYS_FILE"
    echo >> "\$TEMP_KEYS_FILE" # Ensure a newline after each key
done

# Atomically replace the old authorized_keys file with the new one.
# This is safer than appending, as it handles key removal gracefully.
mv "\$TEMP_KEYS_FILE" "\$AUTHORIZED_KEYS_FILE"

# Set correct ownership and permissions
chown "\$USERNAME":"\$USERNAME" "\$AUTHORIZED_KEYS_FILE"
chmod 600 "\$AUTHORIZED_KEYS_FILE"

log "SSH authorized keys have been updated from Consul."
EOF

chmod +x "$SYNC_SCRIPT_PATH"

# --- Initial Sync and Cron Job setup ---
log "Performing initial SSH key sync..."
bash "$SYNC_SCRIPT_PATH"

# Set up cron job to run the sync script every 5 minutes for the user
(crontab -u "$USERNAME" -l 2>/dev/null; echo "*/5 * * * * $SYNC_SCRIPT_PATH") | crontab -u "$USERNAME" -

log "Advanced SSH configuration complete. A cron job will keep keys synced."
