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

# --- Create Idempotent Authorized Keys Sync Script ---
SYNC_SCRIPT_PATH="/usr/local/bin/update-ssh-authorized-keys.sh"
cat > "$SYNC_SCRIPT_PATH" << 'EOF'
#!/bin/bash
# This script idempotently syncs SSH public keys from the Consul KV store.
# It only writes to the authorized_keys file if there are actual changes.

log_sync() {
    echo "[SSH-Sync] $1"
}

# The USERNAME is set in /etc/environment by a previous script, but we can default to 'user'
if [ -z "$USERNAME" ]; then
    USERNAME="user"
fi

USER_HOME="/home/$USERNAME"
AUTHORIZED_KEYS_FILE="$USER_HOME/.ssh/authorized_keys"
TEMP_KEYS_FILE=$(mktemp)

# Ensure the .ssh directory exists
mkdir -p "$USER_HOME/.ssh"
chown "$USERNAME":"$USERNAME" "$USER_HOME/.ssh"
chmod 700 "$USER_HOME/.ssh"

# Fetch all keys from Consul and decode them into a temporary file.
curl -s "http://127.0.0.1:8500/v1/kv/ssh-keys?recurse" | jq -r '.[].Value' | while read -r val; do
    echo "$val" | base64 -d >> "$TEMP_KEYS_FILE"
    echo >> "$TEMP_KEYS_FILE" # Ensure a newline after each key
done

# Check if the authorized_keys file exists. If not, we must create it.
if [ ! -f "$AUTHORIZED_KEYS_FILE" ]; then
    log_sync "Authorized keys file does not exist. Creating it."
    mv "$TEMP_KEYS_FILE" "$AUTHORIZED_KEYS_FILE"
    chown "$USERNAME":"$USERNAME" "$AUTHORIZED_KEYS_FILE"
    chmod 600 "$AUTHORIZED_KEYS_FILE"
    log_sync "SSH authorized keys created."
# Compare the new keys with the existing ones. Only write if they are different.
elif ! diff -q "$AUTHORIZED_KEYS_FILE" "$TEMP_KEYS_FILE" >/dev/null; then
    log_sync "SSH key changes detected in Consul. Updating local file."
    mv "$TEMP_KEYS_FILE" "$AUTHORIZED_KEYS_FILE"
    chmod 600 "$AUTHORIZED_KEYS_FILE" # Ensure permissions are correct
    log_sync "SSH authorized keys updated."
else
    # The files are the same, no need to do anything. Clean up the temp file.
    rm "$TEMP_KEYS_FILE"
fi
EOF

chmod +x "$SYNC_SCRIPT_PATH"

# --- Initial Sync and Cron Job setup ---
log "Performing initial SSH key sync..."
bash "$SYNC_SCRIPT_PATH"

# Set up cron job to run the sync script every 5 minutes for the user
# The definition of 'log' is not available to the cron job, so we redirect output
(crontab -u "$USERNAME" -l 2>/dev/null; echo "*/5 * * * * $SYNC_SCRIPT_PATH >> /var/log/ssh-key-sync.log 2>&1") | crontab -u "$USERNAME" -

log "Advanced SSH configuration complete. A cron job will keep keys synced idempotently."
