#!/bin/bash
#
# Easy Bootstrap Script for Single-Node Setup
#
# This script simplifies the process of bootstrapping the system on a single
# server for development or as the initial control node for a new cluster.
# It runs the main Ansible playbook using a local inventory file.

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# --- Help Menu ---
show_help() {
    echo "Usage: $0 [options]"
    echo ""
    echo "This script runs the main Ansible playbook to bootstrap the system."
    echo ""
    echo "Options:"
    echo "  --role <role>                Specify the role for this node (all, controller, worker). Default: all."
    echo "  --controller-ip <ip>         Required if --role is 'worker'. IP address of the controller node."
    echo "  --tags <tags>                Comma-separated list of Ansible tags to run."
    echo "  --user <user>                Specify the target user for Ansible. Default: pipecatapp."
    echo "  --github-ssh-user <user>     Specify a GitHub username to import SSH keys for. Can be used multiple times."
    echo "  --purge-jobs                 Stop and purge all running Nomad jobs."
    echo "  --clean-git                  Clean the repository of all untracked files (interactive prompt)."
    echo "  --system-cleanup             Perform a full system cleanup (Purge Jobs, Clean System, Clean Git), with interactive prompts."
    echo "  --verbose [level]            Set verbosity level (0-4). Default 0, or 3 if flag is used without value."
    echo "  --debug                      Alias for --verbose 4."
    echo "  --leave-services-running     Do not clean up Nomad and Consul data on startup."
    echo "  --external-model-server      Skip large model downloads and builds, assuming an external server."
    echo "  --tier <tier>                Specify the node tier (edge, mid, core). Default: mid."
    echo "  --deploy-full-stack          Deploy the full application stack (AI agents, models) instead of just infrastructure."
    echo "  --deploy-partial-stack       Deploy a partial application stack (e.g. 4-8B models) for mid-tier worker nodes."
    echo "  --deploy-minimal-stack       Deploy a minimal application stack (e.g. audio, kiosk, status) for low resource nodes."
    echo "  --continue                   Resume from the last successfully completed playbook."
    echo "  --benchmark                  Run benchmark tests."
    echo "  --deploy-docker              Deploy the pipecat application using Docker (Default)."
    echo "  --run-local                  Deploy the pipecat application using local raw_exec (for debugging)."
    echo "  --home-assistant-debug       Enable debug mode for Home Assistant."
    echo "  --container                  Run the entire infrastructure inside a single large container."
    echo "  --watch <target>             Pause for inspection after the specified target (task/role) completes."
    echo "  -h, --help                   Display this help message and exit."
    echo ""
    echo "OpenCode Autonomous Recovery Options:"
    echo "  If the script crashes, it will attempt to use an OpenCode AI agent to diagnose and fix the error."
    echo "  These can also be set via environment variables (AGENT_API_BASE, AGENT_MODEL, AGENT_API_KEY)."
    echo "  --agent-api-base <url>       URL for a custom LLM provider, like a local Ollama instance (e.g. http://192.168.1.100:11434/v1)."
    echo "  --agent-model <model>        The LLM model to use for debugging (e.g. qwen3:14b, llama3.2:3b, mistral, qwen2.5:1.5b)."
    echo "  --agent-api-key <key>        API key for the model provider (a dummy key like 'sk-dummy' can be used for Ollama)."
}

# --- Initialize flags ---
USE_CONTAINER=false
DO_CLEAN_GIT=false
DO_SYSTEM_CLEANUP=false
DO_PURGE_JOBS=false
DO_STATUS=false
VERBOSE_LEVEL=0
ROLE=""
CONTROLLER_IP=""
CLI_AGENT_API_BASE=""
CLI_AGENT_MODEL=""
CLI_AGENT_API_KEY=""

# --- Network Discovery ---
find_controller() {
    echo -e "\n${BOLD}=== Network Discovery ===${NC}"
    echo -e "Searching for an existing controller on the network..."

    # 1. Provisioning Underlay
    local PXE_SUBNET
    PXE_SUBNET=$(grep -oP '^pxe_subnet:\s*"\K[^"]+' group_vars/all.yaml 2>/dev/null || echo "10.0.0.0")
    if [[ ! "$PXE_SUBNET" == */* ]]; then
        PXE_SUBNET="${PXE_SUBNET}/24"
    fi

    # 2. Cluster Overlay
    local OVERLAY_SUBNET
    OVERLAY_SUBNET=$(grep -oP '^overlay_subnet:\s*"\K[^"]+' group_vars/all.yaml 2>/dev/null || echo "100.64.0.0/10")

    # 3. Local Host Network / Fallback
    local LOCAL_SUBNET
    LOCAL_SUBNET=$(ip route show default | awk '/default/ {print $3}' | awk -F. '{print $1"."$2"."$3".0/24"}' 2>/dev/null || echo "192.168.1.0/24")

    # Install nmap if missing
    if ! command -v nmap >/dev/null 2>&1; then
        echo -e "⏳ Installing nmap for network scanning..."
        if sudo -n true 2>/dev/null; then
            sudo apt-get update -qq && sudo apt-get install -y nmap -qq >/dev/null 2>&1
        else
            echo -e "${YELLOW}⚠️  Requires nmap. You may be prompted for your sudo password to install it.${NC}"
            sudo apt-get update -qq && sudo apt-get install -y nmap -qq >/dev/null 2>&1
        fi
    fi

    local SCAN_RESULTS=""

    # Add a fast-path scan for the first /24 block of the overlay to save time
    local OVERLAY_FAST_PATH="100.64.0.0/24"
    # Only add OVERLAY_FAST_PATH to array if it is different from OVERLAY_SUBNET to avoid scanning same thing twice
    local SUBNETS_TO_SCAN=("$PXE_SUBNET" "$LOCAL_SUBNET" "$OVERLAY_FAST_PATH")
    if [ "$OVERLAY_SUBNET" != "$OVERLAY_FAST_PATH" ]; then
        SUBNETS_TO_SCAN+=("$OVERLAY_SUBNET")
    fi

    spinner() {
        local pid=$1
        local delay=0.1
        local spinstr="|\/-\\"
        while kill -0 "$pid" 2>/dev/null; do
            local temp=${spinstr#?}
            printf " [%c]  " "$spinstr"
            local spinstr=$temp${spinstr%"$temp"}
            sleep $delay
            printf ""
        done
        printf "    "
    }

    echo -e "Scanning networks on port 4646 (Nomad):"

    for subnet in "${SUBNETS_TO_SCAN[@]}"; do
        echo -n -e "  - ${CYAN}${subnet}${NC}... "

        # Fast scan for /10 overlay limits max-retries and timeout aggressively
        # shellcheck disable=SC2086
        local nmap_args="-n -p 4646 --open -T5 --max-retries 1 --host-timeout 500ms --min-rate 10000"

        local tmp_file
        tmp_file=$(mktemp)

        # Run nmap in the background so we can show a spinner
        # shellcheck disable=SC2086
        nmap $nmap_args -oG - "$subnet" > "$tmp_file" 2>/dev/null &
        local nmap_pid=$!

        # Ensure we kill the background process and delete temp file if interrupted
        # Note: escaping the command text for the python replacement
        trap 'kill $nmap_pid 2>/dev/null; rm -f "$tmp_file"; exit 1' INT TERM

        spinner "$nmap_pid"

        # Reset trap back to script default
        trap - INT TERM

        SCAN_RESULTS=$(awk '/4646\/open/ {print $2}' "$tmp_file" 2>/dev/null)
        rm -f "$tmp_file"

        if [ -n "$SCAN_RESULTS" ]; then
            echo -e "\r  - ${CYAN}${subnet}${NC}... Done.          "
            CONTROLLER_IP=$(echo "$SCAN_RESULTS" | head -n 1)
            echo -e "${GREEN}✅ Found controller at: ${CONTROLLER_IP} (on ${subnet})${NC}"
            return 0
        fi
        echo -e "\r  - ${CYAN}${subnet}${NC}... Done.          "
    done

    echo -e "${YELLOW}⚠️  No controller found on any scanned networks.${NC}"
    return 1
}

# --- Profile System Resources ---
profile_system() {
    echo -e "\n${BOLD}=== Profiling System Resources ===${NC}"

    local CPU_CORES
    CPU_CORES=$(nproc 2>/dev/null || echo 1)
    local RAM_KB
    RAM_KB=$(awk '/MemTotal/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)
    local RAM_GB=$(( RAM_KB / 1024 / 1024 ))
    local DISK_KB
    DISK_KB=$(df -k / | awk 'NR==2 {print $4}' 2>/dev/null || echo 0)
    local DISK_GB=$(( DISK_KB / 1024 / 1024 ))

    echo -e "Detected CPU Cores: ${CYAN}${CPU_CORES}${NC}"
    echo -e "Detected Total RAM: ${CYAN}${RAM_GB} GB${NC}"
    echo -e "Detected Available Disk: ${CYAN}${DISK_GB} GB${NC}"

    # Auto-detect role if not explicitly set
    if [ -z "$ROLE" ]; then
        if [ "$RAM_GB" -le 4 ] || [ "$DISK_GB" -le 20 ]; then
            echo -e "${YELLOW}⚠️  Low resource machine detected ($RAM_GB GB RAM, $DISK_GB GB Disk). Defaulting role to 'worker', enabling external models and minimal stack.${NC}"
            ROLE="worker"
            PROCESSED_ARGS+=("--role" "worker" "--external-model-server" "--deploy-minimal-stack")
        elif [ "$RAM_GB" -ge 16 ] && [ "$CPU_CORES" -ge 4 ] && [ "$DISK_GB" -ge 256 ]; then
            echo -e "${GREEN}✅ Powerful machine detected. Defaulting role to 'all' and enabling full stack deployment.${NC}"
            ROLE="all"
            PROCESSED_ARGS+=("--role" "all" "--deploy-full-stack")
        else
            echo -e "${CYAN}ℹ️  Standard machine detected. Defaulting role to 'worker' and enabling partial stack deployment.${NC}"
            ROLE="worker"
            PROCESSED_ARGS+=("--role" "worker" "--deploy-partial-stack")
        fi
    else
        echo -e "Role explicitly set to: ${CYAN}${ROLE}${NC}"
    fi

    # Network Discovery & Role Fallback
    if [ "$ROLE" = "worker" ] && [ -z "$CONTROLLER_IP" ]; then
        if find_controller; then
            # Controller found, CONTROLLER_IP is set. Add it to PROCESSED_ARGS.
            PROCESSED_ARGS+=("--controller-ip" "$CONTROLLER_IP")
        else
            echo -e "${YELLOW}⚠️  No controller found. Falling back to role 'all' (initializing as controller).${NC}"
            ROLE="all"

            # Remove the previous --role worker and add --role all
            local NEW_PROCESSED_ARGS=()
            local SKIP_NEXT=false
            for ((j=0; j<${#PROCESSED_ARGS[@]}; j++)); do
                local arg="${PROCESSED_ARGS[$j]}"
                if [ "$SKIP_NEXT" = true ]; then
                    SKIP_NEXT=false
                    continue
                fi
                if [ "$arg" = "--role" ]; then
                    NEW_PROCESSED_ARGS+=("--role" "all")
                    SKIP_NEXT=true
                elif [[ "$arg" =~ ^--role=.*$ ]]; then
                    NEW_PROCESSED_ARGS+=("--role" "all")
                else
                    NEW_PROCESSED_ARGS+=("$arg")
                fi
            done
            PROCESSED_ARGS=("${NEW_PROCESSED_ARGS[@]}")

            # Also add --deploy-full-stack since we are becoming the controller
            PROCESSED_ARGS+=("--deploy-full-stack")
        fi
    fi

    # Give some feedback about the network if it's set
    if [ -n "$CONTROLLER_IP" ]; then
         echo -e "Connecting to main controller at: ${BLUE}${CONTROLLER_IP}${NC}"
    fi
}

# --- Parse command-line arguments for wrapper logic ---
# We use a while loop to handle optional values for flags like --verbose
ARGS=("$@")
PROCESSED_ARGS=()
SKIP_NEXT=false

for ((i=0; i<${#ARGS[@]}; i++)); do
    arg="${ARGS[$i]}"

    if [ "$SKIP_NEXT" = true ]; then
        SKIP_NEXT=false
        continue
    fi

    case $arg in
        --status)
            DO_STATUS=true
            ;;
        --system-cleanup)
            DO_SYSTEM_CLEANUP=true
            DO_PURGE_JOBS=true
            DO_CLEAN_GIT=true
            ;;
        --deploy-full-stack)
            PROCESSED_ARGS+=("--deploy-full-stack")
            ;;
        --deploy-partial-stack)
            PROCESSED_ARGS+=("--deploy-partial-stack")
            ;;
        --deploy-minimal-stack)
            PROCESSED_ARGS+=("--deploy-minimal-stack")
            ;;
        --clean-git|--clean) # Support legacy --clean just in case, but map to clean-git
            DO_CLEAN_GIT=true
            # Don't pass to provisioning
            ;;
        --purge-jobs)
            DO_PURGE_JOBS=true
            # Don't pass to provisioning as a direct arg, we handle logic
            ;;
        --container)
            USE_CONTAINER=true
            PROCESSED_ARGS+=("$arg")
            ;;
        --debug)
            VERBOSE_LEVEL=4
            PROCESSED_ARGS+=("$arg")
            ;;
        --verbose)
            # Check next arg
            NEXT_ARG="${ARGS[$((i+1))]}"
            if [[ -n "$NEXT_ARG" && ! "$NEXT_ARG" =~ ^- ]]; then
                VERBOSE_LEVEL="$NEXT_ARG"
                PROCESSED_ARGS+=("--verbose" "$VERBOSE_LEVEL")
                SKIP_NEXT=true
            else
                VERBOSE_LEVEL=3
                PROCESSED_ARGS+=("--verbose" "3")
            fi
            ;;
        --role)
            NEXT_ARG="${ARGS[$((i+1))]}"
            if [[ -n "$NEXT_ARG" && ! "$NEXT_ARG" =~ ^- ]]; then
                ROLE="$NEXT_ARG"
                PROCESSED_ARGS+=("--role" "$ROLE")
                SKIP_NEXT=true
            fi
            ;;
        --github-ssh-user)
            NEXT_ARG="${ARGS[$((i+1))]}"
            if [[ -n "$NEXT_ARG" && ! "$NEXT_ARG" =~ ^- ]]; then
                PROCESSED_ARGS+=("--github-ssh-user" "$NEXT_ARG")
                SKIP_NEXT=true
            fi
            ;;
        --tier)
            NEXT_ARG="${ARGS[$((i+1))]}"
            if [[ -n "$NEXT_ARG" && ! "$NEXT_ARG" =~ ^- ]]; then
                TIER="$NEXT_ARG"
                PROCESSED_ARGS+=("--tier" "$TIER")
                SKIP_NEXT=true
            fi
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        --agent-api-base)
            NEXT_ARG="${ARGS[$((i+1))]}"
            if [[ -n "$NEXT_ARG" && ! "$NEXT_ARG" =~ ^- ]]; then
                CLI_AGENT_API_BASE="$NEXT_ARG"
                SKIP_NEXT=true
            fi
            ;;
        --agent-model)
            NEXT_ARG="${ARGS[$((i+1))]}"
            if [[ -n "$NEXT_ARG" && ! "$NEXT_ARG" =~ ^- ]]; then
                CLI_AGENT_MODEL="$NEXT_ARG"
                SKIP_NEXT=true
            fi
            ;;
        --agent-api-key)
            NEXT_ARG="${ARGS[$((i+1))]}"
            if [[ -n "$NEXT_ARG" && ! "$NEXT_ARG" =~ ^- ]]; then
                CLI_AGENT_API_KEY="$NEXT_ARG"
                SKIP_NEXT=true
            fi
            ;;
        *)
            PROCESSED_ARGS+=("$arg")
            ;;
    esac
done

# Apply CLI arguments to environment variables if provided
if [ -n "$CLI_AGENT_API_BASE" ]; then
    export AGENT_API_BASE="$CLI_AGENT_API_BASE"
fi
if [ -n "$CLI_AGENT_MODEL" ]; then
    export AGENT_MODEL="$CLI_AGENT_MODEL"
fi
if [ -n "$CLI_AGENT_API_KEY" ]; then
    export AGENT_API_KEY="$CLI_AGENT_API_KEY"
fi

# --- Move to the script's directory ---
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR" || exit 1

# Run system profiling before we proceed, unless just asking for status
if [ "$DO_STATUS" != true ]; then
    profile_system
fi

LOG_FILE="bootstrap_debug.log"
AGENT_LOG="agent_recovery.log"
true > "$LOG_FILE"

# --- Error Handling & Auto-Recovery ---
# shellcheck disable=SC2317
handle_error() {
    local error_line="$1"

    # Avoid recursive error loops
    if [ "${IN_ERROR_HANDLER:-0}" -eq 1 ]; then
        echo -e "\n${RED}❌ Critical error inside the recovery handler. Halting to prevent infinite loop.${NC}"
        exit 1
    fi
    # Use local variable instead of export to prevent state leakage across exec
    local IN_ERROR_HANDLER=1

    echo -e "\n${BOLD}${RED}⚠️  Bootstrap failed at line ${error_line}!${NC}"
    echo -e "${YELLOW}Initiating autonomous recovery via OpenCode...${NC}"

    # Determine OpenCode command path
    local opencode_bin="opencode"
    if [ -x "$SCRIPT_DIR/node_modules/.bin/opencode" ]; then
        opencode_bin="$SCRIPT_DIR/node_modules/.bin/opencode"
    elif ! command -v opencode >/dev/null 2>&1; then
        echo -e "${RED}❌ OpenCode not found in environment. Cannot attempt recovery.${NC}"
        exit 1
    fi

    # Extract log context
    local log_snippet
    log_snippet=$(tail -n 50 "$LOG_FILE" 2>/dev/null || echo "No log output available.")

    local prompt="You are an autonomous debugging agent. The bootstrap.sh script just failed at line ${error_line}.
Here is the recent log output context:

\`\`\`
${log_snippet}
\`\`\`

Your task is to:
1. Analyze the error carefully.
2. Fix the underlying issue by modifying bootstrap.sh, Ansible playbooks, or other configuration files as necessary.
3. Commit the changes to the Git repository with a descriptive commit message, and explicitly push them to the remote repository.
4. Do not ask for user confirmation, execute the fix autonomously and exit.
"

    echo -e "Agent thought process and actions will be logged to: ${CYAN}${AGENT_LOG}${NC}"
    echo -e "⏳ Please wait while the agent attempts to fix the issue..."

    # Configure API endpoint for Local/Network LLMs
    local opencode_cmd=("$opencode_bin" run)

    # Determine the model and provider settings with a local-first priority
    if [ -n "${AGENT_API_BASE:-}" ]; then
        # 1. User explicitly provided an API base via CLI or ENV
        export OPENCODE_API_BASE="$AGENT_API_BASE"
        export OPENCODE_API_KEY="${AGENT_API_KEY:-sk-dummy}"
        opencode_cmd+=(--model "${AGENT_MODEL:-openai/qwen2.5-coder}")
    elif [ -f ~/.config/opencode/opencode.json ] && grep -q '"provider"' ~/.config/opencode/opencode.json; then
        # 2. Check for an existing, working local OpenCode configuration (e.g. Ollama)
        local configured_provider
        local configured_model
        # Use python to safely parse the JSON if possible, otherwise rely on fallback
        configured_provider=$(python3 -c "import json, sys; config=json.load(sys.stdin); provider_keys=list(config.get('provider', {}).keys()); print(provider_keys[0] if provider_keys else '')" < ~/.config/opencode/opencode.json 2>/dev/null)
        if [ -n "$configured_provider" ]; then
            configured_model=$(python3 -c "import json, sys; provider='$configured_provider'; config=json.load(sys.stdin); model_keys=list(config.get('provider', {}).get(provider, {}).get('models', {}).keys()); print(model_keys[0] if model_keys else '')" < ~/.config/opencode/opencode.json 2>/dev/null)
            if [ -n "$configured_model" ]; then
                opencode_cmd+=(--model "${AGENT_MODEL:-${configured_provider}/${configured_model}}")
            else
                # Fallback if parsing failed
                opencode_cmd+=(--model "${AGENT_MODEL:-openai/gpt-4o-mini}")
                export OPENAI_API_KEY="${AGENT_API_KEY:-${OPENAI_API_KEY:-sk-dummy}}"
            fi
        else
            opencode_cmd+=(--model "${AGENT_MODEL:-openai/gpt-4o-mini}")
            export OPENAI_API_KEY="${AGENT_API_KEY:-${OPENAI_API_KEY:-sk-dummy}}"
        fi
    elif curl -s http://127.0.0.1:8500/v1/health/service/llamacpp-rpc-api?passing | grep -qi '"Status":\s*"passing"' 2>/dev/null; then
        # 3. Check for a local llamacpp-rpc cluster instance via Consul
        # Currently, if this matches, OpenCode still needs a compatible openai wrapper.
        # We assume the default wrapper is accessible locally.
        export OPENCODE_API_BASE="http://127.0.0.1:8000/v1" # Adjust if your local cluster exposes OpenAI compat on a different port
        export OPENCODE_API_KEY="${AGENT_API_KEY:-sk-dummy}"
        opencode_cmd+=(--model "${AGENT_MODEL:-openai/local-model}")
    else
        # 4. Fallback to remote provider
        opencode_cmd+=(--model "${AGENT_MODEL:-openai/gpt-4o-mini}")
        # Explicitly export OPENAI_API_KEY so the OpenAI provider doesn't fail
        export OPENAI_API_KEY="${AGENT_API_KEY:-${OPENAI_API_KEY:-sk-dummy}}"
    fi

    # Run OpenCode headlessly. Catch error explicitly in case set -e is active elsewhere
    local agent_status=0
    "${opencode_cmd[@]}" "$prompt" > "$AGENT_LOG" 2>&1 || agent_status=$?

    if [ "$agent_status" -eq 0 ]; then
        echo -e "${GREEN}✅ Autonomous recovery successful!${NC}"
        echo -e "${CYAN}Resuming bootstrap process...${NC}"
        # Prevent trap from firing again during exec
        trap - ERR
        # Re-execute the script, appending --continue. Fallback to empty if ARGS is not defined yet.
        exec "$0" "${ARGS[@]:-}" "--continue"
    else
        echo -e "${RED}❌ Autonomous recovery failed. Please review ${AGENT_LOG} for details.${NC}"
        exit 1
    fi
}

# Set the global trap
trap 'handle_error $LINENO' ERR

# --- Helper: Run Step ---
run_step() {
    local desc="$1"
    local cmd="$2"

    # Levels 3 and 4 show output
    if [ "$VERBOSE_LEVEL" -ge 3 ]; then
        echo -e "\n${BOLD}${CYAN}--- Running ${desc} ---${NC}"
        # Execute and tee to log
        eval "$cmd" 2>&1 | tee -a "$LOG_FILE"
        local status=${PIPESTATUS[0]} # Capture exit code of the evaluated command

        if [ "$status" -eq 0 ]; then
            echo -e "${GREEN}✅ ${desc} complete.${NC}"
        else
            echo -e "${RED}❌ ${desc} failed.${NC}"
            return "$status"
        fi
    else
        echo -n -e "⏳ ${desc}..."

        local tmp_log
        tmp_log=$(mktemp)
        eval "$cmd" > "$tmp_log" 2>&1
        local status=$?

        cat "$tmp_log" >> "$LOG_FILE"

        if [ $status -eq 0 ]; then
            echo -e "\r\033[K${GREEN}✅ ${desc} Complete${NC}"
        else
            echo -e "\r\033[K${RED}❌ ${desc} Failed${NC}"
            echo -e "${YELLOW}--- Error Log ---${NC}"
            cat "$tmp_log"
            echo -e "${YELLOW}-----------------${NC}"
            rm "$tmp_log"
            return $status
        fi
        rm "$tmp_log"
    fi
}

ask_confirm() {
    local prompt="$1"
    read -p "$prompt [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        return 0
    else
        return 1
    fi
}

# --- Environment Setup (Reusable) ---
VENV_DIR="$SCRIPT_DIR/.venv"

# shellcheck disable=SC2317
setup_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv "$VENV_DIR"
    fi
}

ensure_python_environment() {
    echo -e "\n${BOLD}=== Environment Setup ===${NC}"

    run_step "Creating Python virtual environment" "setup_venv"

    # Activate venv for this script execution
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"

    run_step "Upgrading pip" "pip install --upgrade pip"

    if [ -f "requirements-dev.txt" ]; then
        run_step "Installing Python dependencies" "pip install --no-cache-dir -r requirements-dev.txt"
    else
        echo "⚠️  Warning: requirements-dev.txt not found. Skipping dependency installation."
    fi

    run_step "Installing OpenCode AI Agent" "npm ci"

    run_step "Installing Ansible Core" "pip install ansible-core pyyaml"

    # --- Find Ansible Playbook executable ---
    ANSIBLE_GALAXY_EXEC="$VENV_DIR/bin/ansible-galaxy"

    # Install Ansible collections
    if [ -x "$ANSIBLE_GALAXY_EXEC" ]; then
        export ANSIBLE_CONFIG="$(pwd)/ansible.cfg"
        run_step "Installing Ansible collections" "$ANSIBLE_GALAXY_EXEC collection install community.general ansible.posix community.docker community.sops"
    else
        echo "Error: ansible-galaxy not found at $ANSIBLE_GALAXY_EXEC." >&2
        exit 1
    fi
}

# --- Cleanup Actions ---

perform_purge_jobs() {
    echo -e "\n${BOLD}${YELLOW}⚠️  Purge Jobs initiated.${NC}"
    if ask_confirm "Are you sure you want to stop and purge all Nomad jobs?"; then
        # Ensure we have the python environment to run the script
        ensure_python_environment

        echo "Running provisioning script to purge jobs..."
        # Pass --purge-jobs and --only-purge
        python3 scripts/provisioning.py --purge-jobs --only-purge
        local status=$?
        if [ $status -eq 0 ]; then
            echo -e "${GREEN}✅ Jobs purged.${NC}"
        else
             echo -e "${RED}❌ Job purge failed.${NC}"
        fi
    else
        echo "Job purge cancelled."
    fi
}

perform_system_cleanup() {
    echo -e "\n${BOLD}${YELLOW}⚠️  System Cleanup initiated (Docker, Apt, Logs).${NC}"
    if ask_confirm "Are you sure you want to aggressively clean system resources?"; then
        if [ -x "scripts/cleanup.sh" ]; then
            # We assume the user has sudo if they are running this
            run_step "Running system cleanup script" "sudo ./scripts/cleanup.sh"
        else
            echo -e "${RED}❌ scripts/cleanup.sh not found or not executable.${NC}"
        fi
    else
        echo "System cleanup cancelled."
    fi
}

perform_git_clean() {
    echo -e "\n${BOLD}${YELLOW}⚠️  Git Clean initiated.${NC}"
    echo "This will permanently delete all untracked files."
    echo "--------------------------------------------------"
    git clean -ndx
    echo "--------------------------------------------------"

    if ask_confirm "Are you sure you want to permanently delete these files?"; then
        if ! run_step "Cleaning repository" "git clean -fdx"; then
            echo -e "\n${YELLOW}⚠️  Standard cleanup failed. This is often due to files created with sudo.${NC}"
            if ask_confirm "Do you want to try cleaning with sudo?"; then
                # Ensure sudo credentials
                if ! sudo -n true 2>/dev/null; then
                    sudo -v
                fi
                run_step "Cleaning repository (with sudo)" "sudo git clean -fdx"
            else
                echo "Cleanup skipped."
            fi
        fi
    else
        echo "Git clean cancelled."
    fi
}

# --- Status Action ---
if [ "$DO_STATUS" = true ]; then
    echo -e "${BOLD}=== Cluster Status ===${NC}"
    ensure_python_environment
    python3 scripts/provisioning.py --only-status "${PROCESSED_ARGS[@]}"
    exit $?
fi

# --- Execute Cleanup Actions ---
# We execute these BEFORE everything else to ensure a clean slate if requested.

if [ "$DO_PURGE_JOBS" = true ]; then
    perform_purge_jobs
fi

if [ "$DO_SYSTEM_CLEANUP" = true ]; then
    perform_system_cleanup
fi

if [ "$DO_CLEAN_GIT" = true ]; then
    perform_git_clean
fi

# If the user only requested cleanup, we might want to stop here?
# But typically bootstrap means "setup". If I wanted to JUST clean, I might not expect it to start building again.
# However, for now we follow the pattern: cleanup then proceed.


# --- Container Mode ---
if [ "$USE_CONTAINER" = true ]; then
    echo -e "${BOLD}--- Running in Container Mode ---${NC}"

    # --- Host-side Cluster Detection ---
    check_for_existing_cluster() {
        echo "--- Checking for existing cluster on host ---"
        CLUSTER_EXISTS=false
        if nc -z localhost 4646 2>/dev/null || nc -z localhost 8500 2>/dev/null; then
            echo "✅ Detected existing Nomad/Consul service on the host."
            CLUSTER_EXISTS=true
        else
            echo "ℹ️  No existing cluster detected on the host. Will start a new one."
        fi
    }

    # Check if we are already inside the container
    if [ -f "/.dockerenv" ] && [ "$(hostname)" = "pipecat-dev-runner" ]; then
        echo "✅ Already inside the container. Proceeding with bootstrap..."
    else
        IMAGE_NAME="pipecat-dev-container"
        CONTAINER_NAME="pipecat-dev-runner"

        check_for_existing_cluster

        echo "Building container image: $IMAGE_NAME..."
        if ! docker build -t "$IMAGE_NAME" docker/dev_container/; then
            echo "❌ Failed to build container image."
            exit 1
        fi

        echo "Checking for existing container..."
        if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
            echo "Removing existing container..."
            docker rm -f "$CONTAINER_NAME"
        fi

        # --- Dynamically configure and start container ---
        HOST_IP=$(hostname -I | awk '{print $1}')
        if [ -z "$HOST_IP" ]; then
            echo "❌ Error: Could not determine host IP address."
            exit 1
        fi

        DOCKER_RUN_CMD=(docker run -d --privileged --name "$CONTAINER_NAME" \
            --hostname "$CONTAINER_NAME" \
            -v /sys/fs/cgroup:/sys/fs/cgroup:rw --cgroupns=host \
            -v "$SCRIPT_DIR":/opt/cluster-infra -e "HOST_IP=$HOST_IP")

        if [ "$CLUSTER_EXISTS" = true ]; then
            echo "Configuring container as a WORKER to join the existing cluster."
        else
            echo "Configuring container as a new CONTROLLER."
            DOCKER_RUN_CMD+=(-p 4646:4646 -p 8500:8500 -p 8081:8081 -p 8000:8000)
        fi

        DOCKER_RUN_CMD+=("$IMAGE_NAME")

        echo "Starting container..."
        if ! "${DOCKER_RUN_CMD[@]}"; then
            echo "❌ Failed to start container."
            exit 1
        fi

        echo "Waiting for container to initialize..."
        sleep 5

        echo "Executing bootstrap inside the container..."
        # Pass processed args
        docker exec -it "$CONTAINER_NAME" /bin/bash -c "cd /opt/cluster-infra && ./bootstrap.sh ${PROCESSED_ARGS[*]}"
        EXIT_CODE=$?

        echo "Container bootstrap finished with exit code: $EXIT_CODE"
        echo "You can access the container using: docker exec -it $CONTAINER_NAME /bin/bash"
        echo "To stop and remove the container: docker rm -f $CONTAINER_NAME"

        exit $EXIT_CODE
    fi
fi

# --- Run Initial Machine Setup ---
echo -e "${BOLD}=== System Bootstrap ===${NC}"
if [ -f "initial-setup/setup.sh" ]; then
    if [ -f "/.dockerenv" ] && [ "$(hostname)" = "pipecat-dev-runner" ]; then
         echo "🐳 Container environment detected. Skipping initial machine setup (setup.sh)."
    else
        # We need to ensure sudo doesn't hang on prompt hidden by redirection
        if sudo -n true 2>/dev/null; then
            # Sudo is already cached
            run_step "Initial machine setup" "sudo bash initial-setup/setup.sh"
        else
            echo "You may be prompted for your sudo password to run the initial setup script."
            sudo -v
            run_step "Initial machine setup" "sudo bash initial-setup/setup.sh"
        fi
    fi
else
    echo "⚠️  Warning: initial-setup/setup.sh not found. Skipping pre-configuration."
fi

# --- Install Python dependencies (Virtual Environment) ---
# Ensure environment is ready (it might have been set up by purge_jobs, or deleted by git clean)
ensure_python_environment

# --- Run Provisioning Script ---
# echo "🚀 Handing over to Python provisioning script..."
# Pass processed arguments to the python script.
python3 scripts/provisioning.py "${PROCESSED_ARGS[@]}"
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "\n${GREEN}✨ Bootstrap complete.${NC}"
else
    echo -e "\n${RED}❌ Bootstrap failed with exit code $EXIT_CODE.${NC}"
fi

exit $EXIT_CODE
