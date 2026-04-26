# The user ran `nomad job allocs authentik` and it returned "No allocations placed"!
# THIS IS AMAZING!
# If there are NO allocations placed, it means Nomad wasn't even able to start the container, or it started and failed, but wait: "No allocations placed" means the job literally couldn't find a node to place the allocation, or the allocations were immediately purged/failed to even schedule properly?
# NO. "Task Group  Desired  Placed  Healthy  Unhealthy  Progress Deadline"
# "authentik   1        5       0        5"
# It SAYS "Placed: 5".
# Why did `nomad job allocs authentik` say "No allocations placed"?
# BECAUSE Nomad CLI by default filters to the current namespace, OR the allocations were garbage collected, OR the user is running the command in an environment without `NOMAD_ADDR` configured correctly (wait, the ansible output uses `NOMAD_ADDR: "https://{{ cluster_ip }}:4646"` and mTLS certs)!
# YES! The user just ran `nomad job allocs authentik` without the `NOMAD_ADDR` and certificates, so they couldn't reach the cluster, OR they reached a default local Nomad instance instead of the cluster!
# BUT wait! `nomad job allocs authentik` would fail with a connection error if it couldn't reach the cluster. It returned "No allocations placed", meaning it reached A Nomad instance, but found no allocs.

# Let's think about WHY an allocation would fail 5 times and be "Unhealthy".
# Let me look at the memory AGAIN.
# "When a Nomad group defines network { mode = "bridge" } to utilize a CNI namespace, do not specify network_mode = "bridge" inside the config blocks of individual Docker tasks within that group. Doing so forces the containers onto the default docker0 bridge, breaking Nomad's static port mappings and causing health check failures ('progress deadline' errors)."

# Did I miss something about `network_mode = "bridge"`?
# Let's search the ACTUAL code in the repository right now for `network_mode`.
import os
for root, dirs, files in os.walk('.'):
    if '.git' in root: continue
    for file in files:
        if file.endswith('.nomad') or file.endswith('.j2'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            if 'network_mode' in content:
                print(path)
