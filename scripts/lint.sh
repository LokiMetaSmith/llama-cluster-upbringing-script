#!/bin/bash
#
# Unified Linting Script
#
# This script runs a series of linters to ensure code quality and consistency
# across the repository. It checks YAML, Markdown, Nomad (HCL), and Jinja2 files.
# It uses an exclude file at scripts/lint_exclude.txt to ignore problematic files.

set -e # Exit immediately if a command exits with a non-zero status.

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

echo "--- Running YAML Linter ---"
# Find all yaml files.
YAML_FILES_TO_LINT=$(find . -type f \( -name "*.yaml" -o -name "*.yml" \))

# If an exclude file exists, filter the list of files.
if [ -f "$EXCLUDE_FILE" ]; then
    EXCLUDE_PATTERNS=$(grep -v '^#' "$EXCLUDE_FILE" | grep -v '^$')
    if [ -n "$EXCLUDE_PATTERNS" ]; then
        YAML_FILES_TO_LINT=$(echo "$YAML_FILES_TO_LINT" | grep -vFf <(echo "$EXCLUDE_PATTERNS"))
    fi
fi

# Run yamllint only if there are files to lint.
if [ -n "$YAML_FILES_TO_LINT" ]; then
    # We are intentionally word-splitting the file list.
    # shellcheck disable=SC2086
    yamllint $YAML_FILES_TO_LINT
fi

echo "--- Running Markdown Linter ---"
# Use npx to run the version specified in package.json.
# The ignore arguments must be unquoted to be treated as separate flags.
npx markdownlint-cli "**/*.md" --ignore "node_modules/**" $MARKDOWN_IGNORE_ARGS

echo "--- Running Nomad Formatter Check ---"
if command -v ansible-playbook &> /dev/null; then
    # Run the check via Ansible to ensure it runs on a provisioned node
    ansible-playbook -i local_inventory.ini ansible/lint_nomad.yaml
else
    echo "⚠️  Warning: ansible-playbook not found. Skipping Nomad format check."
    echo "Please install Ansible to enable this check."
fi

echo "--- Running Jinja2 Linter ---"
# Pass the exclude arguments to djlint. They must be unquoted.
djlint . $DJLINT_EXCLUDE_ARGS

echo "✅ All linters passed successfully!"