# DSpark Speculative Decoding Architecture Report

## Overview
DSpark is a specialized speculative decoding framework built to optimize the inference speed of Large Language Models (LLMs). Speculative decoding traditionally uses a smaller "draft" model to guess upcoming tokens rapidly, which the large "target" model then verifies in a single batch step. DSpark addresses two major bottlenecks in existing architectures: drafting speed vs. accuracy (suffix decay), and system-level verification efficiency (wasted compute under high load).

### Core Components
DSpark relies on a novel two-part mechanism:
1. **Semi-Autoregressive Generation (Drafting):**
   - **Parallel Backbone:** Generates token hidden states in a single parallel forward pass (similar to DFlash) offering $O(1)$ latency scaling with block length.
   - **Sequential Head:** Instead of independent logits per token, a lightweight Markov or RNN-based projection layer introduces conditional dependency between draft tokens. This resolves "multi-modal collisions" (where combinations of words make no sense together) and prevents "suffix decay" common in pure parallel drafters.

2. **Confidence-Scheduled Verification:**
   - **Confidence Head:** A lightweight sigmoid classifier trained to predict the survival probability of each draft token. It uses *Sequential Temperature Scaling* (STS) to calibrate these probabilities effectively.
   - **Hardware-Aware Prefix Scheduler:** A system that estimates the expected yield (accepted tokens) versus the compute cost (Target Model Step Time/SPS). It actively truncates the verification length to drop low-confidence suffix tokens, ensuring critical compute batch capacity is not wasted during high-concurrency periods.

## Evaluation for Local Cluster Models (9B/35B scale)

Integrating the DSpark techniques into our local inference pipeline (which utilizes models like Orthrus-9B and Qwen3.5-35B on constrained legacy hardware) offers significant potential, though it requires adapting the framework from high-end GPU clusters (like DeepSeek V4) to our multi-node CPU/split-inference setup.

### 1. Applicability of Semi-Autoregressive Drafters
- **Current State:** Our local models currently do not utilize speculative decoding due to the overhead of running two models simultaneously on constrained RAM (e.g. 8-16GB per machine).
- **Opportunity:** DSpark demonstrates that a very shallow parallel drafter (1 to 2 transformer layers) coupled with a Markov head can significantly outperform deeper parallel models.
- **Implementation Strategy:** We can extract the embedding and LM head from our local targets (e.g., Qwen 35B or Orthrus 9B) and train a highly compressed 1-2 layer parallel backbone. This minimal drafter footprint can reside entirely in the CPU RAM of an Edge node.

### 2. Adapting the Hardware-Aware Prefix Scheduler
- **Current State:** Our cluster experiences highly variable inference latency because computation is split via `llamacpp-rpc` across varying CPU nodes.
- **Opportunity:** DSpark's scheduler relies on a pre-profiled Steps-Per-Second (SPS) curve. In our heterogeneous environment, verification cost is high and variable.
- **Implementation Strategy:** We can implement a dynamic SPS profile that updates based on the current Swarm network state (e.g., active RPC nodes, ping times). By utilizing the Confidence Head on the Edge node, the system can dynamically prune draft batches. For instance, if the network is saturated, it truncates the batch tightly to avoid blocking the main inference loop.

### 3. Training Feasibility (DeepSpec)
- **Framework Integration:** The DeepSpec repository open-sources the training tools for DSpark. Since our dataset is relatively domain-specific (Ansible, Nomad, Home Assistant), we would need to generate a distilled prompt/response dataset using our existing 35B model.
- **Limitations:** Training a parallel backbone requires target model hidden states. We would need to temporarily spin up a high-memory cloud instance to generate the training data (extracting the KV states), as our distributed CPU cluster lacks the bandwidth for efficient gradient syncing across split architectures.

## Conclusion
While the pre-trained `deepseek-ai/DeepSeek-V4-Pro-DSpark` is far beyond our hardware capabilities (1.6T params), the underlying algorithmic approach of **Semi-Autoregressive Drafting combined with Confidence-Scheduled Verification** is highly applicable to our architecture. It provides a blueprint for creating ultra-lightweight, high-yield drafters that can maximize our limited distributed compute resources without congesting the RPC network.

**Next Steps for Integration:**
1. Clone the `DeepSpec` repository to a dedicated research instance.
2. Generate a specialized dataset of local cluster workflows using our 35B model.
3. Train a 2-layer DSpark draft model targeted at the `Orthrus-9B` architecture.
4. Integrate the Confidence-Scheduler logic into our Python `WorkflowRunner` to dynamically adjust `llama.cpp` verification batches.
