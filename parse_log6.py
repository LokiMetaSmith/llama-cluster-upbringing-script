# If Nomad says `Template Missing: kv.block(authentik/secret-key)`, it means Nomad Consul template engine cannot find the key.
# Why?
# Is it because we passed the wrong token?
# `CONSUL_HTTP_TOKEN="{{ consul_bootstrap_token | default('') }}"`
# Wait, `CONSUL_HTTP_TOKEN` sets the env var inside the container!
# BUT what about Nomad fetching the template from Consul?
# In `authentik.nomad.j2`:
#       template {
#         data = <<EOH
# CONSUL_HTTP_TOKEN="{{ consul_bootstrap_token | default('') }}"
# AUTHENTIK_SECRET_KEY="{{ '{{' }} key "authentik/secret-key" {{ '}}' }}"
# EOH
#         destination = "secrets/authentik.env"
#         env         = true
#       }
# If Consul has ACLs enabled, the Nomad client needs a token to fetch the key.
# But Nomad is NOT passing `consul_bootstrap_token` to the Nomad template engine!
# To pass it, the Nomad job must have:
#       vault {
#         policies = ["..."]
#       }
# Or we can just bypass Nomad template engine for the secret key!
# Why don't we just render the secret key directly via Ansible Jinja2 instead of Nomad template?!
# NO. If we render it directly in the Nomad job file, the secret key is stored in plaintext in the Nomad job definition on disk and in the API. This is bad security practice.
# BUT wait! `CONSUL_HTTP_TOKEN` is already rendered in plaintext in the Nomad job definition!
# `CONSUL_HTTP_TOKEN="{{ consul_bootstrap_token | default('') }}"`
# If we are already putting the Consul bootstrap token in plaintext, why use `key "authentik/secret-key"`?
# Wait! Is it possible that the key is missing because it actually wasn't created because of a typo?
# "authentik/secret-key"

# Let's check `postgres` crashing:
# "Docker container exited with non-zero exit code: 1"
# Why would `postgres:15-alpine` crash with exit code 1?
# Usually permissions on the data directory: `/var/lib/postgresql/data`.
# In `ansible/roles/authentik/tasks/main.yml`:
# - name: Set postgres volume permissions
#   ansible.builtin.shell: chown -R 70:70 "{{ nomad_volumes_dir }}/authentik/postgres" && chmod 700 "{{ nomad_volumes_dir }}/authentik/postgres"
#   become: yes
# This seems perfectly fine.

# Let's read the Memory rule VERY carefully:
# "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."

# WAIT. "explicitly include the volumes block in the task definition"
# In Nomad 1.7.7, there is a `volume` block:
#     task "postgresql" {
#       volume "postgres" {
#         type = "host"
#         source = "postgres"
#         read_only = false
#       }
#     }
# And the group block needs:
#   group "authentik" {
#     volume "postgres" {
#       type = "host"
#       source = "authentik-postgres"
#     }
#   }
# BUT the memory specifically says "(e.g., mapping a host directory to /var/lib/postgresql/data)".
# The string `"/host:/var/lib/postgresql/data"` is EXPLICITLY the Docker `volumes` configuration.

# BUT wait! If it is ALREADY there, what if the memory meant that I should NOT put it in `config`, but instead use `volume_mount`?
# NO! "(e.g., mapping a host directory to /var/lib/postgresql/data)" -> `volume_mount` does NOT use this syntax! It uses `destination = "/var/lib/postgresql/data"`.

# Wait! Look at `task "postgresql"` config:
#       config {
#         image = "postgres:15-alpine"
#         ports = ["postgres"]
#         volumes = [
#           "{{ nomad_volumes_dir }}/authentik/postgres:/var/lib/postgresql/data"
#         ]
#       }
# What if it's MISSING `volumes = [...]` from the memory rule's perspective?
# What if my local git checkout ALREADY has the fix, but the user's does NOT?!
# NO. The user explicitly stated: "the repo is up to date with the git repo."
