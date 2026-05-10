#!/bin/bash
# Trigger a Nomad task checkpoint utilizing Docker's experimental CRIU support.

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <container_id> <checkpoint_name>"
    echo "Example: $0 e3b0c44298fc llm_checkpoint_1"
    # return error
    /bin/false
fi

CONTAINER_ID=$1
CHECKPOINT_NAME=$2
CHECKPOINT_DIR="/opt/nomad/volumes/checkpoints"

echo "Creating checkpoint '${CHECKPOINT_NAME}' for container '${CONTAINER_ID}'..."

# Run docker checkpoint create
sudo docker checkpoint create --checkpoint-dir="${CHECKPOINT_DIR}" "${CONTAINER_ID}" "${CHECKPOINT_NAME}"

echo "Checkpoint created successfully at ${CHECKPOINT_DIR}/${CONTAINER_ID}/checkpoints/${CHECKPOINT_NAME}"
