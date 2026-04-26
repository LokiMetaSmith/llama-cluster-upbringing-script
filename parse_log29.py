# Wait! Let's examine the output of `nomad alloc status 0779f51c-027d-aceb-fe84-e1d2cec40dff postgres`.
# The user's output for `postgres` task was:
# Task "postgresql" is "dead"
# Task Events:
# Started At     = 2026-04-26T00:04:51Z
# Finished At    = 2026-04-26T00:04:51Z
# Total Restarts = 2
# Last Restart   = 2026-04-26T00:04:32Z
#
# Recent Events:
# Time                  Type            Description
# 2026-04-26T00:04:51Z  Killing         Sent interrupt. Waiting 5s before force killing
# 2026-04-26T00:04:51Z  Not Restarting  Exceeded allowed attempts 2 in interval 30m0s and mode is "fail"
# 2026-04-26T00:04:51Z  Terminated      Exit Code: 1, Exit Message: "Docker container exited with non-zero exit code: 1"

# The reason it was "Not Restarting" is because "mode is fail"!
# Nomad's default restart mode is "fail", which means it will NOT continuously restart.
# If I add `restart { mode = "delay" }`, it WILL restart indefinitely and wait for the race condition to pass!
# The reviewer said: "Modifying the restart policy to delay just changes Nomad's behavior to continuously restart a crashing task... It does not fix the underlying reason the task is crashing or failing its health checks in the first place."
# But why DID `postgres` crash?
# The data directory permission issue?
# "explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."
# Is there ANY OTHER WAY to define the volumes block in the task definition?
