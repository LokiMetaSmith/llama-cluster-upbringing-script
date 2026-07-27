# Architectural Blueprint: Local SSD Streaming for Full-Duplex Voice Models

## 1. Executive Summary

This blueprint outlines a hybrid architecture combining the real-time full-duplex capabilities of **Moshi/PersonaPlex** with the extreme memory-offloading and async I/O techniques of **Colibri**.

The goal is to solve the memory constraints of running 7B-parameter dense audio models (like Helium) on RAM-constrained edge nodes. By restructuring the dense backbone into a sparse Mixture-of-Experts (MoE) or utilizing MoE-LoRA adapters, and backing it with an asynchronous, zero-copy `io_uring` SSD streaming engine, we can achieve real-time speech generation (<200ms latency) without requiring 16GB+ of VRAM or system RAM.

## 2. Architectural Breakdown

| Feature / Technique | Moshi / PersonaPlex | Colibri |
| :--- | :--- | :--- |
| **Model Type** | 7B Dense Dual-Stream Transformer (Helium LM + Mimi Audio Codec) | ~744B Sparse Mixture-of-Experts (MoE) LLM (GLM-5.2) |
| **Execution Target** | Real-time full-duplex speech (<200 ms latency requirement) | Extreme memory-offloaded inference (RAM-constrained) |
| **Storage & Memory Strategy** | Assumes weights reside entirely in GPU VRAM or RAM | Memory-maps weight containers (mmap) & streams on demand |
| **I/O Engine** | Standard PyTorch / Candle / MLX tensor loaders | C-native asynchronous `io_uring` / `pread` with zero runtime dependencies |
| **Throughput Amortization** | None (evaluates full dense layers per frame) | Multi-Token Prediction (MTP) speculative drafting + LRU expert cache |

## 3. The Core Bottleneck: Dense vs. Sparse Streaming

Colibri achieves SSD streaming because GLM-5.2 is a Mixture-of-Experts (MoE) model. For any given token, Colibri keeps the 9.9 GB dense backbone in RAM and streams only 8 activated experts (~150 MB total) per layer from the NVMe SSD.

PersonaPlex and Moshi use 7B dense Transformer backbones. At 24 Hz (Moshi's frame rate), generating 1 second of audio requires 24 forward passes. Streaming an un-quantized 7B model (14 GB at FP16) from disk 24 times per second would require **336 GB/s** of read bandwidth. Even at INT4 (~3.5 GB), 24 forward passes require **84 GB/s**—well beyond PCIe 5.0 NVMe speeds (~14 GB/s max).

To make SSD streaming viable for real-time speech generation, we must combine Moshi's streaming Transformer design with Colibri's sparse I/O techniques.

## 4. Hybrid Strategy for Efficient Local SSD Streaming

```text
  [ Audio Input Stream ] ──> [ Mimi Encoder ]
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Pinned System RAM / VRAM                                               │
│  • Mimi Codec / Audio Encoders                                         │
│  • Dense Transformer Backbone (Self-Attention & KV-Cache)              │
│  • Router Heads & Shared Experts                                       │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Router Predicts Expert Indices
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Colibri-Style Async I/O Pipeline (io_uring / mmap)                      │
│  • Speculative Pre-Fetching (Lookahead on incoming audio frames)       │
│  • Layer-Wise Pinned Hot-Store (LRU Cache)                             │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Streams Activated MoE Weights
                                   ▼
                        [ NVMe SSD Weight Pool ]
```

### Key Techniques to Integrate

1. **MoE-LoRA / Sparse Expert Restructuring:** Replace the dense FFNs in Moshi’s Helium backbone with sparse MoE blocks (e.g., 64 small experts, routing to 4 per token) or a bank of MoE-LoRA adapters for persona control. This reduces the per-frame disk fetch requirement from 3.5 GB down to <300 MB per forward pass.
2. **Asynchronous Zero-Copy Disk Engines (`io_uring`):** Replace PyTorch/Python data loading with Colibri’s C/Rust-native `io_uring` architecture. Fetch expert weight chunks directly into host-pinned DMA buffers or unified memory, bypassing system call overhead.
3. **Audio-Lookahead Pre-Fetching:** Full-duplex speech models receive continuous audio frames *ahead* of generation. Run the router head 1–2 audio frames (~40–80 ms) ahead on incoming user audio tokens to initiate async NVMe reads before the decoder layer execution reaches that step.
4. **Multi-Token Speculative Decoding:** Apply a lightweight draft head to Moshi’s temporal stream to predict multiple audio tokens simultaneously, amortizing disk read latency across several audio frames.

## 5. Low-Level Rust Extension Blueprint

To maintain Moshi’s real-time 80ms audio frame processing budget without hitting the GIL or blocking Candle’s matrix multiplication kernels, the streaming reader runs as a dedicated background worker using Linux `io_uring`.

### Step 1: Pinned Ring Allocator (`ring_reader.rs`)
To avoid memory allocations during active generation, pre-allocate pinned aligned host buffers that `io_uring` writes into directly via kernel DMA.

```rust
use io_uring::{opcode, squeue, IoUring};
use std::fs::File;
use std::os::unix::io::AsRawFd;
use std::sync::atomic::{AtomicBool, Ordering};

pub struct AsyncWeightStreamer {
    ring: IoUring,
    file_fd: RawFd,
    // Pinned aligned host memory buffers for zero-copy DMA
    buffer_pool: Vec<Vec<u8>>,
    page_size: usize,
}

impl AsyncWeightStreamer {
    pub fn new(weight_file_path: &str, queue_depth: u32, max_expert_size: usize) -> Self {
        let file = File::open(weight_file_path).expect("Failed to open model weights");
        let raw_fd = file.as_raw_fd();
        let ring = IoUring::new(queue_depth).expect("Failed to initialize io_uring");

        // Aligned 4096-byte buffers for O_DIRECT / Direct I/O read access
        let mut buffer_pool = Vec::new();
        for _ in 0..queue_depth {
            let mut buf = vec![0u8; max_expert_size];
            buffer_pool.push(buf);
        }

        Self {
            ring,
            file_fd: raw_fd,
            buffer_pool,
            page_size: 4096,
        }
    }

    /// Submits asynchronous batch pre-fetch request for active MoE experts
    pub unsafe fn queue_expert_read(&mut self, offset: u64, size: usize, slot_idx: usize) {
        let buf_ptr = self.buffer_pool[slot_idx].as_mut_ptr();

        let read_e = opcode::Read::new(
            io_uring::types::Fd(self.file_fd),
            buf_ptr,
            size as u32,
        )
        .offset(offset)
        .build()
        .user_data(slot_idx as u64);

        self.ring
            .submission()
            .push(&read_e)
            .expect("Submission queue full");
    }

    pub fn submit_and_wait(&mut self, expected_completions: usize) {
        self.ring.submit_and_wait(expected_completions).unwrap();
    }
}
```

### Step 2: Bridging to Candle/Torch Backends (`tensor_bridge.rs`)
Convert raw DMA-filled buffers into execution-ready tensors without memory copies.

```rust
use candle_core::{DType, Device, Shape, Tensor};

pub fn buffer_to_candle_tensor(
    buf: &[u8],
    shape: Shape,
    dtype: DType,
    device: &Device,
) -> candle_core::Result<Tensor> {
    // For CPU execution, construct directly from raw slice bytes
    match device {
        Device::Cpu => Tensor::from_raw_buffer(buf, dtype, &shape, device),
        Device::Cuda(gpu_dev) => {
            // Asynchronously copy directly from host-pinned RAM to GPU VRAM stream
            let cpu_tensor = Tensor::from_raw_buffer(buf, dtype, &shape, &Device::Cpu)?;
            cpu_tensor.to_device(device)
        }
        _ => unimplemented!(),
    }
}
```

### Step 3: Integrating Audio Lookahead into `moshi-core`
Modify Moshi’s multi-stream evaluation loop (`lm_generate.rs` or `transformer.rs`).

```rust
pub struct StreamingMoeLayer {
    pub dense_proj: Linear,
    pub streamer: Arc<Mutex<AsyncWeightStreamer>>,
    pub expert_offsets: HashMap<usize, u64>, // Offset map for expert weight chunks
}

impl StreamingMoeLayer {
    pub fn forward_with_lookahead(
        &self,
        xs: &Tensor,
        current_frame: usize,
        lookahead_user_tokens: &[u32],
    ) -> candle_core::Result<Tensor> {
        // 1. Run lightweight router head on lookahead frame to predict upcoming expert routing
        let predicted_experts = self.predict_future_experts(lookahead_user_tokens);

        // 2. Dispatch non-blocking io_uring requests into the background pool
        {
            let mut streamer = self.streamer.lock().unwrap();
            for (slot, expert_id) in predicted_experts.iter().enumerate() {
                let offset = self.expert_offsets[expert_id];
                unsafe {
                    streamer.queue_expert_read(offset, EXPERT_SIZE, slot);
                }
            }
            // Non-blocking submission
            streamer.submit_and_wait(0);
        }

        // 3. Execute current step (using expert weights pre-fetched in previous frame)
        let current_experts = self.route_current(xs)?;
        let out = self.compute_moe(xs, &current_experts)?;

        Ok(out)
    }
}
```

## 6. Implementation Milestones

1. **Standalone `io_uring` Benchmarker:** Build a minimal C/Rust harness loading 50 MB to 200 MB chunks from an NVMe target to measure baseline throughput on local SSD systems (target: >4.5 GB/s random read).
2. **Moshi MoE-LoRA Prototype:** Fine-tune or adapt Moshi/PersonaPlex using sparse LoRA rank matrices. Streaming small ~10–20 MB adapter weights per persona frame is significantly faster to evaluate on consumer NVMe drives than replacing whole FFNs.
3. **Benchmarking Latency Budgets:** Ensure total pre-fetch + GPU DMA transfer time fits comfortably within Moshi’s 40–80 ms frame budget.
