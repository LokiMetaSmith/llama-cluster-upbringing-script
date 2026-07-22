#!/bin/bash
# Builds a custom, bootable, headless Debian ISO for the Pipecat agent cluster.

set -euo pipefail

# --- Arguments ---
KEEP_CACHE=0
FLASH=0
INJECT_DIR=""
INJECT_NEXT=0

for arg in "$@"; do
    if [ "$INJECT_NEXT" -eq 1 ]; then
        INJECT_DIR="$arg"
        INJECT_NEXT=0
        continue
    fi

    if [ "$arg" = "-h" ] || [ "$arg" = "--help" ]; then
        echo "Usage: ./build_iso.sh [--keep-cache] [--flash] [--inject <folder_path>]"
        echo ""
        echo "Builds a custom, bootable, headless Debian ISO for the Pipecat agent cluster."
        echo "Automatically spins up a Debian Trixie Docker container to ensure native live-build compatibility."
        echo ""
        echo "Options:"
        echo "  --keep-cache             Preserve the package cache and build artifacts to speed up subsequent runs"
        echo "  --flash                  Interactively select a USB drive and flash the built ISO to it"
        echo "  --inject <folder_path>   Inject a folder into a new CONFIGS partition on the flashed USB drive"
        exit 0
    elif [ "$arg" = "--keep-cache" ]; then
        KEEP_CACHE=1
    elif [ "$arg" = "--flash" ]; then
        FLASH=1
    elif [ "$arg" = "--inject" ]; then
        INJECT_NEXT=1
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

    if [ "$FLASH" -eq 1 ]; then
        echo "=== USB Flashing Utility ==="
        ISO_FILE="${BUILD_DIR}/${ISO_NAME}-${ARCHITECTURE}.iso"

        if [ ! -f "$ISO_FILE" ]; then
            echo "Error: ISO file not found at $ISO_FILE"
            exit 1
        fi

        echo "Available removable drives:"
        if command -v lsblk >/dev/null 2>&1; then
            # Show disk path, size, model. Filter for typical USB properties if possible, but keep it broad enough.
            lsblk -o NAME,SIZE,MODEL,TRAN,RM | grep -E "usb| 1 " | grep -v "loop" || echo "Could not auto-detect USB drives, or none found."
            echo ""
            lsblk -d -o NAME,SIZE,MODEL,RM
        elif command -v diskutil >/dev/null 2>&1; then
            diskutil list external
        else
            echo "Warning: Could not detect 'lsblk' or 'diskutil'. Please find your device path manually."
        fi

        echo ""
        read -p "Enter the full path to the USB drive(s) you want to flash (e.g., /dev/sdb /dev/sdc): " USB_DRIVES

        if [ -z "$USB_DRIVES" ]; then
            echo "Error: No drives specified. Aborting."
            exit 1
        fi

        echo ""
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        echo "WARNING: ALL DATA ON THE FOLLOWING DRIVES WILL BE PERMANENTLY DESTROYED:"
        echo "$USB_DRIVES"
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        read -p "Type 'yes' to proceed: " CONFIRM

        if [ "$CONFIRM" != "yes" ]; then
            echo "Aborting."
            exit 1
        fi

        for USB_DRIVE in $USB_DRIVES; do
            echo "=== Processing $USB_DRIVE ==="
            if [ ! -b "$USB_DRIVE" ] && [ ! -c "$USB_DRIVE" ]; then
                echo "Error: $USB_DRIVE is not a valid block or character device. Skipping."
                continue
            fi

            echo "Flashing $ISO_FILE to $USB_DRIVE..."

            # Check if status=progress is supported (GNU dd vs BSD dd)
            # Using raw bytes (4194304 = 4MB) to avoid BSD vs GNU suffix discrepancies (e.g., '4m' vs '4M')
            if dd --help 2>&1 | grep -q 'status=progress'; then
                sudo dd if="$ISO_FILE" of="$USB_DRIVE" bs=4194304 status=progress oflag=sync
            else
                sudo dd if="$ISO_FILE" of="$USB_DRIVE" bs=4194304
            fi

            echo "Syncing filesystem..."
            sync

            echo "Verifying checksum..."
            # Cross-platform file size
            ISO_SIZE=$(wc -c < "$ISO_FILE" | tr -d ' ')

            # Cross-platform sha256 checksumming (macOS has shasum, Linux has sha256sum)
            if command -v sha256sum >/dev/null 2>&1; then
                ISO_CHECKSUM=$(sha256sum "$ISO_FILE" | awk '{print $1}')
                USB_CHECKSUM=$(sudo dd if="$USB_DRIVE" bs=4194304 count=$(( (ISO_SIZE + 4194303) / 4194304 )) 2>/dev/null | head -c "$ISO_SIZE" | sha256sum | awk '{print $1}')
            else
                ISO_CHECKSUM=$(shasum -a 256 "$ISO_FILE" | awk '{print $1}')
                USB_CHECKSUM=$(sudo dd if="$USB_DRIVE" bs=4194304 count=$(( (ISO_SIZE + 4194303) / 4194304 )) 2>/dev/null | head -c "$ISO_SIZE" | shasum -a 256 | awk '{print $1}')
            fi

            if [ "$ISO_CHECKSUM" != "$USB_CHECKSUM" ]; then
                echo "Error: Checksum mismatch for $USB_DRIVE!"
                echo "Expected: $ISO_CHECKSUM"
                echo "Got:      $USB_CHECKSUM"
                echo "The flash may have failed or the drive is corrupted."
                exit 1
            fi
            echo "Checksum verification passed for $USB_DRIVE."

            if [ -n "$INJECT_DIR" ]; then
                if [ ! -d "$INJECT_DIR" ]; then
                    echo "Error: Injection directory '$INJECT_DIR' not found. Skipping injection for $USB_DRIVE."
                else
                    if [ "$(uname -s)" = "Darwin" ]; then
                        echo "Warning: Automated partition injection is not supported on macOS due to missing Linux-native tools (fdisk, mkfs.vfat, partprobe)."
                        echo "Skipping injection for $USB_DRIVE."
                    else
                        echo "Injecting files from $INJECT_DIR into a new CONFIGS partition..."

                        PART_COUNT_BEFORE=$(lsblk -rno NAME "$USB_DRIVE" | grep -v "$(basename "$USB_DRIVE")$" | wc -l)

                        # Create a new primary FAT32 partition using fdisk.
                        # 'n' for new, newlines to accept defaults (primary, partition number, start, end),
                        # 't' for type, 'c' for W95 FAT32 (LBA), 'w' to write.
                        echo -e "n\n\n\n\n\nt\n\nc\nw" | sudo fdisk "$USB_DRIVE" || true
                        sudo partprobe "$USB_DRIVE"

                        PART_COUNT_AFTER=$(lsblk -rno NAME "$USB_DRIVE" | grep -v "$(basename "$USB_DRIVE")$" | wc -l)

                        if [ "$PART_COUNT_AFTER" -le "$PART_COUNT_BEFORE" ]; then
                            echo "Error: Failed to safely create a new partition on $USB_DRIVE. Skipping injection."
                        else
                            # Find the newly created partition (highest partition number on the device)
                            NEW_PART_NUM=$(lsblk -lno NAME "$USB_DRIVE" | grep -Eo "[0-9]+$" | sort -n | tail -1)
                            NEW_PART="${USB_DRIVE}${NEW_PART_NUM}"
                            if [ ! -b "$NEW_PART" ]; then NEW_PART="${USB_DRIVE}p${NEW_PART_NUM}"; fi

                            if [ -b "$NEW_PART" ]; then
                                echo "Formatting $NEW_PART as FAT32..."
                                sudo wipefs -a "$NEW_PART" || true
                                sudo mkfs.vfat -n "CONFIGS" "$NEW_PART"

                                MNT_DIR=$(mktemp -d)
                                sudo mount "$NEW_PART" "$MNT_DIR"
                                sudo cp -a "$INJECT_DIR"/. "$MNT_DIR"/
                                sudo umount "$MNT_DIR"
                                rm -rf "$MNT_DIR"
                                echo "Files injected successfully."
                            else
                                echo "Error: Could not find the newly created partition on $USB_DRIVE."
                            fi
                        fi
                    fi
                fi
            fi

            echo "--- Flashing Complete for $USB_DRIVE ---"
        done
        echo "=== All Flashing Operations Complete! ==="
    fi

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
  --archive-areas "main contrib non-free non-free-firmware" \
  --apt-indices true \
  --apt-recommends false \
  --security false \
  --firmware-chroot true \
  --firmware-binary true \
  --linux-packages "linux-image" \
  --linux-flavours "amd64" \
  --bootloader "syslinux,grub-efi" \
  --initramfs "live-boot" \
  --initsystem "systemd" \
  --debian-installer-distribution "$DISTRIBUTION" \
  --debian-installer live \
  --win32-loader false \
  --bootappend-live "boot=live components quiet splash nomodeset locales=en_US.UTF-8 keyboard-layouts=us live-config.username=pipecatapp live-config.user-fullname=PipecatApp" \
  --bootappend-install "auto=true priority=critical file=/preseed.cfg nomodeset netcfg/choose_interface=auto netcfg/link_wait_timeout=5 netcfg/dhcp_timeout=15 netcfg/prompt_for_interface=false"

echo "=== Injecting project files ==="
# Explicitly install live-config inside the chroot so autologin functions correctly
mkdir -p config/package-lists
echo "live-boot live-config live-config-systemd ssh-import-id" > config/package-lists/live.list.chroot

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
