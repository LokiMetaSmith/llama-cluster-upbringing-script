#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

REPO_URL="https://github.com/b4rtaz/distributed-llama.git"
REPO_DIR="distributed-llama-repo"

# --- Clone Repository ---
echo "Checking for repository directory: $REPO_DIR"
if [ -d "$REPO_DIR" ]; then
    echo "Directory $REPO_DIR already exists."
    #
    # TODO: Add logic to offer to update the repo, e.g., git pull
    # For now, we'll just proceed, assuming it's up-to-date or the user wants to use the existing version.
    #
    # read -p "Directory $REPO_DIR already exists. Do you want to pull the latest changes? (y/n) " -n 1 -r
    # echo
    # if [[ $REPLY =~ ^[Yy]$ ]]; then
    #     echo "Pulling latest changes..."
    #     cd "$REPO_DIR"
    #     git pull
    #     cd ..
    # fi
else
    echo "Cloning $REPO_URL into $REPO_DIR..."
    if git clone "$REPO_URL" "$REPO_DIR"; then
        echo "Repository cloned successfully."
    else
        echo "Error: Failed to clone repository."
        exit 1
    fi
fi

# --- Compile Project ---
echo "Changing directory to $REPO_DIR"
cd "$REPO_DIR"

echo "Compiling main application (dllama)..."
if make dllama; then
    echo "dllama compiled successfully."
else
    echo "Error: Failed to compile dllama."
    exit 1
fi

echo "Compiling API server (dllama-api)..."
if make dllama-api; then
    echo "dllama-api compiled successfully."
else
    echo "Error: Failed to compile dllama-api."
    exit 1
fi

echo "Compilation finished."

# --- Basic Invocation Examples ---
echo ""
echo "--------------------------------------------------"
echo "Basic Invocation Examples (commented out):"
echo "--------------------------------------------------"
echo "# To run these examples, you'll need to be in the $REPO_DIR directory."
echo "# Ensure you have a model and tokenizer available."
echo ""
echo "# Example: Run worker node"
echo "# ./dllama worker --port 9999 --nthreads 4"
echo ""
echo "# Example: Run root node (replace with actual model and tokenizer paths)"
echo "# ./dllama inference --model <path_to_model> --tokenizer <path_to_tokenizer> --workers <worker_ip:port>"
echo ""
echo "# Example: Run API server (replace with actual model and tokenizer paths)"
echo "# ./dllama-api --model <path_to_model> --tokenizer <path_to_tokenizer> --host 0.0.0.0 --port 8080"
echo "--------------------------------------------------"

# --- Permissions ---
# The script itself needs execute permissions.
# This can be done by running: chmod +x setup_distributed_llama.sh
# Adding a line to make itself executable (though it's often done by the user post-creation)
if [ -f "$0" ]; then
    chmod +x "$0"
    echo "Made the script ($0) executable."
fi

echo ""
echo "Setup script completed successfully."
exit 0
