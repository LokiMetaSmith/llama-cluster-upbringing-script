#!/bin/bash

log "Setting up auto-provisioning 'call home' service..."

if [ -z "${CONTROL_NODE_IP:-}" ]; then
    log "CONTROL_NODE_IP not set in setup.conf. Skipping auto-provisioning setup."
    exit 0
fi

# Create the call-home script
cat > /usr/local/bin/call-home.sh << 'EOF'
#!/bin/bash
# This script runs once on first boot to trigger Ansible provisioning.

# Find the IP address of this machine
IP_ADDRESS=$(hostname -I | awk '{print $1}')
CONTROL_NODE_IP="{{ CONTROL_NODE_IP_PLACEHOLDER }}"

echo "Attempting to call home to control node at ${CONTROL_NODE_IP}..."

# Try to call home for up to 5 minutes
for i in {1..30}; do
    curl -s -X POST -H "Content-Type: application/json" \
        -d "{\"ip_address\": \"${IP_ADDRESS}\"}" \
        "http://${CONTROL_NODE_IP}:8001/api/ready-for-provisioning"

    if [ $? -eq 0 ]; then
        echo "Successfully called home. Provisioning should begin shortly."
        # Disable the service to prevent it from running again
        systemctl disable call-home.service
        rm /usr/local/bin/call-home.sh
        exit 0
    fi
    echo "Call home failed. Retrying in 10 seconds..."
    sleep 10
done

echo "Could not call home to control node after 5 minutes. Please check network connectivity and control node status."
exit 1
EOF

# Replace placeholder with actual IP
sed -i "s/{{ CONTROL_NODE_IP_PLACEHOLDER }}/${CONTROL_NODE_IP}/" /usr/local/bin/call-home.sh
chmod +x /usr/local/bin/call-home.sh

# Create the systemd service file
cat > /etc/systemd/system/call-home.service << 'EOF'
[Unit]
Description=Call Home to Trigger Ansible Provisioning
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/call-home.sh

[Install]
WantedBy=multi-user.target
EOF

# Enable the service
systemctl enable call-home.service

log "Auto-provisioning service created and enabled. Node will call home on next boot."
