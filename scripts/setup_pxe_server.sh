#!/bin/bash
set -euo pipefail

# Move to repository root
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

echo "=== Pipecat PXE Server Setup ==="
echo "This script configures the current node to act as a PXE boot server"
echo "for hands-free network installations of the Pipecat OS."
echo ""

# Ensure Ansible is installed
if ! command -v ansible-playbook >/dev/null 2>&1; then
    echo "Installing Ansible..."
    sudo apt-get update && sudo apt-get install -y ansible
fi

# Determine target OS for PXE clients
PXE_OS="${1:-debian}"

if [ "$PXE_OS" != "debian" ] && [ "$PXE_OS" != "nixos" ]; then
    echo "Error: Supported PXE OS arguments are 'debian' or 'nixos'."
    echo "Usage: ./setup_pxe_server.sh [debian|nixos]"
    exit 1
fi

echo "Setting up PXE server for: $PXE_OS"

# Run the Ansible playbook locally
ansible-playbook -i "localhost," -c local playbooks/pxe_setup.yaml \
    -e "pxe_os=$PXE_OS" \
    -e "ansible_python_interpreter=$(which python3)"

echo "=== Setup Complete ==="
echo "You can now connect other machines to the same network and boot them via PXE."