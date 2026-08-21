#!/bin/bash

# Configuration
VERSION_FILE=".repo_version"

# Function to extract major and minor version numbers
get_major_minor() {
    local version=$1
    if [[ "$version" =~ ^([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
        echo "${BASH_REMATCH[1]}.${BASH_REMATCH[2]}"
    else
        echo ""
    fi
}

# Ensure the version file exists before pulling (so we have a baseline)
if [ ! -f "$VERSION_FILE" ]; then
    echo "1.0.0" > "$VERSION_FILE"
fi

# Get the current version before pull
OLD_VERSION=$(cat "$VERSION_FILE")
OLD_MAJOR_MINOR=$(get_major_minor "$OLD_VERSION")

echo "Current version: $OLD_VERSION"
echo "Pulling latest changes..."

# Pull changes from git
git pull

# Check if git pull succeeded
if [ $? -ne 0 ]; then
    echo "Error: git pull failed."
    exit 1
fi

# Ensure the version file exists after pulling
if [ ! -f "$VERSION_FILE" ]; then
    echo "1.0.0" > "$VERSION_FILE"
fi

# Get the new version after pull
NEW_VERSION=$(cat "$VERSION_FILE")
NEW_MAJOR_MINOR=$(get_major_minor "$NEW_VERSION")

echo "New version: $NEW_VERSION"

# Compare major/minor versions to determine if reinitialization is needed
if [ "$OLD_MAJOR_MINOR" != "$NEW_MAJOR_MINOR" ]; then
    echo "Major or minor version change detected ($OLD_VERSION -> $NEW_VERSION). Reinitializing..."
    ./bootstrap.sh
else
    echo "No major or minor version change detected. Skipping reinitialization."
fi
