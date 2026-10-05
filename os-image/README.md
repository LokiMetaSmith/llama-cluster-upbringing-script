# Bootable Pipecat Cluster ISO & Automated Node Upbringing

This directory contains the `live-build` configurations to generate custom, bootable Debian ISOs for the Pipecat AI agent cluster. It supports both **zero-touch automatic cluster joining** on first boot and manual bootstrap configurations.

---

## 🚀 Key Features

* **Debian 13 (Trixie) Base**: Modern kernel and headless environment tailored for edge nodes and compute workers.
* **Automatic Hardware Clock Calibration**: Bundled `chrony` prevents RTC drift on bare-metal systems, eliminating GPG package signature verification failures.
* **Zero-Bypass Mutual TLS**: Installs cluster Root CAs into system trust stores and issues mTLS certificates for Consul and Nomad.
* **Headscale / Tailscale Mesh Integration**: Connects nodes directly to the encrypted WireGuard mesh without manual authentication prompts.
* **Zero-Touch Auto-Enrollment**: Automatically mounts credentials, joins the mesh, registers with Consul/Nomad, and launches the local Pipecat frontend on port `8007`.

---

## 🔑 Credential Extraction Workflow

To enable an ISO to automatically join an existing cluster, the required cryptographic keys and tokens must be extracted from the running controller.

### 1. Extract Keys via the Extraction Tool

Run [`scripts/extract_cluster_keys.sh`](../scripts/extract_cluster_keys.sh) from the repository root:

```bash
# If running directly on the controller:
./scripts/extract_cluster_keys.sh --output /tmp/cluster_keys_bundle

# Or if running from an operator workstation over SSH:
./scripts/extract_cluster_keys.sh --controller 192.168.1.148 --output /tmp/cluster_keys_bundle
```

### 2. Extracted Bundle Structure

The output directory contains the complete cryptographic identity needed by a worker node:

| File | Purpose | Security Permissions |
| :--- | :--- | :--- |
| `controller_ip` | LAN IP of the controller (e.g. `192.168.1.148`) | `0644` |
| `headscale_url` | Endpoint for the Headscale WireGuard controller (`http://<ip>:8085`) | `0644` |
| `mesh_auth_key` | 30-day reusable Headscale pre-auth key for mesh enrollment | `0600` |
| `nomad_ca.pem` | Nomad cluster Root Certificate Authority | `0644` |
| `nomad_cli.cert.pem` / `key` | Client CLI credentials for administrative `nomad` commands | `0644` / `0600` |
| `nomad_node.cert.pem` / `key` | Mutual TLS certificates for the Nomad client agent daemon | `0644` / `0600` |
| `consul_ca.pem` | Consul Root CA certificate | `0644` |
| `consul_token` | Scoped Consul ACL bootstrap token for service registration | `0600` |
| `authorized_keys` | Operator SSH public keys (including FIDO/FIDO2 hardware keys) | `0600` |

---

## 💿 Building and Burning the ISO

There are two methods to prepare installation media with the extracted credentials:

### Method A: USB Injection (Generic ISO + Dynamic `CONFIGS` Partition)

This method writes a standard ISO to a USB flash drive and appends a dedicated FAT32 partition labeled `CONFIGS` containing the credentials. This allows using the same base ISO while updating or rotating keys per flash:

```bash
cd os-image
sudo ./build_iso.sh --flash --inject /tmp/cluster_keys_bundle
```

The script will:
1. Identify connected USB drives.
2. Flash the hybrid bootable ISO.
3. Automatically allocate a second FAT32 partition labeled `CONFIGS`.
4. Copy the keys bundle into the `CONFIGS` partition.

Alternatively, use the interactive wrapper [`scripts/imprint_usb_keychain.sh`](../scripts/imprint_usb_keychain.sh):
```bash
./scripts/imprint_usb_keychain.sh 192.168.1.148
```

### Method B: Pre-Bundled ISO (Unattended Burning / Virtual Media / BMC)

For deployments via IPMI/iKVM virtual media, PXE, or multi-node CD burning where secondary USB partitions are impractical, pre-bundle the keys directly into the ISO filesystem:

```bash
cd os-image
sudo ./build_iso.sh --keys-bundle /tmp/cluster_keys_bundle
```

This bakes the credentials directly into `/opt/cluster_keys` inside the read-only squashfs image.

---

## ⚡ First-Boot Auto-Enrollment Behavior

When a bare-metal machine boots from the provisioned media:

1. **Hardware Clock Sync**: The system launches `chrony` and runs `chronyc makestep` to synchronize time with UTC, preventing Debian mirror signature errors.
2. **Credential Detection**: [`00-usb-imprint.sh`](../initial-setup/modules/00-usb-imprint.sh) searches for `/opt/cluster_keys` or a disk partition labeled `CONFIGS`.
3. **SSH Setup**: Injects `authorized_keys` into `/home/pipecatapp/.ssh/authorized_keys` with `0600` permissions.
4. **Mesh Joining**: Launches Tailscale and connects to Headscale (`tailscale up --login-server=... --authkey=...`). The node receives an IP in the `100.64.0.0/10` overlay network.
5. **Certificates & Trust Store**:
   - Copies Root CAs to `/etc/nomad.d/tls/ca.pem` and `/etc/consul.d/ca.pem`.
   - Appends Root CAs to `/usr/local/share/ca-certificates/` and runs `update-ca-certificates`.
   - Copies node and CLI mTLS certificates and keys.
6. **Consul & Nomad Startup**: Starts client daemons, joins the cluster via `retry_join = ["100.64.0.1"]`, and registers with the cluster orchestrator.
7. **Frontend Startup**: Pipecat Mission Control launches and binds to `0.0.0.0:8007`, serving local users and proxying cluster requests.

---

## 🔍 Verification & Health Checks

Once the node boots, verify its cluster status from the controller or any connected workstation:

```bash
# Complete cluster audit (Mesh, Consul, Nomad, Web frontends)
./scripts/cluster_ctl.sh status

# Test distributed task execution on the newly joined node
./scripts/cluster_ctl.sh test-job
```

### Manual Joining Fallback

If an existing worker node was booted without pre-copied credentials, use the remote join script from the controller:

```bash
./scripts/join_worker.sh --worker-ip <WORKER_LAN_IP> --node-id <UNIQUE_ID>
```
