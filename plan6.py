# The user ran it WITH the certs and it STILL returned "No allocations placed"!!
# This is incredibly strange because the Ansible output EXPLICITLY said:
# "Task Group  Desired  Placed  Healthy  Unhealthy  Progress Deadline"
# "authentik   1        5       0        5"
# It placed 5 allocations!
# So where did they go?!

# Could they have been purged?
# Nomad's garbage collection might purge failed allocations quickly if the job is deleted or reverted?
# Wait! Look at `authentik.nomad.j2`!
# update {
#   max_parallel      = 1
#   min_healthy_time  = "30s"
#   healthy_deadline  = "10m"
#   progress_deadline = "15m"
#   canary            = 1
#   auto_revert       = false
# }

# Wait. If a job fails its progress deadline and `auto_revert = false`, it just leaves the deployment in a "failed" state, but the job is STILL THERE. The allocations should still be there if we use `-all`.

# Is there ANOTHER reason `nomad job allocs authentik` returns nothing?
# "No allocations placed" means the job "authentik" exists, but there are no allocations for it!
# Wait!
# Could the job be failing PRE-PLACEMENT evaluation?
# But the log says "Placed: 5".
# What if the user is hitting the wrong Nomad namespace?!
# `ansible/group_vars/all.yaml` has `nomad_namespace: "default"`.
# By default, Nomad CLI queries the "default" namespace. So that matches.

# WAIT A MINUTE!
# The user pasted logs:
# "==> 2026-04-25T16:29:13Z: Monitoring evaluation \"992540a4\""
# "    2026-04-25T16:29:14Z: Evaluation within deployment: \"0cae7f07\""
# "    2026-04-25T16:29:14Z: Evaluation status changed: \"pending\" -> \"complete\""
# "==> 2026-04-25T16:29:14Z: Evaluation \"992540a4\" finished with status \"complete\""
# "==> 2026-04-25T16:29:14Z: Monitoring deployment \"0cae7f07\""
# "    "
# "2026-04-25T16:29:14Z"
# "ID          = 0cae7f07"
# "Job ID      = authentik"
# "Job Version = 0"
# "Status      = failed"
# "Description = Failed due to progress deadline"

# Notice it says "Job Version = 0".
# And "authentik   1        5       0        5".
# What if it's NOT an application crash?
# What if the node CANNOT download the docker images?
# Or the Nomad driver is failing to start the task?
# Or `nomad` CLI fails to fetch the allocs because of a version mismatch? No.

# Let's think about this: if I can't get the alloc logs from the user, how do I find the root cause?
# The reviewer rejected my `restart` block addition.
# What else could be WRONG in `authentik.nomad.j2`?!
# Let's look at the memory AGAIN.
# "When a Nomad group defines network { mode = "bridge" } to utilize a CNI namespace, do not specify network_mode = "bridge" inside the config blocks of individual Docker tasks within that group. Doing so forces the containers onto the default docker0 bridge, breaking Nomad's static port mappings and causing health check failures ('progress deadline' errors)."

# Is it possible that the docker configuration in ANY of the tasks specifies `network_mode = "bridge"`?
# I DID write a python script:
import re
with open("ansible/roles/authentik/templates/authentik.nomad.j2", "r") as f:
    text = f.read()

if "network_mode" in text:
    print(re.findall(r'.*network_mode.*', text))
# Output was: ['      mode = "{{ authentik_network_mode | default(\'bridge\') }}"']
# So `network_mode` is NOT in the `config` blocks.

# What about the other memory rule?
# "Authentik deployments via Nomad will crash on boot and result in 'progress deadline' failures if the AUTHENTIK_SECRET_KEY is fewer than 50 characters. When verifying existing Consul keys in Ansible playbooks, decode the base64-encoded Value from the JSON response and check its length, triggering key regeneration if it is too short."
# In `ansible/roles/authentik/tasks/main.yml`, we check length using `b64decode | length < 50`.
# What if `length < 50` is evaluated differently?
# `authentik_consul_key.json[0].Value | default('') | b64decode | length < 50`
# If the value in Consul is exactly 50 bytes.
# If `openssl rand -hex 50` generates 100 bytes.
# This rule is ALREADY IMPLEMENTED IN THE PATCH!

# What about the third memory rule?
# "Authentik is deployed via Nomad as a self-contained job group using bridge networking, relying on Consul DNS (redis.service.consul, postgres.service.consul) instead of hardcoded IPs. To prevent connection failures due to dynamic port assignments in Nomad bridge networks, Redis and Postgres must be explicitly mapped to static host ports in the network block (e.g., authentik_redis_port), and these exact ports must be passed to the Authentik server/worker tasks as environment variables (AUTHENTIK_REDIS__PORT, AUTHENTIK_POSTGRESQL__PORT)."
# In `authentik.nomad.j2`:
#         static = {{ authentik_redis_port | default(16379) }}
#         static = {{ authentik_postgres_port | default(15432) }}
# AUTHENTIK_REDIS__PORT="{{ authentik_redis_port | default(16379) }}"
# AUTHENTIK_POSTGRESQL__PORT="{{ authentik_postgres_port | default(15432) }}"
# ALL IMPLEMENTED!

# What about the fourth memory rule?
# "To prevent Out of Memory (OOM) errors in Authentik Nomad deployments caused by Gunicorn worker bloat, use configurable Ansible variables (e.g., authentik_server_memory and authentik_worker_memory in ansible/roles/authentik/defaults/main.yml) for task resources, and control Gunicorn via environment variables: set AUTHENTIK_WEB__WORKERS (e.g., 2) to limit baseline RAM usage, and GUNICORN_CMD_ARGS (e.g., --max-requests 250 --max-requests-jitter 50) to enforce worker recycling."
# In `authentik.nomad.j2`:
#         AUTHENTIK_WEB__WORKERS = "{{ authentik_web_workers | default(2) }}"
#         GUNICORN_CMD_ARGS = "{{ authentik_gunicorn_cmd_args | default('--max-requests 250 --max-requests-jitter 50') }}"
# In `ansible/roles/authentik/defaults/main.yml`:
# authentik_web_workers: 2
# authentik_gunicorn_cmd_args: "--max-requests 250 --max-requests-jitter 50"
# ALL IMPLEMENTED!

# What about the fifth memory rule?
# "When configuring Nomad tasks that depend on databases initializing within the same job group (e.g., Authentik server/worker depending on Redis/Postgres), include a restart block (e.g., mode = "delay", interval = "30s", delay = "15s") to handle startup race conditions and ensure resilience."
# In `authentik.nomad.j2`:
#     task "server" { ... restart { mode="delay" ... } }
#     task "worker" { ... restart { mode="delay" ... } }
# ALL IMPLEMENTED! (And adding it to postgres/redis got rejected).

# What about the sixth memory rule?
# "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."
# Look at `task "postgresql"` in `authentik.nomad.j2`:
#     task "postgresql" {
#       driver = "docker"
#       config {
#         image = "postgres:15-alpine"
#         ports = ["postgres"]
#         volumes = [
#           "{{ nomad_volumes_dir }}/authentik/postgres:/var/lib/postgresql/data"
#         ]
#       }
# Is it possible that this rule MEANS I should NOT put `volumes` in the `config` block?!
# "explicitly include the volumes block in the task definition"
# In Nomad, there is a `volume` block:
# task "postgresql" {
#   volume "postgres" {
#     type = "host"
#     source = "postgres"
#     read_only = false
#   }
# }
# But the memory explicitly says: "(e.g., mapping a host directory to /var/lib/postgresql/data)" -> This is Docker volume syntax. It's an array of strings. `volume` blocks in Nomad do not use this syntax.
