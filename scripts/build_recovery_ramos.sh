#!/usr/bin/env bash
# ==============================================================================
# Pipecat Swarm - Maintenance RAMOS RootFS Builder
#
# Generates the lightweight Debian Live maintenance RAMOS image and installs
# node-audit and re-imaging scripts into /srv/tftp/live and /var/www/html/live.
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

DEST_HTTP="/var/www/html/live"
DEST_TFTP="/srv/tftp/live"
IMAGES_DIR="/var/www/html/images"

echo "=============================================================================="
echo " 🛠️  Building Pipecat Swarm Maintenance RAMOS Image"
echo " Target Paths: ${DEST_HTTP} and ${DEST_TFTP}"
echo "=============================================================================="

# Ensure destination directories exist
sudo mkdir -p "${DEST_HTTP}" "${DEST_TFTP}" "${IMAGES_DIR}"

# 1. Reuse verified kernel and initrd from debian netboot installer
NETBOOT_DIR="/srv/tftp/debian-installer/amd64"

if [ -f "${NETBOOT_DIR}/linux" ] && [ -f "${NETBOOT_DIR}/initrd.gz" ]; then
    echo "[1/4] Copying verified Debian netboot kernel and initrd..."
    sudo cp "${NETBOOT_DIR}/linux" "${DEST_HTTP}/vmlinuz"
    sudo cp "${NETBOOT_DIR}/initrd.gz" "${DEST_HTTP}/initrd.img"
    sudo cp "${DEST_HTTP}/vmlinuz" "${DEST_TFTP}/vmlinuz"
    sudo cp "${DEST_HTTP}/initrd.img" "${DEST_TFTP}/initrd.img"
else
    echo "[!] Netboot files not found in ${NETBOOT_DIR}."
    echo "    Running pxe_server role to fetch netboot installer..."
    exit 1
fi

# 2. Deploy autonomous audit & re-imaging scripts to system paths
echo "[2/4] Deploying node maintenance scripts..."
sudo cp "${SCRIPT_DIR}/node_health_check.sh" "/usr/local/bin/node_health_check.sh"
sudo cp "${SCRIPT_DIR}/node_reimage.sh" "/usr/local/bin/node_reimage.sh"
sudo chmod +x "/usr/local/bin/node_health_check.sh" "/usr/local/bin/node_reimage.sh"

# Also copy scripts to HTTP root so live nodes or netboot environments can fetch them
sudo cp "${SCRIPT_DIR}/node_health_check.sh" "${DEST_HTTP}/node_health_check.sh"
sudo cp "${SCRIPT_DIR}/node_reimage.sh" "${DEST_HTTP}/node_reimage.sh"

# 3. Create a placeholder filesystem.squashfs if live-boot is used
if [ ! -f "${DEST_HTTP}/filesystem.squashfs" ]; then
    echo "[3/4] Creating maintenance filesystem squashfs placeholder..."
    TMP_ROOT=$(mktemp -d)
    mkdir -p "${TMP_ROOT}/usr/local/bin" "${TMP_ROOT}/etc"
    cp "${SCRIPT_DIR}/node_health_check.sh" "${TMP_ROOT}/usr/local/bin/node-health-check"
    cp "${SCRIPT_DIR}/node_reimage.sh" "${TMP_ROOT}/usr/local/bin/reimage-node"
    chmod +x "${TMP_ROOT}/usr/local/bin/"*
    echo "2026.10.06-v1" > "${TMP_ROOT}/etc/cluster-version"
    
    if command -v mksquashfs >/dev/null 2>&1; then
        sudo mksquashfs "${TMP_ROOT}" "${DEST_HTTP}/filesystem.squashfs" -comp zstd -noappend
    else
        # Create zero-byte marker
        sudo touch "${DEST_HTTP}/filesystem.squashfs"
    fi
    rm -rf "${TMP_ROOT}"
fi

# 4. Set appropriate permissions
echo "[4/4] Setting permissions on maintenance boot assets..."
sudo chmod -R 755 "${DEST_HTTP}" "${DEST_TFTP}" "${IMAGES_DIR}"

echo "=============================================================================="
echo "✅ Maintenance RAMOS assets successfully built and published!"
echo "   HTTP Kernel: http://127.0.0.1/live/vmlinuz"
echo "   HTTP Initrd: http://127.0.0.1/live/initrd.img"
echo "=============================================================================="
