# Agent Handover: PersonaPlex & Colibri SSD Streaming Architecture

**To the succeeding agent:** This document serves as my last will and testament regarding the implementation of the PersonaPlex full-duplex conversational model and the Colibri-inspired local SSD streaming architecture.

## 1. Context & Motivation

The user requires a real-time, low-latency (<200ms) full-duplex conversational AI to serve as live NPCs on their **CommandDeck** system. They selected NVIDIA's **PersonaPlex** (a 7B Moshi-based model).

**The Core Challenge:** The user's infrastructure relies heavily on low-power mesh nodes (e.g., Core 2 Duo, 4-8GB RAM). A standard 7B dense model cannot run natively on this hardware due to severe memory and memory-bandwidth constraints.

**The Solution:** We pursued a dual-track strategy:
1.  **Centralized GPU Orchestrator:** Run PersonaPlex on high-tier cluster nodes and stream audio over websockets from the mesh nodes.
2.  **Advanced Local SSD Streaming (Colibri Architecture):** A long-term feasibility strategy to convert the dense 7B model into a Sparse Mixture-of-Experts (MoE) and stream the activated expert weights directly from an NVMe SSD asynchronously using `io_uring` or GPUDirect Storage, bypassing the host RAM limits entirely.

## 2. Accomplishments (What We Built)

### A. Documentation & Evaluation
*   **`evaluations/personaplex_evaluation.md`**: A comprehensive evaluation report covering hardware feasibility, comparisons to cascading Whisper+TTS pipelines, and a specific focus on translating XML/JSON tabletop simulation state into PersonaPlex's hybrid text/audio prompt.
*   **`evaluations/colibri_moshi_ssd_streaming.md`**: An architectural blueprint detailing how to merge Moshi's streaming transformer with Colibri's sparse asynchronous SSD I/O. It includes advanced optimizations like GPUDirect (cuFile), Early-Layer Predictive Routing, and EAGLE-style speculative drafting.

### B. The Rust SSD Streaming Prototype (`colibri_io_uring/`)
We successfully prototyped the core low-level mechanics of the SSD streaming engine in Rust:
*   **Zero-Copy `io_uring` Streamer (`streamer.rs`):** Uses Linux `io_uring` and `O_DIRECT` to read data via kernel DMA directly into page-aligned host buffers (allocated via `libc::posix_memalign`), bypassing the OS page cache.
*   **Hardware-Agnostic VRAM Streamer (`vram_streamer.rs`):** Defined a trait for direct NVMe-to-VRAM transfers, along with C-FFI wrappers for NVIDIA (`cuFile`), AMD (`hipMemcpyAsync`), and Intel Level Zero.
*   **Candle Tensor Bridge (`tensor_bridge.rs`):** Implemented safe zero-copy transmutation (`unsafe { buf.align_to::<f32>() }`) to map the raw DMA byte buffers directly into HuggingFace Candle `Tensor` objects.
*   **Streaming MoE Layer (`moe_layer.rs`):** Built a mock Candle neural network module that simulates the MoE pipeline: running a router, triggering the async disk reads, waiting for completions, and computing the sparse FFN matrix multiplications.

### C. Python Infrastructure (`pipecatapp/` & `command_deck/`)
*   **Structured Data Adapter (`pipecatapp/persona_plex/state_adapter.py`):** Wrote a middleware component that flattens arbitrary XML/JSON tabletop states into the dense natural language strings required by PersonaPlex's text-conditioning channel.
*   **Network Streaming Audio Client (`command_deck/scripts/personaplex_client.py`):** Drafted an asynchronous Python websocket client designed to run on the mesh nodes. It continuously captures local microphone input (mocked via `MockPyAudioStream`), hex-encodes it, and full-duplex streams it to the central PersonaPlex server.

## 3. Current State & Known Issues

*   **The Rust Prototype works and compiles.** The `moe_layer_test` runs successfully, proving the pipeline logic.
*   **The Python Websocket Client test is flaky in the sandbox environment.** Due to virtual environment isolation and module pathing (`PYTHONPATH` issues) within the sandbox `uv run pytest` execution, importing `command_deck.scripts.personaplex_client` sometimes fails. The script itself is syntactically sound and the test mocks `websockets` correctly via `AsyncMock`.

## 4. Next Steps & TODOs for the Succeeding Agent

To carry this project to the finish line, pick up where I left off:

1.  **Resolve Python Test Environment:** Fix the `PYTHONPATH` or `__init__.py` structure in the sandbox so that `uv run pytest tests/test_personaplex_client.py` passes reliably.
2.  **Audio Codec Integration:** Update `personaplex_client.py` to use `pyaudio` for actual microphone capture and `opuslib` to compress the raw PCM frames before sending them over the websocket, reducing network bandwidth.
3.  **Proof of Concept Docker Deployment:** Write the `Dockerfile` and a Nomad job template (`.nomad.j2`) to deploy the actual `moshi.server` with the PersonaPlex weights onto a GPU-equipped cluster node.
4.  **Advance the Rust Architecture:** If the user wants to continue the low-level edge-node streaming, implement the **Early-Layer Predictive Router** milestone described in the `TODO.md` within the `colibri_io_uring/` directory.

May the compiler be ever in your favor.
