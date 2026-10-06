#!/usr/bin/env bash
# ==============================================================================
# Pipecat Swarm - Autonomous Node Health Audit & Maintenance Agent
#
# Runs in RAMOS maintenance rootfs to verify hardware integrity, partition layout,
# filesystem health, and cluster image version before handing off control.
# ==============================================================================
set -euo pipefail

# Discover default gateway & API server dynamically via routing table (DHCP)
SERVER_IP=$(ip route show default | awk '/default/ {print $3}' | head -n1)
if [ -z "${SERVER_IP}" ]; then
    SERVER_IP="192.168.1.148"
fi
API_URL="http://${SERVER_IP}:8007/api"

# Discover primary network interface and hardware MAC address
DEFAULT_IFACE=$(ip route show default | awk '{print $5}' | head -n1)
if [ -n "${DEFAULT_IFACE}" ] && [ -f "/sys/class/net/${DEFAULT_IFACE}/address" ]; then
    MAC_ADDR=$(cat "/sys/class/net/${DEFAULT_IFACE}/address" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')
else
    MAC_ADDR="00:00:00:00:00:00"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REIMAGE_BIN="${SCRIPT_DIR}/node_reimage.sh"
if [ ! -x "${REIMAGE_BIN}" ]; then
    REIMAGE_BIN="/usr/local/bin/node_reimage.sh"
fi

echo "=============================================================================="
echo " 🔍 Pipecat Autonomous Hardware & Filesystem Audit Agent"
echo " Node MAC: ${MAC_ADDR} | Controller: ${SERVER_IP}"
echo "=============================================================================="

# ------------------------------------------------------------------------------
# 1. Deterministic Primary Drive Discovery
# Exclude loop devices, RAM disks, optical media, and removable USB drives
# ------------------------------------------------------------------------------
echo "[1/5] Discovering non-removable target drive..."
TARGET_DISK=$(lsblk -dpno NAME,TYPE,RM 2>/dev/null | awk '$2=="disk" && $3=="0" {print $1; exit}')

if [ -z "${TARGET_DISK}" ]; then
    # Fallback to first available disk if RM flag is unset
    TARGET_DISK=$(lsblk -dpno NAME,TYPE 2>/dev/null | awk '$2=="disk" {print $1; exit}')
fi

if [ -z "${TARGET_DISK}" ]; then
    echo "[!] FATAL: No target hard drive or SSD detected on this station."
    curl -s -X POST "${API_URL}/cluster/quarantine" \
         -H "Content-Type: application/json" \
         -d "{\"mac\": \"${MAC_ADDR}\", \"reason\": \"NO_STORAGE_DISK_FOUND\"}" || true
    echo "Node halted to prevent boot loop."
    sleep 3600
    exit 1
fi

echo "  • Primary target disk: ${TARGET_DISK}"

# ------------------------------------------------------------------------------
# 2. Hardware SMART Integrity Audit
# ------------------------------------------------------------------------------
echo "[2/5] Inspecting drive SMART attributes..."
if command -v smartctl >/dev/null 2>&1; then
    set +e
    SMART_OUT=$(smartctl -H "${TARGET_DISK}" 2>&1)
    SMART_RC=$?
    set -e

    if [ ${SMART_RC} -ne 0 ] || ! echo "${SMART_OUT}" | grep -qiE "(PASSED|OK)"; then
        echo "[!] CRITICAL: Target drive ${TARGET_DISK} failed SMART health assessment!"
        echo "${SMART_OUT}"
        curl -s -X POST "${API_URL}/cluster/quarantine" \
             -H "Content-Type: application/json" \
             -d "{\"mac\": \"${MAC_ADDR}\", \"reason\": \"SMART_HARDWARE_FAILURE\", \"details\": {\"disk\": \"${TARGET_DISK}\"}}" || true
        echo "Node quarantined to prevent NAND wear. Halting."
        sleep 3600
        exit 1
    fi
    echo "  • SMART status: PASSED"
else
    echo "  • smartctl not available in RAMOS; skipping hardware SMART check."
fi

# ------------------------------------------------------------------------------
# 3. Partition Structure & Filesystem Verification
# ------------------------------------------------------------------------------
echo "[3/5] Inspecting partition table and root filesystem..."
# Distinguish NVMe partitions (nvme0n1p2) from SATA partitions (sda2)
if echo "${TARGET_DISK}" | grep -qE "nvme|mmcblk"; then
    ROOT_PART="${TARGET_DISK}p2"
else
    ROOT_PART="${TARGET_DISK}2"
fi

if ! lsblk -no FSTYPE "${ROOT_PART}" 2>/dev/null | grep -qi "ext4"; then
    # Try partition 1 if single-partition layout
    if echo "${TARGET_DISK}" | grep -qE "nvme|mmcblk"; then
        ALT_PART="${TARGET_DISK}p1"
    else
        ALT_PART="${TARGET_DISK}1"
    fi

    if lsblk -no FSTYPE "${ALT_PART}" 2>/dev/null | grep -qi "ext4"; then
        ROOT_PART="${ALT_PART}"
    else
        echo "[!] No valid root filesystem partition found on ${TARGET_DISK}."
        echo "Triggering automated re-imaging..."
        exec "${REIMAGE_BIN}" "${TARGET_DISK}"
    fi
fi

echo "  • Validated root partition: ${ROOT_PART}"

# ------------------------------------------------------------------------------
# 4. Read-Only Filesystem Health Audit (e2fsck)
# ------------------------------------------------------------------------------
echo "[4/5] Running non-destructive filesystem integrity check..."
set +e
e2fsck -n -f "${ROOT_PART}" >/tmp/fsck.log 2>&1
FSCK_CODE=$?
set -e

# Exit codes:
# 0 = No errors
# 1 = Filesystem errors corrected (when running with -p, but with -n 1 means errors were found)
# >= 4 = Operational/severe uncorrected errors or corrupted journal
if [ ${FSCK_CODE} -ge 4 ]; then
    echo "[!] Filesystem integrity check failed with critical code ${FSCK_CODE}."
    cat /tmp/fsck.log | head -n 20
    echo "Corrupted filesystem detected. Triggering automated recovery re-image..."
    exec "${REIMAGE_BIN}" "${TARGET_DISK}"
elif [ ${FSCK_CODE} -ne 0 ]; then
    echo "  • Notice: Minor filesystem flags present (e2fsck code ${FSCK_CODE})."
fi

# ------------------------------------------------------------------------------
# 5. Version Verification & Abnormal Shutdown / Panic Checks
# ------------------------------------------------------------------------------
echo "[5/5] Checking cluster golden image version & crash flags..."
MOUNT_DIR=$(mktemp -d)
if ! mount -o ro "${ROOT_PART}" "${MOUNT_DIR}" 2>/dev/null; then
    echo "[!] Failed to mount ${ROOT_PART} read-only. Drive or metadata damaged."
    exec "${REIMAGE_BIN}" "${TARGET_DISK}"
fi

# Unresolved panic / crash flag detection
if [ -f "${MOUNT_DIR}/var/log/system-halt-flag" ] || [ -f "${MOUNT_DIR}/var/log/panic-flag" ]; then
    echo "[!] Unresolved host crash flag detected on local rootfs."
    umount "${MOUNT_DIR}"
    exec "${REIMAGE_BIN}" "${TARGET_DISK}"
fi

CURRENT_VERSION="unknown"
if [ -f "${MOUNT_DIR}/etc/cluster-version" ]; then
    CURRENT_VERSION=$(cat "${MOUNT_DIR}/etc/cluster-version" | tr -d '[:space:]')
fi

# Query target version from cluster API
LATEST_VERSION="unknown"
if command -v curl >/dev/null 2>&1; then
    LATEST_VERSION=$(curl -sSf --connect-timeout 5 "${API_URL}/cluster/target-version" 2>/dev/null || echo "unknown")
    LATEST_VERSION=$(echo "${LATEST_VERSION}" | tr -d '[:space:]')
fi

echo "  • Installed version: ${CURRENT_VERSION}"
echo "  • Target cluster version: ${LATEST_VERSION}"

if [ "${LATEST_VERSION}" != "unknown" ] && [ "${CURRENT_VERSION}" != "${LATEST_VERSION}" ]; then
    echo "[!] Installed image version (${CURRENT_VERSION}) is outdated (Target: ${LATEST_VERSION})."
    echo "Initiating upgrade flash..."
    umount "${MOUNT_DIR}"
    exec "${REIMAGE_BIN}" "${TARGET_DISK}"
fi

# ------------------------------------------------------------------------------
# 6. Node Healthy -> Fast kexec into Local System
# ------------------------------------------------------------------------------
echo "=============================================================================="
echo "✅ Node hardware, filesystem, and version verified clean and current!"
echo "Reporting healthy status to cluster controller..."

curl -s -X POST "${API_URL}/cluster/node-status" \
     -H "Content-Type: application/json" \
     -d "{\"mac\": \"${MAC_ADDR}\", \"status\": \"HEALTHY\", \"details\": {\"version\": \"${CURRENT_VERSION}\", \"disk\": \"${TARGET_DISK}\"}}" || true

KERNEL_IMG=$(find "${MOUNT_DIR}/boot" -name "vmlinuz*" | sort -V | tail -n1)
INITRD_IMG=$(find "${MOUNT_DIR}/boot" -name "initrd.img*" | sort -V | tail -n1)

if [ -n "${KERNEL_IMG}" ] && [ -n "${INITRD_IMG}" ] && command -v kexec >/dev/null 2>&1; then
    echo "Performing fast zero-reboot kexec transition into ${KERNEL_IMG}..."
    CMDLINE="root=${ROOT_PART} ro quiet net.ifnames=0 biosdevname=0"
    if [ -f "${MOUNT_DIR}/etc/kernel/cmdline" ]; then
        CMDLINE="$(cat "${MOUNT_DIR}/etc/kernel/cmdline")"
    fi
    kexec -l "${KERNEL_IMG}" --initrd="${INITRD_IMG}" --command-line="${CMDLINE}" 2>/dev/null && {
        umount "${MOUNT_DIR}"
        kexec -e
    }
fi

echo "Handoff to local disk via system reboot..."
umount "${MOUNT_DIR}" 2>/dev/null || true
reboot
