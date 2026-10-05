#!/usr/bin/env bash
# ==============================================================================
# verify_pxe_server.sh - Verify Cluster PXE & Network Boot Infrastructure
# ==============================================================================
# Checks status of DHCP, TFTP, HTTP (Nginx), installer assets, and ISO images.
#
# Usage:
#   sudo ./scripts/verify_pxe_server.sh [status|tail|test]
# ==============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

LAN_IP=$(ip -4 route get 1.1.1.1 2>/dev/null | awk '{print $7}' || echo "192.168.1.148")

echo -e "\n${BOLD}${CYAN}============================================================${NC}"
echo -e "${BOLD}${CYAN} 🌐 Pipecat PXE Server Verification (Host: ${LAN_IP})${NC}"
echo -e "${BOLD}${CYAN}============================================================${NC}"

# 1. Services
echo -e "\n${BOLD}[1/5] Service Daemons Status:${NC}"
for svc in isc-dhcp-server tftpd-hpa nginx; do
    if systemctl is-active --quiet "$svc" 2>/dev/null; then
        echo -e "  • ${svc}: ${GREEN}Active (Running)${NC}"
    else
        echo -e "  • ${svc}: ${RED}Inactive or Failed${NC} (Check: sudo systemctl status $svc)"
    fi
done

# 2. Network Ports
echo -e "\n${BOLD}[2/5] Network Port Listeners:${NC}"
# DHCP: UDP 67
if (ss -uln 2>/dev/null || ss -ulpn 2>/dev/null || netstat -uln 2>/dev/null) | grep -E -q ':(67|bootps)\b'; then
    echo -e "  • DHCP Server (UDP 67): ${GREEN}Listening${NC}"
else
    echo -e "  • DHCP Server (UDP 67): ${RED}Not Listening${NC}"
fi

# TFTP: UDP 69
if (ss -uln 2>/dev/null || ss -ulpn 2>/dev/null || netstat -uln 2>/dev/null) | grep -E -q ':(69|tftp)\b'; then
    echo -e "  • TFTP Server (UDP 69): ${GREEN}Listening${NC}"
else
    echo -e "  • TFTP Server (UDP 69): ${RED}Not Listening${NC}"
fi

# HTTP: TCP 80
if (ss -tln 2>/dev/null || ss -tlpn 2>/dev/null || netstat -tln 2>/dev/null) | grep -E -q ':(80|http)\b'; then
    echo -e "  • HTTP Server (TCP 80): ${GREEN}Listening${NC}"
else
    echo -e "  • HTTP Server (TCP 80): ${RED}Not Listening${NC}"
fi

# 3. Active OS Image & ISO Targets
echo -e "\n${BOLD}[3/5] Active OS Image & Boot Target:${NC}"

# Check for custom built ISOs in os-image or web root
FOUND_ISOS=()
POSSIBLE_ISO_PATHS=(
    "/var/www/html/pipecat-installer-amd64.iso"
    "${REPO_ROOT}/os-image/pipecat-installer-amd64.iso"
    "/opt/pipecat-cluster/os-image/pipecat-installer-amd64.iso"
)

# Search /var/www/html and os-image for any .iso
for iso_candidate in /var/www/html/*.iso "${REPO_ROOT}/os-image"/*.iso; do
    if [ -f "$iso_candidate" ]; then
        FOUND_ISOS+=("$iso_candidate")
    fi
done

# Remove duplicates
if [ ${#FOUND_ISOS[@]} -gt 0 ]; then
    echo -e "  ${BOLD}Custom Cluster ISO(s) Available:${NC}"
    for iso_file in "${FOUND_ISOS[@]}"; do
        ISO_NAME=$(basename "$iso_file")
        ISO_SIZE=$(du -h "$iso_file" 2>/dev/null | awk '{print $1}')
        ISO_DATE=$(date -r "$iso_file" "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "unknown")

        # Ensure symlinked to web root for HTTP serving
        if [ ! -f "/var/www/html/${ISO_NAME}" ] && [ -d "/var/www/html" ]; then
            ln -sf "$iso_file" "/var/www/html/${ISO_NAME}" 2>/dev/null || true
        fi

        echo -e "  • ${CYAN}${ISO_NAME}${NC} (${GREEN}${ISO_SIZE}${NC}, Built: ${ISO_DATE})"
        echo -e "    File Location: ${iso_file}"
        echo -e "    HTTP Web URL:  http://${LAN_IP}/${ISO_NAME}"
    done
else
    echo -e "  • Custom ISO: ${YELLOW}pipecat-installer-amd64.iso not found${NC} in os-image/ or /var/www/html/"
    echo -e "    ${MAGENTA}Tip:${NC} Build the custom offline ISO anytime with: ${CYAN}./os-image/build_iso.sh${NC}"
fi

echo -e "\n  ${BOLD}Active Network Netboot Installer:${NC}"
if [ -f "/var/www/html/debian/linux" ] && [ -f "/var/www/html/debian/initrd.gz" ]; then
    KERNEL_SIZE=$(du -h "/var/www/html/debian/linux" 2>/dev/null | awk '{print $1}')
    INITRD_SIZE=$(du -h "/var/www/html/debian/initrd.gz" 2>/dev/null | awk '{print $1}')
    echo -e "  • ${GREEN}Debian 12 (Bookworm) Automated Network Netboot${NC}"
    echo -e "    Kernel:  http://${LAN_IP}/debian/linux (${KERNEL_SIZE})"
    echo -e "    Initrd:  http://${LAN_IP}/debian/initrd.gz (${INITRD_SIZE})"
    echo -e "    Preseed: http://${LAN_IP}/preseed.cfg (Auto-create user: pipecatapp, pass: pipecat, sudo & SSH enabled)"
else
    echo -e "  • ${RED}Netboot kernel/initrd missing${NC} under /var/www/html/debian/"
fi

# 4. Boot Assets
echo -e "\n${BOLD}[4/5] PXE & iPXE Boot Assets:${NC}"
FILES=(
    "/srv/tftp/pxelinux.0"
    "/srv/tftp/pxelinux.cfg/default"
    "/srv/tftp/undionly.kpxe"
    "/srv/tftp/ipxe.efi"
    "/var/www/html/boot.ipxe"
    "/var/www/html/preseed.cfg"
    "/var/www/html/debian/linux"
    "/var/www/html/debian/initrd.gz"
)

ALL_FILES_OK=true
for f in "${FILES[@]}"; do
    if [ -f "$f" ]; then
        SIZE=$(du -h "$f" 2>/dev/null | awk '{print $1}')
        echo -e "  • ${f} -> ${GREEN}Present${NC} (${SIZE})"
    else
        echo -e "  • ${f} -> ${RED}Missing${NC}"
        ALL_FILES_OK=false
    fi
done

# 5. Service Protocol Health Tests
echo -e "\n${BOLD}[5/5] Live Service Health Tests:${NC}"
# HTTP Tests
if curl -s -f "http://127.0.0.1/boot.ipxe" >/dev/null 2>&1; then
    echo -e "  • HTTP http://${LAN_IP}/boot.ipxe -> ${GREEN}HTTP 200 OK${NC}"
else
    echo -e "  • HTTP http://${LAN_IP}/boot.ipxe -> ${RED}Failed to fetch${NC}"
fi

if curl -s -f "http://127.0.0.1/preseed.cfg" >/dev/null 2>&1; then
    echo -e "  • HTTP http://${LAN_IP}/preseed.cfg -> ${GREEN}HTTP 200 OK${NC}"
else
    echo -e "  • HTTP http://${LAN_IP}/preseed.cfg -> ${RED}Failed to fetch${NC}"
fi

# TFTP Protocol Handshake Tests (pxelinux.0 & undionly.kpxe)
for tftp_test_file in "pxelinux.0" "undionly.kpxe"; do
    if [ -f "/srv/tftp/${tftp_test_file}" ]; then
        if python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(2.0)
s.sendto(bytes([0, 1]) + b'${tftp_test_file}' + bytes([0]) + b'octet' + bytes([0]), ('127.0.0.1', 69))
data, _ = s.recvfrom(516)
assert len(data) >= 4 and data[1] == 3
" 2>/dev/null; then
            echo -e "  • TFTP tftp://${LAN_IP}/${tftp_test_file} -> ${GREEN}Handshake 200 OK (Data Block Received)${NC}"
        else
            echo -e "  • TFTP tftp://${LAN_IP}/${tftp_test_file} -> ${RED}RRQ Handshake Failed${NC}"
        fi
    fi
done

echo -e "\n${BOLD}${CYAN}============================================================${NC}"
if [ "$ALL_FILES_OK" = true ]; then
    echo -e "${GREEN}✅ PXE Server is ready to boot new client nodes!${NC}"
    echo -e "  • ${BOLD}Pure TFTP (PXELINUX):${NC}  Loads pxelinux.0 directly over TFTP (No HTTP required)"
    echo -e "  • ${BOLD}iPXE HTTP Chainloading:${NC} Loads undionly.kpxe/ipxe.efi -> http://${LAN_IP}/boot.ipxe"
    echo -e "\nWatching for client requests (e.g. MAC 00:25:ab:7a:0d:7e):"
    echo -e "Run: ${CYAN}./scripts/cluster_ctl.sh pxe logs follow${NC} to view live boot activity."
else
    echo -e "${YELLOW}⚠️  Some files are missing. Run:${NC}"
    echo -e "  ${CYAN}sudo ./scripts/setup_pxe_server.sh debian${NC}"
fi
echo -e "${BOLD}${CYAN}============================================================${NC}\n"
