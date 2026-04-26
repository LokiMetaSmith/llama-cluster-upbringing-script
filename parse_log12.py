# Okay! So Nomad DOES have the Consul token!
# Then why does it say `Missing: kv.block(authentik/secret-key)`?
# Let's check `authentik_consul_key` Ansible output if possible. We can't.
# Wait!
# What if the generated key in `authentik/secret-key` is somehow invalid? No.

# Wait. Is it `Missing: kv.block` because the key in Consul doesn't have a value?!
# If `authentik_consul_key.json[0].Value` is missing or null, `b64decode` might fail in Jinja, causing the task to fail, NOT skip!
# Unless `default('')` is used!
# `authentik_consul_key.json[0].Value | default('') | b64decode | length < 50`
# If `Value` is empty, `default('')` returns `''`.
# `'' | b64decode` returns `''`.
# `length < 50` is TRUE.
# So it SHOULD run!
# BUT IT SKIPPED!
# This means `length < 50` is FALSE.
# This means `Value` is >= 50 characters.
# So the key IS in Consul, and it IS valid.

# So why does Nomad say `Missing: kv.block(authentik/secret-key)`?
# Maybe `kv.block` is missing because we need to query `authentik/secret-key` using a different syntax?
# No, `{{ key "authentik/secret-key" }}` is standard Nomad Consul template syntax.
# What if the Nomad client doesn't have the ACL token with permission to read THAT specific key?
# The Consul bootstrap token has management (root) permissions. If Nomad is configured with it, it has access.

# Could the error `Missing: kv.block` literally mean Nomad cannot connect to Consul?
# If Nomad cannot connect to Consul, it usually says `connection refused` or `error fetching`. `Missing: kv.block` implies it connected, queried the key, and got a 404!
# If Nomad gets 404, but Ansible gets 200, they are hitting DIFFERENT Consul instances!
# How?
# `cluster_ip` in Ansible is the Tailscale IP (`100.64.0.1`).
# Nomad connects to Consul on `127.0.0.1:8500` or via `tailscale0`.
# If it's a multi-node cluster, maybe the key hasn't replicated? Unlikely.
# What if Ansible PUT the key in the `dc1` datacenter, but Nomad is in `dc2`? No, `datacenters = ["dc1"]`.

# Wait! Let's read `patch_authentik.diff` again carefully.
# Did I miss something?
# What if the key in Consul was stored with quotes?
# That shouldn't matter.

# Let's pivot to the Postgres crash.
# "Docker container exited with non-zero exit code: 1"
# Why would Postgres 15 Alpine crash?
# - Data directory has wrong permissions.
# - Password is empty.
# In `env`:
#         POSTGRES_PASSWORD = "{{ authentik_db_password | default('authentik_password') }}"
# Is there a typo?
# `authentik_password` is provided as default.
# What if `authentik_db_password` is an empty string?
# If it is empty, Postgres crashes because it requires a password.
# Let's check `group_vars/all.yaml`!
