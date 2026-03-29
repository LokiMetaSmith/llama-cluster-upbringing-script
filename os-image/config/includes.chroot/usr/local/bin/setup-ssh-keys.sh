#!/bin/bash
# Fetches SSH keys from a provided GitHub username

if [ -z "$1" ]; then
    echo "Usage: $0 <github_username>"
    exit 1
fi

GITHUB_USER="$1"
USER_HOME="/home/pipecatapp"
SSH_DIR="$USER_HOME/.ssh"
AUTH_KEYS="$SSH_DIR/authorized_keys"

# Ensure the .ssh directory exists
mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"

# Fetch the keys
echo "Fetching SSH keys for GitHub user: $GITHUB_USER..."
TMP_KEYS=$(mktemp)
if curl -sLf "https://github.com/${GITHUB_USER}.keys" -o "$TMP_KEYS"; then
    if [ -s "$TMP_KEYS" ]; then
        cat "$TMP_KEYS" >> "$AUTH_KEYS"
        # Ensure proper permissions
        chmod 600 "$AUTH_KEYS"
        chown -R pipecatapp:pipecatapp "$SSH_DIR"
        echo "Successfully added SSH keys to $AUTH_KEYS"

        # Save the config so we don't prompt again
        echo "$GITHUB_USER" | sudo tee /etc/pipecat_github_user >/dev/null
    else
        echo "Error: No keys found for user $GITHUB_USER or user does not exist."
    fi
else
    echo "Error: Failed to fetch keys from GitHub. Check your network connection."
fi

rm -f "$TMP_KEYS"
