#!/usr/bin/env bash
# ==============================================================================
# Pipecat Swarm - Autonomous Node Re-imaging & Identity Injection Agent
#
# Streams golden node image to local disk, updates GPT boundaries, injects
# unique node identity (machine-id, SSH host keys, hostname), and reconciles with swarm.
# ==============================================================================
set -euo pipefail

TARGET_DISK="${1:-}"

if [ -z "${TARGET_DISK}" ]; then
    TARGET_DISK=$(lsblk -dpno NAME,TYPE,RM 2>/dev/null | awk '$2=="disk" && $3=="0" {print $1; exit}')
    if [ -z "${TARGET_DISK}" ]; then
        TARGET_DISK=$(lsblk -dpno NAME,TYPE 2>/dev/null | awk '$2=="disk" {print $1; exit}')
    fi
fi

if [ -z "${TARGET_DISK}" ]; then
    echo "[!] FATAL: No target disk specified or discovered for re-imaging."
    exit 1
fi

SERVER_IP=$(ip route show default | awk '/default/ {print $3}' | head -n1)
if [ -z "${SERVER_IP}" ]; then
    SERVER_IP="192.168.1.148"
fi
API_URL="http://${SERVER_IP}:8007/api"

DEFAULT_IFACE=$(ip route show default | awk '{print $5}' | head -n1)
if [ -n "${DEFAULT_IFACE}" ] && [ -f "/sys/class/net/${DEFAULT_IFACE}/address" ]; then
    MAC_ADDR=$(cat "/sys/class/net/${DEFAULT_IFACE}/address" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')
else
    MAC_ADDR="00:00:00:00:00:00"
fi

echo "=============================================================================="
echo " ⚡ Pipecat Autonomous Re-imaging Pipeline"
echo " Target Disk: ${TARGET_DISK} | Node MAC: ${MAC_ADDR} | Controller: ${SERVER_IP}"
echo "=============================================================================="

# ------------------------------------------------------------------------------
# 1. Thundering Herd Mitigation: MAC-based Jitter Delay
# ------------------------------------------------------------------------------
LAST_OCTET="${MAC_ADDR##*:}"
# Convert hex octet to integer safely with bash arithmetic
JITTER_SEC=$(( 16#${LAST_OCTET} % 30 ))
echo "[1/6] Staggering flash concurrency: Sleeping ${JITTER_SEC}s jitter delay..."
sleep "${JITTER_SEC}"

# ------------------------------------------------------------------------------
# 2. Swarm Identity De-registration & Eviction
# ------------------------------------------------------------------------------
echo "[2/6] Notifying cluster controller to drain and evict old node identity..."
curl -s -X POST "${API_URL}/cluster/evict" \
     -H "Content-Type: application/json" \
     -d "{\"mac\": \"${MAC_ADDR}\", \"reason\": \"REIMAGE_INITIATED\"}" || true

# ------------------------------------------------------------------------------
# 3. Stream Golden Image or Fallback to Automated Netboot Provisioner
# ------------------------------------------------------------------------------
echo "[3/6] Streaming image to target disk: ${TARGET_DISK}..."

# First check if raw zstd stream image exists on controller
GOLDEN_IMAGE_URL="http://${SERVER_IP}/images/debian-golden-node.img.zst"
IMAGE_FOUND=false

if curl -sI -f "${GOLDEN_IMAGE_URL}" >/dev/null 2>&1; then
    IMAGE_FOUND=true
fi

if [ "${IMAGE_FOUND}" = "true" ]; then
    echo "  • Found golden image at ${GOLDEN_IMAGE_URL}"
    # Wipe signatures on target drive
    wipefs -af "${TARGET_DISK}" || true
    # Stream uncompressed image directly to block device with fsync
    curl -sSf "${GOLDEN_IMAGE_URL}" | zstd -d -c | dd of="${TARGET_DISK}" bs=4M status=progress conv=fsync
else
    echo "  • Golden raw image not found at ${GOLDEN_IMAGE_URL}."
    echo "  • Triggering Debian Automated Netboot Preseed fallback installation..."
    # Chainload the automated netboot preseed installer kernel
    exec /usr/bin/kexec -l "/var/www/html/debian/linux" \
        --initrd="/var/www/html/debian/initrd.gz" \
        --command-line="auto=true priority=critical url=http://${SERVER_IP}/preseed.cfg netcfg/choose_interface=auto net.ifnames=0 biosdevname=0 --" 2>/dev/null || reboot
fi

# ------------------------------------------------------------------------------
# 4. Expand GPT Partition Table & Rescan
# ------------------------------------------------------------------------------
echo "[4/6] Aligning GPT partition boundaries..."
if command -v sgdisk >/dev/null 2>&1; then
    sgdisk -e "${TARGET_DISK}" 2>/dev/null || true
fi
if command -v partprobe >/dev/null 2>&1; then
    partprobe "${TARGET_DISK}" 2>/dev/null || true
fi

# ------------------------------------------------------------------------------
# 5. Post-Flash Machine Identity & Secrets Injection
# ------------------------------------------------------------------------------
echo "[5/6] Injecting unique machine identity, hostname, and keys..."
if echo "${TARGET_DISK}" | grep -qE "nvme|mmcblk"; then
    ROOT_PART="${TARGET_DISK}p2"
else
    ROOT_PART="${TARGET_DISK}2"
fi

MOUNT_DIR=$(mktemp -d)
mount "${ROOT_PART}" "${MOUNT_DIR}"

# 1. Update cluster-version stamp
TARGET_VERSION=$(curl -sSf "${API_URL}/cluster/target-version" 2>/dev/null || echo "2026.10.06-v1")
echo "${TARGET_VERSION}" > "${MOUNT_DIR}/etc/cluster-version"

# 2. Assign unique deterministic hostname based on MAC
CLEAN_MAC=$(echo "${MAC_ADDR}" | tr -d ':')
NODE_HOSTNAME="pipecat-${CLEAN_MAC: -6}"
echo "${NODE_HOSTNAME}" > "${MOUNT_DIR}/etc/hostname"
echo "127.0.1.1 ${NODE_HOSTNAME}" >> "${MOUNT_DIR}/etc/hosts"

# 3. Reset machine-id and generate fresh host keys
rm -f "${MOUNT_DIR}/etc/machine-id" "${MOUNT_DIR}/var/lib/dbus/machine-id"
if command -v chroot >/dev/null 2>&1; then
    chroot "${MOUNT_DIR}" systemd-machine-id-setup 2>/dev/null || true
    chroot "${MOUNT_DIR}" ssh-keygen -A 2>/dev/null || true
fi

# 4. Clear any lingering panic or halt crash flags
rm -f "${MOUNT_DIR}/var/log/system-halt-flag" "${MOUNT_DIR}/var/log/panic-flag"

umount -R "${MOUNT_DIR}"

# ------------------------------------------------------------------------------
# 6. Report Completion & Reboot
# ------------------------------------------------------------------------------
echo "[6/6] Re-imaging complete! Reporting to cluster control plane..."
curl -s -X POST "${API_URL}/cluster/node-status" \
     -H "Content-Type: application/json" \
     -d "{\"mac\": \"${MAC_ADDR}\", \"status\": \"REIMAGED\", \"hostname\": \"${NODE_HOSTNAME}\", \"details\": {\"version\": \"${TARGET_VERSION}\", \"disk\": \"${TARGET_DISK}\"}}" || true

echo "=============================================================================="
echo "✅ Node recovery successfully finished. Booting into restored node..."
echo "=============================================================================="
reboot
