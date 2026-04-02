#!/bin/bash
#
# update_cluster.sh
#
# This script updates the pipecat-cluster base image from the git repository
# without keeping a heavy git history. It performs a shallow pull, cleans the
# directory, and then triggers the bootstrap process.

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
REPO_ROOT=$(dirname "$SCRIPT_DIR")

cd "$REPO_ROOT" || exit 1

FORCE=false
# Parse flags for this script specifically (and filter them out for bootstrap.sh)
PASSTHROUGH_ARGS=()
for arg in "$@"; do
    if [ "$arg" == "-y" ] || [ "$arg" == "--force" ]; then
        FORCE=true
    else
        PASSTHROUGH_ARGS+=("$arg")
    fi
done

if [ "$FORCE" = false ]; then
    echo -e "${BOLD}${YELLOW}⚠️  WARNING: This will discard all local changes and untracked files.${NC}"
    read -p "Are you sure you want to update the cluster image? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Update cancelled."
        exit 0
    fi
fi

echo -e "\n${BOLD}=== Updating Repository ===${NC}"

# Ensure we are actually in a git repository before running git commands
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ Not a git repository. Cannot update via git.${NC}"
    exit 1
fi

# Get the current branch name
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [ -z "$CURRENT_BRANCH" ] || [ "$CURRENT_BRANCH" == "HEAD" ]; then
    echo -e "${YELLOW}⚠️  Could not determine current branch or in detached HEAD state. Defaulting to 'main'.${NC}"
    CURRENT_BRANCH="main"
fi

echo "Fetching latest changes for branch: $CURRENT_BRANCH (shallow pull)"
git fetch --depth 1 origin "$CURRENT_BRANCH"
if [ $? -ne 0 ]; then
     echo -e "${RED}❌ Failed to fetch from remote. Check your network connection or remote repository.${NC}"
     exit 1
fi

echo "Resetting local state to match remote origin/$CURRENT_BRANCH..."
git reset --hard "origin/$CURRENT_BRANCH"
if [ $? -ne 0 ]; then
     echo -e "${RED}❌ Failed to reset local state.${NC}"
     exit 1
fi

echo "Cleaning untracked files..."
git clean -fd
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Clean failed. Some files might need root privileges to be removed.${NC}"
fi

echo -e "${GREEN}✅ Repository updated successfully.${NC}"

echo -e "\n${BOLD}=== Restarting Provisioning ===${NC}"
echo "Triggering bootstrap.sh with arguments: ${PASSTHROUGH_ARGS[*]}"

# Pass all remaining arguments passed to this script into bootstrap.sh
./bootstrap.sh "${PASSTHROUGH_ARGS[@]}"
