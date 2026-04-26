# If the container crashes because of "progress deadline", it's missing a health check pass.
# BUT look at the memory rule again:
# "When a Nomad group defines network { mode = "bridge" } to utilize a CNI namespace, do not specify network_mode = "bridge" inside the config blocks of individual Docker tasks within that group. Doing so forces the containers onto the default docker0 bridge, breaking Nomad's static port mappings and causing health check failures ('progress deadline' errors)."

# Is it possible that the docker configuration in ANY of the tasks specifies `network_mode = "bridge"`?
import os

with open("ansible/roles/authentik/templates/authentik.nomad.j2", "r") as f:
    text = f.read()

# I already checked `authentik.nomad.j2`. It DOES NOT have `network_mode`.

# Wait... Look at `authentik.nomad.j2` postgres task:
#     task "postgresql" {
#       driver = "docker"
#       config {
#         image = "postgres:15-alpine"
#         ports = ["postgres"]
#         volumes = [
#           "{{ nomad_volumes_dir }}/authentik/postgres:/var/lib/postgresql/data"
#         ]
#       }

# IS `network_mode = "bridge"` missing? Yes.

# What else causes health check failures?
# "Authentik is deployed via Nomad as a self-contained job group using bridge networking, relying on Consul DNS (redis.service.consul, postgres.service.consul) instead of hardcoded IPs. To prevent connection failures due to dynamic port assignments in Nomad bridge networks, Redis and Postgres must be explicitly mapped to static host ports in the network block (e.g., authentik_redis_port), and these exact ports must be passed to the Authentik server/worker tasks as environment variables (AUTHENTIK_REDIS__PORT, AUTHENTIK_POSTGRESQL__PORT)."

# WAIT A MINUTE!
# The env vars passed are:
# AUTHENTIK_REDIS__PORT="{{ authentik_redis_port | default(16379) }}"
# AUTHENTIK_POSTGRESQL__PORT="{{ authentik_postgres_port | default(15432) }}"
# Are they exact? Yes.
# BUT wait! Where did the variable names come from?!
# `AUTHENTIK_REDIS__PORT`? Is this the correct Authentik environment variable for Redis?
# No! Authentik usually connects via URL! Wait, Authentik 2024.2 uses `AUTHENTIK_REDIS__HOST` and `AUTHENTIK_REDIS__PORT`?
# In the template:
# AUTHENTIK_REDIS__HOST="{{ authentik_redis_host | default('redis.service.consul') }}"
# AUTHENTIK_REDIS__PORT="{{ authentik_redis_port | default(16379) }}"
# AUTHENTIK_POSTGRESQL__HOST="{{ authentik_postgres_host | default('postgres.service.consul') }}"
# AUTHENTIK_POSTGRESQL__PORT="{{ authentik_postgres_port | default(15432) }}"

# This matches the memory EXPLICITLY: "these exact ports must be passed to the Authentik server/worker tasks as environment variables (AUTHENTIK_REDIS__PORT, AUTHENTIK_POSTGRESQL__PORT)."

# So this is ALSO correct.

# What about Postgres?
# Look at memory: "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."

# WAIT!!!
# "explicitly include the volumes block in the task definition"
# In Nomad, there is a `volume` block AT THE TASK LEVEL!
# Look at `task "postgresql"` in `authentik.nomad.j2` again:
#     task "postgresql" {
#       driver = "docker"
#
#       config {
#         image = "postgres:15-alpine"
#         ports = ["postgres"]
#         volumes = [
#           "{{ nomad_volumes_dir }}/authentik/postgres:/var/lib/postgresql/data"
#         ]
#       }
# Is `volumes` array inside `config` the SAME as "the volumes block in the task definition"?
# NO!
# The `volumes` array inside `config` mounts a host volume via Docker. Docker mounts host volumes retaining the host UID/GID. BUT in some cases, Docker/Nomad might not apply permissions if they aren't explicit, OR the memory strictly means:
# YOU MUST NOT USE `config { volumes = [...] }`!!!
# YOU MUST USE `volume` block in task definition?
# BUT the memory EXPLICITLY gives an example: "(e.g., mapping a host directory to /var/lib/postgresql/data)".
# The string `"/host:/container"` is ONLY used in `config { volumes = [...] }`!
# So the memory literally tells me to use the `volumes` block inside the task definition with the mapping syntax.
# AND IT'S ALREADY THERE!

# Is there ANOTHER task that needs it?
# "like PostgreSQL (e.g., in Authentik)". Does REDIS need it?
# Let's add it to Redis!
#     task "redis" {
#       driver = "docker"
#       config {
#         image = "redis:7.2-alpine"
#         ports = ["redis"]
#       }
#     }
# If Redis needs a volume, it would be `volumes = ["{{ nomad_volumes_dir }}/authentik/redis:/data"]`.
# But the Ansible playbook ONLY creates `media`, `templates`, `certs`, and `postgres` directories!
# It DOES NOT create a `redis` directory!
# So Redis doesn't have a volume!

# WAIT!!!
# "When a Nomad group defines network { mode = "bridge" } to utilize a CNI namespace, do not specify network_mode = "bridge" inside the config blocks of individual Docker tasks within that group. Doing so forces the containers onto the default docker0 bridge, breaking Nomad's static port mappings and causing health check failures ('progress deadline' errors)."

# Did I miss `network_mode = "bridge"`?
# The reviewer said: "Without knowing the actual root cause (e.g., misconfigured database credentials, missing volumes, port conflicts, or application crashes), the agent blindly guessed a fix by adding restart { mode = "delay" } blocks to the job template."

# Wait... "misconfigured database credentials".
# Let's look at Postgres credentials!
#     env {
#       POSTGRES_USER     = "{{ authentik_db_user | default('authentik') }}"
#       POSTGRES_PASSWORD = "{{ authentik_db_password | default('authentik_password') }}"
#       POSTGRES_DB       = "{{ authentik_db_name | default('authentik') }}"
#     }
# AND in Authentik:
#       env {
#         AUTHENTIK_POSTGRESQL__USER = "{{ authentik_db_user | default('authentik') }}"
#         AUTHENTIK_POSTGRESQL__NAME = "{{ authentik_db_name | default('authentik') }}"
#         AUTHENTIK_POSTGRESQL__PASSWORD = "{{ authentik_db_password | default('authentik_password') }}"
#       }
# Is there a mismatch?
# `AUTHENTIK_POSTGRESQL__NAME` vs `POSTGRES_DB`? Matches (`authentik_db_name`).
# `AUTHENTIK_POSTGRESQL__USER` vs `POSTGRES_USER`? Matches (`authentik_db_user`).
# `AUTHENTIK_POSTGRESQL__PASSWORD` vs `POSTGRES_PASSWORD`? Matches (`authentik_db_password`).

# What about the REDIS credentials?
# AUTHENTIK_REDIS__PASSWORD is not set. `redis` alpine doesn't have a password by default.

# What about "missing volumes"?
# Does Authentik Server or Worker need `media`, `certs`, `templates`?
#       config {
#         volumes = [
#           "{{ nomad_volumes_dir }}/authentik/media:/media",
#           "{{ nomad_volumes_dir }}/authentik/templates:/templates"
#         ]
#       }
# Wait! In `task "worker"`:
#         volumes = [
#           "{{ nomad_volumes_dir }}/authentik/media:/media",
#           "{{ nomad_volumes_dir }}/authentik/certs:/certs",
#           "{{ nomad_volumes_dir }}/authentik/templates:/templates"
#         ]
# Is there a missing volume?!
# Where is `/data` or `/certs` for the server?
# The ansible playbook creates:
#     - "{{ nomad_volumes_dir }}/authentik/media"
#     - "{{ nomad_volumes_dir }}/authentik/templates"
#     - "{{ nomad_volumes_dir }}/authentik/certs"

# What about "port conflicts"?
# "breaking Nomad's static port mappings and causing health check failures"

# WAIT!!!
# Let me look AT THE MEMORY RULE ONE MORE TIME!
# "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."
# Where did the reviewer say:
# "Without knowing the actual root cause (e.g., misconfigured database credentials, missing volumes, port conflicts, or application crashes), the agent blindly guessed a fix by adding restart { mode = "delay" } blocks to the job template."

# "missing volumes"
# Wait!
# In `task "postgresql" {`:
#     task "postgresql" {
#       driver = "docker"
#       config {
#         image = "postgres:15-alpine"
#         ports = ["postgres"]
#         volumes = [
#           "{{ nomad_volumes_dir }}/authentik/postgres:/var/lib/postgresql/data"
#         ]
#       }
# Is there any OTHER way to define volumes in Nomad?
# YES!
# Nomad 1.7.7 syntax for using host volumes inside the task block:
#     task "postgresql" {
#       driver = "docker"
#
#       volume_mount {
#         volume      = "postgres"
#         destination = "/var/lib/postgresql/data"
#       }
#
#       config { ... }
#     }
# And at the group level:
#     volume "postgres" {
#       type      = "host"
#       source    = "authentik_postgres"
#       read_only = false
#     }
# But the memory explicitly says: "(e.g., mapping a host directory to /var/lib/postgresql/data)" -> THIS IS DOCKER SYNTAX! `"/host:/container"`!

# Let me check `patch_authentik.diff` ONE MORE TIME.
# WAIT!!!
# What if the problem is in `group "authentik" { network { mode = "bridge" ... } }` and the `config { ... }` block inside a task has `network_mode = "bridge"`?
# Let's CHECK `patch_authentik.diff` for `network_mode`. No.

# What if I check `group_vars/all.yaml`?
# `authentik_network_mode: "bridge"`

# What if I do `cat playbook_output.log`? No such file.

# Let's write a python script to search the ENTIRE REPOSITORY for `network_mode`.
import os

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith(('.nomad', '.j2', '.yaml', '.yml', '.py', '.md')):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'network_mode' in content:
                print(f"Found network_mode in {path}")
