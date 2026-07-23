#!/bin/bash
# Builds a custom, bootable, headless Debian ISO for the Pipecat agent cluster.

set -euo pipefail

# --- Arguments ---
KEEP_CACHE=0
FLASH=0
INJECT_DIR=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            echo "Usage: ./build_iso.sh [--keep-cache] [--flash] [--inject <dir>]"
            echo ""
            echo "Builds a custom, bootable, headless Debian ISO for the Pipecat agent cluster."
            echo "Automatically spins up a Debian Trixie Docker container to ensure native live-build compatibility."
            echo ""
            echo "Options:"
            echo "  --keep-cache    Preserve the package cache and build artifacts to speed up subsequent runs"
            echo "  --flash         Interactively select USB drives and flash the built ISO to them"
            echo "  --inject <dir>  Inject the contents of a directory into a new FAT32 CONFIGS partition on the USB drive (Linux only, implies --flash)"
            exit 0
            ;;
        --keep-cache)
            KEEP_CACHE=1
            shift
            ;;
        --flash)
            FLASH=1
            shift
            ;;
        --inject)
            INJECT_DIR="$2"
            FLASH=1
            shift 2
            ;;
        *)
            echo "Unknown option $1"
            exit 1
            ;;
    esac
done

if [ -n "$INJECT_DIR" ]; then
    if [ ! -d "$INJECT_DIR" ]; then
        echo "Error: Inject directory '$INJECT_DIR' does not exist."
        exit 1
    fi
    # Make INJECT_DIR absolute before we cd around
    INJECT_DIR="$(cd "$INJECT_DIR" && pwd)"
fi

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

    # Pass along DOCKER_ARGS ensuring we don't pass host-specific flashing args to the inner container build loop
    # Run this script inside a privileged container
    echo "Executing build inside debian:${DISTRIBUTION} container..."
    sudo docker run --rm -it --privileged \
        -v "$BUILD_DIR/..:/opt/pipecat-cluster" \
        -w "/opt/pipecat-cluster/os-image" \
        "debian:${DISTRIBUTION}" \
        bash -c "apt-get update && apt-get install -y live-build xorriso mtools dosfstools grub-pc-bin grub-efi-amd64-bin grub-efi-amd64-signed shim-signed syslinux syslinux-utils isolinux rsync && ./build_iso.sh $DOCKER_ARGS"

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
        read -p "Enter the full paths to the USB drives you want to flash, separated by space (e.g., /dev/sdb /dev/sdc): " USB_DRIVES_INPUT

        if [ -z "$USB_DRIVES_INPUT" ]; then
            echo "Error: No drives specified. Aborting."
            exit 1
        fi

        # Convert input into an array
        read -ra USB_DRIVES <<< "$USB_DRIVES_INPUT"

        for USB_DRIVE in "${USB_DRIVES[@]}"; do
            if [ ! -b "$USB_DRIVE" ] && [ ! -c "$USB_DRIVE" ]; then
                echo "Error: $USB_DRIVE is not a valid block or character device. Aborting."
                exit 1
            fi
        done

        echo ""
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        echo "WARNING: ALL DATA ON THE FOLLOWING DRIVES WILL BE PERMANENTLY DESTROYED:"
        for USB_DRIVE in "${USB_DRIVES[@]}"; do
            echo "  - $USB_DRIVE"
        done
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        read -p "Type 'yes' to proceed: " CONFIRM

        if [ "$CONFIRM" != "yes" ]; then
            echo "Aborting."
            exit 1
        fi

        echo "Calculating reference checksum for $ISO_FILE..."
        if command -v md5sum >/dev/null 2>&1; then
            REF_CHECKSUM=$(md5sum "$ISO_FILE" | awk '{print $1}')
            ISO_SIZE=$(stat -c%s "$ISO_FILE")
        elif command -v md5 >/dev/null 2>&1; then
            # macOS fallback
            REF_CHECKSUM=$(md5 -q "$ISO_FILE")
            ISO_SIZE=$(stat -f%z "$ISO_FILE")
        else
            echo "Warning: md5sum or md5 not found. Verification will be skipped."
            REF_CHECKSUM=""
        fi

        for USB_DRIVE in "${USB_DRIVES[@]}"; do
            echo ""
            echo "--- Flashing $ISO_FILE to $USB_DRIVE ---"

            # Check if status=progress is supported (GNU dd vs BSD dd)
            # Using raw bytes (4194304 = 4MB) to avoid BSD vs GNU suffix discrepancies (e.g., '4m' vs '4M')
            if dd --help 2>&1 | grep -q 'status=progress'; then
                sudo dd if="$ISO_FILE" of="$USB_DRIVE" bs=4194304 status=progress oflag=sync
            else
                sudo dd if="$ISO_FILE" of="$USB_DRIVE" bs=4194304
            fi

            echo "Syncing filesystem..."
            sync

            if [ -n "$REF_CHECKSUM" ]; then
                echo "Verifying $USB_DRIVE..."

                # Calculate how many 1MB blocks to read to cover the ISO size (ceiling division)
                DD_COUNT=$(( (ISO_SIZE + 1048575) / 1048576 ))

                if command -v md5sum >/dev/null 2>&1; then
                    DRIVE_CHECKSUM=$(sudo dd if="$USB_DRIVE" bs=1048576 count="$DD_COUNT" 2>/dev/null | head -c "$ISO_SIZE" | md5sum | awk '{print $1}')
                else
                    DRIVE_CHECKSUM=$(sudo dd if="$USB_DRIVE" bs=1048576 count="$DD_COUNT" 2>/dev/null | head -c "$ISO_SIZE" | md5 -q)
                fi

                if [ "$REF_CHECKSUM" != "$DRIVE_CHECKSUM" ]; then
                    echo "ERROR: Checksum mismatch on $USB_DRIVE!"
                    echo "  Expected: $REF_CHECKSUM"
                    echo "  Got:      $DRIVE_CHECKSUM"
                    echo "Aborting further operations."
                    exit 1
                else
                    echo "Verification successful!"
                fi
            fi

            if [ -n "$INJECT_DIR" ]; then
                if [ "$(uname -s)" != "Linux" ]; then
                    echo "Warning: Config injection is currently only supported on Linux. Skipping injection for $USB_DRIVE."
                else
                    echo "--- Injecting Configs into $USB_DRIVE ---"
                    if ! command -v parted >/dev/null 2>&1 || ! command -v mkfs.vfat >/dev/null 2>&1 || ! command -v sgdisk >/dev/null 2>&1; then
                        echo "Error: 'parted', 'sgdisk', and 'dosfstools' are required for injection. Skipping."
                    else
                        # 1. Create partition in remaining free space
                        echo "Fixing GPT backup header to end of disk..."
                        sudo sgdisk -e "$USB_DRIVE" || true

                        echo "Creating CONFIGS partition..."
                        sudo parted -s "$USB_DRIVE" mkpart primary fat32 "$ISO_SIZE"B 100%

                        # Trigger kernel to re-read partition table
                        sudo partprobe "$USB_DRIVE" || true
                        sleep 3 # Give udev a moment to create the device node

                        # Dynamically discover the newly created partition (highest partition number)
                        # We cannot hardcode '2' because isohybrid images often already contain 2 partitions (ISO9660 and EFI)
                        PART_NUM=$(lsblk -nl -o MIN,NAME "$USB_DRIVE" 2>/dev/null | grep -E "^[ ]*[0-9]+[ ]+.*[0-9]+$" | awk '{print $2}' | sed "s#.*${USB_DRIVE##*/}##" | sed 's/^p//' | sort -n | tail -1)

                        if [ -z "$PART_NUM" ]; then
                            echo "Error: Could not determine newly created partition number. Skipping injection."
                        else
                            if [[ "$USB_DRIVE" == *[0-9] ]]; then
                                PART_DEV="${USB_DRIVE}p${PART_NUM}"
                            else
                                PART_DEV="${USB_DRIVE}${PART_NUM}"
                            fi

                            if [ ! -b "$PART_DEV" ]; then
                                echo "Error: Could not find newly created partition $PART_DEV. Skipping injection."
                            else
                            # 2. Format as FAT32
                            echo "Formatting $PART_DEV as FAT32..."
                            sudo mkfs.vfat -n CONFIGS "$PART_DEV"

                                # 3. Mount and Copy
                                MNT_DIR=$(mktemp -d)
                                sudo mount "$PART_DEV" "$MNT_DIR"
                                echo "Copying files from $INJECT_DIR to $PART_DEV..."
                                sudo cp -r "$INJECT_DIR"/* "$MNT_DIR"/

                                sudo sync
                                sudo umount "$MNT_DIR"
                                rm -rf "$MNT_DIR"

                                echo "Injection successful!"
                            fi
                        fi
                    fi
                fi
            fi
        done

        echo "=== All Flashing Complete! ==="
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
  --parent-mirror-bootstrap "https://deb.debian.org/debian/" \
  --mirror-bootstrap "https://deb.debian.org/debian/" \
  --parent-mirror-chroot "https://deb.debian.org/debian/" \
  --mirror-chroot "https://deb.debian.org/debian/" \
  --parent-mirror-binary "https://deb.debian.org/debian/" \
  --mirror-binary "https://deb.debian.org/debian/" \
  --parent-mirror-debian-installer "https://deb.debian.org/debian/" \
  --mirror-debian-installer "https://deb.debian.org/debian/" \
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
