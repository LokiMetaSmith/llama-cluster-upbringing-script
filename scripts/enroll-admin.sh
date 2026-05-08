#!/bin/bash
# Enroll a human operator using a security key challenge

DOMAIN="headscale.local.mesh"
USER="admin-$(hostname)"

echo "Step 1: Authenticating with Hardware Key..."
# This triggers the physical touch on your Yubikey to sign the enrollment request
ssh -o "ControlMaster=no" controller "headscale nodes list" > /dev/null

if [ $? -eq 0 ]; then
    echo "Step 2: Generating Pre-Auth Key..."
    AUTH_KEY=$(ssh controller "sudo headscale --user default preauthkeys create --reusable --expiration 1h 2>/dev/null | tail -n 1")

    echo "Step 3: Joining Tailnet via $DOMAIN..."
    sudo tailscale up --login-server=https://$DOMAIN --authkey=$AUTH_KEY
else
    echo "Authentication failed. Physical key not present or rejected."
fi
