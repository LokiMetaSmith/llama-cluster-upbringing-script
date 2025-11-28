#!/bin/bash

# test_paddler.sh
#
# This script performs basic tests to verify that Paddler (agent and balancer)
# is functioning correctly with a llama.cpp cluster.
#
# Prerequisites:
# 1. Paddler balancer service running.
# 2. At least one Paddler agent service running and connected to the balancer.
# 3. At least one llama.cpp server instance running, configured with --slots,
#    and registered with a Paddler agent.
# 4. `curl` command-line utility installed.
# 5. For more advanced JSON parsing (not strictly required by this script's basic checks),
#    `jq` can be useful (e.g., `sudo apt install jq`).
#
# Usage:
# ./test_paddler.sh [PADDLER_PUBLIC_ADDR] [PADDLER_MANAGEMENT_ADDR]
#
# Or, set environment variables:
# export PADDLER_PUBLIC_ADDR="http://your-balancer-host:8080"
# export PADDLER_MANAGEMENT_ADDR="http://your-balancer-host:8085"
# ./test_paddler.sh
#

# --- Configuration ---
# Default public address for the Paddler balancer (reverse proxy for llama.cpp requests)
DEFAULT_PADDLER_PUBLIC_ADDR="http://localhost:8080"
# Default management address for the Paddler balancer (API for agent status, etc.)
DEFAULT_PADDLER_MANAGEMENT_ADDR="http://localhost:8085"

# Use command-line arguments if provided, otherwise use environment variables or defaults
PADDLER_PUBLIC_ADDR="${1:-${PADDLER_PUBLIC_ADDR:-$DEFAULT_PADDLER_PUBLIC_ADDR}}"
PADDLER_MANAGEMENT_ADDR="${2:-${PADDLER_MANAGEMENT_ADDR:-$DEFAULT_PADDLER_MANAGEMENT_ADDR}}"

# Strip trailing slashes, if any
PADDLER_PUBLIC_ADDR=$(echo "$PADDLER_PUBLIC_ADDR" | sed 's:/*$::')
PADDLER_MANAGEMENT_ADDR=$(echo "$PADDLER_MANAGEMENT_ADDR" | sed 's:/*$::')

echo "--- Paddler Test Script ---"
echo "Using Paddler Balancer Public Address: $PADDLER_PUBLIC_ADDR"
echo "Using Paddler Balancer Management Address: $PADDLER_MANAGEMENT_ADDR"
echo

# Overall test status
all_tests_passed=true

# --- Test Functions ---

# Test 1: Paddler Balancer Management API Check
check_balancer_api() {
    local management_url="${PADDLER_MANAGEMENT_ADDR}/api/v1/agents"
    echo "TEST 1: Checking Paddler balancer management API at $management_url..."

    # Use curl to get agent status. -s for silent, -S to show errors, -f to fail fast on HTTP errors.
    # Adding a timeout of 10 seconds.
    response=$(curl -sSf -m 10 "$management_url")
    curl_exit_code=$?

    if [ $curl_exit_code -ne 0 ]; then
        echo "FAIL: Failed to connect to Paddler balancer management API (curl exit code: $curl_exit_code)."
        echo "Response: $response"
        all_tests_passed=false
        return 1
    fi

    # Basic check: Does the response look like JSON and contain "id" (typical for an agent entry)?
    # A more robust check would use jq if available: echo "$response" | jq '. | length > 0 and .[0].state == "ready"'
    if echo "$response" | grep -q '"id":'; then
        echo "PASS: Successfully connected to management API."
        echo "Connected Agents Summary:"
        # Crude parsing for agent summary without jq. Replace with jq for better output if desired.
        echo "$response" | grep -E '"id":|"name":|"address":|"state":|"slots_total":|"slots_free":' | sed 's/^[[:space:]]*//; s/,$//'
        
        # Check if any agent is in "ready" state (very basic check)
        if echo "$response" | grep -q '"state": "ready"'; then
            echo "INFO: At least one agent appears to be in 'ready' state."
        else
            echo "WARN: No agent explicitly found in 'ready' state. Check agent status details."
            # This is a warning, not a failure, as other states might be valid in some contexts.
        fi
    else
        echo "FAIL: Management API response does not seem to contain valid agent data (expected JSON with 'id' fields)."
        echo "Response: $response"
        all_tests_passed=false
        return 1
    fi
    echo
    return 0
}

# Test 2: Llama.cpp Request through Paddler Balancer
check_llama_request_via_paddler() {
    local public_url="${PADDLER_PUBLIC_ADDR}/completion" # Assuming /completion is the target endpoint
    echo "TEST 2: Attempting a llama.cpp completion request via Paddler at $public_url..."

    # Simple prompt for testing. Adjust if your model needs a specific format.
    # Ensure n_predict is small to get a quick response.
    # The llama.cpp server's /completion endpoint might behave differently based on its version.
    # This is a very basic test.
    payload='{"prompt": "This is a test prompt to check connectivity.", "n_predict": 1, "stream": false}'

    # Use curl to send the request. -s for silent, -X POST, -H for headers, -d for data.
    # Adding a timeout of 20 seconds for the completion.
    response_json=$(curl -sSf -m 20 -X POST -H "Content-Type: application/json" -d "$payload" "$public_url")
    curl_exit_code=$?

    if [ $curl_exit_code -ne 0 ]; then
        echo "FAIL: Request to llama.cpp via Paddler failed (curl exit code: $curl_exit_code)."
        echo "Payload sent: $payload"
        echo "Response: $response_json"
        all_tests_passed=false
        return 1
    fi

    # Basic check: Does the response contain "content" (typical for llama.cpp completion response)?
    # A more robust check would parse JSON and validate the structure.
    if echo "$response_json" | grep -q '"content":'; then
        echo "PASS: Received a response from llama.cpp via Paddler."
        echo "Response snippet: $(echo "$response_json" | head -c 200)..." # Print a snippet
    else
        echo "FAIL: Response from llama.cpp via Paddler does not look like a valid completion."
        echo "Payload sent: $payload"
        echo "Response: $response_json"
        all_tests_passed=false
        return 1
    fi
    echo
    return 0
}

# --- Run Tests ---
check_balancer_api
check_llama_request_via_paddler

# --- Final Status ---
echo "--- Test Summary ---"
if $all_tests_passed; then
    echo "All tests passed successfully!"
    exit 0
else
    echo "One or more tests failed. Please review the output above."
    exit 1
fi
