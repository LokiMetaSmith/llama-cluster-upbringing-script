1. **Create Nomad Startup Wrapper Script (`start_nomad.sh.j2`)**
   - Create `ansible/roles/nomad/templates/start_nomad.sh.j2`.
   - Add logic to calculate `BOOTSTRAP_COUNT` dynamically by pinging expected controller nodes (`100.64.0.2`, `100.64.0.3` or based on `controller_nodes` IPs) to determine `-bootstrap-expect=1` or `-bootstrap-expect=3`.
   - Start the main binary via `exec /usr/local/bin/nomad agent -config=/etc/nomad.d -bootstrap-expect=$BOOTSTRAP_COUNT` (ensure to use `/etc/nomad.d` directly instead of a specific file).

2. **Update Nomad Service Execution (`nomad.service.j2` & `tasks/main.yaml`)**
   - In `ansible/roles/nomad/templates/nomad.service.j2`, update `ExecStart` to `/usr/local/bin/start_nomad.sh`.
   - In `ansible/roles/nomad/tasks/main.yaml`, add a task to deploy `start_nomad.sh.j2` to `/usr/local/bin/start_nomad.sh` with executable permissions before the service start.

3. **Add Autopilot Configuration Blocks**
   - In `ansible/roles/nomad/templates/nomad.hcl.server.j2`, add the `autopilot` block inside the `server` block.
   - In `ansible/roles/nomad/templates/server.hcl.j2`, add the `autopilot` block inside the `server` block.

4. **Create Single-Node Recovery Watchdog**
   - Create `ansible/roles/power_manager/files/watchdog.sh` with the logic to monitor for `500 No Leader` on `/v1/status/leader` and manually inject `peers.json` if alone.
   - Make it a separate service by adding `ansible/roles/power_manager/templates/nomad-watchdog.service.j2`.
   - Update `ansible/roles/power_manager/tasks/main.yaml` to deploy `watchdog.sh` to `/opt/power_manager/watchdog.sh` and the systemd service template.
   - Update handlers in `ansible/roles/power_manager/handlers/main.yaml` to include a handler for restarting the watchdog.

5. **Complete pre-commit steps**
   - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.

6. **Submit**
   - Submit the changes using the git agnostic submit tool.
