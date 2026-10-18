#!/bin/bash
# scripts/halo_pxe_bringup.sh
# Reference implementation for `llama-cluster-upbringing-script`
# Target silicon: Ryzen AI MAX 395 ("Strix Halo"), 64 GB unified DDR5

set -e

echo "Starting Strix Halo APU PXE bring-up..."

# 1. Hardware/OS sanity check
total_mem=$(free -m | awk '/^Mem:/{print $2}')
if [ "$total_mem" -lt 60000 ]; then
  echo "WARNING: Expected ~64GB unified memory for Strix Halo, found ${total_mem}MB."
fi

# 2. ROCm Library Load Order Fix
# This silicon requires careful library loading for the torchaudio/ROCm CUDA-lib path.
# Setting LD_PRELOAD to ensure the correct HSA runtime is loaded first.
export LD_PRELOAD=/opt/rocm/lib/libhsa-runtime64.so.1:$LD_PRELOAD
export HSA_OVERRIDE_GFX_VERSION=11.5.0 # Ensure compatible ISA

# 3. Kernel module verification
if ! lsmod | grep -q amdgpu; then
    echo "ERROR: amdgpu driver not loaded. iGPU not detected."
    exit 1
fi

echo "Strix Halo hardware detected and ROCm environment configured."

# 4. Trigger deployment via Provisioning API (Call Home)
echo "Notifying Provisioning API to trigger Ansible deployment..."
curl -s -X POST -H "Content-Type: application/json" -d '{"node_type": "strix_halo", "status": "ready"}' http://10.10.10.10:8000/api/provisioning/call-home || true

echo "PXE bring-up script completed."
