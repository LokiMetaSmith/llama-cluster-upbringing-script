#!/bin/bash
#
# Unified Linting Script
#
# This script runs a series of linters to ensure code quality and consistency
# across the repository. It checks YAML, Markdown, Nomad (HCL), and Jinja2 files.
# Linter configurations are managed in their respective config files (e.g., .djlint.toml).

set -e # Exit immediately if a command exits with a non-zero status.

echo "--- Running YAML Linter ---"
# yamllint will automatically ignore node_modules based on the .yamllint config.
yamllint .

echo "--- Running Markdown Linter ---"
# We must explicitly ignore the node_modules directory.
npx markdownlint-cli "**/*.md" --ignore "node_modules/**"

echo "--- Running Nomad Formatter Check ---"
if command -v ansible-playbook &> /dev/null; then
    # Run the check via Ansible to ensure it runs on a provisioned node
    ansible-playbook -i local_inventory.ini ansible/lint_nomad.yaml
else
    echo "⚠️  Warning: ansible-playbook not found. Skipping Nomad format check."
    echo "Please install Ansible to enable this check."
fi

echo "--- Running Jinja2 Linter ---"
# Explicitly target the only Jinja2 template and ignore all known false-positive rules.
djlint ansible/jobs/prima-expert.nomad --profile jinja --ignore H022,T001,T027

echo "✅ All linters passed successfully!"