# Docker Bridge Networking Analysis and Resolution

## Verification of Initial Analysis

The initial analysis posited a "Docker Daemon Bug Hypothesis" due to the following symptoms:
1. Port Binding Appears Successful but Connection Refused (via `curl`).
2. Docker Containers Start but Have No Network (`NetworkSettings.Networks` is empty).
3. Host Networking Works, but Bridge Networking DNS Not Working.

While these symptoms perfectly describe what is happening, the root cause is **not** a Docker bug. The issue lies in the Linux kernel network routing (sysctl) and iptables rules configured on the host nodes, which prevents the Nomad bridge network interface from properly communicating.

When Nomad deploys jobs using `network { mode = "bridge" }`, it heavily relies on its installed CNI (Container Network Interface) plugins (`/opt/cni/bin/bridge` and `/opt/cni/bin/firewall`). However, for the CNI bridge to function and route traffic correctly over `iptables` rules (specifically through the `FORWARD` chain, which the host currently sets to `DROP`), the Linux kernel's bridge netfilter module (`br_netfilter`) must be loaded, and specific `sysctl` configurations must be enabled.

Without these settings, Nomad sets up the container in a bridge network namespace, but since the bridged packets are dropped by iptables or ignored by netfilter, the container essentially hangs without a functioning network connection.

### Root Cause
The host is missing the necessary `br_netfilter` module and the sysctl properties required for bridged IPv4/IPv6 traffic to be processed by iptables:
* `net.bridge.bridge-nf-call-arptables = 1`
* `net.bridge.bridge-nf-call-ip6tables = 1`
* `net.bridge.bridge-nf-call-iptables = 1`

### Recommendation and Fix

To fix this natively and restore full CNI bridge capabilities (including Consul DNS resolution and external Tailscale access without port conflicts), the underlying provisioning must be corrected.

The `nomad` Ansible role has been updated (`ansible/roles/nomad/tasks/main.yaml`) to:
1. Load the `br_netfilter` module via `modprobe` and ensure it is loaded on boot.
2. Apply the required sysctl configurations persistently to enable `bridge-nf-call-*` properties.

With these changes applied, you can continue deploying your Nomad jobs, including `authentik.nomad`, using `network { mode = "bridge" }` and they will successfully route traffic and resolve Consul DNS entries.
