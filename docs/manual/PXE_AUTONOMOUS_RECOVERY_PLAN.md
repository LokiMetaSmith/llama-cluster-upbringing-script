# Autonomous PXE Recovery & Swarm Re-imaging Plan

**Document Version:** 1.0.0  
**Status:** In Progress / Active Implementation  
**Audience:** Cluster Engineers, Automated SRE Agents, and Autonomous Healing Daemons

---

## 1. Executive Summary

This document specifies the architecture, state-machine transitions, and implementation for the autonomous PXE recovery pipeline across the Pipecat bare-metal cluster.

Rather than blindly running a destructive Debian installer or netboot preseed on every network boot, the PXE infrastructure delegates boot decisions to an intelligent inspection layer. New and rebooting nodes load a lightweight Debian Live RAM rootfs (maintenance RAMOS) that audits physical hardware, verifies filesystem integrity, inspects the current cluster version, and either boots into the existing healthy installation via `kexec` or autonomously re-images and reconciles the node with the cluster control plane.

---

## 2. Recovery Architecture & Decision Flow

```
PXE Boot (iPXE / TFTP ROM)
       │
       ▼
Query Controller Decision API
http://${server_ip}:8007/api/pxe/boot-decision?mac=${net0/mac}
       │
       ├───────────────────────────────────────┬───────────────────────────────────────┐
       ▼                                       ▼                                       ▼
 [ BOOT_LOCAL ]                         [ QUARANTINE ]                         [ AUDIT_RECOVER ]
 (Verified Healthy)                    (Hardware Failure)                     (Unknown/Dirty/Audit)
       │                                       │                                       │
       ▼                                       ▼                                       ▼
Exit iPXE to Local Drive              Halt Boot & Alert                      Stream Minimal RAMOS
(Fast-path direct boot)              (Prevent Wear Loops)                  (vmlinuz + initrd + squashfs)
                                                                                       │
                                                                                       ▼
                                                                           Execute Node Health Check
                                                                         (/usr/local/bin/node-audit.sh)
                                                                                       │
                         ┌─────────────────────────────────────────────────────────────┤
                         ▼                                                             ▼
                SMART Hardware Audit                                       Target Disk Discovery
                smartctl -H ${DISK}                                       (/dev/disk/by-id/ / lsblk)
                         │                                                             │
                  Corrupted / Failing                                                  ▼
                         │                                                 Filesystem Integrity Check
                         ▼                                                 e2fsck -n -f ${ROOT_PART}
                POST /api/cluster/quarantine                                           │
                (Enter low-power halt)                                 ┌───────────────┴───────────────┐
                                                                       ▼                               ▼
                                                               Clean Filesystem               Corrupted / Unreadable
                                                                       │                       (FSCK Code >= 4)
                                                                       ▼                               │
                                                               Mount / Read-Only                       │
                                                                       │                               │
                                                       ┌───────────────┴───────────────┐               │
                                                       ▼                               ▼               │
                                              Version Matches                  Version Outdated        │
                                              & No Crash Flag                  or Crash Flag Present   │
                                                       │                               │               │
                                                       ▼                               ▼               │
                                              Fast-Path Local Boot            [ AUTONOMOUS RE-IMAGE ] ◄┘
                                              kexec -l /boot/vmlinuz          • Jitter Backoff
                                              (Seamless < 2s boot)            • Nomad / Consul Eviction
                                                                              • Stream Golden Image (.img.zst)
                                                                              • Inject Machine Identity & Keys
                                                                              • Post-Flash Reboot
```

---

## 3. Operational Edge Cases & Hardening Matrix

| Risk / Edge Case | Failure Mode Without Guardrails | Mitigation Implemented |
| :--- | :--- | :--- |
| **Swarm Identity Desync** | Re-imaged node generates new ID; dead node records linger in Nomad and Consul, draining quorum and stranding task allocations. | Pre-flash eviction hook (`/api/cluster/evict`) drains Nomad nodes and removes Consul Serf members prior to disk wipe. |
| **Thundering Herd Bandwidth Collapse** | Rack-wide reboot causes concurrent multi-gigabyte image downloads, saturating 1GbE switch uplinks. | Deterministic MAC-based jitter delay (`0xMAC % 30`) + optional P2P/IPFS mesh distribution. |
| **Hardware Death Spiral** | Dying NAND blocks cause immediate corruption after re-image; node enters infinite reboot/flash loop. | Pre-flash SMART audit (`smartctl -H`); failing drives are reported to `/api/cluster/quarantine` and quarantined. |
| **Device Name Drift** | Target disk shifts between `/dev/sda` and `/dev/nvme0n1` when USB thumb drives or additional PCIe devices exist. | Non-removable drive filter (`RM==0`) and stable disk identification via `/dev/disk/by-id/` and `udevadm`. |
| **Data Loss on Cluster Volumes** | Persistent model caches (IPFS, Nomad allocation data, Docker storage) wiped on every recovery. | Partition isolation: only root OS partition (`part2`) is flashed; persistent data partition (`part3`) is preserved. |
| **PXE vs Local Boot Loops** | When BIOS boots PXE first, node reboot loops through PXE on every clean start. | Dynamic iPXE API returns `exit 1` for nodes with verified clean audit states, immediately handing off to local disk. |
| **Zero-Reboot POST Delay** | Legacy workstations take 30–60s for full hardware POST on reboot. | Healthy audits use Linux `kexec` to boot the on-disk kernel directly from memory without rebooting hardware. |

---

## 4. Implementation Checklist & Progress Tracker

- [x] **Phase 1: Architecture Specification & Planning**
  - [x] Define recovery state machine and decision flow.
  - [x] Document edge cases, hardware quarantine, and partition preservation policies.
  - [x] Create comprehensive manual in `docs/manual/PXE_AUTONOMOUS_RECOVERY_PLAN.md`.

- [x] **Phase 2: Controller API Endpoints (`pipecatapp/web_server.py`)**
  - [x] Implement `GET /api/pxe/boot-decision`: Dynamic iPXE dispatcher.
  - [x] Implement `GET /api/cluster/target-version`: Current cluster golden image version.
  - [x] Implement `POST /api/cluster/evict`: Nomad/Consul node drain and eviction hook.
  - [x] Implement `POST /api/cluster/quarantine`: Hardware failure quarantine registration.
  - [x] Implement `POST /api/cluster/node-status`: Node audit status reports.
  - [x] Implement `GET /api/cluster/nodes`: Cluster recovery telemetry and status table.

- [x] **Phase 3: Autonomous Node Maintenance Scripts**
  - [x] Write `scripts/node_health_check.sh`: Drive discovery, SMART, e2fsck, version check, crash flag check, kexec.
  - [x] Write `scripts/node_reimage.sh`: MAC jitter, eviction notification, image streaming, identity injection.
  - [x] Write `scripts/build_recovery_ramos.sh`: Generator script for the maintenance Live RAM rootfs.

- [x] **Phase 4: iPXE Template & PXE Server Integration**
  - [x] Update `ansible/roles/pxe_server/templates/boot.ipxe.j2` with dynamic controller chainloading.
  - [x] Update `ansible/roles/pxe_server/tasks/main.yaml` to deploy maintenance scripts and live boot directory.

- [x] **Phase 5: Automated Testing & Verification**
  - [x] Add unit tests for API endpoints in `pipecatapp/tests/test_pxe_recovery.py`.
  - [x] Validate compilation with `python3 -m compileall -q pipecatapp`.
  - [x] Run test suite and verify clean status.
