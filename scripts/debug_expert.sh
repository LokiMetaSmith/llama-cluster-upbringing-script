#!/bin/bash
set -e
echo "🚀 Starting the llama Expert service in debug mode..."
nomad job run ansible/jobs/expert-debug.nomad
