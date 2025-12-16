#!/bin/bash
# Profile resources usage and alignment of AI experts and models.

echo "=== AI Infrastructure Profile Report ==="
echo "Generated at: $(date)"
echo ""

# 1. Active Nomad Jobs
echo "--- Active Nomad Jobs ---"
if command -v nomad >/dev/null 2>&1; then
    nomad job status | grep -E 'expert|llamacpp' || echo "No AI jobs found."
else
    echo "Nomad CLI not found."
fi
echo ""

# 2. Registered Consul Services
echo "--- Registered Consul Services ---"
if command -v curl >/dev/null 2>&1; then
    services=$(curl -s http://127.0.0.1:8500/v1/catalog/services | jq -r 'keys[]' | grep -E 'expert|llamacpp')

    if [ -z "$services" ]; then
        echo "No AI services found in Consul."
    else
        for s in $services; do
            echo "Service: $s"
            # Get nodes/tags
            curl -s "http://127.0.0.1:8500/v1/catalog/service/$s" | jq -r '.[] | "  - Node: \(.Node) Address: \(.ServiceAddress):\(.ServicePort) Tags: \(.ServiceTags)"'
        done
    fi
else
    echo "curl or jq not found."
fi
echo ""

# 3. Resource Reservation (Approximation)
echo "--- Resource Reservation (Nomad Allocations) ---"
if command -v nomad >/dev/null 2>&1; then
    # List all allocs for relevant jobs
    allocs=$(nomad job status -json | jq -r '.[] | select(.ID | test("expert|llamacpp")) | .ID')

    for job in $allocs; do
        echo "Job: $job"
        nomad job inspect "$job" | jq -r '.TaskGroups[].Tasks[].Resources | "  CPU: \(.CPU) MHz, Memory: \(.MemoryMB) MB"'
    done
fi
echo ""

# 4. Duplicate Check
echo "--- Duplication Check ---"
# Check if multiple jobs are serving the same model
# We assume the service naming convention llamacpp-rpc-<model>-provider is unique.
# If we see multiple POOLS for the same model, that's bad.

if [ -n "$services" ]; then
    echo "$services" | awk -F'-' '{
        if ($1 == "llamacpp" && $2 == "rpc") {
            # Extract model part (skip llamacpp-rpc and -provider)
            # This is rough parsing
            print $0
        }
    }' | sort | uniq -d | while read -r line; do
        echo "WARNING: Potential Duplicate Service found: $line"
    done
fi

echo "=== End of Report ==="
