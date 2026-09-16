# Swift-Qwen3.8-27b Benchmark Report

## Model Configuration

- **Model Name:** `Swift-Qwen3.8-27B`
- **Architecture:** Image-Text-to-Text / Reasoning
- **Quantization:** `Q4_K_M`
- **File:** `Swift-Qwen3.8-27B-Q4_K_M.gguf`
- **Repository:** `ukisai/Swift-Qwen3.8-27B-GGUF`
- **Expert Category:** `thinking`
- **Allocated Memory:** `20000 MB`

## Context

Swift-Qwen3.8-27B is UkisAI's reasoning-efficient derivative of Qwen3.8-27B, designed to use fewer thinking tokens while maintaining near-identical performance. The `Q4_K_M` quantization provides the best balance of reasoning performance and resource efficiency for our `llama.cpp` deployments.

The model has been configured as the primary (default) model in the `thinking` expert tier in `group_vars/models.yaml` with an assigned memory limit of 20000 MB.

## Execution Instructions

Because standard benchmark automation is not available in the current isolated environment, you will need to execute the benchmark manually on the cluster node.

To evaluate its performance within our orchestration environment:

1. **Submit the Nomad job:**
   ```bash
   nomad job run /opt/nomad/jobs/benchmark.nomad
   ```
   *(Note: Ensure that you provide the correct model path to the job variables if they are not picked up automatically from the global configurations).*

2. **Retrieve the Benchmark Logs:**
   Once the job runs, extract the metrics from the job logs:
   ```bash
   nomad job logs llama-benchmark
   ```

3. **Metrics Recording:**
   Append the inference speed (tokens/sec) and any relevant latency measurements from the job logs to this file for future review.
