#!/bin/bash
set -e

# This script demonstrates how to use the 'heretic' tool to ablate sycophancy from a model.
# It assumes you have a GPU and the 'heretic' tool installed (via the heretic_tool Ansible role).
# It uses a custom dataset of "sycophancy-inducing" prompts and a list of sycophantic phrases
# as "refusal markers" (in this context, "sycophancy markers") to identify the direction to ablate.

# Path to the heretic executable (assuming installed in the default location by the role)
HERETIC_BIN="/opt/heretic_tool/venv/bin/heretic"

# Check if heretic is installed
if [ ! -f "$HERETIC_BIN" ]; then
    echo "Error: heretic executable not found at $HERETIC_BIN"
    echo "Please run the 'heretic_tool' Ansible role first."
    exit 1
fi

# Define the model to modify (e.g., Llama-3-8B-Instruct)
MODEL_ID="meta-llama/Meta-Llama-3-8B-Instruct"

# Define the output directory
OUTPUT_DIR="./cynic-llama-3-8b"

# Sycophancy markers: phrases that indicate the model is being sycophantic.
# Heretic treats these as "refusal markers" to minimize. By passing sycophantic phrases,
# we instruct Heretic to find a direction that minimizes these phrases.
SYCOPHANCY_MARKERS=(
    "you are right"
    "i agree"
    "absolutely"
    "brilliant"
    "great idea"
    "you're correct"
    "insightful"
    "perfect"
    "i understand your point"
    "certainly"
    "of course"
)

# Join markers with spaces for the command line
MARKERS_ARG=""
for marker in "${SYCOPHANCY_MARKERS[@]}"; do
    MARKERS_ARG+=" \"$marker\""
done

echo "Starting sycophancy ablation on $MODEL_ID..."
echo "Using sycophancy markers: ${SYCOPHANCY_MARKERS[*]}"

# Run Heretic
# We use the 'sycophancy_prompts.json' as the "bad" prompts (the ones that trigger the behavior we want to change).
# We use a standard harmless dataset as the "good" prompts.
# By minimizing the "refusal markers" (sycophancy markers) on the "bad" prompts (sycophancy traps),
# Heretic should ablate the direction that leads to sycophancy.

# Note: The flags below are based on the heretic --help output.
# --bad-prompts points to our sycophancy traps.
# --refusal-markers points to our sycophancy phrases.

CMD="$HERETIC_BIN --model $MODEL_ID \
    --bad-prompts ./ansible/roles/pipecatapp/files/datasets/sycophancy_prompts.json \
    --bad-prompts.column text \
    --refusal-markers $MARKERS_ARG \
    --n-trials 50 \
    --device-map auto"

echo "Executing: $CMD"

# Uncomment the following line to actually run it (requires GPU)
# eval $CMD

echo "Ablation command constructed. Run this script on a GPU-enabled machine to generate the Cynic model."
