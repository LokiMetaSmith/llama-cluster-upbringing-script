# Initial Machine Setup

This directory contains the scripts responsible for the very first step of machine configuration, which runs before the main Ansible playbooks.

## Overview

The setup process is designed to be modular and idempotent. The main `setup.sh` script sources a configuration file (`setup.conf`) and then executes a series of numbered scripts from the `modules/` directory. This process handles essential tasks like setting the hostname, configuring the network, and preparing the machine to be managed by Ansible.

## File Descriptions

- **`setup.sh`**: The main entrypoint script. It sources the configuration and runs all scripts in the `modules` directory in order.
- **`setup.conf`**: The primary configuration file. You must edit this file to define the machine's `HOSTNAME`, network settings, and other critical variables before running the setup.
- **`modules/`**: This directory contains the individual, ordered scripts that perform the actual setup tasks.
  - `01-network.sh`: Configures the machine with a static IP (for controllers) or DHCP (for workers).
  - `02-hostname.sh`: Sets the system hostname.
  - `03-user.sh`: Creates a non-root user and adds it to the `sudo` group.
  - `04-ssh.sh`: Generates SSH keys and sets up a key synchronization service using Consul.
  - `05-auto-provision.sh`: Configures a systemd service that will "call home" on the next boot to trigger the main Ansible provisioning process.
- **`update_inventory.sh`**: A script that dynamically generates the initial Ansible inventory file based on the settings in `setup.conf`.
- **`worker-setup/`**: Contains scripts specifically for configuring a new worker node to join an existing cluster.
- **`add_new_worker.sh`**: A convenience script that orchestrates the process of adding a new worker node to the cluster.
