Last updated: 2025-10-12

# Manual Worker Node Setup

This directory contains a script for manually preparing a new worker node to be added to the cluster. This script should be used in cases where the automated PXE boot installation method is not feasible.

## When to Use This

Use this script if:

- You are adding a new worker node to an existing cluster.
- You cannot or do not want to use the PXE boot server to install the operating system.
- You have already performed a minimal installation of Debian Trixie on the new machine.

## Steps

1. **Perform a minimal installation of Debian Trixie** on your new machine. Ensure you create a standard non-root user (e.g., `user`).
2. **Log in as root** on the new machine.
3. **Copy the `setup.sh` script** from this directory to the new machine (e.g., using `scp`).
4. **Make the script executable:**

    ```bash
    chmod +x setup.sh
    ```

5. **Run the script:**

    ```bash
    ./setup.sh
    ```

6. **Follow the Manual Steps:** The script will print a list of manual networking configuration steps that you must perform. This includes setting a static IP address and a hostname for the new node.
7. **Reboot** the new machine after completing the manual steps.
8. **Copy the Ansible Controller's SSH Key:** From your main controller node (`AID-E-24`), run the `ssh-copy-id` command to enable passwordless SSH access to the new worker.

    ```bash
    # Run this from the controller node
    ssh-copy-id user@<new_worker_ip>
    ```

After completing these steps, the new worker node is ready. You can now add it to your `inventory.yaml` file and run the main `playbook.yaml` to provision it and have it join the cluster.
