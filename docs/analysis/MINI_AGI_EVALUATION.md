# mini-AGI Feature Evaluation & Integration RFC

## 1. Executive Summary

This document evaluates the `mini-AGI` project (<https://github.com/volotat/mini-AGI>) for potential feature scraping and integration into our existing infrastructure. The objective is to analyze its core architectural patterns—specifically **dynamic expert growth**, **disk-to-VRAM weight paging**, and **continuous learning**—and assess the feasibility of adapting these mechanisms as an experimental, background worker without disrupting our low-latency real-time inference pathways (e.g., `llama.cpp`, `moshi`).

## 2. Feature Analysis (Scraping)

The `mini-AGI` project presents several innovative mechanisms designed to enable continuous learning on modest hardware:

### 2.1. Disk-to-VRAM Weight Paging

Instead of keeping the entire model in VRAM, `mini-AGI` stores all experts (and their Adam moments) on disk as independent `.npz` files. A working set (32 experts) is paged into VRAM dynamically based on the demand of the incoming text chunk. This allows the model parameter count to be bounded by disk space rather than VRAM, while keeping VRAM usage strictly within an 8 GB envelope.

* **Serialization & Zero-Copy Paging (`.npz` Replacement):** `mini-AGI` relies on standard NumPy `.npz` files (zipped archives). Decompressing and deserializing ZIP archives on every page-in introduces heavy CPU serialization overhead, negating NVMe IOPS gains. This architecture must be modified to replace `.npz` with flat, uncompressed memory-mapped formats (specifically `safetensors`). By utilizing Rust and the `candle` ML framework (specifically `MmapedSafetensors`), we can achieve true zero-copy direct memory access (DMA) transfers from NVMe into pinned host memory and GPU VRAM via custom CUDA streams, drastically reducing paging latency while avoiding Python's GIL and serialization overhead.

### 2.2. Dynamic Expert Growth (Recombination)

The model dynamically grows its capacity. New experts are added conditionally when the existing pool is saturated, there is sufficient disk/VRAM capacity, and the previous cohort of experts has proven useful. New experts are built by recombining hidden units from existing experts rather than random initialization, ensuring they provide immediate value. Experts that remain unaddressed for long periods are pruned (deleted from disk).

### 2.3. Continuous Learning (Anti-Forgetting)

To prevent catastrophic forgetting when training on a single stream of data, the architecture uses an extremely low learning rate for its shared trunk (embeddings, attention, routers, halting head)—specifically 0.1x the learning rate of the experts. Because the routing mechanism ensures that only a sparse subset of experts receives gradient updates for any given chunk, the majority of the model remains untouched, mitigating displacement of existing knowledge.

* **Continual Learning Regression Gates & Poisoning Defense:** Unbounded single-stream gradient updates are susceptible to catastrophic drift, router collapse (where a small subset of experts hogs all tokens), or adversarial data poisoning. We will introduce an automated **frozen regression benchmark**. Every $N$ iterations (or during scheduled "sleep cycles"), training is paused and the model evaluated against a static, ground-truth validation set. If loss or perplexity degrades beyond a set tolerance threshold, the recent expert deltas are discarded and rolled back to the last known healthy snapshot.

## 3. Hardware & I/O Feasibility

Adapting `mini-AGI`'s mechanisms to our Nomad cluster presents significant hardware and I/O challenges:

### 3.1. I/O Constraints and Storage

The paging mechanism relies heavily on rapid disk reads to swap experts into VRAM.

* **OverlayFS Bottlenecks:** By default, our Docker/Nomad tasks utilize OverlayFS, which introduces significant I/O bottlenecks. Running `mini-AGI`'s paging over OverlayFS or network storage will result in severe I/O stalls, completely bottlenecking the continuous learning process.
* **Mitigation:** If deployed, the task must be configured with native Nomad `volume {}` and `volume_mount {}` blocks mapping to dedicated, raw NVMe `host_volume` paths, entirely bypassing the Docker driver's inline OverlayFS mounts.

### 3.2. VRAM and Compute Envelope

* **8 GB VRAM Baseline:** `mini-AGI` is explicitly designed for an 8 GB VRAM GPU. Our baseline nodes (e.g., the Jules environment) have roughly 7.8 GiB of total system RAM and rely heavily on CPU fallbacks when GPUs are constrained.
* **Coexistence:** Allocating a dedicated 8 GB VRAM GPU to a continuous learning worker may conflict with the resources required by our primary real-time inference stack (`llama.cpp`, `moshi`). For this to work, we would need Nomad placement constraints targeting specific high-capacity GPU nodes (using our precise hardware tags like `accel-npu`, `inst-avx512`, etc.) and ensure it does not preempt critical inference tasks. Operating this via CPU fallback would be unfeasibly slow for continuous gradient updates.
* **VRAM Allocation & Fragmentation Shielding:** Dynamically allocating and deallocating tensors in PyTorch VRAM during continuous expert swapping leads to severe CUDA allocator heap fragmentation, eventually causing out-of-memory (OOM) errors even when aggregate VRAM usage is under 8 GB. By implementing this in Rust with `candle`, we must mandate a **static pre-allocated VRAM pool** (ring buffer/slot system). Pre-allocate fixed VRAM slots for the 32 active experts at process initialization. When an expert is paged in, we will execute direct buffer writes into an existing slot's pre-allocated memory address rather than invoking dynamic allocation routines at runtime.

## 4. Proposed Integration Points

Since `mini-AGI` is not intended to replace our fast MoE gateway, it should be treated as an asynchronous, long-running experimental worker. It will be implemented as a **standalone Rust workspace crate** (e.g., `services/mini-agi-worker`). It will intentionally not be coupled to the existing `moshi` codebase to ensure experimental memory paging and background gradient routines never impact latency-critical voice threads.

1. **Background Learner Task (Nomad Job):**

   * Deploy as a low-priority Nomad `raw_exec` or Docker job with strict placement constraints for GPU capability and explicit NVMe host-volume mounts.
   * Configure it to ingest logs, user interactions, or specific system data streams asynchronously, acting as a background "sleep replay" or continual adaptation loop.

2. **MoE Gateway Integration:**

   * The background worker could expose a specialized routing endpoint or occasionally export refined knowledge facts to the `DatalogEngine` ledger.
   * It could serve as a specialized backend for tasks requiring high adaptation but no strict latency guarantees, entirely isolated from the main `MoE Gateway` hot-path.

3. **Nomad Node Mobility & State Persistence:**

   * Nomad `host_volume` paths are node-local. If the host node restarts, drains, or reschedules the allocation, dynamically learned weights, Adam states, and expert topologies remain stranded on that specific NVMe drive.
   * We will architect an asynchronous **snapshot daemon** or checkpointing task. Periodically archive modified expert weights and the routing topology to IPFS or cluster object storage, and register an `ephemeral_disk` or warm-up hook in the Nomad job template to restore the active expert set on rescheduling.

4. **Observability & Prometheus Instrumentation:**

   * Integrate native Prometheus instrumentation to expose operational metrics to the monitoring stack, including:
     * `mini_agi_expert_page_latency_seconds` (histogram measuring NVMe-to-VRAM transfer latency).
     * `mini_agi_expert_cache_hit_ratio` (router locality tracking).
     * `mini_agi_expert_total_count` (gauge monitoring dynamic expert growth and pruning).
     * `mini_agi_trunk_loss` vs. `mini_agi_expert_loss` (divergence tracking).

## 5. Pros and Cons

### Pros

* **Boundless Capacity:** Disk-based paging allows for theoretical unbounded growth of the model's knowledge base.
* **Isolation of Knowledge:** The sparse routing and slow-trunk learning rate effectively isolate knowledge domains, making it ideal for processing diverse, single-stream user interactions over time.
* **Hardware Efficiency (Conceptually):** Proves that continuous learning is possible without a massive GPU cluster, provided I/O speeds are sufficient.

### Cons

* **Severe I/O Dependency:** Requires NVMe storage; highly incompatible with standard OverlayFS or Ceph/network storage setups.
* **Resource Contention:** Demands a dedicated 8 GB VRAM footprint, which may starve primary inference tasks if not scheduled on dedicated hardware.
* **Experimental Nature:** The custom dynamic depth and soft-routing mechanisms are bespoke and may be complex to maintain or debug alongside standard Transformer implementations.

## 6. Next Steps

1. **I/O Benchmarking:** Before writing any implementation code, run a synthetic I/O benchmark on our Nomad host-volumes to ensure our NVMe drives can support the necessary read/write IOPS for expert swapping.
2. **Prototype Paging:** Implement a minimal Rust prototype using the `candle` ML framework to test zero-copy `MmapedSafetensors` disk-to-VRAM loading in a test Nomad job to measure real-world latency within our infrastructure.
3. **Draft Nomad Spec:** Once hardware feasibility is proven, draft a `.nomad.j2` template utilizing host-volume mounts and GPU placement constraints for the background worker.

## 7. Implementation Task Breakdown (TODOs)

To safely test and integrate these mechanisms, we will follow a phased approach:

### Phase 1: Storage and I/O Benchmarking

* [ ] **Create I/O Benchmark Script:** Write a Python script to synthesize random read/writes of 3MB chunk files (simulating the `.npz` expert loads).
* [ ] **Provision Test Host Volume:** Update the Ansible `nomad` role to provision a dedicated `/opt/nomad/data/nvme_test` host volume mounted directly on an NVMe block device.
* [ ] **Deploy Benchmark Job:** Create a temporary Nomad `raw_exec` job to run the benchmark script against the NVMe mount and against a standard OverlayFS mount to quantify the speed delta.

### Phase 2: Rust & Candle Paging Prototype

* [ ] **Initialize Rust Crate:** Create a new, isolated workspace crate (`services/mini-agi-worker`) to prevent any interference with latency-critical `moshi` voice threads.
* [ ] **Implement `MmapedSafetensors` Loader:** Write a Rust module utilizing `candle` to memory-map uncompressed expert weights directly from the NVMe volume.
* [ ] **Implement Static VRAM Slot Allocator:** Prototype a fixed-memory buffer in Rust/`candle` to eliminate runtime CUDA memory allocation calls during swaps.
* [ ] **Simulate Working Set Demand:** Write a script that mocks random text chunk demands and forces the cache to swap 32 experts into the pre-allocated VRAM slots using custom CUDA streams.
* [ ] **Measure Latency:** Run this Rust prototype on the dedicated NVMe volume and verify if the zero-copy paging latency meets the minimum requirement for continuous learning without stalling.

### Phase 3: Background Learner Scaffolding

* [ ] **Draft Nomad Job Specification:** Create `playbooks/templates/nomad/mini_agi_worker.nomad.j2` with explicit GPU placement constraints (`accel-npu`, >8GB VRAM) and the NVMe `volume_mount`.
* [ ] **Build Environment Image:** Write a Dockerfile/build script to compile the Rust binary (using a multi-stage `rustlang/rust:nightly-slim` builder similar to `moshi-rust`) and package it for the background worker.
* [ ] **Deploy Dry-Run:** Deploy the service to the cluster in a dry-run state (not reading real data) to verify scheduling and volume attachment success.

### Phase 4: MoE Gateway & Resilience

* [ ] **DatalogEngine Hook:** Create an API client in the Rust worker that reads the output/knowledge state from the background learner and writes generic `credit` or semantic facts to the `DatalogEngine` ledger.
* [ ] **Experimental Route:** Add a feature flag in the `MoE Gateway` to optionally route a small percentage of asynchronous, latency-insensitive queries (e.g., long-form document summaries) to the new worker for testing.
* [ ] **Add Prometheus Metrics Exporter:** Instrument the worker with `/metrics` endpoints tracking paging latency, cache hits, and expert growth.
* [ ] **Automated Snapshot/Restore Hook:** Write an export script to sync modified expert weights from the local NVMe volume to IPFS at regular checkpoint intervals.
* [ ] **Frozen Validation Test Harness:** Implement the sleep-cycle validation routine to detect model drift before saving persistent weight updates to disk.
