# Moshi Rust Backend Handover: SPSC Ring Buffer Optimization

## Background
We are working on optimizing the `moshi/rust` multi-modal continuous streaming pipeline for the `pipecatapp` repository. Based on an architectural review of a high-performance repository ("Ghostlink"), we identified that replacing standard `std::sync::mpsc::channel` loops with a Zero-Copy Single-Producer Single-Consumer (SPSC) Ring Buffer would significantly reduce CPU cache bouncing and latency for high-frequency audio frames.

## What Has Been Completed

### 1. Docker Build Environment Fixed
The `moshi-rust` Dockerfile (`docker/moshi-rust/Dockerfile`) was failing due to a missing dependency for `candle-transformers` and a missing directory context. We successfully:
* Switched the builder image to `FROM rustlang/rust:nightly-slim AS builder`.
* Added `cmake` to the `apt-get install` commands to bypass the `iter_repeat_n` compile error.
* Added `COPY colibri_io_uring/ /usr/colibri_io_uring/` before the `cargo build` command to restore the missing dependency.

### 2. SPSC Ring Buffer Implemented
We implemented the target ring buffer in a new file: `moshi/rust/moshi-backend/src/ring_buffer.rs`.
* It utilizes `#[repr(align(64))]` for cache-line padding to prevent false sharing between the audio thread and the inference thread.
* It supports `push_batch` and `pop_batch` operations that use `std::ptr::copy_nonoverlapping` to copy contiguous memory blocks directly up to the buffer bounds.
* It is registered in the module tree via `moshi/rust/moshi-backend/src/main.rs`.

## Current State & The Bottleneck

We are currently integrating the `SpscRingBuffer` into the actual streaming logic located in `moshi/rust/moshi-backend/src/stream_both.rs`.

**The Target:**
The current `stream_both.rs` pipeline spins up a thread scope and relies heavily on `std::sync::mpsc::channel`:
```rust
let (tx_i, rx_i) = std::sync::mpsc::channel::<(Vec<u32>, usize)>();
let (tx_o, rx_o) = std::sync::mpsc::channel::<Vec<u32>>();
```

**The Attempt:**
We replaced these channels with instances of our new ring buffer:
```rust
let in_ring = std::sync::Arc::new(crate::ring_buffer::SpscRingBuffer::<(Vec<u32>, usize)>::new(crate::ring_buffer::RingConfig { capacity: 256, backpressure_threshold: 128 }));
let out_ring = std::sync::Arc::new(crate::ring_buffer::SpscRingBuffer::<Vec<u32>>::new(crate::ring_buffer::RingConfig { capacity: 256, backpressure_threshold: 128 }));

let tx_i = in_ring.clone();
let rx_i = in_ring.clone();
let tx_o = out_ring.clone();
let rx_o = out_ring.clone();
```

**The Problem:**
Standard `mpsc::channel` automatically signals disconnected states (`Err(Disconnected)`) when the sender drops, cleanly breaking the `while let Ok(...) = rx.recv()` loops. Our custom `SpscRingBuffer` does not natively track connection state or block; calling `.pop()` just returns `None` if it's empty.

To avoid busy-waiting forever when the stream finishes, we've had to replace `recv()` with explicit loop/yield structures that check the `Arc::strong_count`. For example:
```rust
let (codes, step) = loop {
    match rx_i.pop() {
        Some(v) => break v,
        None => {
            if std::sync::Arc::strong_count(&rx_i) == 1 { return Ok(()); }
            std::thread::yield_now();
        }
    }
};
```

## Next Agent Action Items

Your immediate objective is to complete the integration of the `SpscRingBuffer` inside `moshi/rust/moshi-backend/src/stream_both.rs` and verify the compilation.

### 1. Complete the Loop Patches in `stream_both.rs`
The file has multiple thread closures running `while let Ok(x) = rx.recv()`. You need to carefully substitute these with the ring buffer `pop()` logic, ensuring that the threads yield correctly when empty and break gracefully when the stream terminates. (The `patch.py` script attempts this but may need refinement for `rx_o`).

### 2. Verify Compilation
Once the channels are swapped, run `cargo check` or `cargo build --release --bin moshi-backend` inside `moshi/rust` to ensure the lifetime and threading constraints are satisfied.

### 3. Move on to Generalizing the HMAC Proxy (Future Task)
Once Moshi streaming is optimized and compiling, you can proceed to the final TODO listed in `GHOSTLINK_IDEAS.md`: Extracting Ghostlink's L4 HMAC-SHA256 authentication proxy into an `ansible/roles/lightweight_auth_proxy` to secure our internal raw TCP endpoints.
