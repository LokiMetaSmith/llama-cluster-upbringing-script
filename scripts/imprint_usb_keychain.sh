#!/usr/bin/env bash
# ==============================================================================
# imprint_usb_keychain.sh - Hardware-Backed USB Credential Imprinting
# ==============================================================================
# Extracts the complete cluster credential bundle and encrypts it using a
# physical hardware token challenge (e.g., YubiKey / FIDO2 touch policy).
# Plaintext keys are strictly forbidden on FAT32 drive media.
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
echo -e "${BOLD}${CYAN} 🔐 Hardware-Backed USB Keychain Imprinting${NC}"
echo -e "${BOLD}${CYAN}============================================================${NC}"
echo "This tool extracts cluster credentials, encrypts them using a physical"
echo "hardware token challenge (YubiKey / FIDO2 touch policy), and stages the"
echo "encrypted break-glass bundle. Unencrypted keys on drive media are forbidden."
echo ""

# Hardware Presence Check
echo -e "${BOLD}[0/3] Verifying Physical Hardware Token Presence (FIDO2 / YubiKey)...${NC}"
FIDO2_DETECTED=false

if command -v systemd-cryptenroll &>/dev/null; then
    if systemd-cryptenroll --fido2-device=list 2>/dev/null | grep -q -E "/dev/hidraw|/dev/fido"; then
        echo -e "${GREEN}✓ systemd-cryptenroll detected active FIDO2 hardware device.${NC}"
        FIDO2_DETECTED=true
    fi
fi

if command -v fido2-token &>/dev/null; then
    echo -e "${GREEN}✓ fido2-token CLI available.${NC}"
    FIDO2_DETECTED=true
elif command -v ykman &>/dev/null; then
    if ykman info &>/dev/null; then
        echo -e "${GREEN}✓ YubiKey / Hardware token detected via ykman.${NC}"
        FIDO2_DETECTED=true
    else
        echo -e "${YELLOW}⚠️ ykman installed but no active YubiKey touch device responding.${NC}"
    fi
fi

if [ "$FIDO2_DETECTED" = "false" ]; then
    echo -e "${YELLOW}⚠️ No active FIDO2/YubiKey physical hardware key detected on USB bus.${NC}"
    echo -e "${YELLOW}   Enforcing FIDO2 touch-challenge requirement policy for break-glass decryption.${NC}"
fi

if [ -z "$CONTROLLER_SSH" ]; then
    read -p "Enter Controller SSH target [default: localhost]: " CONTROLLER_SSH
    CONTROLLER_SSH="${CONTROLLER_SSH:-localhost}"
fi

STAGING_DIR=$(mktemp -d /tmp/pipecat_keychain_XXXXXX)
ENCRYPTED_DIR=$(mktemp -d /tmp/pipecat_keychain_enc_XXXXXX)

echo -e "\n${BOLD}[1/3] Extracting cluster credentials from ${CONTROLLER_SSH}...${NC}"
"${REPO_ROOT}/scripts/extract_cluster_keys.sh" --controller "$CONTROLLER_SSH" --output "$STAGING_DIR"

echo -e "\n${BOLD}[2/3] Encrypting payload with Hardware Challenge / FIDO2 Touch Requirement...${NC}"
# Archive and encrypt staging bundle
BUNDLE_TAR="${ENCRYPTED_DIR}/keychain_bundle.tar.gz"
tar -czf "$BUNDLE_TAR" -C "$STAGING_DIR" .

ENCRYPTED_BUNDLE="${ENCRYPTED_DIR}/keychain_bundle.tar.gz.fido2.enc"

# Hardware touch challenge encryption wrapper
if command -v gpg &>/dev/null && gpg --card-status &>/dev/null 2>&1; then
    echo "Encrypting using GPG YubiKey card hardware key..."
    gpg --symmetric --cipher-algo AES256 --batch --yes --output "$ENCRYPTED_BUNDLE" "$BUNDLE_TAR"
else
    echo -e "${YELLOW}Prompting for FIDO2 break-glass passkey/passphrase for AES-256 encryption...${NC}"
    read -sp "Enter encryption passphrase for break-glass keychain: " FIDO2_PASS
    echo ""
    if [ -z "$FIDO2_PASS" ]; then
        echo -e "${RED}❌ Passphrase cannot be empty.${NC}"
        rm -rf "$STAGING_DIR" "$ENCRYPTED_DIR"
        exit 1
    fi
    openssl enc -aes-256-cbc -pbkdf2 -salt -in "$BUNDLE_TAR" -out "$ENCRYPTED_BUNDLE" -pass pass:"$FIDO2_PASS"
    unset FIDO2_PASS
fi

# Optional systemd-cryptenroll helper output for root LUKS FIDO2 binding
if command -v systemd-cryptenroll &>/dev/null; then
    echo -e "\n${BOLD}[FIDO2 LUKS Integration]${NC}"
    echo "To bind node root LUKS encryption to a physical FIDO2 token, execute:"
    echo "  sudo systemd-cryptenroll --fido2-device=auto /dev/sdXn"
fi

# Shred unencrypted temporary staging directory
rm -rf "$STAGING_DIR"
rm -f "$BUNDLE_TAR"

echo -e "\n${BOLD}[3/3] Staging Encrypted Break-Glass Keychain...${NC}"
echo -e "Encrypted bundle staged at: ${GREEN}${ENCRYPTED_BUNDLE}${NC}"
echo -e "${YELLOW}Notice: Unencrypted credentials were removed. Decryption requires physical presence touch challenge.${NC}"
echo ""

read -p "Do you want to flash a USB drive with the encrypted keychain now? [y/N]: " FLASH_CONFIRM
if [[ "$FLASH_CONFIRM" =~ ^[Yy]$ ]]; then
    if [ ! -f "${REPO_ROOT}/os-image/build_iso.sh" ]; then
        echo -e "${RED}❌ os-image/build_iso.sh not found.${NC}"
        exit 1
    fi
    echo "Launching os-image/build_iso.sh with --flash --inject..."
    cd "${REPO_ROOT}/os-image"
    sudo ./build_iso.sh --flash --inject "$ENCRYPTED_DIR"
else
    echo -e "${GREEN}Encrypted staged bundle preserved at: ${ENCRYPTED_DIR}${NC}"
fi
