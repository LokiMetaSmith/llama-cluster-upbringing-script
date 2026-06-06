1. **Understand the problem**:
    - The `ansible/roles/tool_server/tasks/main.yaml` has a task to `Pin tool-server tarball to IPFS`.
    - It runs the command `ipfs add -Q /tmp/tool-server.tar` natively on the host (not via Docker).
    - But `ipfs` command is not installed on the system globally. The IPFS daemon is actually started as a Nomad job (`docker pull ipfs/kubo:latest` and then deployed via Nomad) in `ansible/roles/ipfs/tasks/main.yaml`.
    - So when any app deployment role tries to upload to IPFS (e.g. `tool_server`, `pipecatapp`, `openclaw`, `exo`), it uses `ipfs add ...` assuming the CLI is present.
2. **Solution**:
    - Since `kubo` provides the `ipfs` command, and it makes sense to have it globally available for these operations, we should install the IPFS CLI locally on the controllers (or all nodes) where these playbooks run.
    - I have modified `ansible/roles/ipfs/tasks/main.yaml` to download and install the `ipfs` CLI (kubo) binary from the official release tarball to `/usr/local/bin/ipfs` before it tries to run `ipfs add ...` in other roles.
    - Since the `ipfs` role is run earlier in the playbook list (`playbooks/services/ipfs.yaml` comes before `playbooks/services/app_services.yaml`), modifying `ansible/roles/ipfs/tasks/main.yaml` to install the kubo CLI will fix all subsequent roles.
3. **Pre-commit step**:
    - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
4. **Submit**:
    - Submit the change with a descriptive message.
