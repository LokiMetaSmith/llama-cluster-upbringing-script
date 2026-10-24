#!/bin/bash
set -e

# Configuration
WORKSPACE_DIR="/opt/cluster-infra"
SOURCE_REPO="/mnt/host_repo"

echo "--- Tool Server Entrypoint ---"

# 1. Setup Volatile Workspace (only for core or when WORKSPACE_DIR is mounted)
if [ "$TOOL_SERVER_ROLE" = "core" ] || [ -z "$TOOL_SERVER_ROLE" ] || mount | grep -q "$WORKSPACE_DIR"; then
    if [ -d "$WORKSPACE_DIR" ]; then
        chmod 777 "$WORKSPACE_DIR" 2>/dev/null || true
    fi

    # 2. Populate Workspace
    if [ -d "$SOURCE_REPO" ] && [ -d "$WORKSPACE_DIR" ] && [ -w "$WORKSPACE_DIR" ]; then
        echo "🔄 Populating volatile workspace from $SOURCE_REPO..."
        set +e
        rsync -rlpD --info=progress2 \
            --exclude '.venv' \
            --exclude 'venv' \
            --exclude 'node_modules' \
            --exclude '__pycache__' \
            --exclude '*.pyc' \
            "$SOURCE_REPO/" "$WORKSPACE_DIR/"
        RSYNC_EXIT=$?
        set -e
        if [ $RSYNC_EXIT -eq 0 ] || [ $RSYNC_EXIT -eq 23 ] || [ $RSYNC_EXIT -eq 24 ]; then
            echo "✅ Workspace populated."
        else
            echo "❌ Rsync failed with exit code $RSYNC_EXIT"
            exit $RSYNC_EXIT
        fi
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

        # Safe directory configuration
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
        cd /app
    fi
fi

# Make sure we run the application from its installed directory
cd /app

# 4. Hand off to the main application
echo "🚀 Starting Tool Server..."
exec "$@"
