#!/bin/bash
set -e

# Ensure we are running from the repository root
cd "$(dirname "$0")/.." || exit 1

echo "🚀 Starting the llama Expert service in debug mode..."
nomad job run ansible/jobs/expert-debug.nomad
