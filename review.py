# The code review failed.
# The reviewer said: "The agent asked the user to provide the nomad alloc logs to determine why the containers were crashing. Instead of providing the allocation logs, the user mistakenly pasted the same high-level Ansible output repeatedly. Without knowing the actual root cause (e.g., misconfigured database credentials, missing volumes, port conflicts, or application crashes), the agent blindly guessed a fix by adding restart { mode = "delay" } blocks to the job template."
# And: "Modifying the restart policy to delay just changes Nomad's behavior to continuously restart a crashing task within the same allocation instead of failing the allocation and replacing it. It does not fix the underlying reason the task is crashing or failing its health checks in the first place."
# The reviewer is saying my blind guess was wrong and I MUST find the actual root cause!
# BUT the user's environment is out of my reach. I cannot run `nomad alloc logs`!
# Oh wait...
# Is it possible that the ACTUAL root cause is explicitly stated in the memory?
# Look at memory AGAIN.
# "When a Nomad group defines network { mode = "bridge" } to utilize a CNI namespace, do not specify network_mode = "bridge" inside the config blocks of individual Docker tasks within that group. Doing so forces the containers onto the default docker0 bridge, breaking Nomad's static port mappings and causing health check failures ('progress deadline' errors)."
# Did I check for this? YES. I checked the template and `network_mode = "bridge"` is NOT inside the `config` blocks.

# What about the Postgres memory?
# "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."
# Where is `volumes = [...]` in the template?
# It is inside `config { ... }` block!
# Does Nomad allow a `volumes` list inside the `task` definition (outside `config`)?
# NO! BUT Nomad has a `volume` (singular) block!
# Wait. What if the memory says "explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data)"?
# Actually, the syntax `volumes = [...]` inside `config` block IS the only place where the `["/host:/container"]` mapping works!
# In Nomad 1.7.7, is there a `volumes` block? No.

# Wait, what if the memory implies I SHOULD NOT USE the `volumes = [...]` syntax, BUT instead use the Nomad `volume` block?
# If I use `volume`, it looks like this:
# task "postgresql" {
#   volume_mount {
#     volume      = "postgres"
#     destination = "/var/lib/postgresql/data"
#   }
# }
# BUT then I have to define `volume "postgres"` in the group!
# group "authentik" {
#   volume "postgres" {
#     type = "host"
#     source = "authentik-postgres"
#   }
# }

# Let me re-read the Memory very carefully!
# "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the `volumes` block in the task definition (e.g., mapping a host directory to `/var/lib/postgresql/data`) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."
# Notice the backticks around `volumes`.
# And the example: "mapping a host directory to /var/lib/postgresql/data".
# Wait, look at this syntax:
# task "postgresql" {
#   config { ... }
#   volumes = ["/host:/container"] # INVALID in Nomad?
# }
# NO, in Docker driver, `volumes` is a list of strings IN THE CONFIG BLOCK!
# Wait! Does Nomad 1.0+ support a `volumes` block in the `task` definition?! NO!

# WAIT!!! "Authentik is deployed via Nomad as a self-contained job group using bridge networking, relying on Consul DNS (redis.service.consul, postgres.service.consul) instead of hardcoded IPs. To prevent connection failures due to dynamic port assignments in Nomad bridge networks, Redis and Postgres must be explicitly mapped to static host ports in the network block (e.g., authentik_redis_port), and these exact ports must be passed to the Authentik server/worker tasks as environment variables (AUTHENTIK_REDIS__PORT, AUTHENTIK_POSTGRESQL__PORT)."

# If `network { mode = "bridge" }` is used, is it possible that `port "postgres" { ... }` was misconfigured?
#       port "postgres" {
#         static = {{ authentik_postgres_port | default(15432) }}
#         to = 5432
#       }
# This maps host port 15432 to container port 5432.
# BUT look at the `authentik.nomad.j2` file:
#       port "redis" {
#         static = {{ authentik_redis_port | default(16379) }}
#         to = 6379
#       }
# Is there anything missing in the network block?
