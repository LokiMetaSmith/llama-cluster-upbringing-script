# IT HAS THE VOLUMES BLOCK IN THE CONFIG BLOCK!
# What if it's a "missing volumes" issue?
# Does the `authentik` server or worker task need a volume?!
# The memory DOES NOT mention `server` or `worker` needing a volume.
# Let's check Authentik documentation... Oh I can't.

# Let's look at `Template Missing: kv.block(authentik/secret-key)`.
# WHY would Nomad not be able to find the key?
# In Nomad, the `template` stanza can read keys from Consul.
# `key "authentik/secret-key"`
# If it says `Missing: kv.block(authentik/secret-key)`, it means it successfully queried Consul, but the key was NOT FOUND (404)!
# If the key was NOT FOUND, why did the Ansible playbook SKIP generating it?!
# Ansible playbook logic:
#  when: >
#    authentik_consul_key is not failed and
#    (authentik_consul_key.status == 404 or
#    (authentik_consul_key.status == 200 and authentik_consul_key.json[0].Value | default('') | b64decode | length < 50))

# Let's analyze the Python equivalent of this logic!
def evaluate_when(status, is_failed, length=None):
    if is_failed:
        return False
    if status == 404:
        return True
    if status == 200 and length is not None and length < 50:
        return True
    return False

# If `is_failed` is False (ansible `ignore_errors` makes `is_failed` = True if curl fails, BUT `status_code: [200, 404]` makes 404 count as SUCCESS!
# So if status is 404, `is_failed` is False.
# Then `status == 404` is True.
# Then it SHOULD return True!
# But in the user's log, it SKIPPED!
# This means it returned False!
# If it returned False, `status` CANNOT be 404!
# So `status` MUST be 200 (since 200 and 404 are the only valid status codes, everything else is `is_failed = True`).
# If `status` is 200, the key EXACTLY `authentik/secret-key` EXISTS IN CONSUL!
# Then WHY does Nomad say `Missing: kv.block(authentik/secret-key)`?!

# WHAT IF the `key` function in Nomad template is looking for a DIFFERENT path?
# In Consul, keys don't start with `/`. They are just `authentik/secret-key`.
# What if Ansible queries `http://.../v1/kv/authentik/secret-key`, and gets a 200.
# And Nomad queries `authentik/secret-key`.
# This is completely standard.

# Is it possible that Nomad is configured with `namespace = "default"`, but Consul keys are global?
# Consul doesn't have namespaces in the open-source version unless it's Enterprise.

# Wait! Look at the `authentik.nomad.j2` file again!
# AUTHENTIK_SECRET_KEY="{{ '{{' }} key "authentik/secret-key" {{ '}}' }}"
# If the key has double quotes inside double quotes?!
# NO, Jinja2 renders `{{ key "authentik/secret-key" }}`.
# Nomad's `template` parses `{{ key "authentik/secret-key" }}`.
# This is correct.

# What if `postgres` is failing because of `network_mode = "bridge"`?
# "When a Nomad group defines network { mode = "bridge" } to utilize a CNI namespace, do not specify network_mode = "bridge" inside the config blocks of individual Docker tasks within that group."
# Look at my previous grep! I searched for `network_mode =` in the entire repository.
# Is it possible that I DID specify it, and the user's version of the repo HAS it?
# The user said: "the repo is up to date with the git repo."
# My git repo has `bad440b8`.
# Does `authentik.nomad.j2` have `network_mode`?
# I wrote `fix_authentik12.py` and found `mode = "{{ authentik_network_mode | default('bridge') }}"` in the `network` block, but NOT in the `config` blocks.

# WAIT. Is it possible the error is NOT in `authentik.nomad.j2`?
# What about the memory rule: "Authentik is deployed via Nomad as a self-contained job group using bridge networking, relying on Consul DNS (redis.service.consul, postgres.service.consul) instead of hardcoded IPs. To prevent connection failures due to dynamic port assignments in Nomad bridge networks, Redis and Postgres must be explicitly mapped to static host ports in the network block (e.g., authentik_redis_port), and these exact ports must be passed to the Authentik server/worker tasks as environment variables (AUTHENTIK_REDIS__PORT, AUTHENTIK_POSTGRESQL__PORT)."

# If `postgres` is failing, what if the `postgres` memory rule is the key?
# "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."

# What if I need to use `volume_mount` INSTEAD of `volumes` because Docker driver `volumes` doesn't enforce permissions as reliably as Nomad `volume_mount`?
# In Nomad, using host volumes via `docker` config `volumes` is legacy. Nomad `host_volume` is the modern way.
# BUT the memory specifically uses the syntax `volumes block ... (e.g., mapping a host directory to /var/lib/postgresql/data)`.
# The word "mapping" explicitly describes the `"host:container"` syntax.

# Is it possible that the memory meant: "add a volumes block for REDIS"?
# Redis is stateful.
# Let's add `volumes` block for Redis!
