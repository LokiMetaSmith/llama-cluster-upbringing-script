# The `volumes` block IS in the `config` block of `task "postgresql"`.
# So why did the reviewer say:
# "Without knowing the actual root cause (e.g., misconfigured database credentials, missing volumes, port conflicts, or application crashes), the agent blindly guessed a fix by adding restart { mode = "delay" } blocks to the job template."

# The reviewer explicitly listed "misconfigured database credentials, missing volumes, port conflicts, or application crashes" as EXAMPLES of what a root cause COULD be. Not necessarily what it IS.
# I had to check the logs to find out!
# And I did check the logs!
# The logs said: `Template Missing: kv.block(authentik/secret-key)`!
# THIS IS THE ACTUAL ROOT CAUSE OF THE `SERVER` AND `WORKER` CRASHING!

# Wait! The `server` and `worker` tasks have `Template Missing: kv.block(authentik/secret-key)`.
# Nomad's `template` block evaluates BEFORE the task starts!
# If a template is missing and not optional, Nomad WILL NOT start the task!
# This perfectly explains why `server` and `worker` show `Started At = N/A` in the logs!
# They NEVER started! Because the template failed to render!
# Since they never started, they couldn't become healthy, leading to the progress deadline!

# AND why did `postgres` fail?
# "Docker container exited with non-zero exit code: 1"
# Is `postgres` failing because it needs a template? No, it has no template.
# Why is `postgres` failing?
# Look at `ansible/roles/authentik/tasks/main.yml`:
# - name: Set postgres volume permissions
#   ansible.builtin.shell: chown -R 70:70 "{{ nomad_volumes_dir }}/authentik/postgres" && chmod 700 "{{ nomad_volumes_dir }}/authentik/postgres"
# Postgres 15 needs the data directory to be owned by `postgres` (UID 70 on alpine).
# So the directory permissions ARE set correctly on the host.

# Wait, look at this memory AGAIN:
# "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."
# What if `volumes` is NOT enough for Docker to mount it with correct permissions?!
# Actually, the memory says "explicitly include the volumes block in the task definition".
# If it's already there, why did Postgres crash?
# Let's check `postgres` environment variables:
#       env {
#         POSTGRES_USER     = "{{ authentik_db_user | default('authentik') }}"
#         POSTGRES_PASSWORD = "{{ authentik_db_password | default('authentik_password') }}"
#         POSTGRES_DB       = "{{ authentik_db_name | default('authentik') }}"
#       }
# Is there a typo? `POSTGRES_PASSWORD`, `POSTGRES_USER`, `POSTGRES_DB`. These are correct.

# What if `postgres` is crashing because `redis` is dead? No, `redis` is fine!
# `Task "redis" is "dead"` -> `Exit Code: 0`. It exited gracefully when the job was killed.
# Wait! Look at `redis` events:
# `2026-04-26T00:04:51Z Sibling Task Failed Task's sibling "postgresql" failed`
# So `postgres` failed FIRST, causing the whole allocation to be killed!
# `2026-04-26T00:04:32Z Terminated Exit Code: 1`
# Why did `postgres` fail?
# "Docker container exited with non-zero exit code: 1"
# Wait! Is `postgres` failing because the volume directory ALREADY HAS DATA from a different version? No.
# Could the `volumes` block be inside the `task` block rather than `config`?!
# NO! Nomad 1.x `volume` block uses `source = "..."` and requires a group `volume` block.
# BUT look at the memory rule again: "explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data)"
# Wait! "in the task definition"
# In HCL, `task "postgresql" { ... }` is the task definition.
# `config { volumes = [ ... ] }` is INSIDE the task definition.
# Could the memory mean something else?
# What if it's NOT in the file?
# I checked the file, it IS there!
# If it's there, maybe Postgres crashes for some other reason?

# Look at the memory: "When configuring Nomad tasks that depend on databases initializing within the same job group (e.g., Authentik server/worker depending on Redis/Postgres), include a restart block (e.g., mode = "delay", interval = "30s", delay = "15s") to handle startup race conditions and ensure resilience."
# Is it possible that the `restart` block I added to Postgres fixed the `postgres` crash, but `server` still failed because of `Template Missing`, causing the whole allocation to be marked failed?!
# YES!
# If `server` fails because of `Template Missing`, the whole allocation fails!
# "2026-04-26T00:04:51Z  Sibling Task Failed  Task's sibling "postgresql" failed"
# Wait! The logs say `server` and `worker` were killed because `postgresql` failed!
# "Sibling Task Failed  Task's sibling "postgresql" failed"
# So `postgresql` failed, which caused the alloc to fail!
# BUT WHY did `postgresql` fail?!
# Exit code 1.
# Maybe it's missing `network_mode = "bridge"`?
# NO, memory says "do not specify network_mode = "bridge" inside the config blocks".

# Let's fix the `Template Missing` error first!
# We can fix `Template Missing` by making sure the Nomad client has a Consul token OR by rendering the key directly in Ansible.
# But wait!
# If the task fails because of `Template Missing`, DOES it fail the sibling tasks?!
# Yes! If any task fails to start (e.g. template missing), the allocation fails!
# But the log shows:
# `2026-04-26T00:04:14Z  Terminated      Exit Code: 1` for postgres.
# Postgres started and immediately terminated with code 1.
# The server task NEVER started.
# "Started At = N/A"
# "2026-04-26T00:04:17Z  Template             Missing: kv.block(authentik/secret-key)"
# Because the template couldn't be rendered, the `server` task hung in `Template` phase.
# Meanwhile, `postgres` started at 00:04:14 and crashed at 00:04:14.
# Then `postgres` restarted at 00:04:32 and crashed at 00:04:32.
# Then `postgres` reached its max restart limit and failed the whole allocation at 00:04:51!
# Then the whole allocation was killed!

# So there are TWO ROOT CAUSES!
# 1. `server` and `worker` templates are missing `authentik/secret-key` because Nomad lacks Consul token!
# 2. `postgres` is crashing with Exit Code 1!

# Let's fix `Template Missing` by passing `vault` or setting `consul { token }`?
# NO! Look at the memory rule for the SECRET KEY!
# "Authentik deployments via Nomad will crash on boot and result in 'progress deadline' failures if the AUTHENTIK_SECRET_KEY is fewer than 50 characters. When verifying existing Consul keys in Ansible playbooks, decode the base64-encoded Value from the JSON response and check its length, triggering key regeneration if it is too short."
# Wait, if the template `Missing: kv.block` error happens, how could Authentik crash on boot because of `< 50 chars`?
# If the template renders, but the key is < 50 chars, Authentik container crashes!
# This implies the template CAN render successfully in a normal environment!
# Then why did it fail to render here?
# Maybe the key REALLY doesn't exist in Consul!
# Why wouldn't it exist?
# In the Ansible run:
# TASK [authentik : Check if Authentik secret key exists in Consul] -> ok
# TASK [authentik : Generate Authentik secret key] -> skipped
# TASK [authentik : Publish Authentik secret key to Consul] -> skipped
# WHY did it skip if it doesn't exist?!
# Let's write a python script to test my theory on Ansible `when` evaluation!
