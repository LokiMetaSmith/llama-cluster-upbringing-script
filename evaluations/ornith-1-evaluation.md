# Ornith-1 Evaluation for Local LLM Provider (llama-cluster-upbringing-script)

## Overview
This document evaluates the [`Ornith-1` repository](https://github.com/deepreinforce-ai/Ornith-1) (specifically the `Ornith-1.0` model series) for inclusion as a core coding model backend within the `llama-cluster-upbringing-script` cluster, acting as the local LLM provider for OpenClaw.

## Hardware Footprint & Local Deployment Viability
The `Ornith-1.0` series provides checkpoints in multiple sizes and formats. The evaluation focuses on the smaller checkpoints: 9B Dense and 35B MoE, particularly in GGUF formats.

- **9B Dense (`Ornith-1.0-9B-GGUF`)**:
  - Fits easily on consumer hardware or a single GPU. The bf16 version comfortably fits on a single 80GB GPU, so the quantized GGUF versions will have a significantly smaller footprint, making it ideal for standard cluster nodes.
  - Highly viable for local inference using `llama.cpp` or `Ollama`.

- **35B MoE (`Ornith-1.0-35B-GGUF`)**:
  - The Mixture-of-Experts architecture means it only activates a subset of parameters during inference, providing faster generation speeds compared to a dense 35B model.
  - While the full bf16 requires multi-GPU serving, the GGUF quantized formats allow it to fit on multi-GPU consumer nodes or Apple Silicon with sufficient Unified Memory.

Both GGUF versions are directly compatible with our local inference engines (`llama.cpp` via `llama-server` or `Ollama`), making them highly viable for our local cluster deployment.

## Unsloth Compatibility & MTaC Pipeline
The model is officially compatible with **Unsloth**. The repository documentation explicitly provides a quickstart for loading the model using `Unsloth Studio` for fast local inference and fine-tuning.
- This ensures seamless integration with our **MTaC (Model Training as Code)** pipeline, which relies on Unsloth for efficient SFT (Supervised Fine-Tuning). We can confidently use `Ornith-1.0-9B` as a base model for dynamic Unsloth fine-tuning jobs in our Nomad cluster.

## OpenClaw Integration
Integration with OpenClaw is straightforward and officially supported.
- `Ornith-1.0` exposes a fully **OpenAI-compatible server** API when served via `vLLM`, `SGLang`, or `llama.cpp` (`llama-server`).
- The model accurately generates OpenAI-style tool calls.
- **Setup for OpenClaw:** We simply need to configure OpenClaw to point to the local endpoint:
  ```bash
  export OPENAI_BASE_URL="http://<local-cluster-ip>:8000/v1"
  export OPENAI_API_KEY="EMPTY"
  export OPENAI_MODEL="Ornith-1.0"
  ```

## Self-Scaffolding & Agent Workflows Analysis
`Ornith-1.0` features a unique self-improving training framework that jointly optimizes both the solution rollouts and the "scaffolds" (search trajectories/reasoning) driving them.

- **Reasoning (`<think>`) Blocks:** The model is a reasoning model. The assistant turn always begins with a `<think> ... </think>` block before delivering the final answer or tool call.
- **Workflow Impact:**
  - **Server-Side Parsing:** If served via `vLLM` or `SGLang`, the server can be configured with `--reasoning-parser qwen3`. This automatically strips the `<think>` block from the main `content` and surfaces it in a separate `reasoning_content` field in the OpenAI API response.
  - **Tool-Call Parsing:** The model outputs tool calls naturally, and the server can parse them into the standard `tool_calls` array using `--tool-call-parser qwen3_xml` (vLLM) or `--tool-call-parser qwen3_coder` (SGLang).
  - **Impact on OpenClaw/Agents:** Our agent workflows will receive standard OpenAI tool calls without being confused by the reasoning tokens, provided we use a compliant server configuration. If using `llama.cpp`, we may need to ensure our agent framework (or a middleware proxy) correctly handles or strips the `<think>` tags if the raw text is returned before the tool call. The self-scaffolding inherently improves the model's trajectory planning, which should result in fewer tool-call errors and more autonomous problem-solving capabilities.

## Conclusion
`Ornith-1.0` is highly recommended for inclusion. The 9B/35B GGUF checkpoints provide excellent local deployment viability, the Unsloth compatibility aligns perfectly with our MTaC pipeline, and its native OpenAI tool-calling with reasoning blocks makes it an exceptionally strong engine for OpenClaw agents.

## Implementation Steps (TODO)
- [ ] **Download GGUF Checkpoints:** Fetch the `Ornith-1.0-9B-GGUF` and `Ornith-1.0-35B-GGUF` model files onto the cluster.
- [ ] **Configure Cluster Infrastructure:** Deploy the checkpoints to the shared `/opt/nomad/models` IPFS storage or cluster volume for high availability.
- [ ] **Setup Local Inference Server:** Create and dispatch a Nomad job running `llama-server` (or `vLLM` if GPU memory allows) pointing to the Ornith-1 GGUF files.
- [ ] **Configure OpenClaw:** Update the OpenClaw deployment configuration (e.g., environment variables `OPENAI_BASE_URL` and `OPENAI_MODEL`) to point to the newly established local endpoint.
- [ ] **Verify Reasoning Parsing:** Ensure the server is correctly configured to parse `<think>` blocks (e.g., using `--reasoning-parser qwen3`) so agent workflows do not fail due to malformed tool calls.
- [ ] **Test MTaC Pipeline:** Run a small Supervised Fine-Tuning job using the `Ornith-1.0-9B` model via Unsloth within the MTaC pipeline to verify compatibility.
