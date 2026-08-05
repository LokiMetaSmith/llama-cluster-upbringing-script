#!/bin/bash
# ipfs_cleanup.sh
# Finds IPFS pins that are no longer referenced by active models/images and unpins them,
# then performs garbage collection.

IPFS_PATH="/opt/unified_fs/ipfs"
IPFS_CMD="ipfs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${BOLD}${YELLOW}Starting Smart IPFS Cleanup...${NC}"

# Check if IPFS repo exists
if [ ! -d "$IPFS_PATH" ]; then
    echo "No IPFS repo found at $IPFS_PATH. Stopping."
    kill -SIGINT $$
fi

# We use IPFS_PATH env var to target the correct repo
export IPFS_PATH

# Check if IPFS is installed
if ! command -v $IPFS_CMD &> /dev/null; then
    echo "ipfs command not found. Stopping."
    kill -SIGINT $$
fi

echo -e "\n${BOLD}1. Gathering currently pinned CIDs...${NC}"
# Get all pinned CIDs
# output format: <cid> <type>
PINNED_CIDS=$($IPFS_CMD pin ls --type=recursive 2>/dev/null | awk '{print $1}')
PIN_COUNT=$(echo "$PINNED_CIDS" | wc -w)
echo "Found $PIN_COUNT pinned CIDs."

echo -e "\n${BOLD}2. Gathering active references...${NC}"
# Models are expected in /opt/nomad/models or /opt/nomad/models/llm
# Our ansible scripts use ipfs get or docker load. We'll search for CIDs in ansible variables
# or file references if possible.

ACTIVE_CIDS=()

# 1. Search for CID-like strings in /opt/nomad/models
if [ -d "/opt/nomad/models" ]; then
    echo "Scanning /opt/nomad/models for active CIDs..."
    # Find all strings that look like CIDv0 (Qm...) or CIDv1 (bafy...)
    FOUND_CIDS=$(grep -rohE 'Qm[1-9A-HJ-NP-Za-km-z]{44}|baf[a-z2-7]{56}' /opt/nomad/models 2>/dev/null || true)
    for cid in $FOUND_CIDS; do
        ACTIVE_CIDS+=("$cid")
    done
fi

# 2. Add some known CIDs if we can parse them from group_vars or ansible directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
if [ -d "$PROJECT_ROOT/group_vars" ]; then
    echo "Scanning group_vars for active CIDs..."
    FOUND_CIDS=$(grep -rohE 'Qm[1-9A-HJ-NP-Za-km-z]{44}|baf[a-z2-7]{56}' "$PROJECT_ROOT/group_vars" 2>/dev/null || true)
    for cid in $FOUND_CIDS; do
        ACTIVE_CIDS+=("$cid")
    done
fi
if [ -d "$PROJECT_ROOT/ansible" ]; then
    echo "Scanning ansible files for active CIDs..."
    FOUND_CIDS=$(grep -rohE 'Qm[1-9A-HJ-NP-Za-km-z]{44}|baf[a-z2-7]{56}' "$PROJECT_ROOT/ansible" 2>/dev/null || true)
    for cid in $FOUND_CIDS; do
        ACTIVE_CIDS+=("$cid")
    done
fi

# Remove duplicates from active CIDs
UNIQUE_ACTIVE_CIDS=($(echo "${ACTIVE_CIDS[@]}" | tr ' ' '\n' | sort -u))
echo "Found ${#UNIQUE_ACTIVE_CIDS[@]} referenced CIDs."

echo -e "\n${BOLD}3. Unpinning unreferenced objects...${NC}"
UNPINNED_COUNT=0
for cid in $PINNED_CIDS; do
    # Check if this CID is in our active list
    IS_ACTIVE=0
    for active_cid in "${UNIQUE_ACTIVE_CIDS[@]}"; do
        if [ "$cid" == "$active_cid" ]; then
            IS_ACTIVE=1
            break
        fi
    done

    if [ $IS_ACTIVE -eq 0 ]; then
        echo "Unpinning unreferenced CID: $cid"
        $IPFS_CMD pin rm "$cid" >/dev/null 2>&1 || true
        UNPINNED_COUNT=$((UNPINNED_COUNT + 1))
    fi
done

echo "Unpinned $UNPINNED_COUNT old/unreferenced objects."

echo -e "\n${BOLD}4. Running IPFS Garbage Collection...${NC}"
$IPFS_CMD repo gc

echo -e "\n${GREEN}✨ Smart IPFS Cleanup Complete!${NC}"
