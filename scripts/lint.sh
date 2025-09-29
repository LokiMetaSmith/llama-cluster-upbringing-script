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
DJLINT_EXCLUDE_ARGS="node_modules,venv" # Start with default excludes

if [ -f "$EXCLUDE_FILE" ]; then
    # Read file line by line, ignoring comments and empty lines
    while IFS= read -r line || [[ -n "$line" ]]; do
        if [[ "$line" =~ ^#.*$ ]] || [[ -z "$line" ]]; then
            continue
        fi
        MARKDOWN_IGNORE_ARGS+=" --ignore $line"
        DJLINT_EXCLUDE_ARGS+=",$line"
    done < "$EXCLUDE_FILE"
fi

echo "--- Running YAML Linter ---"
# Find all yaml files and filter them using grep. The -f flag reads patterns from a file.
# We filter the exclude file to remove comments and empty lines before passing it to grep.
if [ -f "$EXCLUDE_FILE" ]; then
    EXCLUDE_PATTERNS=$(grep -v '^#' "$EXCLUDE_FILE" | grep -v '^$')
    if [ -n "$EXCLUDE_PATTERNS" ]; then
        # Use process substitution to feed the patterns to grep's -f option
        yamllint $(find . -type f \( -name "*.yaml" -o -name "*.yml" \) | grep -vFf <(echo "$EXCLUDE_PATTERNS"))
    else
        yamllint . # Run on all files if exclude list is empty
    fi
else
    yamllint . # Run on all files if exclude file doesn't exist
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
# Pass the comma-separated exclude list to djlint
djlint . --exclude "$DJLINT_EXCLUDE_ARGS"

echo "✅ All linters passed successfully!"