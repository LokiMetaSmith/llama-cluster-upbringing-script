#!/bin/bash
set -e

# Configuration
WORKSPACE_DIR="/opt/cluster-infra"
SOURCE_REPO="/mnt/host_repo"

echo "--- Tool Server Entrypoint ---"

# 1. Setup Volatile Workspace
# Check if the workspace is mounted as tmpfs (optional check, but good for logging)
if mount | grep -q "$WORKSPACE_DIR"; then
    echo "✅ $WORKSPACE_DIR is mounted."
else
    echo "⚠️  $WORKSPACE_DIR does not appear to be a separate mount. Proceeding anyway."
fi

# 2. Populate Workspace
# We use rsync to efficiently copy the read-only host repo to the RAM disk.
# We copy .git to allow immediate git commands.
echo "🔄 Populating volatile workspace from $SOURCE_REPO..."
if [ -d "$SOURCE_REPO" ]; then
    # We use rsync with -a (archive) to preserve permissions/times
    # We use --delete to ensure the workspace matches the source exactly at startup
    rsync -a --info=progress2 "$SOURCE_REPO/" "$WORKSPACE_DIR/"
    echo "✅ Workspace populated."
else
    echo "❌ Source repo $SOURCE_REPO not found! Agent will have an empty workspace."
fi

# 3. Git Configuration (for the Agent's session)
if [ -d "$WORKSPACE_DIR/.git" ]; then
    cd "$WORKSPACE_DIR"

    # Configure Identity
    GIT_USER="${GIT_USERNAME:-Pipecat Agent}"
    GIT_MAIL="${GIT_EMAIL:-agent@pipecat.ai}"

    git config user.email "$GIT_MAIL"
    git config user.name "$GIT_USER"
    echo "✅ Git identity configured: $GIT_USER <$GIT_MAIL>"

    # Mark the workspace as safe (since ownership might differ in container)
    git config --global --add safe.directory "$WORKSPACE_DIR"

    # Configure Auth for Push (if token provided)
    if [ -n "$GITHUB_TOKEN" ]; then
        echo "🔐 Configuring git credentials using GITHUB_TOKEN..."
        # Use a simple credential helper or replace origin URL
        # Replacing URL is robust for specific remote
        ORIGIN_URL=$(git remote get-url origin)
        if [[ "$ORIGIN_URL" == https://* ]]; then
            # Strip existing auth info if any
            CLEAN_URL=$(echo "$ORIGIN_URL" | sed 's|https://[^@]*@|https://|')
            # Inject token
            NEW_URL=$(echo "$CLEAN_URL" | sed "s|https://|https://$GITHUB_TOKEN@|")
            git remote set-url origin "$NEW_URL"
            echo "✅ Git remote 'origin' updated with token authentication."
        else
            echo "⚠️  Origin URL is not HTTPS or complex. Skipping auto-auth configuration."
            echo "    Current Origin: $ORIGIN_URL"
        fi
    fi
fi

# 4. Hand off to the main application
echo "🚀 Starting Tool Server..."
exec "$@"
