#!/bin/bash
#
# Automatic YAML Linter Fixer
#
# This script automatically fixes common, repetitive style issues reported by
# yamllint to help clean up the codebase efficiently.

set -e

echo "--- Automatically fixing common YAML issues ---"

# Find all .yaml and .yml files, excluding the .yamllint config itself
FILES=$(find . -type f \( -name "*.yaml" -o -name "*.yml" \) -not -path "./.yamllint")

for file in $FILES; do
  echo "Processing $file..."

  # 1. Remove the '---' document start line if it exists on the first line.
  #    This is to comply with the .yamllint rule '{document-start: {present: false}}'.
  sed -i '1{/^---$/d;}' "$file"

  # 2. Remove any trailing whitespace from the end of all lines.
  sed -i 's/[[:space:]]*$//' "$file"

  # 3. Ensure the file ends with a newline character.
  if [ -n "$(tail -c 1 "$file")" ]; then
    echo "" >> "$file"
  fi
done

echo "✅ YAML files have been automatically fixed."
echo "Please run the linter again to check for any remaining issues."