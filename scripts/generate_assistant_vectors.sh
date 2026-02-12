#!/bin/bash
set -e

# Default paths
MODEL_PATH="${1:-/opt/nomad/models/llama/llama-3-8b-instruct.gguf}"
OUTPUT_FILE="${2:-assistant_axis.gguf}"
GENERATOR_BIN="${3:-llama-cvector-generator}"

# Check if model exists
if [ ! -f "$MODEL_PATH" ]; then
    echo "Error: Model file not found at $MODEL_PATH"
    echo "Usage: $0 <path_to_model_gguf> [output_file] [generator_binary]"
    exit 1
fi

# Locate generator binary
if ! command -v "$GENERATOR_BIN" &> /dev/null; then
    # Check common locations
    if [ -f "/usr/local/bin/llama-cvector-generator" ]; then
        GENERATOR_BIN="/usr/local/bin/llama-cvector-generator"
    elif [ -f "./dev_build/llama.cpp/build/bin/llama-cvector-generator" ]; then
        GENERATOR_BIN="./dev_build/llama.cpp/build/bin/llama-cvector-generator"
    else
        echo "Error: llama-cvector-generator binary not found."
        exit 1
    fi
fi

echo "Using generator: $GENERATOR_BIN"
echo "Using model: $MODEL_PATH"

# Generate prompt files
echo "Generating prompt pairs..."
python3 scripts/create_assistant_prompts.py

# Run generator
echo "Running llama-cvector-generator..."
# Adjust parameters (pca-iter, pca-batch) based on available resources if needed
"$GENERATOR_BIN" \
    -m "$MODEL_PATH" \
    --cvector-positive-file cvector_pos.txt \
    --cvector-negative-file cvector_neg.txt \
    --pca-iter 1000 \
    --pca-batch 100 \
    -o "$OUTPUT_FILE"

echo "Control vector generated at $OUTPUT_FILE"
