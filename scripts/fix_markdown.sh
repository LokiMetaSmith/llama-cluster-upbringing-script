#!/bin/bash
#
# Automatic Markdown Linter Fixer
#
# This script uses markdownlint-cli's --fix option to automatically correct
# common formatting and style issues in all Markdown files.

set -e

echo "--- Automatically fixing common Markdown issues ---"

# Use npx to run the version specified in package.json and apply fixes.
# The "**/*.md" pattern ensures it runs on all Markdown files recursively.
npx markdownlint-cli --fix "**/*.md" --ignore "node_modules/**"

echo "✅ Markdown files have been automatically fixed."
echo "Please run the linter again to check for any remaining issues."