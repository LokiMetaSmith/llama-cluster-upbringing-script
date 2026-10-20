#!/bin/bash
set -e

ARCHIVE_PATH="${1:-/tmp/takeout-archive.zip}"
MOUNT_DIR="${2:-/mnt/takeout-hoard}"

if [ ! -f "$ARCHIVE_PATH" ]; then
    echo "Error: Takeout archive not found at $ARCHIVE_PATH"
    echo "Usage: $0 [path_to_takeout_zip] [target_mount_dir]"
    exit 1
fi

echo "Cleaning and preparing $MOUNT_DIR..."
sudo rm -rf "$MOUNT_DIR"/*
sudo mkdir -p "$MOUNT_DIR"

echo "Extracting archive $ARCHIVE_PATH into $MOUNT_DIR..."
sudo unzip -q -o "$ARCHIVE_PATH" -d "$MOUNT_DIR"
sudo chown -R 1000:1000 "$MOUNT_DIR"

echo "Google Takeout successfully unpacked to $MOUNT_DIR."
