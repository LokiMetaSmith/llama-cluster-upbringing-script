#!/bin/bash
set -euo pipefail

# This script can be set up as a cron job on the controller to monitor and alert
# if nodes join the tailnet using the physical USB bootstrap key.

WEBHOOK_URL="${SLACK_WEBHOOK_URL:-}"
if [ -z "$WEBHOOK_URL" ]; then
    echo "Warning: SLACK_WEBHOOK_URL is not set. Alerts will only be logged."
fi

# Get all nodes that authenticated using the usb-bootstrap tag
BOOTSTRAP_NODES=$(sudo headscale nodes list -o json | jq -r '.[] | select(.preAuthKey != null and .preAuthKey.tags != null and (.preAuthKey.tags[] == "tag:usb-bootstrap")) | .name')

if [ -n "$BOOTSTRAP_NODES" ]; then
    MESSAGE="🚨 *SECURITY ALERT*: The physical USB bootstrap key was used to enroll the following node(s):\n$BOOTSTRAP_NODES\n\nIf this was not an intentional bare-metal provisioning event, revoke the key immediately using \`scripts/revoke_usb_key.sh\`."

    echo -e "$MESSAGE"

    if [ -n "$WEBHOOK_URL" ]; then
        curl -s -X POST -H 'Content-type: application/json' --data "{\"text\": \"$MESSAGE\"}" "$WEBHOOK_URL" > /dev/null
    fi
fi
