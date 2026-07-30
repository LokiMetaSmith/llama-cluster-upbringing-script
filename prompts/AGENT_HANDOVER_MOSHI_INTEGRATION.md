# Agent Handover: Full Moshi Core Integration (The Final Frontier)

**To the succeeding Advanced Coding Agent:**

You are tasked with a highly complex, systems-level engineering challenge. You must merge a custom, ultra-low-latency NVMe SSD streaming engine (written in Rust) directly into the core transformer architecture of a state-of-the-art conversational AI model.

## 1. Context & The Architecture

The user operates a decentralized compute cluster ("CommandDeck") heavily reliant on low-power mesh nodes (e.g., Core 2 Duo, 4-8GB RAM). They need to run **PersonaPlex** (a 7B parameter, full-duplex conversational model based on the [Moshi architecture](https://arxiv.org/abs/2410.00037)).

Because a 7B dense model cannot fit in the RAM of these edge nodes, we have developed the **Colibri Architecture**: a strategy to convert the dense transformer into a sparse Mixture-of-Experts (MoE) and stream the activated expert weights *asynchronously* straight from an NVMe SSD into GPU VRAM or Host RAM, bypassing the OS page cache using Linux `io_uring`.

## 2. What Has Been Built So Far

In the `colibri_io_uring/` directory, the foundational low-level engine is complete:
*   **`streamer.rs` (`AsyncWeightStreamer`):** A zero-copy disk I/O engine using `io_uring` and `O_DIRECT`. It allocates page-aligned, pinned host memory using `posix_memalign`.
*   **`tensor_bridge.rs`:** Provides `buffer_to_candle_tensor`, safely transmuting raw DMA `&[u8]` byte slices into `candle_core::Tensor` objects without host-side memory copies.
*   **`moe_layer.rs` (`StreamingMoeLayer`):** A proof-of-concept pipeline demonstrating "Early-Layer Predictive Routing". It runs a lightweight router head on *lookahead* audio tokens to predict upcoming expert requirements, queues non-blocking `io_uring` reads, and then executes the matrix multiplication once the kernel completes the DMA transfer.

## 3. Your Mission: The Moshi Injection

Your task is to fork the actual `kyutai-labs/moshi` Rust inference core and surgically inject our `colibri_io_uring` engine.

**Key Objectives:**

1.  **Fork and Integrate:** Integrate the `moshi-core` crate (which uses `candle-core`) into our workspace.
2.  **Locate the Transformer Backbone:** Identify the dense Feed-Forward Network (FFN) blocks within Moshi's Transformer layers (likely within `moshi/rust/moshi-core/src/transformer.rs` or similar).
3.  **Inject the Streaming Layer:** Replace the static, memory-bound FFNs with our `StreamingMoeLayer`.
4.  **Implement Audio-Lookahead:** Moshi is a full-duplex speech model. You must modify the generation loop to pass incoming user audio tokens (from the Mimi codec) 1-2 frames *ahead* of the current generation step into the `forward_with_lookahead` method. This hides the SSD read latency behind the preceding layer computations.

## 4. Critical Warnings & Constraints

*   **Memory Safety (Use-After-Free):** The `tensor_bridge` relies on raw pointers bridging the gap between kernel DMA buffers and Candle tensors. You **must** ensure the `io_uring` buffers are not dropped, overwritten, or freed while the `candle_core::Tensor` is still evaluating. Valgrind has been used extensively to verify our current memory safety; do not break it.
*   **Latency Budget:** Real-time audio requires a strict <200ms end-to-end latency budget (approx 40-80ms per frame). Your modifications to the Moshi evaluation loop must remain strictly non-blocking. Use the asynchronous `submit_and_wait(0)` logic carefully to avoid stalling the main audio thread.
*   **Sparse Equivalency:** For testing purposes, you may need to map dense weights to "dummy" MoE chunks on disk to prove the mechanical pipeline works before the user provides the actual mathematically sparsified (MoE-LoRA) model weights.

Good luck. You are touching the bleeding edge of local LLM deployment.
