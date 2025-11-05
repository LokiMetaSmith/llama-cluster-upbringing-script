#!/bin/bash

# A CI/CD-friendly script to check for unintended changes in Ansible playbooks.
#
# - It compares the playbook's --check output to a baseline.
# - If differences are found, it prints the diff and exits with an error code (1).
# - If no differences are found, it exits with success (0).
#
# This script assumes the baseline file is managed by the CI system (e.g., a cache).

# Exit on error
set -e

# --- Configuration ---
SCRIPT_DIR="$(dirname "$0")"
TEST_SCRIPT="$SCRIPT_DIR/test_playbooks_dry_run.sh"
DIFF_LOGS=(*.diff.log playbooks/*.diff.log playbooks/services/*.diff.log)

# --- Main Script ---

echo "--- Ansible Change Detection CI Check ---"

# Ensure the test script is executable
chmod +x "$TEST_SCRIPT"

# If no baseline exists, this is a problem. The CI cache should have restored it.
# The only exception is the very first run on a new branch.
if ! ls *.baseline.log >/dev/null 2>&1; then
  echo "No baselines found. This is expected for the first run on a new branch."
  echo "Creating new baselines now. This run will pass by default."
  "$TEST_SCRIPT" --update-baseline
  exit 0
fi

# A baseline exists, so run the comparison.
echo "Baselines found. Running comparison..."
"$TEST_SCRIPT"

# Check the result of the comparison.
for log in "${DIFF_LOGS[@]}"; do
  if [ -s "$log" ]; then
    echo "!!! ANSIBLE CHANGES DETECTED !!!"
    echo "The following differences were found in $log:"
    echo "--------------------------------------------------"
    cat "$log"
    echo "--------------------------------------------------"
    echo "If these changes are intentional, the baseline needs to be updated."
    echo "To do this, delete the cache for this branch in the GitHub Actions UI and re-run the workflow."
    exit 1
  fi
done

echo "+++ NO CHANGES DETECTED +++"
echo "The playbook run matches the baseline. Check passed."
exit 0
