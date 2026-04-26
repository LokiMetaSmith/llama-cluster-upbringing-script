# The `Template Missing: kv.block(authentik/secret-key)` error is caused by Nomad NOT BEING ABLE TO READ THE KEY from Consul.
# Why?
# "If Nomad doesn't have a token with access to `authentik/secret-key`, Nomad's Consul queries will return 404 Not Found"
# BUT the Nomad client HAS the token!
# Let's check `ansible/roles/nomad/templates/client.hcl.j2`:
#   consul {
#     token = "{{ nomad_consul_token }}"
#   }
# What if the `nomad_consul_token` is NOT the `consul_bootstrap_token` and doesn't have permissions?
# Yes, `nomad_consul_token` might be a less privileged token.
# Does Nomad have a way to specify the token in the template?
# Nomad documentation:
# "Vault and Consul tokens can be provided per-task or per-job to access secrets or key-value data."
# Nomad `template` block DOES NOT accept a `token` argument! It uses the token of the Nomad client agent or the job's `consul { token = ... }` block!
# Does the `job "authentik"` have a `consul { token = ... }` block?
# NO!
# Wait! In Nomad 1.0+:
# job "authentik" {
#   ...
#   group "authentik" {
#     consul {
#       token = "{{ consul_bootstrap_token }}"
#     }
#     ...
#   }
# }
# Actually, the job can define `consul { namespace = ... }`. Can it define `token`? No, `vault { ... }` can be defined per job, but `consul` token is fetched from Nomad client.

# What if `authentik_consul_key` Ansible task just didn't generate it correctly?
# The user's output said "skipping" for both generation and publishing.
# If it skipped, it was because the key WAS ALREADY IN CONSUL and it was >= 50 characters.

# WHAT IF THE TEMPLATE IS USING THE WRONG SYNTAX?
# AUTHENTIK_SECRET_KEY="{{ '{{' }} key "authentik/secret-key" {{ '}}' }}"
# This produces `{{ key "authentik/secret-key" }}` in the Nomad job file.
# Is there a possibility that `authentik/secret-key` is literal but we need to use single quotes inside?
# `{{ key 'authentik/secret-key' }}`
# Nomad template supports both.

# WHAT IF the issue IS literally just the `volumes` block format in Postgres?
# Look at memory: "explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data)"
# I am looking at `volumes = [ "{{ nomad_volumes_dir }}/authentik/postgres:/var/lib/postgresql/data" ]`.
# Wait! What if I need to map it as a Nomad `volume` block instead of Docker `volumes`?
# In Nomad, you map host volumes via `volume` block.
# BUT the memory literally says: "e.g., mapping a host directory to /var/lib/postgresql/data". The term "mapping" implies `[host]:[container]` syntax which is Docker.

# What if I change `b64decode` to `b64decode | string` in Ansible playbook?

# Let me use the `knowledgebase_lookup` with "Template Missing: kv.block(authentik/secret-key)"!
