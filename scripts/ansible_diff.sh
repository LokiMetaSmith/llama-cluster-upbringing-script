#!/bin/bash

# A script to compare Ansible playbook runs to detect changes over time.
# It establishes a baseline from a --check run on a known-good system state
# and compares subsequent --check runs against it.

# Exit on error
set -e

# --- Configuration & Defaults ---
PLAYBOOK="playbook.yaml"
BASELINE_LOG="ansible_run.baseline.log"
CURRENT_CHECK_LOG="ansible_run.check.log"
DIFF_LOG="ansible_diff.log"
INVENTORY="local_inventory.ini"
EXTRA_VARS="target_user=jules" # Default extra vars

# --- Argument Parsing ---
UPDATE_BASELINE=false
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --update-baseline)
      UPDATE_BASELINE=true
      shift # past argument
      ;;
    -i|--inventory)
      INVENTORY="$2"
      shift # past argument
      shift # past value
      ;;
    -e|--extra-vars)
      EXTRA_VARS="$2"
      shift # past argument
      shift # past value
      ;;
    *)    # unknown option
      echo "Unknown option: $1"
      echo "Usage: $0 [--update-baseline] [-i INVENTORY] [-e 'EXTRA_VARS']"
      exit 1
      ;;
  esac
done


# --- Functions ---
run_playbook() {
  local output_log=$1
  shift
  local ansible_args="$@"

  echo "Running: ansible-playbook -i $INVENTORY $PLAYBOOK --extra-vars=\"$EXTRA_VARS\" $ansible_args"
  ansible-playbook -i "$INVENTORY" "$PLAYBOOK" --extra-vars="$EXTRA_VARS" $ansible_args > "$output_log" 2>&1
  echo "Playbook run finished. Log saved to $output_log"
}

# --- Main Script ---

# Handle baseline update
if [ "$UPDATE_BASELINE" = true ]; then
  echo "--- Updating Baseline ---"
  echo "Step 1: Applying playbook to ensure system is in the desired state..."
  run_playbook "/dev/null" "" # Run for real, discard output
  echo "Step 2: Running in --check mode to create a clean baseline..."
  run_playbook "$BASELINE_LOG" "--check --diff"
  echo "Baseline updated successfully."
  exit 0
fi

# Handle initial run (no baseline exists)
if [ ! -f "$BASELINE_LOG" ]; then
  echo "--- Initial Run ---"
  echo "No baseline found at '$BASELINE_LOG'."
  echo "Please create one by running the playbook to configure the system, then run this script with the --update-baseline flag."
  echo "Example: ./scripts/ansible_diff.sh --update-baseline"
  exit 1
fi

# --- Comparison Run ---
echo "--- Comparing to Baseline ---"
echo "A baseline exists. Running playbook in --check --diff mode."
run_playbook "$CURRENT_CHECK_LOG" "--check --diff"

echo "Comparing current check run with the baseline..."
diff -u "$BASELINE_LOG" "$CURRENT_CHECK_LOG" > "$DIFF_LOG" || [ $? -eq 1 ]

if [ -s "$DIFF_LOG" ]; then
  echo "Differences found between the --check run and the baseline."
  echo "This indicates that running the playbook will result in changes."
  echo "Review the differences in '$DIFF_LOG'."
else
  echo "No differences found. The system state matches the baseline."
  rm "$DIFF_LOG"
fi

# Clean up the temporary check log
rm "$CURRENT_CHECK_LOG"

echo "Comparison finished."
