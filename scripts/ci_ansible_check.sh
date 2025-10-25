#!/bin/bash

# A CI/CD-friendly script to check for unintended changes in Ansible playbooks.
#
# - On the first run in a new environment, it establishes a baseline.
# - On subsequent runs, it compares the playbook's --check output to the baseline.
# - If differences are found, it prints the diff and exits with an error code (1).
# - If no differences are found, it exits with success (0).

# Exit on error
set -e

# --- Configuration ---
# Assuming this script is run from the repository root
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

# If no baseline exists, create one for the CI environment.
if [ ! -f "$BASELINE_LOG" ]; then
  echo "No baseline found. Creating a new one for this CI environment."
  echo "This run will be considered successful by default."
  # Use --update-baseline to run the playbook and then create the check baseline
  "$DIFF_SCRIPT" --update-baseline -i "$INVENTORY" -e "$EXTRA_VARS"
  echo "Baseline created. Future runs will be compared against this."
  exit 0
fi

# A baseline exists, so run the comparison.
echo "Baseline found. Running comparison..."
"$DIFF_SCRIPT" -i "$INVENTORY" -e "$EXTRA_VARS"

# Check the result of the comparison.
# The diff script creates ansible_diff.log only if there are differences.
if [ -s "$DIFF_LOG" ]; then
  echo "!!! ANSIBLE CHANGES DETECTED !!!"
  echo "The following differences were found between the current playbook and the baseline:"
  echo "--------------------------------------------------"
  cat "$DIFF_LOG"
  echo "--------------------------------------------------"
  echo "To approve these changes, the baseline must be updated in the CI environment."
  exit 1
else
  echo "+++ NO CHANGES DETECTED +++"
  echo "The playbook run matches the baseline. Check passed."
  exit 0
fi
