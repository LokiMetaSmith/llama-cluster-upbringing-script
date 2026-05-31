#!/bin/bash

# Default to 'main', but allow the user to specify a target branch (e.g., ./git-cleanup.sh master)
TARGET_BRANCH=${1:-main}
REMOTE=${2:-origin}

echo "🔍 Checking for remote branches merged into '$TARGET_BRANCH' on '$REMOTE'..."

# 1. Update local knowledge of the remote to ensure accuracy
echo "🔄 Fetching latest from remote..."
git fetch $REMOTE --prune

# 2. Find merged remote branches
# - Looks for branches merged into the target branch
# - Greps only for the remote branches
# - Safely excludes common protected branches: main, master, develop, staging, release
# - Strips the "origin/" prefix to get the raw branch name
MERGED_BRANCHES=$(git branch -r --merged $REMOTE/$TARGET_BRANCH \
    | grep "$REMOTE/" \
    | grep -Ev "(^\*|$TARGET_BRANCH|master|develop|staging|release)" \
    | sed "s/$REMOTE\///")

# 3. Handle the case where there is nothing to delete
if [ -z "$MERGED_BRANCHES" ]; then
    echo "✨ No merged branches found to clean up! Your repo is spotless."
    exit 0
fi

# 4. The Dry Run / Safety Check
echo "⚠️  The following branches have been merged into $TARGET_BRANCH and will be DELETED from $REMOTE:"
echo "----------------------------------------------------"
echo "$MERGED_BRANCHES"
echo "----------------------------------------------------"

# 5. Prompt for confirmation before executing the destructive command
read -p "🚨 Are you sure you want to permanently delete these remote branches? (y/N): " CONFIRM

if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "🗑️  Deleting branches from $REMOTE..."
    echo "$MERGED_BRANCHES" | xargs -n 1 git push --delete $REMOTE
    echo "✅ Cleanup complete!"
else
    echo "🛑 Aborted. No branches were deleted."
    exit 0
fi