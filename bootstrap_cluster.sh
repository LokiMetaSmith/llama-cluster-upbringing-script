#!/bin/bash
#
# Cluster Bootstrap Script
# Strictly provisions the host environment, OS, network, Nomad/Consul cluster bootstrapping, and system daemon provisioning.
#

set -e

# Run the original bootstrap but strictly for cluster provisioning
echo "Starting cluster upbringing pipeline..."
./bootstrap.sh --cluster-only --role all --deploy-full-stack "$@"
