#!/bin/bash

echo "Configuring user..."

# Check if the user is already in the sudo group
if groups "$USERNAME" | grep -q '\bsudo\b'; then
    echo "User $USERNAME is already in the sudo group."
else
    echo "Adding user $USERNAME to the sudo group..."
    usermod -aG sudo "$USERNAME"
    echo "User $USERNAME added to the sudo group."
fi

echo "User configuration complete."
