# Autonomous PXE RAMOS Inspection & Recovery Pipeline (Fleet Architecture: 2016–2026)

## 1. Problem Post-Mortem & Architectural Failure Analysis

In previous provisioning iterations, PXE clients experienced boot-loops or crashed during early boot for the following root causes:

1. **Option ROM Incompatibility on Legacy Hardware (c. 2016)**:
   - Older network interface cards running Intel UNDI 2.1 real-mode BIOS ROMs crash with General Protection Faults or memory freezes when attempting to execute 32-bit `undionly.kpxe`.
   - **Resolution**: Strict DHCP Option 93 (`client-arch`) routing sends 16-bit real-mode `pxelinux.0` to BIOS machines (`Arch:00000`) and native 64-bit `ipxe.efi` to modern UEFI systems (`Arch:00007`/`00009`).

2. **The "Local Boot Freeze" (The Blinking Cursor Bug)**:
   - When netboot installers finished debian preseed setups, they wrote GPT partition tables without a `bios_grub` partition or failed to install `grub-pc` into Sector 0 MBR.
   - When the node booted through PXELINUX and hit `localboot 0`, the BIOS found no boot code on `/dev/sda` Sector 0, leaving an inactive blinking cursor on a black screen.
   - **Resolution**: Deployment of a universal **Hybrid Partition Layout**:
     - Partition 1 (`1 MiB`, `EF02`): Unformatted BIOS Boot Partition where `grub-install --target=i386-pc` embeds `core.img`.
     - Partition 2 (`512 MiB`, `EF00`): FAT32 EFI System Partition (`/boot/efi`) with `BOOTX64.EFI`.
     - Partition 3 (`Rest of disk`, `8300`): Linux root filesystem (`ext4`) labeled `rootfs`.
     - Sector 0: Protective MBR with Stage 1 bootloader.

3. **Installer Flapping Loop**:
   - Without an inspection step, any netboot client repeatedly booted into the netboot installer over and over again upon rebooting.
   - **Resolution**: The default network target boots a dedicated Debian Live RAM rootfs (**RAMOS**). Local disks are NEVER written to until an automated audit is performed.

---

## 2. Recovery Workflow Architecture

```
                       PXE Network Boot (DHCP Option 93)
                                      │
            ┌─────────────────────────┴─────────────────────────┐
            ▼                                                   ▼
   Legacy BIOS (Arch 0)                                UEFI (Arch 7/9)
   pxelinux.0 + ldlinux.c32                            ipxe.efi
            │                                                   │
            └─────────────────────────┬─────────────────────────┘
                                      ▼
                        Boot RAMOS Live Maintenance Rootfs
                     (vmlinuz + initrd.img + filesystem.squashfs)
                                      │
                                      ▼
                      Autonomous Audit Agent (node_health_check.sh)
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
 [1] Storage Discovery       [2] SMART Integrity Check    [3] Filesystem & Version Audit
 - nvme0n1 / sda detection   - smartctl -H                - Read-only e2fsck -n -f
 - Non-removable filter      - Halt & Quarantine if bad   - Check /etc/cluster-version
                                                          - Check crash flags
                                                                   │
                                        ┌──────────────────────────┴──────────────────────────┐
                                        ▼                                                     ▼
                            [Disk Outdated / Damaged]                              [Node Healthy & Current]
                                        │                                                     │
                                        ▼                                                     ▼
                        Automated Re-imaging (node_reimage.sh)                      Direct kexec handoff
                        - Staggered jitter delay                                    into local disk kernel
                        - Evict old Raft / swarm node identity                      (Zero-reboot handoff)
                        - Stream debian-golden-node.img.zst
                        - Expand GPT partition boundaries
                        - Inject unique hostname, machine-id, SSH keys
                        - Re-arm cluster state
```

---

## 3. Substrate Artifacts & Locations

| Component | Path on Controller (`192.168.1.148`) | Serving Protocol |
| :--- | :--- | :--- |
| **TFTP Root** | `/srv/tftp/` | TFTP (Port 69) |
| **PXELINUX Binary** | `/srv/tftp/pxelinux.0` | TFTP |
| **PXELINUX Modules** | `/srv/tftp/*.c32` (`ldlinux.c32`, etc.) | TFTP |
| **PXELINUX Config** | `/srv/tftp/pxelinux.cfg/default` | TFTP |
| **UEFI iPXE Binary**| `/srv/tftp/ipxe.efi` | TFTP |
| **RAMOS Kernel** | `/srv/tftp/live/vmlinuz` & `/var/www/html/live/vmlinuz` | TFTP / HTTP (Port 80) |
| **RAMOS Initrd** | `/srv/tftp/live/initrd.img` & `/var/www/html/live/initrd.img` | TFTP / HTTP |
| **RAMOS SquashFS** | `/var/www/html/live/filesystem.squashfs` (zstd, 4.7 GB) | HTTP |
| **Golden Disk Image**| `/var/www/html/images/debian-golden-node.img.zst` (4.6 GB) | HTTP |
| **Control Plane API**| `http://192.168.1.148:8007/api/` | HTTP |

---

## 4. Key CLI Commands & Maintenance Playbook

### Query Node Status & History
```bash
curl -s http://192.168.1.148:8007/api/cluster/nodes | jq .
```

### Inspect Target Image Version
```bash
curl -s http://192.168.1.148:8007/api/cluster/target-version
```

### Force Node Re-Image (Set Version Upgrade)
```bash
curl -X POST http://192.168.1.148:8007/api/cluster/target-version \
     -H "Content-Type: application/json" \
     -d '{"version": "2026.10.07-v2"}'
```

### Monitor PXE / DHCP Boot Activity
```bash
journalctl -u isc-dhcp-server -u tftpd-hpa -f
```
