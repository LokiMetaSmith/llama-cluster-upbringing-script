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
DIFF_SCRIPT="$SCRIPT_DIR/ansible_diff.sh"
BASELINE_LOG="ansible_run.baseline.log"
DIFF_LOG="ansible_diff.log"
INVENTORY="local_inventory.ini"
EXTRA_VARS="target_user=jules"

# --- Main Script ---

echo "--- Ansible Change Detection CI Check ---"

# Ensure the diff script is executable
chmod +x "$DIFF_SCRIPT"

# If no baseline exists, this is a problem. The CI cache should have restored it.
# The only exception is the very first run on a new branch.
if [ ! -f "$BASELINE_LOG" ]; then
  echo "No baseline found. This is expected for the first run on a new branch."
  echo "Creating a new baseline now. This run will pass by default."
  "$DIFF_SCRIPT" --update-baseline -i "$INVENTORY" -e "$EXTRA_VARS"
  exit 0
fi

# A baseline exists, so run the comparison.
echo "Baseline found. Running comparison..."
"$DIFF_SCRIPT" -i "$INVENTORY" -e "$EXTRA_VARS"

# Check the result of the comparison.
if [ -s "$DIFF_LOG" ]; then
  echo "!!! ANSIBLE CHANGES DETECTED !!!"
  echo "The following differences were found between the current playbook and the baseline:"
  echo "--------------------------------------------------"
  cat "$DIFF_LOG"
  echo "--------------------------------------------------"
  echo "If these changes are intentional, the baseline needs to be updated."
  echo "To do this, delete the cache for this branch in the GitHub Actions UI and re-run the workflow."
  exit 1
else
  echo "+++ NO CHANGES DETECTED +++"
  echo "The playbook run matches the baseline. Check passed."
  exit 0
fi
