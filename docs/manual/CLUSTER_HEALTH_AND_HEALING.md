# Cluster Health Probing and Self-Healing Guide

This guide describes the unified, system-wide health probing, diagnostics logging, and self-healing subsystem for the llama-cluster.

The primary tool is `scripts/troubleshoot.py`, which integrates diagnostics, health probing, and recovery loops for both **Nomad** and **Systemd** into a cohesive standalone command-line interface.

---

## Architecture Overview

The health subsystem runs independently of `pipecatapp` and other user space web server processes, allowing operators and autonomous agents to diagnose, inspect, and recover cluster services even when the primary applications are offline or degraded.

```
                  +--------------------------------+
                  |    scripts/troubleshoot.py     |
                  +---------------+----------------+
                                  |
         +------------------------+------------------------+
         |                                                 |
         v                                                 v
+--------+--------+                               +--------+--------+
|   Nomad Jobs    |                               | Systemd Services|
|  & Allocations  |                               | (Consul, Nomad, |
+--------+--------+                               |  Docker, etc.)  |
         |                                        +--------+--------+
         v                                                 |
+--------+--------+                                        v
| 404 Fallback to |                               +--------+--------+
| Events / Docker |                               | Journalctl Logs |
| Logs Directly   |                               +-----------------+
+-----------------+
```

---

## Command Reference

Run the tool using either Python 3 directly, or via the `bootstrap.sh` entry point (which automatically sets up the Python virtual environment and dependencies if needed):

```bash
./bootstrap.sh --troubleshoot <command> [options]
```

Or directly using Python 3:

```bash
python3 scripts/troubleshoot.py <command> [options]
```

### 1. `probe` (System-Wide Health Probe)
Queries the real-time status of all critical parts of the cluster:
- **Nomad:** Jobs and active scheduling status.
- **Systemd:** Key infrastructure daemons (`consul`, `nomad`, `docker`, `tailscaled`, `unified_fs`, `power-agent`, `provisioning-api`, `paddler-balancer`) as well as any other currently failed units on the host.
- **Docker:** Evaluates if containers are running and healthy.

**Usage:**
```bash
python3 scripts/troubleshoot.py probe
```
*To output raw, machine-readable JSON for integration into other agents:*
```bash
python3 scripts/troubleshoot.py probe --json
```

### 2. `heal` (Force-Run & Self-Healing Sequence)
Initiates a forceful remediation cycle:
- Identifies failed/dead Nomad jobs or Systemd services.
- Captures error diagnostics/logs (with advanced fallback logic) into `logs/healer/` prior to intervention.
- Triggers `nomad job restart` or falls back to running the Ansible `playbooks/heal_job.yaml` playbook.
- Restarts failed Systemd services via `systemctl restart`.
- Pauses to allow initializations, and runs post-verification to ensure high-fidelity status.

**Usage:**
```bash
python3 scripts/troubleshoot.py heal
```

### 3. `daemon` (Autonomous Self-Healing Loop)
Launches the persistent background cycle similar to `supervisor.py`. It runs periodically at a configurable interval to probe system health, automatically trigger healing when degradation occurs, and log stats cleanly.

**Usage:**
```bash
python3 scripts/troubleshoot.py daemon --interval 60
```

### 4. `report` (Comprehensive Diagnostics Report)
Generates a highly detailed diagnostics log file including system resources, docker statuses, consul catalog configurations, and the latest logs from failed allocations and units.

**Usage:**
```bash
python3 scripts/troubleshoot.py report
```

---

## Log Instrument Design & 404 Fallback

Standard Nomad logs query a client node via the HTTP API, which often returns `404 (state not found on client)` for newly scheduled, unscheduled, or crashed allocations.

Our script implements a high-quality **3-tier log fallback mechanism** inside `fetch_alloc_logs_with_fallback`:

1. **API Events Extraction:** If the log API is unvailable (404), the script queries `/v1/allocation/{alloc_id}` and parses the `TaskStates` structure to extract specific `DriverError`, `SetupError`, `ValidationError`, or scheduler logs.
2. **Local Docker Logs:** If the task utilizes Docker, the script filters all local containers by label matching the allocation ID (`com.hashicorp.nomad.alloc_id`) and reads container logs directly via the local Docker daemon.
3. **Direct Log File Read:** The script inspects the local physical allocation store at `/opt/nomad/data/alloc/{alloc_id}/alloc/logs/` for absolute files, extracting the final log entries.

This keeps all relevant data together, structured, and easy to parse, giving developers and agents absolute transparency into crashes.
