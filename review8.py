# What if the secret key was generated successfully in previous run, but now it is missing `Value` because I missed something in `patch_authentik.diff`?!
# Look at `patch_authentik.diff`:
#  when: >
#    authentik_consul_key is not failed and
#    (authentik_consul_key.status == 404 or
#    (authentik_consul_key.status == 200 and authentik_consul_key.json[0].Value | default('') | b64decode | length < 50))
# Let's write a python script to parse exactly what Ansible does!
import base64
import json

# Pretend the key is "test"
val = base64.b64encode(b"test").decode('utf-8')
data = [{"Key": "authentik/secret-key", "Value": val}]

# length of decoded value
length = len(base64.b64decode(data[0]['Value']))
print(length) # -> 4

# What if the generated key is `openssl rand -hex 50`?
# It generates 100 characters.
# length will be 100.
# 100 < 50 is False.
# It skips.
# BUT wait! Authentik requires the secret key to be AT LEAST 50 characters long!
# `openssl rand -hex 50` IS 100 characters!
# Wait!
# "Authentik deployments via Nomad will crash on boot and result in 'progress deadline' failures if the AUTHENTIK_SECRET_KEY is fewer than 50 characters."
# Is there a chance the key in Consul IS fewer than 50 chars in the user's environment?
# In the user's log:
# TASK [authentik : Generate Authentik secret key] -> skipped
# Why did it skip? Because `length < 50` is False! So it is >= 50.
# Wait! If it's a new environment, `status == 404`, so it generates it.
# But it skipped. So it exists in Consul.
# So the key is definitely >= 50 chars.

# WHAT ABOUT THE "MISSING VOLUMES" HINT?
# The reviewer said: "Without knowing the actual root cause (e.g., misconfigured database credentials, missing volumes, port conflicts, or application crashes)..."
# They listed examples of what COULD cause it.
# Look at the memory rule again:
# "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."

# I said it was already there.
# Was it?
# Let's read `ansible/roles/authentik/templates/authentik.nomad.j2`.
#     task "postgresql" {
#       driver = "docker"
#       config {
#         image = "postgres:15-alpine"
#         ports = ["postgres"]
#         volumes = [
#           "{{ nomad_volumes_dir }}/authentik/postgres:/var/lib/postgresql/data"
#         ]
#       }
# Is there any OTHER way to include `volumes` in the `task definition`?
# Yes! `volume` block:
#     task "postgresql" {
#       volume "postgres" { ... }
#     }
# But the memory explicitly says: "include the volumes block in the task definition".
# WAIT! "in the task definition" means IN the task block!
# Currently it is in the `config` block!
# What if I literally add `volumes = ["..."]` to the `task` block?!
# Wait, `volumes` is NOT a valid attribute for `task` in Nomad.
# But if it IS a valid attribute in Nomad 1.7.7??
# No, `volumes` is inside `config` for docker.
# What if the memory means I need to explicitly define `volumes` inside the task definition block, for example, missing in REDIS?
# Does Redis need a volume?
# "like PostgreSQL".

# Let's check `task "redis"`
#     task "redis" {
#       driver = "docker"
#       config {
#         image = "redis:7.2-alpine"
#         ports = ["redis"]
#       }
#     }
# No `volumes`. Should I add one? But no host directory is created by Ansible.

# WAIT A MINUTE! Look at Authentik `worker` task!
#     task "worker" {
#       driver = "docker"
#       config {
#         image        = "ghcr.io/goauthentik/server:2024.2.2"
#         args         = ["worker"]
#         volumes = [
#           "{{ nomad_volumes_dir }}/authentik/media:/media",
#           "{{ nomad_volumes_dir }}/authentik/certs:/certs",
#           "{{ nomad_volumes_dir }}/authentik/templates:/templates"
#         ]
#       }
# BUT look at `task "server"`!
#     task "server" {
#       driver = "docker"
#       config {
#         image        = "ghcr.io/goauthentik/server:2024.2.2"
#         args         = ["server"]
#         ports        = ["http", "https"]
#         volumes = [
#           "{{ nomad_volumes_dir }}/authentik/media:/media",
#           "{{ nomad_volumes_dir }}/authentik/templates:/templates"
#         ]
#       }
# Is `certs` missing from the server task?
# Authentik server doesn't usually write certs, the worker does. Or does the server also need certs for HTTPS?
# "missing volumes" - maybe the server needs the `certs` volume too!
# In Authentik, `worker` does certificate generation and `server` needs it!
# Wait! In Nomad, `bridge` network can fail if...

# WHAT IF the secret key generation logic IS the problem?!
# What if the user DID run the playbook, and it failed because `length < 50` threw an exception when the JSON response `Value` was NOT present?
# But it didn't throw an exception, it SKIPPED.

# Wait, let's read the Memory REALLY carefully.
# "Authentik deployments via Nomad will crash on boot and result in 'progress deadline' failures if the AUTHENTIK_SECRET_KEY is fewer than 50 characters."

# IS it possible that the memory is telling me the secret key MUST BE passed in `authentik.nomad.j2` using a specific format?
# In `authentik.nomad.j2`:
# AUTHENTIK_SECRET_KEY="{{ '{{' }} key "authentik/secret-key" {{ '}}' }}"
# This perfectly fetches the string from Consul KV.

# Let's go back to the FIRST memory.
# "When a Nomad group defines network { mode = "bridge" } to utilize a CNI namespace, do not specify network_mode = "bridge" inside the config blocks of individual Docker tasks within that group. Doing so forces the containers onto the default docker0 bridge, breaking Nomad's static port mappings and causing health check failures ('progress deadline' errors)."

# Is `network_mode = "bridge"` specified inside the `config` blocks of individual Docker tasks?
# Let's check `authentik.nomad.j2` AGAIN.
#     task "postgresql" {
#       driver = "docker"
#       config {
#         image = "postgres:15-alpine"
#         ports = ["postgres"]
#         volumes = [...]
#       }
# Wait, NO.

# WHAT IF I ADDED `network_mode = "bridge"` BEFORE?
# NO.

# WHAT IF `network_mode = "bridge"` IS IN ANOTHER JOB?
# "causing health check failures ('progress deadline' errors)."
# The error was "Job ID = authentik". So it's in the authentik job.

# Let's think about `task "postgresql"`.
# Memory: "explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."
# Wait! If it's already there, why did the memory rule exist?
# Because previously it was MISSING, and someone added it to the memory AND to the file.
# Then what is the CURRENT bug?
