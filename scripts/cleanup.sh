#!/bin/bash
# This script cleans up temporary files created by the project.

set -e

echo "Removing temporary files..."

# Remove downloaded archives
rm -f /tmp/consul.zip
rm -f /tmp/nomad.zip
rm -f /tmp/cni-plugins.tgz
rm -f /tmp/get-docker.sh
rm -f /tmp/pipecatapp.tar

# Remove extracted directories
rm -rf /tmp/consul
rm -rf /tmp/nomad

echo "Cleanup complete."
