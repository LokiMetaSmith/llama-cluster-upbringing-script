#!/bin/bash
#
# Agent Preflight Checklist
#
# This script MUST be run by the agent prior to submitting code.
# It runs all tests, linters, static analysis, and dead code detection.

# Ensure we are running from the repository root
cd "$(dirname "$0")/.." || exit 1

EXIT_CODE=0

echo "======================================"
echo "    AGENT PREFLIGHT CHECKLIST       "
echo "======================================"

echo ""
echo "[1/4] Running Linters (scripts/lint.sh)..."
./scripts/lint.sh
if [ $? -ne 0 ]; then
    echo "❌ Linters failed."
    EXIT_CODE=1
else
    echo "✅ Linters passed."
fi

echo ""
echo "[2/4] Running Static Analysis (mypy)..."
if command -v mypy &> /dev/null; then
    mypy pipecatapp scripts
    if [ $? -ne 0 ]; then
        echo "❌ mypy failed."
        EXIT_CODE=1
    else
        echo "✅ mypy passed."
    fi
else
    echo "⚠️  mypy not found. Please ensure it is installed (pip install mypy)."
    EXIT_CODE=1
fi

echo ""
echo "[3/4] Running Dead Code Detection (vulture)..."
if command -v vulture &> /dev/null; then
    vulture
    if [ $? -ne 0 ]; then
        echo "❌ vulture detected potential dead code. Please review and clean it up, or whitelist false positives in .vulture_whitelist.py"
        EXIT_CODE=1
    else
        echo "✅ vulture passed."
    fi
else
    echo "⚠️  vulture not found. Please ensure it is installed (pip install vulture)."
    EXIT_CODE=1
fi

echo ""
echo "[4/4] Running Unit Tests with Coverage (pytest)..."
if command -v pytest &> /dev/null; then
    # We only care if tests pass, coverage drop doesn't strictly fail unless configured later,
    # but we generate the report for the agent to review.
    pytest --cov=pipecatapp --cov-report=term-missing tests/unit/
    if [ $? -ne 0 ]; then
        echo "❌ Unit tests failed."
        EXIT_CODE=1
    else
        echo "✅ Unit tests passed."
    fi
else
    echo "⚠️  pytest not found. Please ensure it is installed."
    EXIT_CODE=1
fi

echo ""
echo "======================================"
if [ "$EXIT_CODE" -ne 0 ]; then
    echo "❌ PREFLIGHT CHECKS FAILED."
    echo "You must fix the issues above before submitting your code."
    exit 1
else
    echo "✅ PREFLIGHT CHECKS PASSED SUCCESSFULLY."
    exit 0
fi
