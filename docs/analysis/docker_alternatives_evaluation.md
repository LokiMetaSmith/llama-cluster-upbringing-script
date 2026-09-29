# Architectural Evaluation: Moving Away from Docker

Moving away from Docker makes substantial sense, especially on CPU-bound and storage-constrained nodes where Docker’s daemon overhead, build cache accumulation, and `vfs`/`overlay2` layer bloat create constant friction.
Here is an architectural evaluation of the alternatives, how they integrate into an orchestrated Linux environment (like Nomad), and whether they solve the underlying storage pain.

---

## Why Docker Becomes a Liability on Lean Nodes

1. **Storage Multiplying (`vfs` vs. COW):** If nested environments or restricted permissions force the Docker engine into the `vfs` storage driver, copy-on-write is disabled. Every `RUN` and `COPY` layer duplicates the entire root filesystem, exhausting disk blocks and inodes rapidly.
2. **Build Cache and Layer Retention:** The Docker daemon retains intermediate layer caches and buildkit state unless aggressively and continuously pruned.
3. **Daemon Footprint:** `dockerd` and `containerd` maintain persistent state, background shims, and health-check loops even when idle, introducing memory and CPU jitter.

---

## The Viable Alternatives

| Runtime / Driver | Type | Nomad Native? | Storage Architecture | Daemon Overhead | Best Use Case |
| --- | --- | --- | --- | --- | --- |
| **Nomad `exec` Driver** | Chroot / cgroups v2 | **Built-in** | Direct host filesystem | **None** (zero daemons) | Lightweight services, CLI tools, Python/Node daemons |
| **LXC / Incus** | System Containers | Community plugin (`nomad-driver-lxc`) | Single rootfs (subvolume, ZFS/Btrfs, ext4) | Minimal background daemon | Stateful persistent services (Postgres, Gitea, IPFS) |
| **`containerd`** | OCI Container Engine | Plugin (`nomad-driver-containerd`) | Native Snapshotters (overlayfs) | Low (daemon, but no Docker layer) | Drop-in OCI replacement without Docker CLI/daemon |
| **Podman** | Daemonless OCI | Plugin (`nomad-driver-podman`) | Native rootless overlay / shared storage | **None** (fork/exec per task) | Drop-in Docker replacement without persistent daemon |

---

## Option 1: Native Nomad `exec` / `raw_exec` (Zero-Overhead)

Because Nomad already runs on the host with detected, healthy `exec` and `raw_exec` drivers, you can run workloads directly using Linux cgroups v2 and namespace isolation without any container runtime.

* **How it works:** Nomad provisions an isolated chroot environment, isolates process namespaces (IPC, NET, PID, UTS), and enforces CPU/memory boundaries using cgroups v2.
* **Storage impact:** **Zero layer duplication.** Files are run either directly from host paths or from an unpacked release archive. There is no overlayfs layer stack, no image build steps, and no builder cache.
* **Drawback:** Dependencies must exist in the host environment (or be provided via virtual environments, standalone binaries, or system packages installed via Ansible).

## Option 2: LXC / Incus (System Containers)

Instead of packaging ephemeral application layers into OCI blobs, LXC treats containers like lightweight Linux machines sharing the host kernel.

* **Storage impact:** An LXC container uses a single, flat root directory or a dedicated Btrfs/ZFS subvolume. Updating a package (`apt-get upgrade`) modifies files in-place rather than writing new immutable layers.
* **Best fit:** Heavy, stateful services with large data footprints (IPFS, databases, Gitea, media indexing). Because IPFS manages its own internal sharded blockstore, running it inside LXC prevents Docker from trying to layer-manage or snapshot the container’s underlying disk.
* **Nomad integration:** Can be scheduled via `nomad-driver-lxc`, or managed as persistent system infrastructure via Ansible.

## Option 3: Replace `dockerd` with `containerd` or Podman

If maintaining standard OCI images (from Dockerfiles or registries) is necessary for portability:

* **Containerd:** Running `nomad-driver-containerd` talks directly to the containerd socket. It eliminates `dockerd`, bypassing the high-level Docker engine, its bridge networking conflicts, and its independent volume database.
* **Podman:** Podman operates without any central daemon. When Nomad launches a task, it executes `podman run` directly as a child process. If the task stops, the process exits cleanly—no orphaned dockerd state, no dead container shims left behind.

---

## Practical Migration Path

1. **Move I/O-Heavy Storage Daemons to Host / `exec`:** Services that manage their own blockstores (such as IPFS) or local databases run much cleaner as direct system services or Nomad `exec` tasks using host volumes. This eliminates container filesystem translation layers and prevents runaway overlay bloat.
2. **Eliminate In-Sandbox Docker Builds:** If building tool images, avoid running `docker build` with `vfs` inside resource-constrained sandboxes. Build images on a staging runner using native `overlay2` or `buildah`, push to a local registry (like Gitea), and pull pre-built images.
3. **Adopt Podman or `containerd` for Remaining OCI Tasks:** Swap the Nomad `docker` driver for `nomad-driver-podman` or `nomad-driver-containerd` to drop the heavy Docker daemon while preserving existing Dockerfiles.

---

## Implementation Roadmap & Action Items

### Phase 1: High-I/O Storage Decoupling (Immediate Wins)

*IPFS manages its own sharded blockstore. Running it under Docker adds overhead and contributes heavily to overlay/disk exhaustion. We will migrate it to run natively.*

* [ ] **Create native IPFS Nomad job template**
  * Update `ansible/roles/ipfs/templates/ipfs.nomad.j2` to use the `exec` or `raw_exec` driver instead of `docker`.
  * Remove the Docker `image` declaration and instead execute the locally installed `/usr/local/bin/ipfs` binary.
* [ ] **Adjust IPFS Ansible role**
  * Ensure `ansible/roles/ipfs/tasks/main.yaml` handles Kubo binary extraction, `/usr/local/bin` placement, and permissions correctly across all target nodes.
* [ ] **Data Migration & Validation**
  * Ensure the existing IPFS repository under `/opt/unified_fs_backend/ipfs/` seamlessly transitions to the native daemon without permission errors.

### Phase 2: Build Pipeline & Inode Remediation (Fixing `vfs` bloat)

*The `tool-server` build tasks suffer from inode exhaustion due to Docker `vfs` duplicating entire root filesystems per layer. We need to eliminate nested Docker builds.*

* [ ] **Evaluate Buildah for sandbox building**
  * Create a test Ansible task verifying `buildah` installation and functionality in the cluster environment.
  * Convert `ansible/tasks/build_cached_image.yaml` to use `buildah bud` instead of `docker build`.
* [ ] **Refactor `tool-server` build pipeline**
  * If Buildah is unviable, refactor `ansible/roles/tool_server` to run the tools in native virtual environments directly supervised by Nomad `exec` tasks, skipping containerization entirely.
* [ ] **Purge local Docker build cache**
  * Ensure automated cluster scripts wipe orphaned `vfs` build layers (`/var/lib/docker/vfs`) post-migration to reclaim gigabytes of disk and inodes.

### Phase 3: Runtime Transition & Driver Evaluation

*For remaining auxiliary services (`postgres`, `authentik`, `gitea`, etc.), evaluate swapping the Nomad `docker` task driver.*

* [ ] **Install and configure Podman**
  * Create a new Ansible role `podman` to install the daemonless runtime and dependencies across worker nodes.
* [ ] **Deploy Nomad Podman plugin**
  * Update the `nomad` Ansible role to download and configure `nomad-driver-podman` into Nomad's plugin directory.
* [ ] **Service validation testing**
  * Convert a non-critical service (e.g., `opengist` or `radicle`) in its Nomad job template from `driver = "docker"` to `driver = "podman"` to verify networking, volume mounts, and stability.
* [ ] **Deprecate Docker**
  * Systematically roll out Podman or Containerd to all remaining OCI-based jobs, followed by the complete removal of the Docker daemon from the cluster via Ansible provisioning.
