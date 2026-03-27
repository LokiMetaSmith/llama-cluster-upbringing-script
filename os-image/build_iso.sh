#!/bin/bash
# Builds a custom, bootable, headless Debian ISO for the Pipecat agent cluster.

set -euo pipefail

# --- Arguments ---
if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
    echo "Usage: ./build_iso.sh"
    echo ""
    echo "Builds a custom, bootable, headless Debian ISO for the Pipecat agent cluster."
    echo "Must be run as root (or with sudo) because live-build strictly requires root privileges."
    exit 0
fi

# --- Dependencies Check ---
if ! command -v xorriso &> /dev/null || ! command -v mtools &> /dev/null; then
    echo "Dependencies xorriso and/or mtools are required but not installed. Installing..."
    if [ "$(id -u)" -ne 0 ]; then
        sudo apt-get update && sudo apt-get install -y xorriso mtools grub-pc-bin grub-efi-amd64-bin
    else
        apt-get update && apt-get install -y xorriso mtools grub-pc-bin grub-efi-amd64-bin
    fi
fi

if ! command -v isohybrid &> /dev/null; then
    echo "isohybrid is required but not installed. Installing syslinux-utils..."
    if [ "$(id -u)" -ne 0 ]; then
        sudo apt-get update && sudo apt-get install -y syslinux-utils
    else
        apt-get update && apt-get install -y syslinux-utils
    fi
fi

# --- Configuration ---
DISTRIBUTION="trixie" # Recommended in README
ARCHITECTURE="amd64"
ISO_NAME="pipecat-installer"

# Move to the build directory
BUILD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BUILD_DIR"

echo "=== Cleaning previous build artifacts ==="
# Ensure old configs or broken debootstrap artifacts don't interfere
if [ "$(id -u)" -ne 0 ]; then
    sudo lb clean || true
else
    lb clean || true
fi

echo "=== Initializing live-build configuration ==="
lb config \
  --distribution "$DISTRIBUTION" \
  --architecture "$ARCHITECTURE" \
  --mode debian \
  --parent-mirror-bootstrap "http://deb.debian.org/debian/" \
  --mirror-bootstrap "http://deb.debian.org/debian/" \
  --parent-mirror-chroot "http://deb.debian.org/debian/" \
  --mirror-chroot "http://deb.debian.org/debian/" \
  --parent-mirror-binary "http://deb.debian.org/debian/" \
  --mirror-binary "http://deb.debian.org/debian/" \
  --parent-mirror-debian-installer "http://deb.debian.org/debian/" \
  --mirror-debian-installer "http://deb.debian.org/debian/" \
  --archive-areas "main contrib non-free-firmware" \
  --apt-indices true \
  --apt-recommends false \
  --security false \
  --firmware-chroot false \
  --firmware-binary false \
  --linux-packages "linux-image" \
  --linux-flavours "amd64" \
  --bootloader "grub-efi" \
  --initramfs "live-boot" \
  --initsystem "systemd" \
  --debian-installer-distribution "$DISTRIBUTION" \
  --debian-installer false \
  --win32-loader false \
  --bootappend-live "boot=live components quiet splash locales=en_US.UTF-8 keyboard-layouts=us"

echo "=== Injecting project files ==="
# Add required packages to chroot so the build environment can generate a hybrid EFI ISO
mkdir -p config/package-lists
echo "syslinux-utils xorriso mtools grub-pc-bin grub-efi-amd64-bin" > config/package-lists/build-deps.list.chroot

# Ensure the root of the repo is copied to /opt/pipecat-cluster
# The `lb build` command automatically includes files placed in `config/includes.chroot/`
mkdir -p config/includes.chroot/opt/pipecat-cluster
rsync -a --exclude 'os-image' --exclude '.git' ../ config/includes.chroot/opt/pipecat-cluster/

echo "=== Building the ISO (requires root privileges) ==="
# Ensure user has sudo permissions, as live-build strictly requires root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script requires sudo to run 'lb build'."
    sudo lb build
else
    lb build
fi

# Rename the generated ISO to match expected output name
if [ -f "binary.hybrid.iso" ]; then
    mv binary.hybrid.iso "${ISO_NAME}-${ARCHITECTURE}.iso"
elif [ -f "binary.iso" ]; then
    mv binary.iso "${ISO_NAME}-${ARCHITECTURE}.iso"
fi

echo "=== Build Complete ==="
echo "The ISO image should be available in the $BUILD_DIR directory as ${ISO_NAME}-${ARCHITECTURE}.iso"
