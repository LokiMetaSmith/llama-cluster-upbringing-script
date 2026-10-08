#!/usr/bin/env bash
# ==============================================================================
# join_worker.sh - Automated Provisioning & Cluster Enrollment for Edge Workers
# ==============================================================================
# This script provisions an edge node (e.g. freshly booted from custom Debian ISO)
# and seamlessly joins it into the Tailscale/Headscale mesh, Consul cluster, and
# Nomad cluster as an active worker and local cluster frontend.
#
# Usage (run from controller or operator workstation):
#   ./scripts/join_worker.sh --worker-ip 192.168.1.183 --node-id 1
#
# Flags:
#   --worker-ip <ip>      LAN IP address of the worker device (required)
#   --node-id <int>       Unique worker numeric ID (1-49, default: 1)
#   --controller-ip <ip>  LAN IP of the controller (default: detected or 192.168.1.148)
#   --user <username>     SSH user on worker (default: pipecatapp)
#   --password <pass>     SSH password for initial connection if keys not yet exchanged
# ==============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

WORKER_IP=""
NODE_ID="1"
CONTROLLER_IP=""
SSH_USER="pipecatapp"
SSH_PASS="pipecat"

show_help() {
    echo -e "${BOLD}Usage:${NC} $0 --worker-ip <IP> [options]"
    echo ""
    echo "Options:"
    echo "  --worker-ip <ip>      LAN IP address of the target worker (required)"
    echo "  --node-id <id>        Numeric worker ID (default: 1)"
    echo "  --controller-ip <ip>  LAN IP of controller (auto-detected if omitted)"
    echo "  --user <user>         SSH username (default: pipecatapp)"
    echo "  --password <pass>     SSH password (default: pipecat)"
    echo "  -h, --help            Show this message"
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --worker-ip) WORKER_IP="$2"; shift 2 ;;
        --node-id) NODE_ID="$2"; shift 2 ;;
        --controller-ip) CONTROLLER_IP="$2"; shift 2 ;;
        --user) SSH_USER="$2"; shift 2 ;;
        --password) SSH_PASS="$2"; shift 2 ;;
        -h|--help) show_help; exit 0 ;;
        *) echo -e "${RED}Unknown option: $1${NC}"; show_help; exit 1 ;;
    esac
done

if [ -z "$WORKER_IP" ]; then
    echo -e "${RED}❌ Error: --worker-ip is required.${NC}"
    show_help
    exit 1
fi

# Detect Controller IP if not passed
if [ -z "$CONTROLLER_IP" ]; then
    CONTROLLER_IP=$(ip -4 route get 8.8.8.8 2>/dev/null | grep -oP 'src \K\S+' || true)
    if [ -z "$CONTROLLER_IP" ]; then
        CONTROLLER_IP="192.168.1.148"
    fi
fi

HOSTNAME="pipecat-${NODE_ID}-worker"
UNDERLAY_IP="10.0.0.$((50 + NODE_ID))"
MESH_IP="100.64.0.$((1 + NODE_ID))"
CONTROLLER_MESH_IP="100.64.0.1"

echo -e "\n${BOLD}${CYAN}============================================================${NC}"
echo -e "${BOLD}${CYAN} 🚀 Provisioning Worker Node: ${HOSTNAME}${NC}"
echo -e "${BOLD}${CYAN}============================================================${NC}"
echo -e "Target LAN IP        : ${GREEN}${WORKER_IP}${NC}"
echo -e "Assigned Underlay IP : ${GREEN}${UNDERLAY_IP}${NC}"
echo -e "Target Mesh IP       : ${GREEN}${MESH_IP}${NC}"
echo -e "Controller LAN / Mesh: ${BLUE}${CONTROLLER_IP} / ${CONTROLLER_MESH_IP}${NC}"
echo ""

# Helper to run ssh commands on worker
remote_exec() {
    ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 "${SSH_USER}@${WORKER_IP}" "$@"
}

remote_sudo() {
    ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 "${SSH_USER}@${WORKER_IP}" "echo '${SSH_PASS}' | sudo -S bash -c '$*'"
}

# 1. Establish SSH Key Authentication
echo -e "${BOLD}[1/8] Verifying SSH connectivity...${NC}"
if ! remote_exec "echo 'Connected!'" &>/dev/null; then
    echo -e "${YELLOW}Deploying SSH public key to worker...${NC}"
    if command -v sshpass &>/dev/null; then
        sshpass -p "${SSH_PASS}" ssh-copy-id -o StrictHostKeyChecking=accept-new "${SSH_USER}@${WORKER_IP}"
    else
        echo -e "${YELLOW}Please authenticate if prompted:${NC}"
        ssh-copy-id -o StrictHostKeyChecking=accept-new "${SSH_USER}@${WORKER_IP}" || true
    fi
fi
echo -e "${GREEN}✅ SSH connectivity established.${NC}"

# 2. Hostname and Underlay Networking
echo -e "\n${BOLD}[2/8] Setting Hostname and Underlay Network...${NC}"
remote_sudo "hostnamectl set-hostname ${HOSTNAME}"
remote_sudo "grep -q '${HOSTNAME}' /etc/hosts || echo '127.0.1.1 ${HOSTNAME}' >> /etc/hosts"

# Find primary ethernet interface on worker
PRIMARY_IFACE=$(remote_exec "ip -4 route show default 2>/dev/null | awk '/default/ {print \$5}'" || echo "eno1")
echo -e "Primary Interface: ${CYAN}${PRIMARY_IFACE}${NC}"

remote_sudo "ip addr add ${UNDERLAY_IP}/24 dev ${PRIMARY_IFACE} label ${PRIMARY_IFACE}:0 2>/dev/null || true"
echo -e "${GREEN}✅ Hostname and underlay IP ${UNDERLAY_IP} set.${NC}"

# 3. Synchronize Clock (Essential to avoid GPG signature errors on Debian 13)
echo -e "\n${BOLD}[3/8] Synchronizing Hardware Clock (Chrony / NTP)...${NC}"
remote_sudo "apt-get update -qq 2>/dev/null || true; apt-get install -y -qq chrony"
remote_sudo "chronyc makestep || true; systemctl restart chrony"
echo -e "${GREEN}✅ Clock synchronized to UTC.$(NC)"

# 4. Clean Package Repositories
echo -e "\n${BOLD}[4/8] Updating Debian Package Repositories...${NC}"
remote_sudo "sed -i '/deb cdrom:/d' /etc/apt/sources.list /etc/apt/sources.list.d/* 2>/dev/null || true"
remote_sudo "cat > /etc/apt/sources.list << 'EOF'
deb http://deb.debian.org/debian/ trixie main non-free-firmware non-free contrib
deb http://security.debian.org/debian-security trixie-security main non-free-firmware non-free contrib
deb http://deb.debian.org/debian/ trixie-updates main non-free-firmware non-free contrib
EOF"
remote_sudo "apt-get update -qq"
echo -e "${GREEN}✅ Repositories upgraded to Debian 13 mirrors.${NC}"

# 5. Join Headscale Mesh Network
echo -e "\n${BOLD}[5/8] Enrolling in Tailscale / Headscale Mesh...${NC}"
# Generate a pre-auth key from Headscale on the controller
PREAUTH_KEY=""
if command -v headscale &>/dev/null; then
    PREAUTH_KEY=$(headscale --user default preauthkeys create --expiration 24h 2>/dev/null | tail -n 1 || true)
fi

if [ -z "$PREAUTH_KEY" ]; then
    PREAUTH_KEY=$(ssh -o StrictHostKeyChecking=accept-new "${SSH_USER}@${CONTROLLER_IP}" "sudo headscale --user default preauthkeys create --expiration 24h 2>/dev/null | tail -n 1" || true)
fi

remote_sudo "command -v tailscale &>/dev/null || (curl -fsSL https://tailscale.com/install.sh | sh)"
if [ -n "$PREAUTH_KEY" ]; then
    echo -e "Connecting to Headscale server: http://${CONTROLLER_IP}:8085..."
    remote_sudo "tailscale up --login-server=http://${CONTROLLER_IP}:8085 --authkey=${PREAUTH_KEY} --accept-routes --reset"
fi
echo -e "${GREEN}✅ Joined mesh network with IP: $(remote_exec "tailscale ip -4 2>/dev/null || echo 'mesh-active'")${NC}"

# 6. Synchronize Certificates and Trust Store
echo -e "\n${BOLD}[6/8] Distributing Cluster TLS Certificates...${NC}"
remote_sudo "mkdir -p /etc/consul.d /etc/nomad.d/tls /usr/local/share/ca-certificates"

# Copy Root CAs
scp -o StrictHostKeyChecking=accept-new /etc/consul.d/ca.pem "${SSH_USER}@${WORKER_IP}:/tmp/consul-ca.pem"
scp -o StrictHostKeyChecking=accept-new /etc/nomad.d/tls/ca.pem "${SSH_USER}@${WORKER_IP}:/tmp/nomad-ca.pem"
remote_sudo "cp /tmp/consul-ca.pem /etc/consul.d/ca.pem && cp /tmp/nomad-ca.pem /etc/nomad.d/tls/ca.pem"
remote_sudo "cp /tmp/nomad-ca.pem /usr/local/share/ca-certificates/nomad-ca.crt && update-ca-certificates"

# Copy Client Certs
scp -o StrictHostKeyChecking=accept-new /etc/nomad.d/tls/cli.cert.pem "${SSH_USER}@${WORKER_IP}:/tmp/cli.cert.pem"
scp -o StrictHostKeyChecking=accept-new /etc/nomad.d/tls/cli.key.pem "${SSH_USER}@${WORKER_IP}:/tmp/cli.key.pem"
scp -o StrictHostKeyChecking=accept-new /etc/nomad.d/tls/cert.pem "${SSH_USER}@${WORKER_IP}:/tmp/node.cert.pem"
scp -o StrictHostKeyChecking=accept-new /etc/nomad.d/tls/key.pem "${SSH_USER}@${WORKER_IP}:/tmp/node.key.pem"
remote_sudo "cp /tmp/cli.cert.pem /etc/nomad.d/tls/cli.cert.pem && cp /tmp/cli.key.pem /etc/nomad.d/tls/cli.key.pem && chmod 644 /etc/nomad.d/tls/cli.key.pem"
remote_sudo "cp /tmp/node.cert.pem /etc/nomad.d/tls/cert.pem && cp /tmp/node.key.pem /etc/nomad.d/tls/key.pem && chmod 600 /etc/nomad.d/tls/key.pem"
echo -e "${GREEN}✅ Mutual TLS cryptographic infrastructure established.${NC}"

# 7. Configure and Start Consul & Nomad Clients
echo -e "\n${BOLD}[7/8] Configuring and Launching Consul and Nomad Clients...${NC}"
CONSUL_TOKEN="f6976354-9daa-251e-ef81-5fadb26f4fb5"

remote_sudo "cat > /etc/consul.d/consul.hcl << 'EOF'
datacenter = \"dc1\"
data_dir   = \"/opt/consul\"
server     = false

addresses {
  http = \"0.0.0.0\"
}

bind_addr = \"0.0.0.0\"
advertise_addr = \"${MESH_IP}\"

retry_join = [\"${CONTROLLER_MESH_IP}\"]

ports {
  http  = 8500
  https = 8501
  grpc  = 8502
  dns   = 8600
}

acl {
  enabled                  = true
  default_policy           = \"deny\"
  enable_token_persistence = true
  tokens {
    initial_management = \"${CONSUL_TOKEN}\"
    default            = \"${CONSUL_TOKEN}\"
    agent              = \"${CONSUL_TOKEN}\"
  }
}
EOF"

remote_sudo "mkdir -p /opt/consul /opt/nomad && chown -R consul:consul /opt/consul /etc/consul.d 2>/dev/null || true"
remote_sudo "systemctl restart consul"

# Configure Nomad Client
remote_sudo "cat > /etc/nomad.d/client.hcl << 'EOF'
data_dir  = \"/opt/nomad\"
bind_addr = \"0.0.0.0\"

addresses {
  http = \"0.0.0.0\"
  rpc  = \"${MESH_IP}\"
  serf = \"${MESH_IP}\"
}

advertise {
  http = \"${MESH_IP}\"
  rpc  = \"${MESH_IP}\"
  serf = \"${MESH_IP}\"
}

client {
  enabled = true
  servers = [\"${CONTROLLER_MESH_IP}\"]

  meta {
    node_type = \"worker\"
  }

  host_volume \"pipecatapp\" {
    path      = \"/opt/pipecatapp\"
    read_only = false
  }

  host_volume \"models\" {
    path      = \"/opt/unified_fs_backend/models\"
    read_only = true
  }

  host_volume \"unified_fs\" {
    path      = \"/opt/unified_fs_backend\"
    read_only = false
  }

  host_volume \"ipfs\" {
    path      = \"/opt/unified_fs_backend/ipfs\"
    read_only = false
  }

  host_volume \"nomad_tls\" {
    path      = \"/etc/nomad.d/tls\"
    read_only = true
  }
}

consul {
  address = \"127.0.0.1:8500\"
  token   = \"${CONSUL_TOKEN}\"
}

plugin \"docker\" {
  config {
    endpoint = \"unix:///var/run/docker.sock\"
    volumes {
      enabled = true
    }
  }
}

plugin \"raw_exec\" {
  config {
    enabled = true
  }
}

tls {
  http = true
  rpc  = true

  ca_file   = \"/etc/nomad.d/tls/ca.pem\"
  cert_file = \"/etc/nomad.d/tls/cert.pem\"
  key_file  = \"/etc/nomad.d/tls/key.pem\"

  verify_server_hostname = true
  verify_https_client    = true
}
EOF"

remote_sudo "systemctl restart nomad"

# Nomad CLI profile
remote_sudo "cat > /etc/profile.d/nomad.sh << 'EOF'
#!/bin/sh
export NOMAD_ADDR=\"https://${CONTROLLER_MESH_IP}:4646\"
export NOMAD_CACERT=\"/etc/nomad.d/tls/ca.pem\"
export NOMAD_CLIENT_CERT=\"/etc/nomad.d/tls/cli.cert.pem\"
export NOMAD_CLIENT_KEY=\"/etc/nomad.d/tls/cli.key.pem\"
EOF
chmod +x /etc/profile.d/nomad.sh"

echo -e "${GREEN}✅ Consul & Nomad clients running and joined to cluster.${NC}"

# 8. Synchronize Codebase & Verify
echo -e "\n${BOLD}[8/8] Synchronizing Codebase and Runtime...${NC}"
remote_sudo "mkdir -p /opt/pipecat-cluster /opt/pipecatapp /opt/unified_fs_backend/models /opt/unified_fs_backend/ipfs"
remote_sudo "chown -R ${SSH_USER}:${SSH_USER} /opt/pipecatapp /opt/pipecat-cluster"

echo -e "\n${BOLD}${GREEN}============================================================${NC}"
echo -e "${BOLD}${GREEN} 🎉 Worker Node ${HOSTNAME} Successfully Enrolled!${NC}"
echo -e "${BOLD}${GREEN}============================================================${NC}"
echo -e "Consul Membership:"
consul members -token="${CONSUL_TOKEN}" | grep -E "Node|${HOSTNAME}" || true
echo ""
echo -e "Nomad Nodes:"
NOMAD_ADDR="https://${CONTROLLER_MESH_IP}:4646" NOMAD_CACERT="/etc/nomad.d/tls/ca.pem" NOMAD_CLIENT_CERT="/etc/nomad.d/tls/cli.cert.pem" NOMAD_CLIENT_KEY="/etc/nomad.d/tls/cli.key.pem" nomad node status || true
echo ""
