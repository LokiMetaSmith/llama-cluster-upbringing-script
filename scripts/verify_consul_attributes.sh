#!/bin/bash
set -e

# verify_consul_attributes.sh
#
# This script verifies that the local Nomad agent has correctly populated
# the 'attr.consul.version' attribute. This is critical to avoid "Constraint Mismatch"
# errors where jobs like 'mqtt' require Consul version >= 1.8.0.
#
# Usage: ./verify_consul_attributes.sh
#
# It requires 'nomad' to be in the path and the Nomad agent to be running.

echo "Verifying Nomad node attributes..."

# Check if nomad is installed
if ! command -v nomad &> /dev/null; then
    echo "Error: 'nomad' command not found."
    exit 1
fi

# Fetch node status and stats
# We use -self to check the local client agent
OUTPUT=$(nomad node status -self -stats -json 2>/dev/null)

if [ $? -ne 0 ]; then
    echo "Error: Failed to query Nomad agent. Is it running?"
    exit 1
fi

# Extract the Consul version attribute
# Nomad JSON output structure for attributes: .Attributes["consul.version"]
CONSUL_VERSION=$(echo "$OUTPUT" | jq -r '.Attributes["consul.version"] // empty')

if [ -z "$CONSUL_VERSION" ]; then
    echo "FAIL: 'attr.consul.version' is MISSING."
    echo "Diagnosis: Nomad likely started before Consul was ready."
    echo "Resolution: Restart Nomad service (systemctl restart nomad) to refresh attributes."
    exit 1
else
    echo "PASS: Found Consul version: $CONSUL_VERSION"
    exit 0
fi
