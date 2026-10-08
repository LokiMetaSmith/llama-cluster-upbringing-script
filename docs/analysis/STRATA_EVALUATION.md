# Strata Evaluation Report

## Overview

[Strata](https://github.com/Niko1221/Strata) is an inference engine designed to run massive Mixture of Experts (MoE) models (such as the 125-billion-parameter Qwen3.8-Flash-Next) on consumer-grade hardware. It achieves this by employing a hybrid offloading mechanism that distributes the model's experts across VRAM, system RAM, and SSD storage.
Instead of requiring hundreds of gigabytes of VRAM, Strata caches the most frequently used experts in GPU VRAM, keeps all experts available in system RAM (if capacity allows), and relies on a lookup table on an SSD to stream experts as needed. A smaller helper model handles initial speculative decoding ("guess"), and the large model verifies ("check") in batches, which mitigates the high latency of disk I/O.

## Pros

- **Enables Massive Models on Consumer Hardware**: Makes running 100B+ parameter MoE models possible on single machines with 12GB+ VRAM by intelligently swapping experts.
- **Speculative Decoding Pipeline**: The "guess-and-check" architecture masks the latency of fetching experts from slower memory tiers by batching the validation step.
- **OpenAI-Compatible API**: Features a built-in server that is compatible with standard OpenAI/Anthropic toolchains and agents.
- **Cross-Platform & Multi-GPU Support**: Works across Windows/Linux and supports NVIDIA and AMD consumer cards, including multi-GPU configurations.

## Cons (Hardware Context specific)

While Strata's hybrid architecture is impressive for powerful gaming PCs, it presents severe challenges for our constrained heterogeneous cluster profile:

- **High Minimum RAM Requirements**: Strata's smallest recommended configuration (Coder model) requires a minimum of **32 GB of system RAM**. Our cluster consists of commodity nodes with only **8–16 GB of RAM**, making Strata unbootable or forcing it to rely entirely on disk-backed swap.
- **Disk I/O Bottlenecks & Cache Miss Penalties**: For nodes operating beneath the 64GB-80GB RAM threshold, Strata aggressively reads experts from the SSD. On local SATA or slower NVMe drives, an expert cache miss results in severe latency spikes. The disk I/O bottlenecks directly degrade Time To First Token (TTFT) and Inter-Token Latency (ITL).
- **Nomad/Consul Orchestration Friction**: Strata is heavily optimized as a desktop application (designed around standalone setup scripts and manual user interactions). Adapting it for headless, stateless distributed deployment under Nomad would require significant wrapping and lifecycle management overhead.
- **Incompatible with Distributed Inference**: Strata relies on vertical scaling (VRAM + RAM + SSD on a single machine). Our cluster topology relies on horizontal scaling (distributing inference across multiple small nodes), which Strata does not support out-of-the-box.

## Feature Replication vs. Inclusion

Given our infrastructure, running Strata as a standalone runtime is not viable. However, the core concept—**Tiered MoE Expert Caching and Offloading**—is highly valuable.

### Is Feature Replication a Better Option?

**Yes.** Replicating the tiered MoE expert caching logic directly within our existing engines (e.g., `vLLM` or `llama.cpp`) is a cleaner, lower-overhead approach for the following reasons:

1. **Leveraging Existing Frameworks**:
   - `llama.cpp` already possesses robust CPU/GPU tensor splitting (`mmap` fallback) and RPC-based distributed inference capabilities. Enhancing its MoE router to prioritize VRAM for active experts and asynchronously prefetch from RAM/Disk would mimic Strata's behavior without introducing a new runtime.
   - `vLLM` is introducing custom offload managers and chunked prefill. Implementing an expert-level caching eviction policy (e.g., LRU) for MoE routing in vLLM would integrate natively with our current deployment stack and PagedAttention mechanisms.

2. **Horizontal Distribution**: Instead of relying on SSDs (which are slow in our cluster), we can replicate the "offload" tier horizontally over the network. Using `llama.cpp` RPC or distributed tensor parallelism, "inactive" experts can reside in the RAM of adjacent compute nodes rather than on a local SATA drive, utilizing network bandwidth instead of disk I/O.

3. **Resource Control**: By integrating into `vLLM` or `llama.cpp`, we maintain strict control over memory bounds, adhering to the 8GB per-node memory limit enforced by our Nomad constraints.

## Recommendation

**Do not include Strata as a standalone component.** Its minimum hardware requirements (32GB+ RAM) and reliance on vertical scaling via SSDs directly conflict with our cluster's constraints (8-16GB RAM commodity nodes).

**Action Plan:**

- Document Strata's speculative decoding and expert caching heuristics as reference architecture.
- Explore adding expert-aware LRU eviction policies or tiered offloading to our existing `llama.cpp` / `vLLM` implementations.
- Prioritize network-distributed expert routing over local disk swapping to better utilize our horizontally scaled cluster.
