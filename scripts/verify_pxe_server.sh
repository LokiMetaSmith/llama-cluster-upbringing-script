#!/usr/bin/env bash
# ==============================================================================
# verify_pxe_server.sh - Verify Cluster PXE & Network Boot Infrastructure
# ==============================================================================
# Checks status of DHCP, TFTP, HTTP (Nginx), and verifies installer assets.
#
# Usage:
#   sudo ./scripts/verify_pxe_server.sh [status|tail|test]
# ==============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

LAN_IP=$(ip -4 route get 1.1.1.1 2>/dev/null | awk '{print $7}' || echo "192.168.1.148")

echo -e "\n${BOLD}${CYAN}============================================================${NC}"
echo -e "${BOLD}${CYAN} 🌐 Pipecat PXE Server Verification (Host: ${LAN_IP})${NC}"
echo -e "${BOLD}${CYAN}============================================================${NC}"

# 1. Services
echo -e "\n${BOLD}[1/4] Service Daemons Status:${NC}"
for svc in isc-dhcp-server tftpd-hpa nginx; do
    if systemctl is-active --quiet "$svc" 2>/dev/null; then
        echo -e "  • ${svc}: ${GREEN}Active (Running)${NC}"
    else
        echo -e "  • ${svc}: ${RED}Inactive or Failed${NC} (Check: systemctl status $svc)"
    fi
done

# 2. Network Ports
echo -e "\n${BOLD}[2/4] Network Port Listeners:${NC}"
# DHCP: UDP 67
if ss -ulpn 2>/dev/null | grep -q ":67 "; then
    echo -e "  • DHCP Server (UDP 67): ${GREEN}Listening${NC}"
else
    echo -e "  • DHCP Server (UDP 67): ${RED}Not Listening${NC}"
fi

# TFTP: UDP 69
if ss -ulpn 2>/dev/null | grep -q ":69 "; then
    echo -e "  • TFTP Server (UDP 69): ${GREEN}Listening${NC}"
else
    echo -e "  • TFTP Server (UDP 69): ${RED}Not Listening${NC}"
fi

# HTTP: TCP 80
if ss -tlpn 2>/dev/null | grep -q ":80 "; then
    echo -e "  • HTTP Server (TCP 80): ${GREEN}Listening${NC}"
else
    echo -e "  • HTTP Server (TCP 80): ${RED}Not Listening${NC}"
fi

# 3. Boot Assets
echo -e "\n${BOLD}[3/4] PXE & iPXE Boot Assets:${NC}"
FILES=(
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

# 4. HTTP Fetch Test
echo -e "\n${BOLD}[4/4] Local HTTP Health Test:${NC}"
if curl -s -f "http://127.0.0.1/boot.ipxe" >/dev/null 2>&1; then
    echo -e "  • http://${LAN_IP}/boot.ipxe -> ${GREEN}HTTP 200 OK${NC}"
else
    echo -e "  • http://${LAN_IP}/boot.ipxe -> ${RED}Failed to fetch${NC}"
fi

if curl -s -f "http://127.0.0.1/preseed.cfg" >/dev/null 2>&1; then
    echo -e "  • http://${LAN_IP}/preseed.cfg -> ${GREEN}HTTP 200 OK${NC}"
else
    echo -e "  • http://${LAN_IP}/preseed.cfg -> ${RED}Failed to fetch${NC}"
fi

echo -e "\n${BOLD}${CYAN}============================================================${NC}"
if [ "$ALL_FILES_OK" = true ]; then
    echo -e "${GREEN}✅ PXE Server is ready to boot new client nodes!${NC}"
    echo -e "Watching for client requests (e.g. MAC 00:25:ab:7a:0d:7e):"
    echo -e "Run: ${CYAN}journalctl -u isc-dhcp-server -f${NC} to see DHCP handshakes live."
else
    echo -e "${YELLOW}⚠️  Some files are missing. Run:${NC}"
    echo -e "  ${CYAN}sudo ./scripts/setup_pxe_server.sh debian${NC}"
fi
echo -e "${BOLD}${CYAN}============================================================${NC}\n"
