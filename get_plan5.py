# The user clearly ran `nomad job allocs authentik` and it returned "No allocations placed".
# And they didn't get any logs.
# If they ran it on the command line without the NOMAD_ADDR and certs, they might have hit a local instance instead of the secure cluster.
# BUT we still need to figure out the root cause!
# I got rejected because I just guessed `restart`.

# Could the root cause be EXACTLY what is described in the memory?!
# "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."

# In `authentik.nomad.j2`:
#     task "postgresql" {
#       driver = "docker"
#       config {
#         image = "postgres:15-alpine"
#         ports = ["postgres"]
#         volumes = [
#           "{{ nomad_volumes_dir }}/authentik/postgres:/var/lib/postgresql/data"
#         ]
#       }
# Is `volumes = [...]` considered "the volumes block in the task definition"?
# NO! It is inside the `config` block.
# The memory explicitly says: "explicitly include the volumes block in the task definition".
# Let's read the Nomad documentation!
# Nomad task definition block allows a `volume` block:
#     task "postgresql" {
#       volume "postgres" {
#         type = "host"
#         source = "postgres_data"
#         read_only = false
#       }
#     }
# And the group block needs:
#   group "authentik" {
#     volume "postgres_data" {
#       type = "host"
#       source = "authentik-postgres"
#     }
#   }
# BUT wait! The memory gives a specific example: "(e.g., mapping a host directory to /var/lib/postgresql/data)".
# The Docker `config` parameter `volumes` DOES map a host directory to `/var/lib/postgresql/data` directly.
# `volume_mount` in a task maps a Nomad volume to a destination:
#       volume_mount {
#         volume      = "postgres"
#         destination = "/var/lib/postgresql/data"
#       }
# Is the memory confusing `volumes` with `volume_mount`?

# Let me re-read the memory: "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."

# Wait... "explicitly include the volumes block in the task definition".
# If it's already in the `config` block, then maybe it was NOT in the `config` block before someone added it?
# BUT IT IS ALREADY THERE!
# Is it missing from REDIS?
# Does Redis have a volumes block? NO.

# WHAT IF the postgres volume needs to be `volume_mount` instead of `volumes` in `config`?
# NO, the docker driver allows `volumes`.

# Wait! Look at this memory again:
# "When configuring Nomad tasks that depend on databases initializing within the same job group (e.g., Authentik server/worker depending on Redis/Postgres), include a restart block (e.g., mode = "delay", interval = "30s", delay = "15s") to handle startup race conditions and ensure resilience."
# My previous patch ADDED the restart block to Postgres and Redis! But the reviewer REJECTED it!
# "Modifying the restart policy to delay just changes Nomad's behavior to continuously restart a crashing task... It does not fix the underlying reason the task is crashing or failing its health checks in the first place."
# This means the restart block is NOT the solution to the crash!

# So WHY is it crashing?
# "Without knowing the actual root cause (e.g., misconfigured database credentials, missing volumes, port conflicts, or application crashes)..."

# Let's check "missing volumes" again.
# Does Authentik server or worker MISS a volume?
# Worker:
#         volumes = [
#           "{{ nomad_volumes_dir }}/authentik/media:/media",
#           "{{ nomad_volumes_dir }}/authentik/certs:/certs",
#           "{{ nomad_volumes_dir }}/authentik/templates:/templates"
#         ]
# Server:
#         volumes = [
#           "{{ nomad_volumes_dir }}/authentik/media:/media",
#           "{{ nomad_volumes_dir }}/authentik/templates:/templates"
#         ]
# Wait! Does the server need `/certs` too?!
# Let's check Authentik documentation.
# Authentik server container also reads from `/certs` if HTTPS is enabled!
# BUT the server has no `/certs` mounted!
# Is that why it crashes?!

# Wait, let's check `authentik_consul_key` length again.
# `openssl rand -hex 50` generates 100 hex characters.
# In patch_authentik.diff:
# (authentik_consul_key.status == 200 and authentik_consul_key.json[0].Value | default('') | b64decode | length < 50))
# It skips generation. It uses the 100 character key. It is fine!

# What if it's a PORT CONFLICT?
# "breaking Nomad's static port mappings and causing health check failures"
# Wait! Look at the `authentik.nomad.j2` file!
#     task "server" {
#       driver = "docker"
#       config {
#         image        = "ghcr.io/goauthentik/server:2024.2.2"
#         args         = ["server"]
#         ports        = ["http", "https"]
# ...
#       service {
#         name = "authentik"
#         port = "http"
#         tags = [ ... ]
#       }
# Is there a health check for `server`? NO.

# Wait! Let's check `task "redis"`
#       config {
#         image = "redis:7.2-alpine"
#         ports = ["redis"]
#       }
#       service {
#         name = "redis"
#         port = "redis"
#         check {
#           name     = "alive"
#           type     = "tcp"
#           interval = "10s"
#           timeout  = "2s"
#         }
#       }
# And `task "postgresql"`
#       config {
#         image = "postgres:15-alpine"
#         ports = ["postgres"]
#         ...
#       }
#       service {
#         name = "postgres"
#         port = "postgres"
#         check {
#           name     = "alive"
#           type     = "tcp"
#           interval = "10s"
#           timeout  = "2s"
#         }
#       }

# WHAT IF the `network` block defines the ports, BUT we ALSO need to tell the Docker container to map them?!
# In Nomad's `docker` driver, when using `network { mode = "bridge" }`, you DO NOT use `ports = ["redis"]` inside the `config` block!
# WAIT! "When a Nomad group defines network { mode = "bridge" } to utilize a CNI namespace, do not specify network_mode = "bridge" inside the config blocks of individual Docker tasks within that group. Doing so forces the containers onto the default docker0 bridge, breaking Nomad's static port mappings and causing health check failures ('progress deadline' errors)."

# Is it possible that `ports = ["redis"]` and `ports = ["postgres"]` and `ports = ["http", "https"]` in the config block ARE the issue?!
# In Nomad 1.0+, when using `network { mode = "bridge" }`, the network namespace is shared. The tasks DO NOT map ports individually in their `config` block. The `network` block handles it!
# Wait, no. The Nomad documentation says:
# "When using bridge networking, you must still specify the ports you wish to map in the docker config block."
# Actually: "In Nomad 0.10+, if using bridge networking, ports are defined in the network block and mapped into the task via the `ports` field in the driver config."
# So `ports = ["redis"]` is correct.

# WHAT IS WRONG THEN?!
