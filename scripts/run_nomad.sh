#!/bin/bash
# Nomad Job Submission Script
#
# This script provides a simple interface to deploy Nomad job files
# without requiring Ansible playbooks.
#
# Usage:
#   ./run_nomad.sh <command> <job-file> [options]
#
# Commands:
#   run     - Deploy a job
#   plan   - Dry-run validation
#   status - Show job status
#   stop   - Stop and remove a job
#   status - Show all jobs
#
# Examples:
#   ./run_nomad.sh run ansible/jobs/redis.nomad
#   ./run_nomad.sh plan ansible/jobs/postgres.nomad
#   ./run_nomad.sh status
#   ./run_nomad.sh stop redis

set -e

NOMAD_HOST="${NOMAD_HOST:-127.0.0.1}"
NOMAD_PORT="${NOMAD_PORT:-4646}"
NOMAD_ADDR="http://${NOMAD_HOST}:${NOMAD_PORT}"
NOMAD_CERT="${NOMAD_CERT:-}"
NOMAD_TOKEN="${NOMAD_TOKEN:-}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Usage function
usage() {
    echo "Nomad Job Submission Script"
    echo ""
    echo "Usage: $0 <command> <job-file> [options]"
    echo ""
    echo "Commands:"
    echo "  run <file>    Deploy a job (or -plan for dry-run)"
    echo "  plan <file>   Dry-run validation"
    echo "  status [job]  Show job status"
    echo "  stop <job>    Stop and purge a job"
    echo "  list          List all jobs"
    echo ""
    echo "Options:"
    echo "  -h, --host HOST    Nomad host (default: ${NOMAD_HOST})"
    echo "  -p, --port PORT    Nomad port (default: ${NOMAD_PORT})"
    echo "  -t, --token TOKEN  ACL token"
    echo ""
    echo "Examples:"
    echo "  $0 run ansible/jobs/redis.nomad"
    echo "  $0 plan ansible/jobs/postgres.nomad"
    echo "  $0 status redis"
    echo "  $0 stop postgres"
    echo "  $0 list"
    exit 1
}

# Build nomad command with options
nomad_cmd() {
    local cmd="nomad"

    if [[ -n "$NOMAD_CERT" ]]; then
        cmd="$cmd -tls-cert=$NOMAD_CERT"
    fi

    if [[ -n "$NOMAD_TOKEN" ]]; then
        cmd="$cmd -token=$NOMAD_TOKEN"
    fi

    echo "$cmd"
}

# Run a job
run_job() {
    local job_file="$1"
    local dry_run="${2:-false}"

    if [[ ! -f "$job_file" ]]; then
        echo -e "${RED}Error: Job file not found: $job_file${NC}" >&2
        exit 1
    fi

    local cmd=( "$(nomad_cmd)" job "$job_file" )

    if [[ "$dry_run" == "true" ]]; then
        echo -e "${YELLOW}Planning job...${NC}"
        "${cmd[@]}" plan
    else
        echo -e "${YELLOW}Running job...${NC}"
        "${cmd[@]}" run -detach
    fi
}

# Show job status
show_status() {
    local job_name="${1:-}"
    local cmd=$(nomad_cmd)

    if [[ -n "$job_name" ]]; then
        $cmd job status "$job_name"
    else
        $cmd job status
    fi
}

# Stop a job
stop_job() {
    local job_name="$1"
    local cmd=$(nomad_cmd)

    echo -e "${YELLOW}Stopping job $job_name...${NC}"
    $cmd job stop -purge "$job_name"
}

# List jobs
list_jobs() {
    local cmd=$(nomad_cmd)
    $cmd job status
}

# Main
main() {
    local command="${1:-}"
    shift || usage

    case "$command" in
        run)
            local job_file="${1:-}"
            shift || usage
            run_job "$job_file" "false"
            ;;
        plan)
            local job_file="${1:-}"
            shift || usage
            run_job "$job_file" "true"
            ;;
        status)
            local job_name="${1:-}"
            show_status "$job_name"
            ;;
        stop)
            local job_name="${1:-}"
            [[ -z "$job_name" ]] && usage
            stop_job "$job_name"
            ;;
        list)
            list_jobs
            ;;
        -h|--help|help)
            usage
            ;;
        *)
            echo -e "${RED}Unknown command: $command${NC}" >&2
            usage
            ;;
    esac
}

main "$@"