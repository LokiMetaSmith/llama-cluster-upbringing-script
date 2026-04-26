# If the repo is up to date, then my local file exactly matches what ran.
# And `postgres` crashed with exit code 1.
# What causes Postgres to crash with exit code 1?
# - "chmod: changing permissions of '/var/lib/postgresql/data': Operation not permitted" -> because Nomad Docker driver mounts the host volume but the container runs as `postgres` and maybe the Docker daemon doesn't let it chown if the host volume is already created?
# - "chown: changing ownership of '/var/lib/postgresql/data': Operation not permitted"
# - Or missing environment variables?
#   POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB are all provided.
# - Or the volume isn't mapped properly because `nomad_volumes_dir` is not an absolute path?
#   It's `/opt/nomad/volumes`. That's absolute.

# Let's consider the `authentik_secret_key` issue again.
# "Template Missing: kv.block(authentik/secret-key)"
# Does `authentik.nomad.j2` need to fetch the key using Consul HTTP API instead of Nomad Template Engine, if ACLs are blocking it?
# OR we can just inject it from Ansible!
# Why doesn't the template just do:
# AUTHENTIK_SECRET_KEY="{{ authentik_generated_key.stdout | default(authentik_consul_key.json[0].Value | default('') | b64decode) }}"
# If we do that, we bypass Nomad's Consul Template altogether, and just hardcode the secret into the Nomad job file via Ansible.
# Is that what the patch `patch_authentik.diff` implied?
# The patch diff ONLY changed `ansible/roles/authentik/tasks/main.yml`.
# It didn't change `authentik.nomad.j2`.

# Wait! Let's check `group_vars/all.yaml` for `authentik_network_mode`.
# `authentik_network_mode: "bridge"`

# What if the reviewer's message means: "You blindly guessed by adding `restart { mode = "delay" }`. You NEED to read the Nomad alloc logs. I will give them to you."
# The user gave me the Nomad alloc logs!
# And I see:
# 1. postgres is crashing with Exit Code 1.
# 2. server/worker are failing with "Template Missing: kv.block(authentik/secret-key)".

# To fix "Template Missing: kv.block(authentik/secret-key)":
# The key genuinely does not exist in Consul!
# WHY DOES IT NOT EXIST?
# Let's look at `ansible/roles/authentik/tasks/main.yml`.
# - name: Check if Authentik secret key exists in Consul
#   ansible.builtin.uri:
#     url: "http://{{ cluster_ip | default('127.0.0.1') }}:{{ consul_http_port | default(8500) }}/v1/kv/authentik/secret-key"
#     method: GET
#     headers:
#       X-Consul-Token: "{{ consul_bootstrap_token | default(omit) }}"
#     status_code: [200, 404]
#   register: authentik_consul_key
#   ignore_errors: yes

# If the key does NOT exist, `authentik_consul_key.status` should be 404.
# Then the "Generate Authentik secret key" task:
#   when: >
#     authentik_consul_key is not failed and
#     (authentik_consul_key.status == 404 or
#     (authentik_consul_key.status == 200 and authentik_consul_key.json[0].Value | default('') | b64decode | length < 50))
# If it is 404, it WILL run!
# BUT IT SKIPPED!
# If it skipped, it CANNOT be 404.
# So `authentik_consul_key.status` must be 200.
# If it is 200, then the key DOES exist in Consul!
# BUT Nomad template engine says `Template Missing: kv.block(authentik/secret-key)`.
# WHY would Nomad think it doesn't exist if Ansible can read it and get a 200?!
# 1. Nomad is hitting a different Consul Datacenter.
# 2. Nomad Consul integration does not have the `X-Consul-Token`!
# Ansible uses `X-Consul-Token: "{{ consul_bootstrap_token }}"`.
# If Consul has ACLs enabled (which it likely does, since we use `consul_bootstrap_token`), Nomad's client needs a token to read from Consul!
# If the Nomad client doesn't have a token configured for Consul, it will get a 403 Forbidden or 404 Not Found (Consul hides keys you don't have access to).
# Therefore, Nomad Template Engine fails to render the template!

# HOW DO WE FIX IT?
# Since `CONSUL_HTTP_TOKEN="{{ consul_bootstrap_token | default('') }}"` is passed as an env var, Authentik has the token.
# BUT Nomad Template Engine doesn't use the task's environment variables to authenticate with Consul!
# We can just render the secret key directly using Ansible!
# Instead of `AUTHENTIK_SECRET_KEY="{{ '{{' }} key "authentik/secret-key" {{ '}}' }}"`
# We can just render the value we fetched in Ansible!
