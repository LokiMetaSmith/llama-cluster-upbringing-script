#!/bin/bash

# Comment out or remove existing mpirun commands
# mpirun -np benchmark-matmult
# mpirun -np ./main -m ./models/ggml-vocal-llama.gguf

# --- llama-server command with RPC ---
# This command starts the llama-server with RPC enabled.
# TODO: Configure the following variables according to your setup.

# MODEL_PATH: Path to the GGUF model file
# MODEL_PATH="models/L3.3-Q4_K_M.gguf"

# RPC_HOSTS: Comma-separated list of RPC server addresses and ports
# Example: "192.168.1.19:50052,192.168.1.15:50052"
# RPC_HOSTS="<YOUR_RPC_HOSTS_HERE>"

# CONTEXT_SIZE: Size of the prompt context
# CONTEXT_SIZE=16384

# N_GPU_LAYERS: Number of layers to offload to GPU
# N_GPU_LAYERS=200

# OTHER_ARGS: Other arguments for llama-server
# OTHER_ARGS="--flash-attn --split-mode row --threads 12 --tensor-split 13,13,24"

# Make sure llama-server is in your PATH or provide the full path to the executable.
# llama-server -m "$MODEL_PATH" --rpc "$RPC_HOSTS" -c "$CONTEXT_SIZE" -ngl "$N_GPU_LAYERS" $OTHER_ARGS

echo "llama-server command is configured in run.sh but commented out by default."
echo "Please edit run.sh to set your MODEL_PATH, RPC_HOSTS, and other parameters, then uncomment the llama-server command."

# Example placeholder command (commented out):
# llama-server -m "models/your-model.gguf" --rpc "host1:port,host2:port" -c 4096 -ngl 100 --flash-attn
