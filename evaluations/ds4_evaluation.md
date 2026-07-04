# Evaluation of DwarfStar (ds4) for Cluster Inclusion

## Overview
DwarfStar (ds4) is a native inference engine optimized for DeepSeek V4 Flash and PRO models. It offers specific features like SSD streaming for models larger than RAM and highly optimized kernels for Metal, CUDA, and ROCm.

## Integration Progress
- **Ansible Role**: Created `ansible/roles/ds4` for node-level installation and compilation. It defaults to CPU build for evaluation.
- **Model Management**: Added DeepSeek V4 Flash/PRO GGUF definitions to `group_vars/models.yaml` and updated `seed_models` role.
- **Nomad Support**: Developed `ansible/jobs/ds4-server.nomad.j2` for deploying the inference server.
- **App Integration**: Extended `pipecatapp/llm_clients.py` with `<think>` block stripping to support reasoning models like DeepSeek V4.
- **System Routing**: Wired `ds4-server` into the expert deployment pipeline in `ansible/roles/pipecatapp`.

## Distributed Inference Evaluation
`ds4` supports splitting layers across multiple machines (Coordinator/Worker model).
- **Coordination with llama.cpp RPC**: While llama.cpp RPC exposes GPUs as remote backends to a single orchestrator, `ds4` distributed mode uses a pipelined approach where each node owns a slice of layers.
- **Suitability**: `ds4`'s distributed mode is highly specialized for DeepSeek V4 and provides better prefill speedups through pipelining compared to generic RPC setups. It is recommended for the DeepSeek V4 PRO (512GB+) use case where multiple machines are required.

## Recommendations
1. **Lightweight Evaluation**: The current integration forces CPU mode for initial tests. This is suitable for functional verification but will be slow for large models.
2. **Production Path**: For production, use `ds4_build_type: cuda-generic` or `rocm` and ensure high-bandwidth interconnects (Thunderbolt/10GbE) are used for distributed mode.
3. **Reasoning Models**: The inclusion of `ds4` significantly enhances the cluster's ability to run frontier-class reasoning models locally.
