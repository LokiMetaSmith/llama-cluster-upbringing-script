#!/bin/bash

echo "Configuring hostname..."

# Check if the hostname is already set
if [ "$(hostname)" == "$HOSTNAME" ]; then
    echo "Hostname is already set to $HOSTNAME."
    exit 0
fi

hostnamectl set-hostname "$HOSTNAME"

# Update /etc/hosts
sed -i "s/127.0.1.1.*/127.0.1.1\t$HOSTNAME/g" /etc/hosts

echo "Hostname set to $HOSTNAME."
