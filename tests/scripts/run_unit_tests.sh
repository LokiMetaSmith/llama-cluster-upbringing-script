#!/usr/bin/env bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Detect and activate virtual environment if needed
if [[ -z "$VIRTUAL_ENV" ]]; then
    if [[ -d "$REPO_ROOT/.venv" ]]; then
        # echo "Activating virtual environment at $REPO_ROOT/.venv"
        source "$REPO_ROOT/.venv/bin/activate"
    fi
fi

# Detect Python interpreter
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python not found. Please install Python 3."
    exit 1
fi

$PYTHON_CMD -m pytest "$REPO_ROOT/tests/unit/"
