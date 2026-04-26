# If `authentik_consul_key` throws an error that is NOT 404 or 200 (like 403, 500, or connection refused), `ignore_errors: yes` makes it pass, but it is marked as `failed`.
# So `authentik_consul_key is not failed` evaluates to FALSE.
# Then the "Generate Authentik secret key" task is skipped!
# And the "Publish Authentik secret key to Consul" is skipped!
# So the key is missing in Consul!

# BUT WHY would it throw an error?
# Wait! `consul_http_port` is `8500`. `cluster_ip` is used.
# If `cluster_ip` is `100.64.0.1` (from the user's `NOMAD_ADDR="https://100.64.0.1:4646"`).
# If the playbook runs against `localhost`, it will hit `http://100.64.0.1:8500`.
# Is Consul listening on that IP?
# If `authentik_consul_key` failed, why didn't the playbook output show it as a failed task (ignored)?
# Look at the user's playbook output:
# TASK [authentik : Check if Authentik secret key exists in Consul]
# ok: [localhost]
# If `ignore_errors: yes` triggered, it would say `fatal: [localhost]: FAILED! ... ...ignoring`
# But it says `ok: [localhost]`!
# That means it DID NOT FAIL!
# It returned HTTP 200 OK!

# If it returned 200 OK, why does Nomad say `Missing: kv.block(authentik/secret-key)`?
# Nomad's `template` block:
# AUTHENTIK_SECRET_KEY="{{ '{{' }} key "authentik/secret-key" {{ '}}' }}"
# Which renders as: `{{ key "authentik/secret-key" }}`
# If Nomad says `Missing: kv.block(authentik/secret-key)`, it means the key is NOT in Consul!
# But Ansible got a 200 OK for `http://.../v1/kv/authentik/secret-key`?
# How is that possible?!
# Maybe Ansible hit a DIFFERENT Consul cluster?
# Ansible hit: `http://{{ cluster_ip }}:8500/v1/kv/authentik/secret-key`
# And Nomad is using its local Consul agent.
# Since it's a cluster, they should be the same.

# Wait... what if the value returned by Ansible had `length >= 50`?
# The Nomad log says `Missing: kv.block(authentik/secret-key)`. This means it does NOT exist.
# Is it possible that `authentik_consul_key.json` exists, but there is NO `authentik/secret-key`?
# If you query a folder in Consul KV `http://.../v1/kv/authentik/`, it returns 200 OK with all keys.
# But we queried `/v1/kv/authentik/secret-key`.
# Wait! What if `consul_bootstrap_token` is wrong, and it returned a 403, and Ansible masked it? No, if it was 403, the task would FAIL and be "ignored" in red. It said `ok: [localhost]`. This means it matched `status_code: [200, 404]`.
# If it was 404, `status == 404`.
# Then `(authentik_consul_key.status == 404)` is TRUE.
# Then `authentik_consul_key is not failed` is TRUE.
# So the "Generate" task SHOULD run!
# BUT IT SKIPPED!
# If it skipped, `status` CANNOT be 404!
# So `status` MUST BE 200!
# And `length < 50` must be FALSE. Meaning `length >= 50`.
# If `status` is 200, the key EXACTLY `authentik/secret-key` exists in Consul.
# Then why does Nomad complain `Missing: kv.block(authentik/secret-key)`?!

# Because Nomad is using Consul namespaces, OR it is hitting a different Consul cluster, OR Nomad's Consul integration lacks the correct ACL token!
# Let's check the template:
#       template {
#         data = <<EOH
# CONSUL_HTTP_TOKEN="{{ consul_bootstrap_token | default('') }}"
# AUTHENTIK_SECRET_KEY="{{ '{{' }} key "authentik/secret-key" {{ '}}' }}"
# ...
# Wait! Nomad's `template` block does NOT use `CONSUL_HTTP_TOKEN` from the `.env` file to fetch the template!
# The `template` block is evaluated by the Nomad Client BEFORE the container starts.
# To allow Nomad to fetch Consul keys that require a token, you must provide the token in the Nomad `template` block configuration!
# Or the Nomad client itself must have a Consul token configured in its `consul { token = "..." }` block.
# Wait, `template` block HAS NO `CONSUL_HTTP_TOKEN` variable!
# It relies on the Nomad client's Consul token!
# If Nomad doesn't have a token with access to `authentik/secret-key`, Nomad's Consul queries will return 404 Not Found (because Consul ACLs hide keys you don't have access to).
# Therefore, Nomad thinks the key is `Missing: kv.block(authentik/secret-key)`!

# HOW DO WE PASS THE TOKEN TO THE TEMPLATE STANZAS?
# In Nomad:
# template {
#   data = <<EOH
#     ...
#   EOH
#   destination = "secrets/file.env"
#   env = true
# }
# Wait! Is there another memory rule?
# Memory: "Authentik is deployed via Nomad as a self-contained job group using bridge networking..."
# Memory: "When configuring Nomad tasks that depend on databases initializing within the same job group (e.g., Authentik server/worker depending on Redis/Postgres), include a restart block (e.g., mode = "delay", interval = "30s", delay = "15s") to handle startup race conditions and ensure resilience."
# Memory: "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."

# Wait... what if the template just doesn't use the token properly?
# Or what if `postgres` is failing for EXACTLY the reason the memory mentioned?
# "explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."
# Look at `task "postgresql"`:
#     task "postgresql" {
#       driver = "docker"
#       config {
#         image = "postgres:15-alpine"
#         ports = ["postgres"]
#         volumes = [
#           "{{ nomad_volumes_dir }}/authentik/postgres:/var/lib/postgresql/data"
#         ]
#       }
# Is there a `volume` block in the task definition?
# "explicitly include the volumes block in the task definition"
# The word is `volumes` (plural).
# In Nomad's Docker driver, `volumes` can be specified. It's already there!

# What if I need to fetch the postgres logs to see WHY it failed?
# The user can run: `nomad alloc logs 0779f51c-027d-aceb-fe84-e1d2cec40dff postgres`
