Last updated: 2025-10-12

# NixOS-based PXE Boot Server Setup

This document explains how to set up a PXE boot server using NixOS. This method leverages the declarative nature of NixOS to provide a reproducible and robust PXE environment for provisioning bare-metal machines.

## 1. Overview

This setup uses a new Ansible role, `nixos_pxe_server`, to configure a designated NixOS machine to act as a PXE server. Unlike the traditional, imperative setup used for Debian, the NixOS model defines the entire server configuration—including DHCP, TFT, and HTTP services, as well as the bootable client system itself—in a single, declarative file (`configuration.nix`).

### Key Differences from the Debian Method

* **Declarative Configuration:** All services are defined in one Nix file, not installed and configured with sequential commands. This makes the setup more reliable and easier to maintain.
* **No Preseed:** NixOS does not use preseed files. Instead, a complete, minimal NixOS system is built on the server and served to clients over the network.
* **Atomic Updates:** `nixos-rebuild switch` atomically builds and activates the new configuration. If the build fails, the system is automatically rolled back to the last known good configuration.
* **Reproducibility:** The entire PXE server and the client operating system it serves can be perfectly reproduced from the same Nix configuration.

## 2. Setup

### 2.1. Prerequisites

* A machine with NixOS installed. This machine will become your PXE server.
* A static IP address configured on the PXE server's network interface.

### 2.2. Configure Ansible

You need to define several variables in your Ansible inventory (`group_vars/all.yaml` or `host_vars`) to configure the `nixos_pxe_server` role.

First, you must add a variable to select the PXE operating system. In `group_vars/all/main.yaml`, add:

```yaml
# Select the PXE server OS ('debian' or 'nixos')
pxe_os: nixos
```

Then, define the NixOS-specific variables:

```yaml
# The network interface on the PXE server to listen on.
pxe_interface: "enp0s8"

# The SSH public key to install on the provisioned clients for root access.
pxe_client_ssh_key: "ssh-rsa AAAA..."

# DHCP configuration
pxe_subnet: "192.168.1.0"
pxe_netmask: "255.255.255.0"
pxe_range_start: "192.168.1.200"
pxe_range_end: "192.168.1.250"
pxe_router: "192.168.1.1"
```

### 2.3. Apply the `nixos_pxe_server` Role

Create a playbook, for example `pxe_setup.yaml`, that conditionally includes the correct role based on the `pxe_os` variable.

```yaml
---
- hosts: your_pxe_server_hostname
  tasks:
    - name: Include Debian PXE role
      include_role:
        name: pxe_server
      when: pxe_os == 'debian'

    - name: Include NixOS PXE role
      include_role:
        name: nixos_pxe_server
      when: pxe_os == 'nixos'
```

Run the playbook:

```bash
ansible-playbook pxe_setup.yaml
```

The playbook will:

1. Copy the templated `configuration.nix` file to `/etc/nixos/` on the server.
2. Copy the templated `boot.ipxe` script to `/var/www/`.
3. Run `nixos-rebuild switch`. This command will:
    * Build the minimal NixOS netboot environment (kernel and initrd).
    * Install and configure the DHCP, TFTP, and Nginx services.
    * Start the services and make them available on the network.

### 2.4. Client Boot Process

When a client machine is set to network boot, it will:

1. Contact the DHCP server and receive an IP address.
2. Download and run the iPXE bootloader (`.kpxe` or `.efi`) from the TFTP server.
3. iPXE will then download and execute the `boot.ipxe` script from the HTTP server.
4. The script instructs iPXE to download the NixOS kernel (`bzImage`) and initrd.
5. The client boots into a fully functional, minimal NixOS environment running in RAM, with SSH access enabled. From here, you can proceed with further provisioning.
