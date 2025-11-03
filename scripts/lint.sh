#!/bin/bash
#
# Unified Linting Script
#
# This script runs a series of linters to ensure code quality and consistency.
# It accumulates failures and reports them at the end, rather than exiting on
# the first error.

EXIT_CODE=0

# Helper function to run a command, capture its exit code, and print status.
run_linter() {
    local name="$1"
    shift
    echo "--- Running $name ---"

    # Check if the command exists
    if ! command -v "$1" &> /dev/null; then
        echo "⚠️  Warning: command '$1' not found. Skipping."
        echo
        return
    fi

    # Execute the command with its arguments
    "$@"
    local status=$?
    if [ $status -ne 0 ]; then
        # The linter's own stderr is the primary error report.
        # We set a flag to indicate failure but don't print extra messages.
        EXIT_CODE=1
    fi
    echo
}

# --- Build Exclude Arguments ---
EXCLUDE_FILE="scripts/lint_exclude.txt"
MARKDOWN_IGNORE_ARGS=""
# Start with default excludes, using separate flags for each
DJLINT_EXCLUDE_ARGS="--exclude node_modules --exclude venv"

if [ -f "$EXCLUDE_FILE" ]; then
    # Read file line by line, ignoring comments and empty lines
    while IFS= read -r line || [[ -n "$line" ]]; do
        if [[ "$line" =~ ^#.*$ ]] || [[ -z "$line" ]]; then
            continue
        fi
        MARKDOWN_IGNORE_ARGS+=" --ignore $line"
        DJLINT_EXCLUDE_ARGS+=" --exclude $line"
    done < "$EXCLUDE_FILE"
fi

# --- Run Linters ---

# YAML Linter
# Find all yaml files and filter them.
YAML_FILES_TO_LINT=$(find . -type f \( -name "*.yaml" -o -name "*.yml" \))
if [ -f "$EXCLUDE_FILE" ]; then
    EXCLUDE_PATTERNS=$(grep -v '^#' "$EXCLUDE_FILE" | grep -v '^$')
    if [ -n "$EXCLUDE_PATTERNS" ]; then
        YAML_FILES_TO_LINT=$(echo "$YAML_FILES_TO_LINT" | grep -vFf <(echo "$EXCLUDE_PATTERNS"))
    fi
fi
if [ -n "$YAML_FILES_TO_LINT" ]; then
    # Word splitting is intentional and required for yamllint to receive multiple files.
    # shellcheck disable=SC2086
    run_linter "YAML Linter" yamllint $YAML_FILES_TO_LINT
fi

# Markdown Linter
# Word splitting is intentional for ignore args.
# shellcheck disable=SC2086
run_linter "Markdown Linter" npx markdownlint-cli "**/*.md" --ignore "node_modules/**" $MARKDOWN_IGNORE_ARGS

# Nomad Formatter Check (not a linter, run directly)
if command -v ansible-playbook &> /dev/null; then
    echo "--- Running Nomad Formatter Check ---"
    ansible-playbook -i local_inventory.ini ansible/lint_nomad.yaml
    echo
else
    echo "⚠️  Warning: ansible-playbook not found. Skipping Nomad format check."
    echo
fi

# Jinja2 Linter
# Word splitting is intentional for exclude args.
# shellcheck disable=SC2086
run_linter "Jinja2 Linter" djlint . $DJLINT_EXCLUDE_ARGS


# --- Final Exit Status ---
if [ "$EXIT_CODE" -ne 0 ]; then
    echo "❌ One or more linters failed."
    exit 1
fi

echo "✅ All linters passed successfully!"
exit 0
