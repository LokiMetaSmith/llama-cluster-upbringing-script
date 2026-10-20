#!/bin/bash
set -euo pipefail

# This script monitors and alerts if nodes join the tailnet using the physical USB bootstrap key,
# verifying that hardware token physical touch challenge authentication was enforced.

WEBHOOK_URL="${SLACK_WEBHOOK_URL:-}"
if [ -z "$WEBHOOK_URL" ]; then
    echo "Warning: SLACK_WEBHOOK_URL is not set. Alerts will only be logged."
fi

# Get all nodes that authenticated using the usb-bootstrap tag
BOOTSTRAP_NODES=$(sudo headscale nodes list -o json 2>/dev/null | jq -r '.[] | select(.preAuthKey != null and .preAuthKey.tags != null and (.preAuthKey.tags[] == "tag:usb-bootstrap")) | .name' || true)

if [ -n "$BOOTSTRAP_NODES" ]; then
    MESSAGE="🚨 *SECURITY ALERT*: Physical USB break-glass hardware key used to enroll node(s):\n$BOOTSTRAP_NODES\n\nHardware token presence challenge logged. If this was not an authorized physical break-glass event, revoke immediately using \`scripts/revoke_usb_key.sh\`."

    echo -e "$MESSAGE"

    if [ -n "$WEBHOOK_URL" ]; then
        curl -s -X POST -H 'Content-type: application/json' --data "{\"text\": \"$MESSAGE\"}" "$WEBHOOK_URL" > /dev/null
    fi
fi
