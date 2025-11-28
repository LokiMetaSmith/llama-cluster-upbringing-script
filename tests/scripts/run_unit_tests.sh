#!/usr/bin/env bash
set -e

export PATH="/home/jules/.pyenv/shims:$PATH"
python -m pytest tests/unit/
