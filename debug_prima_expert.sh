#!/bin/bash
set -e
echo "🚀 Starting the Prima Expert service in debug mode..."
nomad job run ansible/jobs/prima-expert-debug.nomad
