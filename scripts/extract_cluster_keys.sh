#!/usr/bin/env bash
# ==============================================================================
# extract_cluster_keys.sh - Deterministic Cluster Credential Bundle Extractor
# ==============================================================================
# Extracts all cryptographic infrastructure (mTLS Root CAs, client certificates,
# Consul ACL tokens, Headscale preauth keys, and authorized SSH keys) from the
# cluster controller and packages them into a staging directory for ISO burning
# or USB FAT32 CONFIGS injection.
#
# Usage (run directly on controller or from remote operator machine):
#   ./scripts/extract_cluster_keys.sh --output /path/to/staging_dir
#
# Flags:
#   -o, --output <dir>       Target output directory (default: ./cluster_keys_bundle)
#   -c, --controller <host>  Controller SSH host if running remotely (default: localhost)
#   --expiration <duration>  Expiration for reusable Headscale key (default: 720h / 30d)
#   --user <ssh_user>        SSH user for remote controller access (default: pipecatapp)
# ==============================================================================

set -euo pipefail

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

OUTPUT_DIR="${REPO_ROOT}/cluster_keys_bundle"
CONTROLLER_HOST="localhost"
KEY_EXPIRATION="720h"
SSH_USER="pipecatapp"

show_help() {
    echo -e "${BOLD}Usage:${NC} $0 [options]"
    echo ""
    echo "Options:"
    echo "  -o, --output <dir>       Target directory for extracted credentials (default: ./cluster_keys_bundle)"
    echo "  -c, --controller <host>  Controller SSH host/IP (default: localhost)"
    echo "  --expiration <duration>  Headscale pre-auth key expiration (default: 720h)"
    echo "  --user <user>            SSH user if accessing controller remotely (default: pipecatapp)"
    echo "  -h, --help               Show this guide"
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -o|--output) OUTPUT_DIR="$2"; shift 2 ;;
        -c|--controller) CONTROLLER_HOST="$2"; shift 2 ;;
        --expiration) KEY_EXPIRATION="$2"; shift 2 ;;
        --user) SSH_USER="$2"; shift 2 ;;
        -h|--help) show_help; exit 0 ;;
        *) echo -e "${RED}Unknown argument: $1${NC}"; show_help; exit 1 ;;
    esac
done

echo -e "\n${BOLD}${CYAN}============================================================${NC}"
echo -e "${BOLD}${CYAN} 🔑 Pipecat Cluster Credential Extractor${NC}"
echo -e "${BOLD}${CYAN}============================================================${NC}"
echo -e "Output Directory : ${GREEN}${OUTPUT_DIR}${NC}"
echo -e "Controller Target: ${BLUE}${CONTROLLER_HOST}${NC}"
echo ""

mkdir -p "${OUTPUT_DIR}"
chmod 700 "${OUTPUT_DIR}"

exec_controller() {
    if [ "$CONTROLLER_HOST" = "localhost" ] || [ "$CONTROLLER_HOST" = "127.0.0.1" ]; then
        if [ "$(id -u)" -eq 0 ]; then
            bash -c "$*"
        else
            sudo bash -c "$*"
        fi
    else
        ssh -o StrictHostKeyChecking=accept-new "${SSH_USER}@${CONTROLLER_HOST}" "sudo bash -c '$*'"
    fi
}

copy_from_controller() {
    local src="$1"
    local dest="$2"
    if [ "$CONTROLLER_HOST" = "localhost" ] || [ "$CONTROLLER_HOST" = "127.0.0.1" ]; then
        if [ "$(id -u)" -eq 0 ]; then
            cp "$src" "$dest"
        else
            sudo cp "$src" "$dest"
            sudo chown "$(id -u):$(id -g)" "$dest"
        fi
    else
        ssh -o StrictHostKeyChecking=accept-new "${SSH_USER}@${CONTROLLER_HOST}" "sudo cat '$src'" > "$dest"
    fi
}

# 1. Determine Controller IP
echo -e "${BOLD}[1/6] Determining Controller IP & Headscale Endpoint...${NC}"
if [ "$CONTROLLER_HOST" = "localhost" ] || [ "$CONTROLLER_HOST" = "127.0.0.1" ]; then
    CONTROLLER_IP=$(ip -4 route get 8.8.8.8 2>/dev/null | grep -oP 'src \K\S+' || echo "192.168.1.148")
else
    CONTROLLER_IP="$CONTROLLER_HOST"
fi
echo "$CONTROLLER_IP" > "${OUTPUT_DIR}/controller_ip"
echo "http://${CONTROLLER_IP}:8085" > "${OUTPUT_DIR}/headscale_url"
echo -e "  • Controller IP: ${GREEN}${CONTROLLER_IP}${NC}"
echo -e "  • Headscale URL: ${GREEN}http://${CONTROLLER_IP}:8085${NC}"

# 2. Extract Headscale Mesh Pre-Auth Key
echo -e "\n${BOLD}[2/6] Generating Reusable Headscale Pre-Auth Key...${NC}"
AUTH_KEY=$(exec_controller "headscale --user default preauthkeys create --reusable --expiration ${KEY_EXPIRATION} 2>/dev/null | tail -n 1")
if [ -z "$AUTH_KEY" ]; then
    echo -e "${RED}❌ Failed to generate Headscale pre-auth key.${NC}"
    exit 1
fi
echo "$AUTH_KEY" > "${OUTPUT_DIR}/mesh_auth_key"
chmod 600 "${OUTPUT_DIR}/mesh_auth_key"
echo -e "  • Key: ${GREEN}${AUTH_KEY:0:8}...${AUTH_KEY: -8}${NC} (valid for ${KEY_EXPIRATION})"

# 3. Extract Nomad Mutual TLS Certificates & Root CA
echo -e "\n${BOLD}[3/6] Extracting Nomad mTLS Certificates...${NC}"
copy_from_controller "/etc/nomad.d/tls/ca.pem" "${OUTPUT_DIR}/nomad_ca.pem"
copy_from_controller "/etc/nomad.d/tls/cli.cert.pem" "${OUTPUT_DIR}/nomad_cli.cert.pem"
copy_from_controller "/etc/nomad.d/tls/cli.key.pem" "${OUTPUT_DIR}/nomad_cli.key.pem"
copy_from_controller "/etc/nomad.d/tls/cert.pem" "${OUTPUT_DIR}/nomad_node.cert.pem"
copy_from_controller "/etc/nomad.d/tls/key.pem" "${OUTPUT_DIR}/nomad_node.key.pem"
chmod 644 "${OUTPUT_DIR}/nomad_ca.pem" "${OUTPUT_DIR}/nomad_cli.cert.pem" "${OUTPUT_DIR}/nomad_node.cert.pem"
chmod 600 "${OUTPUT_DIR}/nomad_cli.key.pem" "${OUTPUT_DIR}/nomad_node.key.pem"
echo -e "  • Extracted: ${GREEN}nomad_ca.pem, nomad_cli.cert.pem, nomad_cli.key.pem, nomad_node.cert.pem, nomad_node.key.pem${NC}"

# 4. Extract Consul Root CA & ACL Management Token
echo -e "\n${BOLD}[4/6] Extracting Consul CA & ACL Token...${NC}"
copy_from_controller "/etc/consul.d/ca.pem" "${OUTPUT_DIR}/consul_ca.pem"
chmod 644 "${OUTPUT_DIR}/consul_ca.pem"

CONSUL_TOKEN=$(exec_controller "grep -oP 'CONSUL_HTTP_TOKEN=\K\S+' /etc/consul.d/consul.env 2>/dev/null || grep -oP 'consul_bootstrap_token:\s*\"\K[^\"]+' /opt/pipecat-cluster/group_vars/all.yaml 2>/dev/null || echo 'f6976354-9daa-251e-ef81-5fadb26f4fb5'")
echo "$CONSUL_TOKEN" > "${OUTPUT_DIR}/consul_token"
chmod 600 "${OUTPUT_DIR}/consul_token"
echo -e "  • Extracted: ${GREEN}consul_ca.pem, consul_token${NC}"

# 5. Collect Operator Authorized SSH Keys
echo -e "\n${BOLD}[5/6] Bundling Authorized SSH Public Keys...${NC}"
> "${OUTPUT_DIR}/authorized_keys"
# Gather controller's authorized keys
if [ "$CONTROLLER_HOST" = "localhost" ] || [ "$CONTROLLER_HOST" = "127.0.0.1" ]; then
    cat ~/.ssh/authorized_keys 2>/dev/null >> "${OUTPUT_DIR}/authorized_keys" || true
else
    ssh -o StrictHostKeyChecking=accept-new "${SSH_USER}@${CONTROLLER_HOST}" "cat ~/.ssh/authorized_keys 2>/dev/null || true" >> "${OUTPUT_DIR}/authorized_keys"
fi
# Also gather local user's public keys if present
for pub in ~/.ssh/*.pub; do
    if [ -f "$pub" ]; then
        cat "$pub" >> "${OUTPUT_DIR}/authorized_keys"
        echo "" >> "${OUTPUT_DIR}/authorized_keys"
    fi
done
# Deduplicate lines
sort -u "${OUTPUT_DIR}/authorized_keys" -o "${OUTPUT_DIR}/authorized_keys"
chmod 600 "${OUTPUT_DIR}/authorized_keys"
echo -e "  • Collected $(wc -l < "${OUTPUT_DIR}/authorized_keys") authorized public key(s)."

# 6. Verify Bundle Integrity
echo -e "\n${BOLD}[6/6] Verifying Bundle Integrity...${NC}"
REQUIRED_FILES=(
    "controller_ip"
    "headscale_url"
    "mesh_auth_key"
    "nomad_ca.pem"
    "nomad_cli.cert.pem"
    "nomad_cli.key.pem"
    "nomad_node.cert.pem"
    "nomad_node.key.pem"
    "consul_ca.pem"
    "consul_token"
    "authorized_keys"
)

MISSING=0
for req in "${REQUIRED_FILES[@]}"; do
    if [ ! -s "${OUTPUT_DIR}/${req}" ]; then
        echo -e "  ❌ Missing or empty required file: ${RED}${req}${NC}"
        MISSING=$((MISSING + 1))
    else
        echo -e "  ✅ Validated: ${GREEN}${req}${NC} ($(stat -c%s "${OUTPUT_DIR}/${req}" 2>/dev/null || stat -f%z "${OUTPUT_DIR}/${req}") bytes)"
    fi
done

if [ "$MISSING" -gt 0 ]; then
    echo -e "\n${RED}Bundle verification failed with ${MISSING} missing item(s).${NC}"
    exit 1
fi

echo -e "\n${BOLD}${GREEN}============================================================${NC}"
echo -e "${BOLD}${GREEN} 🎉 Cluster Credential Bundle Generated Successfully!${NC}"
echo -e "${BOLD}${GREEN}============================================================${NC}"
echo -e "Directory: ${BOLD}${OUTPUT_DIR}${NC}"
echo ""
echo "Next Steps to Burn or Inject onto an ISO / USB:"
echo ""
echo "  Option A (Inject into FAT32 CONFIGS partition on bootable USB):"
echo "    cd os-image && sudo ./build_iso.sh --flash --inject \"${OUTPUT_DIR}\""
echo ""
echo "  Option B (Pre-bundle directly into custom bootable ISO):"
echo "    cd os-image && sudo ./build_iso.sh --keys-bundle \"${OUTPUT_DIR}\""
echo ""
