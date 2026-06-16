#!/bin/bash

# Memory Check
NOMAD_MEM=$(systemctl show -p MemoryCurrent nomad.service 2>/dev/null | awk -F= '{print $2}')
CONSUL_MEM=$(systemctl show -p MemoryCurrent consul.service 2>/dev/null | awk -F= '{print $2}')
DOCKER_MEM=$(systemctl show -p MemoryCurrent docker.service 2>/dev/null | awk -F= '{print $2}')
CONTAINERD_MEM=$(systemctl show -p MemoryCurrent containerd.service 2>/dev/null | awk -F= '{print $2}')
IPFS_MEM=$(systemctl show -p MemoryCurrent ipfs.service 2>/dev/null | awk -F= '{print $2}')

# Sum
echo "NOMAD_MEM=$NOMAD_MEM"
echo "CONSUL_MEM=$CONSUL_MEM"
echo "DOCKER_MEM=$DOCKER_MEM"
echo "CONTAINERD_MEM=$CONTAINERD_MEM"
