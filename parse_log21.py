# Okay. No specific knowledge base hit.

# Wait, let's look at the INITIAL memory rule that the reviewer thought I violated:
# "Authentik is deployed via Nomad as a self-contained job group using bridge networking, relying on Consul DNS (redis.service.consul, postgres.service.consul) instead of hardcoded IPs. To prevent connection failures due to dynamic port assignments in Nomad bridge networks, Redis and Postgres must be explicitly mapped to static host ports in the network block (e.g., authentik_redis_port), and these exact ports must be passed to the Authentik server/worker tasks as environment variables (AUTHENTIK_REDIS__PORT, AUTHENTIK_POSTGRESQL__PORT)."

# Is `AUTHENTIK_REDIS__PORT` set exactly to the static host port?!
# In the `network` block:
#       port "redis" {
#         static = {{ authentik_redis_port | default(16379) }}
#         to = 6379
#       }
# In the `template` block:
# AUTHENTIK_REDIS__PORT="{{ authentik_redis_port | default(16379) }}"
# Yes.

# What about Postgres?
#       port "postgres" {
#         static = {{ authentik_postgres_port | default(15432) }}
#         to = 5432
#       }
# In the `template` block:
# AUTHENTIK_POSTGRESQL__PORT="{{ authentik_postgres_port | default(15432) }}"
# Yes.

# Wait! "When a Nomad group defines network { mode = "bridge" } to utilize a CNI namespace, do not specify network_mode = "bridge" inside the config blocks of individual Docker tasks within that group. Doing so forces the containers onto the default docker0 bridge, breaking Nomad's static port mappings and causing health check failures ('progress deadline' errors)."
# IS IT POSSIBLE THAT `network_mode = "bridge"` is set inside the Postgres config?
# I checked before. It is not.

# Let's fix the problem BY rendering the secret key correctly into the template WITHOUT using `key "authentik/secret-key"` so that we BYPASS the Nomad Template Missing error!
# In `ansible/roles/authentik/templates/authentik.nomad.j2`:
# Change `AUTHENTIK_SECRET_KEY="{{ '{{' }} key "authentik/secret-key" {{ '}}' }}"`
# To `AUTHENTIK_SECRET_KEY="{{ authentik_generated_key.stdout if authentik_generated_key is not skipped else authentik_consul_key.json[0].Value | b64decode }}"`

# BUT WAIT! Why did Postgres crash?
# `Docker container exited with non-zero exit code: 1`
# If the postgres volume directory `/opt/nomad/volumes/authentik/postgres` doesn't have the right permissions, Postgres crashes.
# Ansible uses `chown -R 70:70`.
# Is 70:70 the right UID/GID for postgres on alpine?
# YES, `postgres` user in alpine linux has UID 70.
# Why would it crash?
# What if `authentik_db_password` is not defined, AND `authentik_password` is also missing or empty?
# Let's check `ansible/roles/authentik/defaults/main.yml`.
import yaml
with open("ansible/roles/authentik/defaults/main.yml") as f:
    defaults = yaml.safe_load(f)
print(defaults)
