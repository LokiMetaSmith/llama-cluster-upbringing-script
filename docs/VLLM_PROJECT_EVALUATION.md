# vLLM Project Evaluation

This document summarizes the evaluation of repositories within the `vllm-project` organization for potential incorporation into our project.

## Summary

After reviewing the `vllm-project` GitHub organization, three key repositories were identified as highly relevant to our goals:

1.  **Semantic Router** (`semantic-router`) - **Highly Recommended**
2.  **GuideLLM** (`guidellm`) - **Recommended for Capacity Planning**
3.  **vLLM Omni** (`vllm-omni`) - **Watch for Future Use**

## Detailed Findings

### 1. Semantic Router (`semantic-router`)

*   **Description**: A system-level intelligent router for "Mixture-of-Models" (MoM). It serves as a super-fast decision layer that routes requests to different models or tools based on semantic meaning using vector embeddings.
*   **Relevance**: We currently use a "Router Agent" based on an LLM. `semantic-router` is designed to replace or augment this by using lightweight embedding models (like `minilm`) to make routing decisions in milliseconds rather than seconds.
*   **Hardware Support**: Fully supports NVIDIA and AMD GPUs (AMD is a sponsor).
*   **Action Plan**: Create a new Ansible role `semantic_router` to deploy this as a service. This will allow us to define routing rules (e.g., "math questions" -> Math Expert, "coding" -> Coding Expert) statically or dynamically without burning tokens on a router LLM.

### 2. GuideLLM (`guidellm`)

*   **Description**: A benchmarking and evaluation platform for optimizing real-world LLM inference. It helps determine the resources (GPU memory, replicas) needed to meet Service Level Objectives (SLOs).
*   **Relevance**: Our `models.yaml` currently hardcodes `memory_mb`. GuideLLM can help us scientifically determine these values by simulating load (e.g., "10 concurrent users") and measuring Time To First Token (TTFT) and Inter-Token Latency (ITL).
*   **Action Plan**: Use this tool (can be run as a standalone container or utility) to tune our production configurations.

### 3. vLLM Omni (`vllm-omni`)

*   **Description**: An extension of vLLM to support omni-modality models (audio, video, text) in a single inference engine. Supports models like Qwen-Omni.
*   **Relevance**: Our current pipeline uses separate components for STT (Whisper), LLM (Llama), and TTS (Piper). `vllm-omni` represents the future where a single model handles end-to-end "speech-to-speech" or "video-to-text".
*   **Status**: Experimental but promising.
*   **Action Plan**: Keep on the roadmap. Once "omni" models become more accessible and stable, we can simplify our architecture by replacing the `stt` -> `llm` -> `tts` chain with a single `vllm-omni` service.

## Core vLLM Updates

The core `vllm` repository is already in use but required updates to support our mixed hardware environment:
*   **AMD GPU Support**: Updated the `vllm` Ansible role to detect AMD GPUs (via `rocm-smi` or device checks) and automatically deploy the ROCm-optimized Docker image (`vllm/vllm-openai:latest-rocm`) instead of the NVIDIA one.
