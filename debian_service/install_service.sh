#!/bin/bash

# This script guides you through installing the distributed-llama service.
# Some commands will require sudo privileges to execute.

# --- Variables ---
INIT_SCRIPT_WORKSPACE_PATH="distributed-llama-init-script/distributed-llama"
CONFIG_FILE_WORKSPACE_PATH="distributed-llama-default-config"

# --- Preamble ---
echo "--- distributed-llama Service Installation Guide ---"
echo "This script will provide instructions to install the service."
echo "You may need to run some commands with 'sudo'."
echo "Ensure you have already run './setup_distributed_llama.sh' to set up the application code."
echo "---"
echo ""

# --- User and Directories Creation ---
echo "INFO: 1. Create a dedicated user for the service (if it doesn't exist):"
echo "   sudo adduser --system --group llamauser"
echo "---"
echo ""

echo "INFO: 2. Create the installation directory for distributed-llama (e.g., /opt/distributed-llama):"
echo "   sudo mkdir -p /opt/distributed-llama"
echo "   sudo chown llamauser:llamauser /opt/distributed-llama"
echo "   INFO: Remember to run './setup_distributed_llama.sh' inside /opt/distributed-llama if you haven't already."
echo "---"
echo ""

echo "INFO: 3. Create PID and Log directories:"
echo "   sudo mkdir -p /var/run/distributed-llama"
echo "   sudo chown llamauser:llamauser /var/run/distributed-llama"
echo "   sudo chmod 755 /var/run/distributed-llama" # Ensure user can write PID
echo "   sudo mkdir -p /var/log/distributed-llama"
echo "   sudo chown llamauser:llamauser /var/log/distributed-llama"
echo "   sudo chmod 755 /var/log/distributed-llama" # Ensure user can write logs
echo "---"
echo ""

# --- Deploy Scripts ---
echo "INFO: 4. Copy the init script to /etc/init.d/:"
echo "   Make sure '${INIT_SCRIPT_WORKSPACE_PATH}' exists in your current directory or provide the correct path."
echo "   sudo cp \"${INIT_SCRIPT_WORKSPACE_PATH}\" /etc/init.d/distributed-llama"
echo "---"
echo ""

echo "INFO: 5. Copy the configuration file to /etc/default/:"
echo "   Make sure '${CONFIG_FILE_WORKSPACE_PATH}' exists in your current directory or provide the correct path."
echo "   sudo cp \"${CONFIG_FILE_WORKSPACE_PATH}\" /etc/default/distributed-llama"
echo "---"
echo ""

# --- Set Permissions ---
echo "INFO: 6. Set execute permissions on the init script:"
echo "   sudo chmod +x /etc/init.d/distributed-llama"
echo "---"
echo ""

# --- Enable Service ---
echo "INFO: 7. Register the service to start on boot (for SysVinit systems):"
echo "   sudo update-rc.d distributed-llama defaults"
echo "   INFO: If your system uses systemd, this script will still work, but you might"
echo "         consider creating a native systemd unit file for deeper integration."
echo "---"
echo ""

# --- Configuration Reminder ---
echo "IMPORTANT: 8. You MUST edit /etc/default/distributed-llama and set the MODEL_PATH and TOKENIZER_PATH variables."
echo "   These paths should point to your downloaded model and tokenizer files."
echo "   The INSTALL_DIR should also be correctly set if it's not '/opt/distributed-llama'."
echo "   Example: sudo nano /etc/default/distributed-llama"
echo "---"
echo ""

# --- Service Usage ---
echo "INFO: 9. Once configured, you can manage the service using:"
echo "   sudo service distributed-llama start"
echo "   sudo service distributed-llama stop"
echo "   sudo service distributed-llama restart"
echo "   sudo service distributed-llama status"
echo "---"
echo ""
echo "Installation guide complete. Please review all steps and ensure configurations are correct."
