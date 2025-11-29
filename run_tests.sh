#!/usr/bin/env bash
set -e

# Resolve the directory of the script to ensure absolute paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
REPO_ROOT="$SCRIPT_DIR"

# Function to display help
show_help() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  --unit          Run unit tests"
    echo "  --integration   Run integration tests (Python only)"
    echo "  --e2e           Run end-to-end tests (pytest)"
    echo "  --all           Run all tests (unit, integration, e2e)"
    echo "  --help          Display this help message"
}

# Default values
RUN_UNIT=false
RUN_INTEGRATION=false
RUN_E2E=false

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --unit) RUN_UNIT=true ;;
        --integration) RUN_INTEGRATION=true ;;
        --e2e) RUN_E2E=true ;;
        --all) RUN_UNIT=true; RUN_INTEGRATION=true; RUN_E2E=true ;;
        --help) show_help; exit 0 ;;
        *) echo "Unknown parameter passed: $1"; show_help; exit 1 ;;
    esac
    shift
done

# If no flags provided, show help
if [ "$RUN_UNIT" = false ] && [ "$RUN_INTEGRATION" = false ] && [ "$RUN_E2E" = false ]; then
    show_help
    exit 1
fi

# Set path for pyenv shims if needed (copied from existing script)
export PATH="/home/jules/.pyenv/shims:$PATH"

# Function to run pytest with reporting
run_pytest() {
    local target="$1"
    local report_file="$2"
    python -m pytest "$target" --junitxml="$report_file"
}

# Run Unit Tests
if [ "$RUN_UNIT" = true ]; then
    echo "========================================"
    echo "Running Unit Tests..."
    echo "========================================"
    run_pytest "$REPO_ROOT/tests/unit/" "$REPO_ROOT/report_unit.xml"
fi

# Run Integration Tests
if [ "$RUN_INTEGRATION" = true ]; then
    echo "========================================"
    echo "Running Integration Tests..."
    echo "========================================"
    run_pytest "$REPO_ROOT/tests/integration/" "$REPO_ROOT/report_integration.xml"
fi

# Run E2E Tests
if [ "$RUN_E2E" = true ]; then
    echo "========================================"
    echo "Running E2E Tests..."
    echo "========================================"
    run_pytest "$REPO_ROOT/tests/e2e/" "$REPO_ROOT/report_e2e.xml"
fi

echo "========================================"
echo "Done. Test reports generated in $REPO_ROOT/report_*.xml"
