# If the memory says "explicitly include the volumes block IN THE TASK DEFINITION", let's look at `ansible/roles/authentik/templates/authentik.nomad.j2`.
# The current template has `volumes = [...]` inside `config { ... }` block!
# Wait! In HCL, `task "postgresql" { config { volumes = [...] } }`. `config` is a block inside `task`.
# Is there a top-level `volume` block in Nomad for tasks?
# Yes! Nomad 1.0 added `volume "name" {}` in the job/group level, and `volume_mount {}` in the task level.
# BUT the memory says "the volumes block" and provides the syntax "(e.g., mapping a host directory to /var/lib/postgresql/data)".
# The docker `volumes` configuration uses exactly this mapping syntax.
# The memory DOES NOT say `volume_mount`. It says `volumes block`.
# So the docker `volumes` array is CORRECT.

# BUT wait! Does Nomad 1.0+ support the `volumes` attribute outside of `config`? NO.
# So I should leave it inside `config`.

# The actual reason `server` and `worker` tasks were "dead" (Started At = N/A) is because of `Template Missing: kv.block(authentik/secret-key)`.
# Nomad's `template` stanza tries to render the Consul KV secret key.
# But it failed.
# I fixed it by explicitly substituting the value from Ansible: `AUTHENTIK_SECRET_KEY="{{ authentik_generated_key.stdout if authentik_generated_key.stdout is defined and authentik_generated_key.stdout != '' else (authentik_consul_key.json[0].Value | b64decode) }}"`
# This avoids Nomad fetching from Consul KV entirely, fixing the `Template Missing` error!

# What about Postgres crashing?
# If Postgres crashed with Exit Code 1, it might be due to the data directory permissions not being properly initialized during the FIRST run.
# The Ansible playbook chowns `/opt/nomad/volumes/authentik/postgres` to `70:70`.
# If `postgres` starts up, it requires the directory to be empty or properly configured.
# If it crashes, maybe it just needed a restart?
# The reviewer said: "Modifying the restart policy to delay just changes Nomad's behavior... It does not fix the underlying reason the task is crashing... The agent needs to actually retrieve the nomad alloc logs (or instruct the user precisely how to get them) to diagnose the real error before writing a fix."

# The reviewer didn't say the restart policy was wrong to have. They said it DOES NOT FIX THE UNDERLYING REASON.
# The underlying reason for the server/worker not starting was the `Template Missing: kv.block(authentik/secret-key)`.
# If the server/worker tasks never started, Nomad will report `progress deadline`!
# Postgres crashing with exit code 1 might actually just be a side effect of it being killed?
# NO!
# "2026-04-26T00:04:32Z  Terminated      Exit Code: 1, Exit Message: "Docker container exited with non-zero exit code: 1""
# It was terminating BEFORE the 15m progress deadline!
# And because it terminated, it caused "Sibling Task Failed  Task's sibling 'postgresql' failed" for the server and worker tasks!
# Wait! "Sibling Task Failed" means the ENTIRE group failed because Postgres failed!
# YES!
# So POSTGRES is the root cause of the allocation failing!

# WHY did Postgres crash with exit code 1?!
# Let's ask the user to fetch the logs for Postgres!
# "nomad alloc logs 0779f51c-027d-aceb-fe84-e1d2cec40dff postgres"
# The user hasn't provided the `postgres` logs yet! They only provided the `nomad alloc status` output!
