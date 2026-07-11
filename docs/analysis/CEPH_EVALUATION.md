# Ceph Storage Cluster Evaluation Report

## 1. Overview

This report evaluates the **Ceph Storage Cluster** for potential inclusion in our Distributed Conversational AI Pipeline architecture.

A Ceph Storage Cluster is a highly scalable, open-source, software-defined storage platform. It eliminates single points of failure by pooling commodity hardware to provide unified Block Storage (RBD), Object Storage (RGW), and File Storage (CephFS). A functional cluster relies on three core types of daemons working together via the Reliable Autonomic Distributed Object Store (RADOS):
- **Ceph OSDs (Object Storage Daemons):** Store, replicate, and recover actual data across physical drives on storage nodes.
- **Ceph Monitors (MONs):** Maintain the master map of the cluster state and node health, ensuring all clients know exactly where to locate data.
- **Ceph Managers (MGRs):** Track runtime metrics, manage quotas, and provide the cluster’s graphical web dashboard.

### Current Storage Architecture
Currently, our pipeline maintains hardware agnosticism and optimizes storage footprint across our legacy cluster using a hybrid distributed model:
- **Distributed FS / Share:** A shared distributed file system mounted at `unified_fs_mount_point` serves as the primary cross-node storage.
- **IPFS with Filestore Optimization:** An IPFS daemon (`kubo`) is configured with the experimental `FilestoreEnabled` setting. Multi-gigabyte machine learning models (e.g., GGUF, Whisper, TTS models) are seeded into the cluster using `ipfs add --nocopy`, which avoids physical duplication by referencing the raw byte data directly on the distributed mount.
- **Ephemeral Files:** Temporary Docker images and build artifacts are loaded directly without `--nocopy` to prevent datastore corruption.

---

## 2. Evaluation Criteria

We evaluate Ceph against our specific cluster constraints: **legacy hardware** (Core 2 Duo, 8GB RAM), **mesh networking over Tailscale**, **massive machine learning models** (GGUF), and **deployment simplicity**.

### 2.1. Legacy Hardware & Resource Constraints
- **Ceph Requirements:** Ceph is resource-intensive. Typically, Ceph recommends at least 1 GB of RAM per 1 TB of OSD storage, plus additional RAM for MON and MGR daemons (often 2–4 GB each). For maintaining monitor quorum, a minimum of three nodes is recommended.
- **Our Hardware Context:** Our cluster consists of legacy machines with limited resources (e.g., Intel Core 2 Duo and only 8 GB of RAM). Running Ceph's OSD, MON, and MGR daemons alongside heavy AI tasks (e.g., localized GGUF inference, vision processing, speech synthesis) would severely deplete available RAM, leading to memory swapping and potential OOM (Out Of Memory) crashes.
- **Verdict:** Ceph's daemon overhead is too heavy for legacy 8 GB RAM machines.

### 2.2. Network Constraints (Tailscale and 1GbE Mesh)
- **Ceph Requirements:** Fast, dedicated networking is essential. Ceph requires robust bandwidth and extremely low latency, with 10 GbE or higher being the enterprise standard for separating public and cluster/replication traffic. Low-latency interconnects are necessary to prevent MON timeouts and OSD flapping.
- **Our Network Context:** Our cluster communicates strictly over a `tailscale0` VPN mesh interface, often bound by physical 1 GbE ethernet or Wi-Fi links on legacy hardware. Running Ceph’s high-frequency heartbeat and background data replication over an encrypted VPN mesh layer would saturate the network, introduce severe latency spikes, and degrade real-time conversational streaming (which requires low-latency Audio and STT/TTS round-trips).
- **Verdict:** Mesh networking over Tailscale/1GbE is incompatible with Ceph's performance demands.

### 2.3. ML Model Storage & GGUF Workloads
- **Current Setup:** Our IPFS `FilestoreEnabled` (`--nocopy`) optimization lets us reference large models directly from a shared distributed mount without duplicating gigabytes of storage across every single host.
- **Ceph Setup:** While CephFS can store these files, or RGW can expose them via S3 API, Ceph's standard replication models (typically 3x replication) would copy these multi-gigabyte models across multiple physical nodes. While erasure coding could mitigate this, the computational overhead of EC on old Core 2 Duo CPUs is extremely high.
- **Verdict:** IPFS with `--nocopy` is far more efficient for distributing large static ML assets on our constrained, heterogeneous legacy hardware.

### 2.4. Operation & Provisioning Complexity
- **Current Setup:** Our shared filesystem and IPFS setup are lightweight, easy to provision via basic Ansible tasks, and require minimal background orchestration or health monitoring.
- **Ceph Setup:** Ceph introduces significant administrative complexity (CRUSH maps, keyring distributions, cluster health checks, and PG/placement group tuning). Any network partition on our wireless/Tailscale links would trigger recovery loops, causing massive disk I/O and CPU spikes on the legacy nodes.
- **Verdict:** The operational complexity of Ceph significantly outweighs its benefits for this specific project.

---

## 3. Pros and Cons Breakdown

| Category | Ceph Storage Cluster | Current Stack (Unified FS + IPFS `--nocopy`) |
| :--- | :--- | :--- |
| **Pros** | - Unified Block, Object, and File storage.<br>- Self-healing, enterprise-grade redundancy.<br>- Exabyte-scale potential.<br>- No single point of failure (RADOS replication). | - Extremely lightweight CPU/RAM footprint.<br>- Zero-copy distribution of multi-gigabyte models via IPFS Filestore.<br>- Highly tolerant to network latency/Tailscale overhead.<br>- Simplistic Ansible orchestration. |
| **Cons** | - High RAM/CPU overhead (incompatible with 8GB Core 2 Duo nodes).<br>- Requires dedicated 10GbE networking.<br>- Complex to configure, manage, and recover.<br>- Heavy background write/rebuild latency. | - Shared mount can become a single point of failure (if not backed by distributed storage).<br>- Lacks native raw block device pooling.<br>- IPFS `--nocopy` requires care to avoid file reference breaks. |

---

## 4. Final Recommendation

### **Do we need Ceph?**
**No, we do not recommend integrating a Ceph Storage Cluster into our legacy pipeline.**

While Ceph is an outstanding enterprise storage platform, its physical resource requirements (RAM, CPU, 10GbE low-latency networking) directly conflict with our constraints. Deploying Ceph on a cluster of legacy Core 2 Duo machines with 8GB RAM running over a Tailscale mesh would lead to severe resource contention, high network latency, and cluster instability.

### **Alternative Strategic Actions**
1. **Strengthen the Shared Filesystem:** Instead of Ceph, we should focus on making the `unified_fs_mount_point` more resilient (e.g., using a lightweight, latency-tolerant DFS such as GlusterFS configured with replica-2 or a simple thin-provisioned NFS with automated backup scripts).
2. **Double-down on IPFS Offloading:** Maintain the IPFS `FilestoreEnabled` `--nocopy` strategy for large ML weights, and use pinning services or peer-to-peer syncing only for necessary active nodes to minimize RAM/disk consumption.
3. **Automate recovery via Btrfs snapshots:** Continue using our `btrfs_snapshot` Ansible role and `recover_os.py` scripts to protect and restore node state instantly, keeping our persistent data layer simple, predictable, and highly performant.
