#!/usr/bin/env bash
# ==============================================================================
# integrate_netboot_firmware.sh
# ==============================================================================
# Injects missing non-free network NIC firmware (Realtek r8169/r8125, Broadcom bnx2/bnx2x)
# directly into Debian Netboot installer's initrd.gz to allow fully automated PXE
# installations on legacy and commodity client nodes without driver stall.
# ==============================================================================
set -euo pipefail

TFTP_DIR="${1:-/srv/tftp/debian-installer/amd64}"
WEB_DIR="${2:-/var/www/html/debian}"
STAGING_DIR="/tmp/netboot_firmware_staging"

echo "=== Integrating Non-Free Network Firmware into Debian Netboot ==="
echo "Target TFTP Directory: $TFTP_DIR"

if [ ! -d "$TFTP_DIR" ]; then
    echo "Error: TFTP directory $TFTP_DIR does not exist."
    exit 1
fi

# Ensure cpio is installed
if ! command -v cpio >/dev/null 2>&1; then
    apt-get update && apt-get install -y cpio
fi

# 1. Preserve original clean initrd.gz if not already preserved
if [ ! -f "$TFTP_DIR/initrd.gz.orig" ]; then
    echo "Backing up original netboot initrd.gz -> initrd.gz.orig..."
    cp -p "$TFTP_DIR/initrd.gz" "$TFTP_DIR/initrd.gz.orig"
fi

# 2. Setup clean staging directories
rm -rf "$STAGING_DIR"
mkdir -p "$STAGING_DIR/debs" \
         "$STAGING_DIR/extracted" \
         "$STAGING_DIR/root/lib/firmware" \
         "$STAGING_DIR/root/usr/lib/firmware" \
         "$STAGING_DIR/root/firmware"

# 3. Download key firmware packages
echo "Downloading core network firmware packages (Realtek, Broadcom)..."
cd "$STAGING_DIR/debs"
chmod 777 "$STAGING_DIR/debs"
apt-get update -o Dir::Etc::sourcelist="sources.list" 2>/dev/null || true
apt-get download firmware-realtek firmware-bnx2 firmware-bnx2x 2>/dev/null || true

# 4. Extract and stage firmware files
echo "Extracting firmware payloads..."
for deb in "$STAGING_DIR/debs"/*.deb; do
    if [ -f "$deb" ]; then
        dpkg-deb -x "$deb" "$STAGING_DIR/extracted"
        cp "$deb" "$STAGING_DIR/root/firmware/"
    fi
done

# Copy firmware files into both /lib/firmware and /usr/lib/firmware
if [ -d "$STAGING_DIR/extracted/usr/lib/firmware" ]; then
    cp -r "$STAGING_DIR/extracted/usr/lib/firmware"/* "$STAGING_DIR/root/usr/lib/firmware/"
    cp -r "$STAGING_DIR/extracted/usr/lib/firmware"/* "$STAGING_DIR/root/lib/firmware/"
fi

# Verify the critical requested file exists
if [ -f "$STAGING_DIR/root/lib/firmware/rtl_nic/rtl8168g-2.fw" ]; then
    echo "✅ Verified: rtl_nic/rtl8168g-2.fw is present in firmware staging."
else
    echo "⚠️ Warning: rtl_nic/rtl8168g-2.fw was not found in downloaded packages!"
fi

# 5. Pack into cpio.gz archive
echo "Packaging firmware cpio archive..."
cd "$STAGING_DIR/root"
find . | cpio -o -H newc 2>/dev/null | gzip -9 > "$STAGING_DIR/firmware_network.cpio.gz"

FIRMWARE_SIZE=$(du -h "$STAGING_DIR/firmware_network.cpio.gz" | cut -f1)
echo "Generated firmware archive: $FIRMWARE_SIZE"

# 6. Concatenate with original initrd
echo "Concatenating initrd.gz.orig + firmware_network.cpio.gz -> initrd.gz..."
cat "$TFTP_DIR/initrd.gz.orig" "$STAGING_DIR/firmware_network.cpio.gz" > "$TFTP_DIR/initrd.gz"
chmod 0644 "$TFTP_DIR/initrd.gz"
if id -u tftp >/dev/null 2>&1; then
    chown tftp:tftp "$TFTP_DIR/initrd.gz" || true
fi

# 7. Sync to web root if present and not a symlink
if [ -d "$WEB_DIR" ] && [ ! -L "$WEB_DIR/initrd.gz" ] && [ -f "$WEB_DIR/initrd.gz" ]; then
    cp -p "$TFTP_DIR/initrd.gz" "$WEB_DIR/initrd.gz"
fi

# Clean up staging
rm -rf "$STAGING_DIR"

echo "=== Network Firmware Integration Complete ==="
echo "Total updated initrd.gz size: $(du -h "$TFTP_DIR/initrd.gz" | cut -f1)"
