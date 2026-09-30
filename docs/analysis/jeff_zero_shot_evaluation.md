# RFC: Evaluation of `jeff` for Zero-Shot Intent Classification
## Executive Summary
This document evaluates the `jeff` zero-shot classification model for potential integration into our distributed conversational AI pipeline. The primary goal is to assess its viability as an ultra-fast, lightweight routing gate for intent classification and tool dispatching, operating under strict legacy hardware constraints (< 512MB RAM, CPU-only).
While `jeff` offers a highly capable and developer-friendly zero-shot classification experience (replacing generation with a single-pass probability readout), its memory footprint and CPU latency profile present significant challenges for our target environment. Integration is feasible only through aggressive quantization (e.g., GGUF 4-bit) and optimization, and it may still not beat traditional BERT-style classifiers for raw speed on legacy CPUs.
## 1. Architecture & Zero-Shot Mechanism
`jeff` provides small, fast decision models (fine-tunes of Qwen 3.5 and Gemma 4) designed to act as zero-shot classifiers based on the RLCD (Reinforcement Learning from Calibrated Decisions) paradigm.
- **RLCD Paradigm:** The core idea is combining multiway preference modeling (Plackett-Luce) with probability calibration (Brier score). This elevates a standard reward model into a calibrated decision API, avoiding token-by-token generation entirely.
- **Parallel Sampler Mechanism:** Instead of autoregressive generation, the model relies on sequence packing and a strict "tree attention" mask. The state, question, and all candidate options are packed into a single sequence. The attention mask prevents cross-candidate contamination, allowing a single shared decision head to evaluate the utilities of all candidates in one parallel forward pass.
- **Sizes:** The available models include `Jeff-Qwen3.5-0.8B`, `Jeff-Qwen3.5-2B`, and `Jeff-Gemma4-E2B`.
- **Zero-Shot:** The options can be anything (support queues, user intents, voice commands), and the model can pick among them without the categories needing to be in the training data.
## 2. Primary Use Case: Intent Classification & Routing
For our pipeline, the primary use case is intent classification and fast tool/agent dispatching. `jeff` could act as a zero-shot routing gate before routing to heavier LLM prompts or MoE experts.
**Comparison with alternatives:**
- **BERT/DeBERTa Classifiers:** Small BERT-style classifiers are extremely fast (often 10s of milliseconds on CPU) and memory-efficient (often < 100MB). However, they typically require fixed categories and explicit training/fine-tuning on those categories.
- **LLM Structured Outputs:** Standard LLM JSON/structured output relies on autoregressive generation, which is slower and consumes more memory.
- **Jeff's Advantage:** `jeff` bridges the gap. It offers the dynamic, zero-shot flexibility of LLMs (you can change routing labels on the fly without retraining) but operates in a single forward pass, making it faster than standard LLM generation.
## 3. Hardware & Runtime Considerations
Our controller and compute nodes are legacy CPU-bound systems (e.g., Intel Core i7) with strict container constraints (e.g., < 512MB RAM).
**Latency (CPU):**
- According to the published benchmarks, the smallest model (`Jeff-Qwen3.5-0.8B`) takes **463 ms per decision** on a high-end 32-thread CPU.
- On a legacy Core i7 (typically 4-8 threads), this latency is expected to degrade significantly, potentially taking 1-2 seconds per decision. This challenges the requirement for an "ultra-fast" routing gate.
**Memory Footprint:**
- The 0.8B model in 16-bit precision requires **1.7 GB** of weights.
- The 2B model requires 4.2 GB.
- Out of the box, standard PyTorch/HuggingFace deployments of these models will exceed our < 512MB RAM budget.
## 4. Export & Portability (ONNX / GGML / GGUF)
To deploy `jeff` as a microservice (via Nomad `docker` driver) within our hardware constraints, the PyTorch dependency must be removed.
- **GGUF / llama.cpp / DwarfStar:** Because `jeff` is based on standard architectures (Qwen 3.5, Gemma 4), the base models are fully supported by `llama.cpp` and our native `ds4` (DwarfStar) engine. The zero-shot classification works by evaluating logits on the first generated token (over specific option tokens). This logic can be implemented using `llama.cpp`'s API or exported to GGUF.
- **Quantization:** To meet the < 512MB RAM limit, the 0.8B model must be heavily quantized. A Q4 (4-bit) quantization would reduce the 1.7GB model size to roughly **450-500 MB**. This fits within the RAM budget, but leaves virtually no headroom for context windows, OS overhead, or Docker runtime overhead.
- **ONNX Runtime:** Exporting to ONNX and utilizing ONNX Runtime (C++) is another viable pathway for CPU optimization. INT8 quantization via ONNX could reduce the size to ~850MB, which still exceeds the 512MB limit, meaning 4-bit quantization (which is better supported by GGUF) is strictly necessary.
## 5. Conclusion & Recommendations
While `jeff` is a highly innovative solution for dynamic zero-shot classification, **it is currently too heavy for a < 512MB RAM legacy CPU environment** without aggressive engineering.
**Recommendations:**
1. **Delay Implementation:** Do not integrate `jeff` into the core Nomad playbooks at this time. The 463ms latency on a 32-thread CPU indicates that legacy CPU performance will be too slow for an "ultra-fast" routing gate.
2. **Alternative for Ultra-Fast Routing:** Stick to small, fine-tuned embeddings or BERT/DeBERTa classifiers for intent routing if speed (< 100ms) and memory (< 100MB) are paramount.
3. **Future Feasibility Study:** If dynamic zero-shot routing is absolutely necessary, conduct an isolated feasibility test by converting `Jeff-Qwen3.5-0.8B` to a Q4_K_M GGUF format and benchmarking it using `llama-cli` on a legacy node. If it exceeds 500ms or 512MB RAM, abandon the approach.
