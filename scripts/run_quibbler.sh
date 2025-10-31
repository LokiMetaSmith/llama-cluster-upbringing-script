#!/bin/bash

# A wrapper script to run quibbler for code review.

# Check for required arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <user_instructions> <agent_plan>"
    exit 1
fi

USER_INSTRUCTIONS="$1"
AGENT_PLAN="$2"
PROJECT_PATH=$(pwd)

# Run quibbler review
quibbler review "${USER_INSTRUCTIONS}" \
    --plan "${AGENT_PLAN}" \
    --path "${PROJECT_PATH}"
