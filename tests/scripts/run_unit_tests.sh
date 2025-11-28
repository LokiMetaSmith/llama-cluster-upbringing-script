#!/usr/bin/env bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

export PATH="/home/jules/.pyenv/shims:$PATH"
python -m pytest "$REPO_ROOT/tests/unit/"
