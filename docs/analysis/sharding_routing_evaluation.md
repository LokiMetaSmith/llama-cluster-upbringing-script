# Architectural Analysis: Database Sharding and Routing for PMMMemory

## 1. Executive Summary

As the Distributed Conversational AI cluster scales, the central `PMMMemory` store (utilizing SQLite/FAISS) becomes a primary bottleneck. Because SQLite lacks native distributed scale-out architecture, running a single monolithic SQLite instance on shared storage under high write contention can lead to locking issues (`database is locked`), high disk I/O latency, and serialization blockages.

To scale the swarm efficiently on legacy hardware without introducing heavy, containerized distributed databases like Vitess, this document proposes a **Lightweight Python-based Sharded Database Proxy and Router** within the `pipecatapp` ecosystem.

This analysis details the architectural impacts on GlusterFS distributed mount points, Btrfs-based snapshot recovery, and the consensus visibility of Agent Work Ledgers (Gas Town beads), and establishes a concrete blueprint for the sharded proxy router implementation.

---

## 2. Table of Contents

- [1. Executive Summary](#1-executive-summary)
- [2. Table of Contents](#2-table-of-contents)
- [3. Current Bottlenecks & Sharding Architecture](#3-current-bottlenecks--sharding-architecture)
- [4. Integration with GlusterFS and Btrfs Recovery](#4-integration-with-glusterfs-and-btrfs-recovery)
- [5. Agent Work Ledgers & Consensus Visibility](#5-agent-work-ledgers--consensus-visibility)
- [6. Technical Specification for the Sharded PMMMemory Proxy](#6-technical-specification-for-the-sharded-pmmmemory-proxy)
- [7. Anti-Rationalization & Verification Safeguards](#7-anti-rationalization--verification-safeguards)

---

## 3. Current Bottlenecks & Sharding Architecture

### Monolithic Bottlenecks
The current `PMMMemory` implementation records:
1. **Cognitive Events** (`events` table) - Append-only, event-sourced chain with SHA-256 links.
2. **Work Items / beads** (`work_items` table) - Gas Town tasks tracked by agents.
3. **Dead Letter Queue** (`dlq` table) - Failures and retries.

Under a unified SQL database file on GlusterFS/NFS, concurrent write locks from worker nodes cause transaction serialization overhead. WAL mode mitigates this partially, but distributed filesystems often struggle with the lock-arbitration and POSIX locking required by SQLite's WAL, resulting in performance degradation.

### The Sharded Proxy Approach
Instead of a single database, the storage is partitioned into $N$ SQLite shards based on a routing hash:

$$\text{Shard ID} = \text{Hash}(\text{Routing Key}) \pmod N$$

#### Sharding Keys:
- **Events:** Sharded by `kind` or `session_id` (meta).
- **Work Items:** Sharded by `id` (or `assignee_id`/agent ID).
- **DLQ:** Sharded by `event_type` or item `id`.

This spreads the write pressure, ensuring that write-heavy workers talking to different shards never lock each other.

---

## 4. Integration with GlusterFS and Btrfs Recovery

### 4.1. GlusterFS Distributed Mount Points
GlusterFS handles distributed replication. Placing multiple small SQLite shard files (e.g., `shard_0.db`, `shard_1.db`) across GlusterFS rather than a single monolithic file provides:
- **Parallel File I/O:** GlusterFS distributes different files across different bricks/disks, bypassing single-file locking bottlenecks.
- **Lower Network Serialization:** Nodes only lock the specific partition/file they are writing to, reducing GlusterFS metadata lock lockup.

### 4.2. Local Node Recovery and Btrfs Snapshots
Our cluster implements automated pre-deployment Btrfs snapshots of `/opt/pipecatapp`.
- **Consistent Backups:** Sharded SQLite databases must be snapshotted consistently. Because shards are separate files, backup processes must use `BEGIN IMMEDIATE` or lock writing during snapshotting to prevent transactional inconsistency across shards.
- **Node-Local SQLite Storage:** To maximize performance, shards can be placed on node-local SSD storage (`/var/lib/pipecatapp/shards/`), while sync/ledger replication processes aggregate them to GlusterFS asynchronously.
- **Disaster Recovery:** If a node crashes, restoring from a Btrfs snapshot restores its local shards to a known historical point. The router must then handle stale shards by pulling missing event logs or work items from peer nodes.

---

## 5. Agent Work Ledgers & Consensus Visibility

In a partitioned database topology, maintaining a global consensus view of task states (Gas Town Work Ledgers) is challenging. If Work Item A is on Shard 0, and Work Item B is on Shard 1, a global query like `list_work_items()` requires a **scatter-gather pattern**.

### 5.1. Maintaining Consensus Visibility
1. **Scatter-Gather Execution:** The sharded proxy broadcasts read queries across all registered shards and merges/deduplicates/sorts the results in-memory before returning them.
2. **Conflict Resolution:** For synchronizations, `sync_work_items_sync` uses the existing `updated_at` timestamps to resolve conflicting states across shards.
3. **Consolidated Indexing / Read-Replicas:** A dedicated, lightweight "Global Consensus Ledger" can act as an indexed read-replica, while the write-heavy events remain sharded.

---

## 6. Technical Specification for the Sharded PMMMemory Proxy

The proposed python proxy `ShardedPMMMemory` wraps multiple `PMMMemory` instances under the same interface.

```python
import hashlib
from typing import Dict, Any, List, Optional
from pipecatapp.pmm_memory import PMMMemory

class ShardedPMMMemory:
    def __init__(self, shard_paths: List[str]):
        self.shards = [PMMMemory(db_path=path) for path in shard_paths]
        self.num_shards = len(shard_paths)

    def _get_shard_index(self, routing_key: str) -> int:
        hasher = hashlib.md5(routing_key.encode("utf-8"))
        return int(hasher.hexdigest(), 16) % self.num_shards

    # Event Sourcing sharded by kind or metadata session
    def add_event_sync(self, kind: str, content: str, meta: Optional[Dict[str, Any]] = None) -> None:
        key = meta.get("session_id", kind) if meta else kind
        shard_idx = self._get_shard_index(key)
        self.shards[shard_idx].add_event_sync(kind, content, meta)
```

### Full Multi-Shard Operations
- **Writes:** Directed to a single shard based on the routing key.
- **Point Reads:** Decided by hashing the resource identifier (e.g., `get_work_item(item_id)` hashes `item_id`).
- **Scans / Lists:** Query all shards in parallel/sequence and combine.

---

## 7. Anti-Rationalization & Verification Safeguards

To prevent bypassing critical safeguards during development and deployment:

| Excuse / Pitfall | Counter-Strategy / Safe Pattern |
| :--- | :--- |
| "The database is small, sharding is overkill." | Legacy hardware crashes quickly under sudden concurrency bursts. Edge nodes will fail without sharding under heavy swarm sizes. |
| "Writing to all shards on scans is too slow." | Implement in-memory caches and leverage SQLite's indexes properly on each shard. |
| "Local Btrfs snapshot restores can corrupt state." | Implement automated synchronization routines (`sync_work_items`) to catch up after rollback. |

### Verification Protocol
1. **Unit Tests:** Direct verification of routing hashing, scatter-gather lists, and atomic shard updates.
2. **Performance Benchmarks:** Compare locking and writing performance under concurrent thread stress tests.
