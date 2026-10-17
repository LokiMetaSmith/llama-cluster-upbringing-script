# Strata Reference Architecture
## Overview
This document outlines the reference architecture derived from the evaluation of the Strata inference engine. Strata was designed to run massive Mixture of Experts (MoE) models (e.g., 100B+ parameter models) on hardware with limited GPU VRAM by employing hybrid offloading strategies. This reference serves as a blueprint for implementing similar caching and offloading heuristics into our existing inference engines (such as `vLLM` or `llama.cpp`) to suit our horizontally-scaled cluster environment, without deploying Strata as a standalone app.
## Core Concepts
### 1. Speculative Decoding Pipeline ("Guess-and-Check")
Strata masks the latency of reading parameters from slower memory tiers through a speculative decoding architecture.
- **Helper Model ("Guess"):** A smaller, faster model runs ahead and generates a sequence of draft tokens. This model typically fits entirely within the GPU VRAM.
- **Target Model ("Check"):** The massive MoE model runs behind the helper model to verify the draft tokens in batches. Since verifying a batch of tokens is highly parallelizable and computationally dense compared to generating them one-by-one, the high latency of fetching MoE experts is amortized across multiple tokens.
### 2. Tiered MoE Expert Caching
Strata splits the model's MoE experts across three distinct tiers, utilizing an eviction policy to cycle experts dynamically:
1. **Tier 1 (GPU VRAM):** Caches the most frequently accessed or currently active experts. This tier provides the lowest latency and highest bandwidth but has the most constrained capacity.
2. **Tier 2 (System RAM):** Holds the entirety of the experts (or the largest subset possible) in standard DDR memory. Accessed more slowly than VRAM but still relatively fast.
3. **Tier 3 (Storage - SSD):** Contains all model weights as a fallback. On a cache miss in VRAM and RAM, experts are streamed directly from disk via a lookup table.
### 3. Eviction Policy and Prefetching Heuristics
The effectiveness of tiered caching relies heavily on predicting which experts will be needed:
- **LRU (Least Recently Used) Eviction:** As VRAM fills up, the least recently accessed experts are evicted back to system RAM or dropped entirely if they reside on disk, creating room for incoming active experts.
- **Expert Prefetching:** The router mechanism in the MoE layer identifies which experts a token will route to during the forward pass. These experts can be asynchronously prefetched from RAM/SSD into VRAM just before they are required.
## Adaptation for Horizontal Clusters
Our cluster topology consists of commodity nodes (8-16 GB RAM) interconnected over a network, rather than single powerful workstations with vast RAM or fast local SSDs.
To adapt the Strata reference architecture to our environment:
- **Avoid Local SSD Swapping:** Due to high latency on slow local drives, SSD offloading should be minimized.
- **Network-Distributed Offloading:** Replace Tier 3 (Local SSD) with **Cluster RAM**. Instead of swapping an inactive expert to a local disk, it is streamed from the RAM of an adjacent compute node over the network (using mechanisms like `llama.cpp` RPC or tensor parallelism).
- **Engine Integration:** Incorporate expert-aware LRU eviction and asynchronous prefetching natively into the MoE routers of `vLLM` (leveraging PagedAttention chunking) or `llama.cpp` (enhancing `mmap` fallbacks).
