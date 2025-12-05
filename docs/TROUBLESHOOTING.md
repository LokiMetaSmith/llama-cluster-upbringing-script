# Troubleshooting Guide

This document provides solutions to common issues encountered when operating the Distributed Conversational AI Pipeline.

## Common Issues

### 1. Nomad Server Checks Failing ("All service checks failing")

**Symptom:**
When viewing the Consul UI or running `consul monitor`, you see Nomad server or client services with the status "All service checks failing". This often appears alongside valid, passing checks for other Nomad instances.

**Example Output:**

```text
_nomad-server-chx5chd3agtnx24itv4quxsopdgskyme
All service checks failing
All node checks passing
loki-at-work
192.168.1.99:4647
rpc
```

**Cause:**
This issue typically occurs after a configuration change (e.g., changing the IP address Nomad binds to) or after resetting the Nomad state (wiping `/opt/nomad/data`) without also resetting the Consul state.

Nomad generates a unique Node ID and persists it in its data directory. If this directory is deleted, Nomad generates a new ID upon restart. However, the old service registrations (linked to the old ID) remain in Consul's persistent store, and since the old instance is no longer running, its health checks fail.

**Solution:**
Use the provided cleanup script to remove these stale service registrations.

1. **Run the pruning script in dry-run mode:**
   This script runs on the controller node (where Consul is running).

   ```bash
   python3 scripts/prune_consul_services.py
   ```

   This will list the stale services that have all health checks in a critical state.

2. **Execute the cleanup:**
   If the list looks correct (i.e., it only contains the failing `_nomad-server-` or `_nomad-client-` IDs), run the script with the `--force` flag:

   ```bash
   python3 scripts/prune_consul_services.py --force
   ```

3. **Verify:**
   Check the Consul UI or `nomad status` to ensure the failing checks are gone.

### 2. "Waiting for cache lock" Error

**Symptom:**
Ansible tasks fail with "Waiting for cache lock: Could not get lock /var/lib/dpkg/lock-frontend".

**Cause:**
This means another process (usually `unattended-upgrades` or a manual `apt` command) is currently installing software.

**Solution:**
Wait for the background process to finish, or if you are sure no other process should be running, reboot the node.

### 3. Nomad Jobs Stuck in "Pending"

**Symptom:**
Jobs submitted to Nomad stay in the "Pending" state and are not placed on any nodes.

**Cause:**

- Lack of resources (CPU/Memory).
- Constraint mismatches (e.g., job requires a specific device or kernel capability).
- Nodes are down or ineligible.

**Solution:**

- Run `nomad job allocs <job_name>` to see allocation status.
- Check `nomad node status` to ensure workers are ready.
- Check `nomad alloc status <alloc_id>` for placement failure reasons.
