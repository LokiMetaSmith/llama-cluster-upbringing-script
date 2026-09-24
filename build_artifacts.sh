#!/bin/bash
#
# Build Artifacts Script
# A standalone workflow strictly for container builds, model downloads/caching, and Nomad job packaging.
#

set -e

# Run the original bootstrap but strictly for artifact builds
echo "Starting artifact building pipeline..."
./bootstrap.sh --build-only "$@"
