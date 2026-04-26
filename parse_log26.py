# Redis doesn't have a host directory created by Ansible!
# In `ansible/roles/authentik/tasks/main.yml`, we only create `media`, `templates`, `certs`, and `postgres` directories.
# If we add a volume for redis to `/opt/nomad/volumes/authentik/redis`, it will crash because the directory doesn't exist on the host!

# SO Redis volume is NOT the issue.

# Let's consider `Template Missing: kv.block(authentik/secret-key)`.
# With my replacement, it now uses Ansible to evaluate it:
# AUTHENTIK_SECRET_KEY="{{ authentik_generated_key.stdout | default(authentik_consul_key.json[0].Value | default('') | b64decode) }}"
# THIS DEFINITELY FIXES THE SERVER/WORKER TEMPLATE MISSING ISSUE!

# Now, WHY did postgres crash?
# Postgres crashed with Exit Code 1.
# What if it's NOT crashing anymore?
# The logs I saw from the user showed Postgres crashing. But what if Postgres crashed because it couldn't connect to Consul?! No, Postgres doesn't connect to Consul.
# What if Postgres crashed because the container ran out of memory?
# `memory = 256`. That's plenty for postgres 15 alpine on startup.

# Could `postgres` be crashing because there are TWO `postgres` tasks running on the same host, conflicting on the port?
# "port conflicts"
# The reviewer said: "(e.g., misconfigured database credentials, missing volumes, port conflicts, or application crashes)"
# Look at the network block for postgres:
#       port "postgres" {
#         static = {{ authentik_postgres_port | default(15432) }}
#         to = 5432
#       }
# Is `15432` conflicting with something else?
# Let's check `group_vars/all.yaml`!
import re
with open("group_vars/all.yaml", "r") as f:
    text = f.read()
for line in text.split('\n'):
    if "15432" in line:
        print(line)
