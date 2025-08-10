# iPXE Boot Server Setup for Automated Debian Installation

This document explains how to set up an advanced PXE boot server that uses iPXE to automate the installation of Debian 12 on new cluster nodes. This method is faster and more reliable than traditional PXE by leveraging HTTP instead of TFTP for the bulk of the file transfers.

## 1. Overview

The `pxe_server` Ansible role automates the setup of all necessary services for a modern, iPXE-based workflow:
- **DHCP:** Assigns IP addresses and provides boot information. It intelligently serves the correct iPXE bootloader (`.kpxe` for BIOS, `.efi` for UEFI) to new clients.
- **TFTP:** Serves only the initial, tiny iPXE bootloader.
- **HTTP (Nginx):** Serves the main iPXE boot script, the Debian kernel, the initrd, and the preseed configuration file.
- **Preseed:** Automates the Debian installation process.

## 2. Setup

### 2.1. Designate a PXE Server
Choose one of your `controller_nodes` to act as the PXE boot server. This machine must have a static IP address.

### 2.2. Apply the `pxe_server` Role
The setup is fully automated by the Ansible role. Simply create a new playbook file, for example `pxe_setup.yaml`, to apply the role to your chosen server:

```yaml
---
- hosts: your_pxe_server_hostname
  roles:
    - pxe_server
```

Run the playbook:
```bash
ansible-playbook pxe_setup.yaml
```
The playbook will install and configure DHCP, TFTP, and Nginx, download the necessary iPXE and Debian boot files, and set up the iPXE boot script.

### 2.3. DHCP Configuration
The DHCP server is configured to serve a range of IP addresses. For a more secure setup, you can edit the template at `ansible/roles/pxe_server/templates/dhcpd.conf.j2` to only respond to specific MAC addresses.

### 2.4. Prepare Client Machines
On each new, bare-metal machine you want to provision:
1.  Enter the BIOS/UEFI setup.
2.  Enable "Network Boot" or "PXE Boot".
3.  Set the network card as the first boot device.
4.  Save and exit.

When the machine boots, it will perform the following automated chainload process:
1. The client's built-in PXE ROM contacts the DHCP server.
2. The DHCP server provides an IP and tells the client to download the iPXE bootloader from the TFTP server.
3. The iPXE bootloader loads and makes a new DHCP request, identifying itself as "iPXE".
4. The DHCP server responds with the URL to the iPXE boot script (e.g., `http://<server_ip>/boot.ipxe`).
5. iPXE downloads and executes the script, which then fetches the Debian kernel/initrd over HTTP and begins the automated installation using the preseed file.

Once the installation is complete, the machine will reboot into a fresh Debian system, ready for the main cluster provisioning with the `playbook.yaml`.
