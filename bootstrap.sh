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
    echo "  --purge-jobs                 Stop and purge all running Nomad jobs before starting."
    echo "  --clean                      Clean the repository of all untracked files (interactive prompt)."
    echo "  --debug                      Enable verbose Ansible output and log to playbook_output.log."
    echo "  --leave-services-running     Do not clean up Nomad and Consul data on startup."
    echo "  --external-model-server      Skip large model downloads and builds, assuming an external server."
    echo "  --continue                   Resume from the last successfully completed playbook."
    echo "  --benchmark                  Run benchmark tests."
    echo "  --deploy-docker              Deploy the pipecat application using Docker (Default)."
    echo "  --run-local                  Deploy the pipecat application using local raw_exec (for debugging)."
    echo "  --home-assistant-debug       Enable debug mode for Home Assistant."
    echo "  --container                  Run the entire infrastructure inside a single large container."
    echo "  --watch <target>             Pause for inspection after the specified target (task/role) completes."
    echo "  -h, --help                   Display this help message and exit."
}

# --- Initialize flags ---
USE_CONTAINER=false
CLEAN_REPO=false
IS_DEBUG=false
ROLE="all"
CONTROLLER_IP=""

# --- Parse command-line arguments for wrapper logic ---
# We need to peek at args to handle --clean and --container before passing everything to Python
for arg in "$@"; do
    case $arg in
        --clean) CLEAN_REPO=true ;;
        --container) USE_CONTAINER=true ;;
        --debug) IS_DEBUG=true ;;
        --role)
            # Simple peek, robust parsing handled by python
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
    esac
done

# --- Move to the script's directory ---
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR"

LOG_FILE="bootstrap_debug.log"
> "$LOG_FILE"

# --- Helper: Run Step ---
run_step() {
    local desc="$1"
    local cmd="$2"

    if [ "$IS_DEBUG" = true ]; then
        echo -e "\n${BOLD}${CYAN}--- Running ${desc} ---${NC}"
        eval "$cmd"
        local status=$?
        if [ $status -eq 0 ]; then
            echo -e "${GREEN}✅ ${desc} complete.${NC}"
        else
            echo -e "${RED}❌ ${desc} failed.${NC}"
            return $status
        fi
    else
        echo -n -e "⏳ ${desc}..."

        local tmp_log=$(mktemp)
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
        ARGS_WITHOUT_CONTAINER=()
        for arg in "$@"; do
            if [[ "$arg" != "--container" ]]; then
                ARGS_WITHOUT_CONTAINER+=("$arg")
            fi
        done

        docker exec -it "$CONTAINER_NAME" /bin/bash -c "cd /opt/cluster-infra && ./bootstrap.sh ${ARGS_WITHOUT_CONTAINER[*]}"
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

# --- Handle the --clean option ---
if [ "$CLEAN_REPO" = true ]; then
    echo -e "\n${YELLOW}⚠️  --clean flag detected. This will permanently delete all untracked files.${NC}"
    echo "Performing a dry run to show what will be deleted:"
    echo "--------------------------------------------------"
    git clean -ndx
    echo "--------------------------------------------------"
    
    read -p "Are you sure you want to permanently delete all files and directories listed above? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_step "Cleaning repository" "git clean -fdx"
    else
        echo "Cleanup cancelled. Exiting."
        exit 1
    fi
fi

# --- Install Python dependencies (Virtual Environment) ---
echo -e "\n${BOLD}=== Environment Setup ===${NC}"
VENV_DIR="$SCRIPT_DIR/.venv"

setup_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv "$VENV_DIR"
    fi
}
run_step "Creating Python virtual environment" "setup_venv"

# Activate venv for this script execution
source "$VENV_DIR/bin/activate"

run_step "Upgrading pip" "pip install --upgrade pip"

if [ -f "requirements-dev.txt" ]; then
    run_step "Installing Python dependencies" "pip install --no-cache-dir -r requirements-dev.txt"
else
    echo "⚠️  Warning: requirements-dev.txt not found. Skipping dependency installation."
fi

run_step "Installing Ansible Core" "pip install ansible-core pyyaml"

# --- Find Ansible Playbook executable ---
# Since we are in a venv, these are guaranteed to be in the path
ANSIBLE_GALAXY_EXEC="$(which ansible-galaxy)"

# Install Ansible collections
if [ -x "$ANSIBLE_GALAXY_EXEC" ]; then
    run_step "Installing Ansible collections" "$ANSIBLE_GALAXY_EXEC collection install community.general ansible.posix community.docker"
else
    echo "Error: ansible-galaxy not found in venv." >&2
    exit 1
fi

# --- Run Provisioning Script ---
# echo "🚀 Handing over to Python provisioning script..."
# Pass all original arguments to the python script.
# Note: The python script parses args independently.
python3 provisioning.py "$@"
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "\n${GREEN}✨ Bootstrap complete.${NC}"
else
    echo -e "\n${RED}❌ Bootstrap failed with exit code $EXIT_CODE.${NC}"
fi

exit $EXIT_CODE
