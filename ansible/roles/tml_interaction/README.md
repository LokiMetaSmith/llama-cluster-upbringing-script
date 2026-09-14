# TML Interaction Role

This role acts as a configuration for the cluster for the Thinking Machines Lab's Interaction Models research preview.
It establishes the routing, continuous multi-modal streaming architecture, and Nomad job configurations for the multi-stream micro-turn models.

It sets up a two-tier architecture:
- `llama-cpp`: Runs the core inference using the multi-modal Inkling weights (e.g. `unsloth/inkling-GGUF:UD-IQ1_S`).
- `moshi-rust`: The Rust backend (`moshi/rust`) that provides the continuous WebRTC audio/video micro-turn streaming architecture.
