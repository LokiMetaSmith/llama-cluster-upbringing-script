#!/bin/bash
TOTAL_APP_SIZE=0

if [ -d "/opt/nomad" ]; then
    SIZE=$(du -sb /opt/nomad 2>/dev/null | cut -f1)
    TOTAL_APP_SIZE=$((TOTAL_APP_SIZE + SIZE))
fi
if [ -d "/opt/consul" ]; then
    SIZE=$(du -sb /opt/consul 2>/dev/null | cut -f1)
    TOTAL_APP_SIZE=$((TOTAL_APP_SIZE + SIZE))
fi
if [ -d "/var/lib/docker" ]; then
    SIZE=$(du -sb /var/lib/docker 2>/dev/null | cut -f1)
    TOTAL_APP_SIZE=$((TOTAL_APP_SIZE + SIZE))
fi
if [ -d "/var/lib/containerd" ]; then
    SIZE=$(du -sb /var/lib/containerd 2>/dev/null | cut -f1)
    TOTAL_APP_SIZE=$((TOTAL_APP_SIZE + SIZE))
fi
if [ -d "/opt/mcp" ]; then
    SIZE=$(du -sb /opt/mcp 2>/dev/null | cut -f1)
    TOTAL_APP_SIZE=$((TOTAL_APP_SIZE + SIZE))
fi
if [ -d "/opt/cluster-infra" ]; then
    SIZE=$(du -sb /opt/cluster-infra 2>/dev/null | cut -f1)
    TOTAL_APP_SIZE=$((TOTAL_APP_SIZE + SIZE))
fi

echo "TOTAL_APP_SIZE_BYTES=$TOTAL_APP_SIZE"
