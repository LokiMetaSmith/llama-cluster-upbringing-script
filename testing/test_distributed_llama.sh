#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
# set -e # We'll handle errors manually to provide better feedback

REPO_DIR="distributed-llama-repo"
SETUP_SCRIPT="setup_distributed_llama.sh"

# Function to print success messages
print_success() {
    echo "SUCCESS: $1"
}

# Function to print error messages and exit
print_error_and_exit() {
    echo "ERROR: $1"
    exit 1
}

# --- Make script executable (self) ---
if [ -f "$0" ]; then
    chmod +x "$0"
    echo "INFO: Made test script ($0) executable."
fi

# --- 1. Ensure setup_distributed_llama.sh is executable and run it ---
echo "INFO: Checking for setup script: $SETUP_SCRIPT"
if [ ! -f "$SETUP_SCRIPT" ]; then
    print_error_and_exit "Setup script '$SETUP_SCRIPT' not found!"
fi

echo "INFO: Making $SETUP_SCRIPT executable..."
chmod +x "$SETUP_SCRIPT"
if [ $? -ne 0 ]; then
    print_error_and_exit "Failed to make $SETUP_SCRIPT executable."
fi
print_success "$SETUP_SCRIPT is executable."

echo "INFO: Running $SETUP_SCRIPT..."
./"$SETUP_SCRIPT"
SETUP_EXIT_CODE=$?
if [ $SETUP_EXIT_CODE -ne 0 ]; then
    print_error_and_exit "$SETUP_SCRIPT failed with exit code $SETUP_EXIT_CODE."
fi
print_success "$SETUP_SCRIPT completed successfully."

# --- 2. Verify compilation products ---
echo "INFO: Verifying compilation products..."

echo "INFO: Checking for directory: $REPO_DIR"
if [ ! -d "$REPO_DIR" ]; then
    print_error_and_exit "Repository directory '$REPO_DIR' not found."
fi
print_success "Directory '$REPO_DIR' exists."

DLLAMA_EXEC="$REPO_DIR/dllama"
echo "INFO: Checking for executable: $DLLAMA_EXEC"
if [ ! -x "$DLLAMA_EXEC" ]; then # Check for existence and execute permission
    print_error_and_exit "Executable '$DLLAMA_EXEC' not found or not executable."
fi
print_success "Executable '$DLLAMA_EXEC' exists and is executable."

DLLAMA_API_EXEC="$REPO_DIR/dllama-api"
echo "INFO: Checking for executable: $DLLAMA_API_EXEC"
if [ ! -x "$DLLAMA_API_EXEC" ]; then # Check for existence and execute permission
    print_error_and_exit "Executable '$DLLAMA_API_EXEC' not found or not executable."
fi
print_success "Executable '$DLLAMA_API_EXEC' exists and is executable."

# --- 3. Basic functionality test ---
echo "INFO: Performing basic functionality tests..."

echo "INFO: Running '$DLLAMA_EXEC --help'..."
if "$DLLAMA_EXEC" --help > /dev/null 2>&1; then # Redirect stdout and stderr to /dev/null
    print_success "'$DLLAMA_EXEC --help' executed successfully."
else
    print_error_and_exit "'$DLLAMA_EXEC --help' failed or returned an error."
fi

echo "INFO: Running '$DLLAMA_API_EXEC --help'..."
if "$DLLAMA_API_EXEC" --help > /dev/null 2>&1; then # Redirect stdout and stderr to /dev/null
    print_success "'$DLLAMA_API_EXEC --help' executed successfully."
else
    print_error_and_exit "'$DLLAMA_API_EXEC --help' failed or returned an error."
fi

# --- 4. Cleanup (optional) ---
# To enable cleanup, uncomment the following lines and the function definition.
#
# cleanup() {
#     echo "INFO: Cleaning up..."
#     if [ -d "$REPO_DIR" ]; then
#         read -p "Do you want to remove the '$REPO_DIR' directory? (y/n) " -n 1 -r
#         echo
#         if [[ $REPLY =~ ^[Yy]$ ]]; then
#             echo "INFO: Removing '$REPO_DIR'..."
#             rm -rf "$REPO_DIR"
#             if [ $? -ne 0 ]; then
#                 echo "WARNING: Failed to remove '$REPO_DIR'."
#             else
#                 print_success "Removed '$REPO_DIR'."
#             fi
#         else
#             echo "INFO: Cleanup skipped by user."
#         fi
#     else
#         echo "INFO: '$REPO_DIR' not found, no cleanup needed for it."
#     fi
# }
#
# cleanup

echo ""
echo "----------------------------------------"
echo "All tests passed successfully!"
echo "----------------------------------------"
exit 0
