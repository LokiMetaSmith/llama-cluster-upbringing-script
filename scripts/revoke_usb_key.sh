#!/bin/bash
set -euo pipefail
echo "=== USB Bootstrap Key Revocation ==="
echo "This script will revoke the physical USB bootstrap key (tag:usb-bootstrap)."
echo ""
read -p "Enter Controller SSH alias/IP (e.g. 'controller'): " CONTROLLER_SSH
if [ -z "$CONTROLLER_SSH" ]; then
    echo "Controller SSH is required."
    return 1 2>/dev/null || true
fi
echo "Authenticating to controller..."
KEY_ID=$(ssh -o "ControlMaster=no" "$CONTROLLER_SSH" "sudo headscale --user default preauthkeys list -o json | jq -r '.[] | select(.tags != null) | select(.tags[] == \"tag:usb-bootstrap\") | .id'")
if [ -z "$KEY_ID" ] || [ "$KEY_ID" == "null" ]; then
    echo "No active key found with tag 'tag:usb-bootstrap'."
    return 0 2>/dev/null || true
fi
echo "Found USB bootstrap key with ID: $KEY_ID"
read -p "Are you sure you want to expire this key? (y/n): " CONFIRM
if [[ "$CONFIRM" == "y" || "$CONFIRM" == "Y" ]]; then
    ssh -o "ControlMaster=no" "$CONTROLLER_SSH" "sudo headscale --user default preauthkeys expire $KEY_ID"
    echo "Key $KEY_ID has been successfully revoked."
else
    echo "Revocation cancelled."
fi
