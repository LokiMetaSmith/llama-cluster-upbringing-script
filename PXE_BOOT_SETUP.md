# PXE Boot Server Setup

This document explains how to set up a PXE boot server to automate the installation of Debian 12 on new cluster nodes.

## 1. Overview

The `pxe_server` Ansible role automates the setup of all necessary services for PXE booting:
- **DHCP:** Assigns IP addresses and provides boot information.
- **TFTP:** Serves the initial boot files.
- **NFS:** Serves the Debian OS packages.
- **Preseed:** Automates the Debian installation process.

## 2. Setup

### 2.1. Designate a PXE Server
Choose one of your `controller_nodes` to act as the PXE boot server. This machine must have a static IP address.

### 2.2. Apply the `pxe_server` Role
Create a new playbook file, for example `pxe_setup.yaml`, to apply the role to your chosen server:

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

### 2.3. Configure DHCP
The DHCP server is configured to serve a range of IP addresses. You may need to edit the template at `ansible/roles/pxe_server/templates/dhcpd.conf.j2` to match your network configuration.

By default, any machine on the network that is configured to PXE boot will be able to get an IP address and start the automated installation. For a more secure setup, you can configure the DHCP server to only respond to specific MAC addresses.

### 2.4. Prepare Client Machines
On each new, bare-metal machine you want to provision:
1.  Enter the BIOS/UEFI setup.
2.  Enable "Network Boot" or "PXE Boot".
3.  Set the network card as the first boot device.
4.  Save and exit.

When the machine boots, it will contact the DHCP server, receive the PXE boot information, and begin the automated Debian installation. Once the installation is complete, the machine will reboot into a fresh Debian system, configured with the settings from our `initial-setup.sh` script, and will be ready for Ansible provisioning.
