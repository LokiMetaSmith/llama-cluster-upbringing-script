# Cluster Diagnostic & Self-Healing Guide

This guide provides a systematic, step-by-step workflow for diagnosing and self-healing a Pipecat Cluster node (e.g. `192.168.1.148` / `yggie-2-controller`) when services are inactive, pending, or dead.

---

## 1. System Health Probing & Status Checklist

Upon SSHing into the target node, initiate high-level status probes:

```bash
cd ~/llama-cluster-upbringing-script/

# Check cluster bootstrap status
sudo ./bootstrap.sh --status

# Probe system-wide health (Nomad, Systemd, Docker, Consul)
python3 scripts/troubleshoot.py probe

# Inspect service dependency tree to find root-cause blockages
python3 scripts/troubleshoot.py deps
```

---

## 2. Root-Cause Diagnosis by Component

### A. Systemd Service Issues (`unified_fs` stuck in `activating`)

If `unified_fs` or core daemons (`nomad`, `consul`, `docker`) fail or stay in `activating`:

1. **Check Journalctl Logs**:
   ```bash
   journalctl -u unified_fs -n 100 --no-pager
   ```
2. **Inspect Process & Mount Status**:
   ```bash
   systemctl status unified_fs
   df -h /opt/pipecat-cluster
   ```
3. **Restart the Service**:
   ```bash
   sudo systemctl restart unified_fs
   ```

---

### B. Nomad Dead / Pending Jobs (`pipecat-app`, `gitea`, `memory-service`, `router`)

When Nomad jobs show status `dead` or `pending`:

1. **Inspect Failure Details & Upstream Dependencies**:
   ```bash
   python3 scripts/troubleshoot.py inspect pipecat-app
   ```
2. **Retrieve Logs (with Automatic Fallback to Task Events & Docker Logs)**:
   ```bash
   # Standard Nomad CLI logs
   nomad alloc logs -stderr <ALLOC_ID> pipecat-task

   # If Nomad returns 404 (state not found on client), use fallback Docker log retrieval:
   docker ps -a --filter label=com.hashicorp.nomad.alloc_id=<ALLOC_ID>
   docker logs --tail 100 <CONTAINER_ID>
   ```
3. **Common Failure Modes**:
   - **Missing Host Volume / Device**: Host volume `/dev/snd` or `/opt/nomad/data` missing.
   - **Port Conflict**: Port `8007` (Pipecat App) or `8080` (Gitea) bound by a stray process (`lsof -i :8007`).
   - **Upstream Dependency Failure**: `pipecat-app` blocked by `unified_fs` or Consul KV state.

---

## 3. Self-Healing & Automated Recovery

Once the root cause is diagnosed, execute recovery:

1. **Run Unified System Self-Healing**:
   ```bash
   # Force-restarts dead jobs and systemd units with verification checks
   python3 scripts/troubleshoot.py heal
   ```

2. **Trigger Full Infrastructure Healing Playbook**:
   ```bash
   # Re-runs Ansible healing playbooks to restore certificates, host mounts, and service configs
   ./bootstrap.sh --heal-cluster
   ```

3. **Start Autonomous Self-Healing Daemon Loop**:
   ```bash
   # Continuous monitoring and healing daemon (runs every 60s)
   python3 scripts/troubleshoot.py daemon --interval 60
   ```

---

## 4. Verification Checkpoints

After triggering healing, verify that all cluster access interfaces and jobs are healthy:

```bash
# Re-check cluster status report
sudo ./bootstrap.sh --status
```

Expected Nominal Output:
- **Nomad UI**: `https://100.64.0.1:4646` (`Active`)
- **Consul UI**: `https://100.64.0.1:8500` (`Active`)
- **Pipecat App**: `https://100.64.0.1:8007` (`Active`)
- **Nomad Allocations**: All core jobs in status `running`.
