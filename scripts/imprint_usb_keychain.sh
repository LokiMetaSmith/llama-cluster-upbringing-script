#!/usr/bin/env bash
# ==============================================================================
# imprint_usb_keychain.sh - Automated USB Credential Imprinting for Live ISO
# ==============================================================================
# Extracts the complete cluster credential bundle (Headscale mesh preauth key,
# Nomad & Consul Root CAs + mTLS certificates, Consul ACL token, and authorized
# SSH keys) and writes them into a FAT32 'CONFIGS' partition on a bootable USB drive.
#
# When any node boots from this USB drive, it automatically enrolls into the
# cluster without requiring manual SSH or configuration.
#
# Usage:
#   ./scripts/imprint_usb_keychain.sh [--controller <host>]
# ==============================================================================

set -euo pipefail

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

CONTROLLER_SSH="${1:-}"

echo -e "\n${BOLD}${CYAN}============================================================${NC}"
echo -e "${BOLD}${CYAN} 🔐 USB Keychain Imprinting for Cluster Auto-Enrollment${NC}"
echo -e "${BOLD}${CYAN}============================================================${NC}"
echo "This tool extracts all necessary mTLS certificates, tokens, and mesh keys"
echo "and stages them for flashing onto a bootable USB drive or building into an ISO."
echo ""

if [ -z "$CONTROLLER_SSH" ]; then
    read -p "Enter Controller SSH target (e.g. 'localhost' or 'pipecatapp@192.168.1.148') [default: localhost]: " CONTROLLER_SSH
    CONTROLLER_SSH="${CONTROLLER_SSH:-localhost}"
fi

STAGING_DIR=$(mktemp -d /tmp/pipecat_keychain_XXXXXX)

echo -e "\n${BOLD}[1/2] Extracting cluster credentials from ${CONTROLLER_SSH}...${NC}"
"${REPO_ROOT}/scripts/extract_cluster_keys.sh" --controller "$CONTROLLER_SSH" --output "$STAGING_DIR"

echo -e "\n${BOLD}[2/2] Preparing for ISO Injection or USB Flashing...${NC}"
echo -e "Credentials staged at: ${GREEN}${STAGING_DIR}${NC}"
echo ""

read -p "Do you want to flash a USB drive and inject these configs now? [y/N]: " FLASH_CONFIRM
if [[ "$FLASH_CONFIRM" =~ ^[Yy]$ ]]; then
    if [ ! -f "${REPO_ROOT}/os-image/build_iso.sh" ]; then
        echo -e "${RED}❌ os-image/build_iso.sh not found.${NC}"
        exit 1
    fi
    echo "Launching os-image/build_iso.sh with --flash --inject..."
    cd "${REPO_ROOT}/os-image"
    sudo ./build_iso.sh --flash --inject "$STAGING_DIR"
else
    echo ""
    echo -e "${GREEN}Staged bundle preserved at: ${STAGING_DIR}${NC}"
    echo "To burn or inject manually later, run one of the following:"
    echo ""
    echo "  • Inject to USB drive:"
    echo "      cd os-image && sudo ./build_iso.sh --flash --inject \"$STAGING_DIR\""
    echo ""
    echo "  • Pre-bake directly into custom ISO:"
    echo "      cd os-image && sudo ./build_iso.sh --keys-bundle \"$STAGING_DIR\""
    echo ""
fi
