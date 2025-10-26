#!/bin/bash

# ---
# Flexible Ansible Playbook Checker
#
# This script recursively finds all .yaml and .yml files, filters them to identify
# likely playbook files (by checking for a '- hosts:' key), and then runs
# 'ansible-playbook --check' on them. It can also log output to a file.
#
# USAGE:
#   ./check_all_playbooks.sh        (Runs with output to console only)
#   ./check_all_playbooks.sh --log  (Runs, outputs to console AND playbook_check.log)
#   ./check_all_playbooks.sh -l     (Same as --log)
# ---

# --- Configuration ---
LOG_FILE="playbook_check.log"
LOGGING_ENABLED=false

# --- Argument Parsing ---
if [[ "$1" == "-l" || "$1" == "--log" ]]; then
  LOGGING_ENABLED=true
fi

# --- Main Logic Function ---
run_playbook_checks() {
  # --- FIX 4: Find the ansible-playbook executable dynamically ---
  local ansible_executable
  if command -v ansible-playbook &> /dev/null; then
    ansible_executable=$(command -v ansible-playbook)
  else
    ansible_executable=$(find "$HOME/.pyenv" -type f -name "ansible-playbook" | head -n 1)
  fi

  if [[ -z "$ansible_executable" ]]; then
    echo "ERROR: 'ansible-playbook' executable not found." >&2
    echo "Please ensure Ansible is installed and in your PATH or pyenv." >&2
    return 1
  fi
  # --- END FIX 4 ---

  echo "Starting Ansible playbook check..."
  echo "Using executable: $ansible_executable"
  echo

  local found_files=0

  # --- FIX 3: Use Process Substitution to avoid a subshell for the while loop ---
  # This ensures the 'found_files' counter works correctly.
  while IFS= read -r -d $'\0' playbook; do

    # --- FIX 2: Improved grep to find '- hosts:' ---
    # This correctly identifies playbooks that start with a list.
    if grep -q -E '^\s*-\s*hosts:' "$playbook"; then
      ((found_files++))
      echo "================================================="
      echo "Checking Playbook: $playbook"
      echo "================================================="

      # --- FIX 1: Use an array for extra_args instead of eval ---
      local extra_args=()

      local playbook_filename
      playbook_filename=$(basename -- "$playbook")

      case "$playbook_filename" in
        "playbook.yaml")
          # Each argument is a separate element in the array
          extra_args=("-e" "target_user=jules")
          ;;
        "promote_controller.yaml")
          extra_args=("-e" "worker_hostname=worker1")
          ;;
        "deploy_app.yaml")
          # Multiple arguments are just more elements
          extra_args=("-e" "app_version=1.5.2" "-e" "skip_database_check=true")
          ;;
        "diagnose_failure.yaml")
          extra_args=("-e" "target_host=server1.example.com")
          ;;
      esac

      # --- FIX 1 (cont.): Execute safely using array expansion ---
      # The "${extra_args[@]}" part expands safely to all our arguments.
      "$ansible_executable" --check "${extra_args[@]}" "$playbook" 2>&1

      if [ $? -eq 0 ]; then
        echo "Dry-run PASSED for ${playbook}"
      else
        echo "Dry-run FAILED for ${playbook}"
      fi
      echo
    fi
  done < <(find . -type f \( -name "*.yaml" -o -name "*.yml" \) \
      -not -path "./testing/*" \
      -not -path "./prompt_engineering/*" \
      -print0) # <-- Process Substitution feeds the loop

  if [ "$found_files" -eq 0 ]; then
    echo "No valid playbook files found."
  else
    echo "================================================="
    echo "All playbook checks complete. Found $found_files playbooks."
    echo "================================================="
  fi
}

# --- Execution ---
if [ "$LOGGING_ENABLED" = true ]; then
  echo "Logging enabled. Output will be in $LOG_FILE"
  > "$LOG_FILE"
  run_playbook_checks 2>&1 | tee -a "$LOG_FILE"
else
  echo "Logging disabled. Output to console only."
  echo
  run_playbook_checks
fi
