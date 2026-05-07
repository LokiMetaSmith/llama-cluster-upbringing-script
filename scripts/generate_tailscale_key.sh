#!/bin/bash
# Generate a reusable Headscale pre-auth key valid for 24 hours

if ! command -v headscale &> /dev/null; then
  echo "Headscale is not installed on this system."
  return 1 2>/dev/null || true
fi

echo "Generating a new reusable pre-auth key for user 'default'..."
AUTH_KEY=$(headscale --user default preauthkeys create --reusable --expiration 24h 2>/dev/null | tail -n 1)

if [ -z "$AUTH_KEY" ]; then
    echo "Failed to generate key. Ensure you are running this as root or the headscale service is running."
    return 1 2>/dev/null || true
fi

SERVER_IP=$(ip -4 route get 8.8.8.8 | grep -oP 'src \K\S+')
if [ -z "$SERVER_IP" ]; then
   SERVER_IP="<YOUR_CONTROLLER_IP>"
fi

echo ""
echo "================================================================="
echo "🔑 Pre-auth Key Generated Successfully!"
echo "================================================================="
echo "Key: $AUTH_KEY"
echo ""
echo "To join an external machine to the Tailscale mesh, run the following command on the target machine:"
echo ""
echo "tailscale up --login-server=http://${SERVER_IP}:8085 --authkey=${AUTH_KEY}"
echo "================================================================="
