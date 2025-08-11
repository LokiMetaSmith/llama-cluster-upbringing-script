#!/bin/bash

log "Configuring hostname..."

# Check if the hostname is already set
if [ "$(/bin/hostname)" == "$HOSTNAME" ]; then
    log "Hostname is already set to $HOSTNAME."
else
    /bin/hostnamectl set-hostname "$HOSTNAME"
fi

# Update /etc/hosts
if grep -q "127.0.1.1" /etc/hosts; then
    sed -i "s/127.0.1.1.*/127.0.1.1\t$HOSTNAME/g" /etc/hosts
else
    echo -e "127.0.1.1\t$HOSTNAME" >> /etc/hosts
fi

log "Hostname set to $HOSTNAME."
