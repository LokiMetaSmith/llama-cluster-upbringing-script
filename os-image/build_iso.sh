#!/bin/bash
# Builds a custom, bootable, headless Debian ISO for the Pipecat agent cluster.

set -euo pipefail

# --- Arguments ---
KEEP_CACHE=0

for arg in "$@"; do
    if [ "$arg" = "-h" ] || [ "$arg" = "--help" ]; then
        echo "Usage: ./build_iso.sh [--keep-cache]"
        echo ""
        echo "Builds a custom, bootable, headless Debian ISO for the Pipecat agent cluster."
        echo "Automatically spins up a Debian Trixie Docker container to ensure native live-build compatibility."
        echo ""
        echo "Options:"
        echo "  --keep-cache  Preserve the package cache and build artifacts to speed up subsequent runs"
        exit 0
    elif [ "$arg" = "--keep-cache" ]; then
        KEEP_CACHE=1
    fi
done

# --- Configuration ---
DISTRIBUTION="trixie" # Recommended in README
ARCHITECTURE="amd64"
ISO_NAME="pipecat-installer"

# Move to the build directory
BUILD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BUILD_DIR"

# --- Docker Wrapper ---
# Ensure we build inside a native Debian Trixie container to avoid host-chroot OS mismatches (e.g., Ubuntu vs Debian)
# which cause bootloader generation failures and 'isohybrid' missing boot record errors.
if [ ! -f /.dockerenv ]; then
    echo "=== Not running in a container. Spinning up a Debian Trixie build environment ==="

    # Check if docker is installed
    if ! command -v docker &> /dev/null; then
        echo "Error: Docker is not installed but is required to build the ISO natively."
        exit 1
    fi

    DOCKER_ARGS=""
    if [ "$KEEP_CACHE" -eq 1 ]; then
        DOCKER_ARGS="--keep-cache"
    fi

    # Run this script inside a privileged container
    echo "Executing build inside debian:${DISTRIBUTION} container..."
    sudo docker run --rm -it --privileged \
        -v "$BUILD_DIR/..:/opt/pipecat-cluster" \
        -w "/opt/pipecat-cluster/os-image" \
        "debian:${DISTRIBUTION}" \
        bash -c "apt-get update && apt-get install -y live-build xorriso mtools dosfstools grub-pc-bin grub-efi-amd64-bin syslinux syslinux-utils isolinux rsync && ./build_iso.sh $DOCKER_ARGS"

    echo "=== Build Complete (Host Wrapper) ==="
    exit 0
fi

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
  --bootloader "syslinux,grub-efi" \
  --initramfs "live-boot" \
  --initsystem "systemd" \
  --debian-installer-distribution "$DISTRIBUTION" \
  --debian-installer live \
  --win32-loader false \
  --bootappend-live "boot=live components quiet splash locales=en_US.UTF-8 keyboard-layouts=us live-config.username=pipecatapp live-config.user-fullname=PipecatApp" \
  --bootappend-install "auto=true priority=critical file=/preseed.cfg"

echo "=== Injecting project files ==="
# Explicitly install live-config inside the chroot so autologin functions correctly
mkdir -p config/package-lists
echo "live-boot live-config live-config-systemd" > config/package-lists/live.list.chroot

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
if [ -f "live-image-${ARCHITECTURE}.hybrid.iso" ]; then
    mv "live-image-${ARCHITECTURE}.hybrid.iso" "${ISO_NAME}-${ARCHITECTURE}.iso"
elif [ -f "binary.hybrid.iso" ]; then
    mv binary.hybrid.iso "${ISO_NAME}-${ARCHITECTURE}.iso"
elif [ -f "binary.iso" ]; then
    mv binary.iso "${ISO_NAME}-${ARCHITECTURE}.iso"
fi

echo "=== Cleaning up build artifacts ==="
# Remove large working directories and leftover files to save space
# Do NOT remove the 'config' directory as it contains tracked source files!
# We do, however, clean up the dynamically injected files.
if [ "$KEEP_CACHE" -eq 1 ]; then
    echo "Skipping full purge to keep cache (--keep-cache flag provided)."
    if [ "$(id -u)" -ne 0 ]; then
        sudo lb clean || true
        sudo rm -rf chroot binary .build \
            *.contents *.files *.packages *.modified_timestamps *.zsync.xz *.headers || true
        sudo rm -rf config/includes.chroot/opt/pipecat-cluster
        sudo rm -f config/package-lists/live.list.chroot
    else
        lb clean || true
        rm -rf chroot binary .build \
            *.contents *.files *.packages *.modified_timestamps *.zsync.xz *.headers || true
        rm -rf config/includes.chroot/opt/pipecat-cluster
        rm -f config/package-lists/live.list.chroot
    fi
else
    if [ "$(id -u)" -ne 0 ]; then
        sudo lb clean --purge || true
        sudo rm -rf chroot cache binary .build \
            *.contents *.files *.packages *.modified_timestamps *.zsync.xz *.headers || true
        sudo rm -rf config/includes.chroot/opt/pipecat-cluster
        sudo rm -f config/package-lists/live.list.chroot
    else
        lb clean --purge || true
        rm -rf chroot cache binary .build \
            *.contents *.files *.packages *.modified_timestamps *.zsync.xz *.headers || true
        rm -rf config/includes.chroot/opt/pipecat-cluster
        rm -f config/package-lists/live.list.chroot
    fi
fi

echo "=== Build Complete ==="
echo "The ISO image should be available locally as ${ISO_NAME}-${ARCHITECTURE}.iso"
