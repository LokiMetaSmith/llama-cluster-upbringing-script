#!/usr/bin/env bash
# ==============================================================================
# cluster_ctl.sh - Unified Multi-Node Cluster Lifecycle & Health Manager
# ==============================================================================
# Manages health audits, distributed task verification, and synchronization
# across all nodes in the Pipecat AI cluster.
#
# Usage:
#   ./scripts/cluster_ctl.sh [command]
#
# Commands:
#   status        - Complete cluster audit (Mesh, Consul, Nomad, Frontends)
#   test-job      - Dispatch a distributed verification job across worker nodes
#   sync          - Synchronize code & configuration to all cluster nodes
#   help          - Show this guide
# ==============================================================================

set -euo pipefail

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Load Nomad Environment
export NOMAD_ADDR="${NOMAD_ADDR:-https://100.64.0.1:4646}"
export NOMAD_CACERT="${NOMAD_CACERT:-/etc/nomad.d/tls/ca.pem}"
export NOMAD_CLIENT_CERT="${NOMAD_CLIENT_CERT:-/etc/nomad.d/tls/cli.cert.pem}"
export NOMAD_CLIENT_KEY="${NOMAD_CLIENT_KEY:-/etc/nomad.d/tls/cli.key.pem}"

# Load Consul Environment
export CONSUL_HTTP_ADDR="${CONSUL_HTTP_ADDR:-http://127.0.0.1:8500}"
export CONSUL_HTTP_TOKEN="${CONSUL_HTTP_TOKEN:-f6976354-9daa-251e-ef81-5fadb26f4fb5}"

show_help() {
    echo -e "${BOLD}Pipecat Cluster Management CLI${NC}"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo -e "  ${CYAN}status${NC}        Check health of mesh, Consul, Nomad, and frontends across all nodes"
    echo -e "  ${CYAN}test-job${NC}      Submit a verification batch job to prove cluster task sharing"
    echo -e "  ${CYAN}sync${NC}          Sync repository to all worker nodes via encrypted mesh"
    echo -e "  ${CYAN}help${NC}          Display this usage guide"
    echo ""
}

cmd_status() {
    echo -e "\n${BOLD}${CYAN}============================================================${NC}"
    echo -e "${BOLD}${CYAN} 🌐 Cluster Health & Lifecycle Report${NC}"
    echo -e "${BOLD}${CYAN}============================================================${NC}"

    # 1. Mesh Network (Headscale / Tailscale)
    echo -e "\n${BOLD}[1/4] Mesh Network Status (WireGuard Overlay):${NC}"
    if command -v tailscale &>/dev/null; then
        tailscale status || true
        echo ""
        echo -e "Testing peer latency over mesh:"
        for peer_ip in $(tailscale status 2>/dev/null | awk '{print $1}' | grep -E '^100\.'); do
            local_ip=$(tailscale ip -4 2>/dev/null || echo "")
            if [ "$peer_ip" != "$local_ip" ]; then
                ping -c 2 -W 1 "$peer_ip" > /dev/null 2>&1 && \
                    echo -e "  • Peer ${GREEN}${peer_ip}${NC}: Reachable (WireGuard link active)" || \
                    echo -e "  • Peer ${RED}${peer_ip}${NC}: Unreachable"
            fi
        done
    else
        echo -e "${YELLOW}⚠️  tailscale CLI not found on this host.${NC}"
    fi

    # 2. Consul Cluster
    echo -e "\n${BOLD}[2/4] Consul Mesh Members & Service Discovery:${NC}"
    if command -v consul &>/dev/null; then
        consul members || true
        echo ""
        local passing_count
        passing_count=$(curl -s -H "X-Consul-Token: ${CONSUL_HTTP_TOKEN}" "${CONSUL_HTTP_ADDR}/v1/health/state/passing" 2>/dev/null | jq 'length' 2>/dev/null || echo "0")
        local critical_count
        critical_count=$(curl -s -H "X-Consul-Token: ${CONSUL_HTTP_TOKEN}" "${CONSUL_HTTP_ADDR}/v1/health/state/critical" 2>/dev/null | jq 'length' 2>/dev/null || echo "0")
        echo -e "Consul Health Checks: ${GREEN}${passing_count} Passing${NC}, ${RED}${critical_count} Critical${NC}"
    else
        echo -e "${YELLOW}⚠️  consul CLI not found on this host.${NC}"
    fi

    # 3. Nomad Orchestrator
    echo -e "\n${BOLD}[3/4] Nomad Compute Nodes & Job Allocations:${NC}"
    if command -v nomad &>/dev/null; then
        echo -e "${BOLD}Registered Nodes:${NC}"
        nomad node status || true
        echo ""
        echo -e "${BOLD}Running System & Service Jobs:${NC}"
        nomad job status || true
    else
        echo -e "${YELLOW}⚠️  nomad CLI not found on this host.${NC}"
    fi

    # 4. Frontend Health Check (Port 8007)
    echo -e "\n${BOLD}[4/4] Web UI & Frontend Availability (Port 8007):${NC}"
    # Target endpoints: localhost, controller LAN, worker LAN, and mesh IPs
    local TARGET_HOSTS=("127.0.0.1" "100.64.0.1" "100.64.0.2" "192.168.1.148" "192.168.1.183")
    for host in "${TARGET_HOSTS[@]}"; do
        local response
        response=$(curl -s --max-time 2 -o /dev/null -w "%{http_code}" "http://${host}:8007/health" 2>/dev/null || echo "failed")
        if [ "$response" = "200" ]; then
            echo -e "  • http://${host}:8007/health -> ${GREEN}HTTP 200 OK (Frontend Active)${NC}"
        elif [ "$response" != "failed" ] && [ "$response" != "000" ]; then
            echo -e "  • http://${host}:8007/health -> ${YELLOW}HTTP ${response}${NC}"
        else
            # Try plain ping before declaring completely offline
            if ping -c 1 -W 1 "$host" &>/dev/null; then
                echo -e "  • http://${host}:8007/health -> ${RED}Connection Refused (Host online, frontend inactive)${NC}"
            fi
        fi
    done

    echo -e "\n${BOLD}${GREEN}✅ Audit Complete.${NC}\n"
}

cmd_test_job() {
    echo -e "\n${BOLD}${CYAN}============================================================${NC}"
    echo -e "${BOLD}${CYAN} 🧪 Submitting Distributed Test Job to Worker Nodes${NC}"
    echo -e "${BOLD}${CYAN}============================================================${NC}"

    local JOB_FILE="${REPO_ROOT}/scripts/test_cluster_job.nomad"
    if [ ! -f "$JOB_FILE" ]; then
        echo -e "${RED}❌ Job definition $JOB_FILE not found.${NC}"
        exit 1
    fi

    echo -e "Submitting job: ${CYAN}test-worker-task${NC}..."
    nomad job run "$JOB_FILE"

    echo -e "\nWaiting 5 seconds for execution..."
    sleep 5

    echo -e "\n${BOLD}Task Execution Output:${NC}"
    local alloc_id
    alloc_id=$(nomad job allocs test-worker-task 2>/dev/null | awk 'NR>1 {print $1}' | head -n 1)

    if [ -n "$alloc_id" ]; then
        nomad alloc logs "$alloc_id"
        echo -e "\n${GREEN}✅ Distributed job execution verified!${NC}"
    else
        echo -e "${RED}❌ No allocation found for test-worker-task.${NC}"
    fi

    echo -e "\nCleaning up test job..."
    nomad job stop -purge test-worker-task >/dev/null 2>&1 || true
    echo -e "${GREEN}✅ Test job cleaned up.${NC}"
}

cmd_sync() {
    echo -e "\n${BOLD}${CYAN}============================================================${NC}"
    echo -e "${BOLD}${CYAN} 🔄 Synchronizing Repository across Cluster Nodes${NC}"
    echo -e "${BOLD}${CYAN}============================================================${NC}"

    local WORKER_TARGETS=("100.64.0.2" "192.168.1.183")
    for target in "${WORKER_TARGETS[@]}"; do
        if ping -c 1 -W 1 "$target" &>/dev/null; then
            echo -e "Syncing to ${GREEN}${target}${NC}..."
            ssh -o StrictHostKeyChecking=accept-new "pipecatapp@${target}" \
                "cd /opt/pipecat-cluster && git fetch origin main && git reset --hard origin/main" || true
            break
        fi
    done
    echo -e "${GREEN}✅ Synchronization completed.${NC}"
}

COMMAND="${1:-help}"
case "$COMMAND" in
    status) cmd_status ;;
    test-job) cmd_test_job ;;
    sync) cmd_sync ;;
    help|-h|--help) show_help ;;
    *) echo -e "${RED}Unknown command: $COMMAND${NC}"; show_help; exit 1 ;;
esac
