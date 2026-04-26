# The reviewer REJECTED my fix.
# "Without knowing the actual root cause (e.g., misconfigured database credentials, missing volumes, port conflicts, or application crashes), the agent blindly guessed a fix by adding restart { mode = "delay" } blocks to the job template."

# I NEED TO DIAGNOSE THE ROOT CAUSE!
# I can't guess! I MUST ask the user to get the logs!
# BUT the user ran `nomad job allocs authentik` and it returned "No allocations placed"!
# WHY did it return "No allocations placed"?
# 1. The user didn't export the NOMAD_ADDR and certs, so it connected to a local default instance instead of the cluster.
# 2. The job was purged.
# 3. The allocs failed to place. BUT the ansible output explicitly says "Placed: 5".
# So they WERE placed!

# How can the user view the allocs for a failed deployment?
# nomad job allocs -all authentik
# If the user doesn't have the certs exported, they MUST export them!
# The memory says: "To enable the Nomad CLI on local nodes when mTLS is enforced, the /etc/profile.d/nomad.sh profile automatically exports NOMAD_ADDR=https://... along with NOMAD_CACERT, NOMAD_CLIENT_CERT, and NOMAD_CLIENT_KEY pointing to the node's distributed certificates."
# So the user just needs to source `/etc/profile.d/nomad.sh` or log out and log back in, or run the command with the correct environment.
