# If `authentik_password` is not defined anywhere, it evaluates to the literal string `'authentik_password'` because of the jinja template!
# `POSTGRES_PASSWORD = "{{ authentik_db_password | default('authentik_password') }}"`
# Yes, the default filter uses the literal string `'authentik_password'`.
# So the password is `authentik_password`.
# So it's not empty!

# So WHY did `postgres` crash?
# Is it because of the volume mapping?
# The memory rule says: "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."
# Is it possible that the memory tells me to put `volumes` inside the `task` definition INSTEAD of `config`?
# In Nomad, there is NO `volumes` attribute in the `task` block.
# Nomad `docker` driver uses `volumes` in `config`.

# BUT WAIT! Nomad DOES have a `volume` block in the task definition.
# If I change `config { volumes = ["..."] }` to:
# task "postgresql" {
#   volume "postgres" {
#     type = "host"
#     source = "postgres"
#     read_only = false
#   }
# }
# And add a `volume` block in the group!
#   group "authentik" {
#     volume "postgres" {
#       type = "host"
#       source = "authentik-postgres"
#     }
#   }
# BUT Ansible creates the directory directly using a host path `{{ nomad_volumes_dir }}/authentik/postgres`.
# So to use Nomad's `volume` blocks, you MUST define the host volume in the Nomad client config.
# We don't have access to the Nomad client config to add `host_volume`!

# So we MUST use Docker driver's `volumes` array!

# WAIT!!!
# What if the `redis` task ALSO needs the `volumes` block?!
# If I don't give redis a volume, it won't crash on boot!

# So WHY did the server fail with `Template Missing: kv.block(authentik/secret-key)`?
# Let's fix THAT first.
# If Nomad template engine is failing to render the secret key, it's 100% because the Nomad client does not have the permissions to read it OR the key actually doesn't exist at the exact path.
# How do we bypass the template engine for this key and let Ansible do the work?
# In `ansible/roles/authentik/templates/authentik.nomad.j2`:
# Change `AUTHENTIK_SECRET_KEY="{{ '{{' }} key "authentik/secret-key" {{ '}}' }}"`
# To something that evaluates using Ansible variables!

# WAIT!!!
# Is the `key` actually stored in `authentik/secret-key`?
# In Ansible: `url: "http://.../v1/kv/authentik/secret-key"`
# If it is stored via Consul API without URL-encoding, the key is `authentik/secret-key`.

# Wait! Look at `ansible/roles/authentik/tasks/main.yml`:
# - name: Publish Authentik secret key to Consul
#   ansible.builtin.uri:
#     url: "http://{{ cluster_ip | default('127.0.0.1') }}:{{ consul_http_port | default(8500) }}/v1/kv/authentik/secret-key"
#     method: PUT
#     body: "{{ authentik_generated_key.stdout }}"

# WHAT IF `authentik_consul_key.status == 200` but the length check failed because `json[0].Value` is base64 encoded and I wrote the Python check wrongly?
# `b64decode | length < 50`
# If the generated key is `openssl rand -hex 50`, its length is 100.
# So `length < 50` is False. The condition is False. So it skips.
# If it skips, the key in Consul remains untouched.
# But WHAT IF the key in Consul doesn't have a value?!
# If it doesn't have a value, `default('')` makes it empty string, `length < 50` is True, and it RE-GENERATES the key!
# So it WOULD NOT skip.

# Is there ANY REASON why Nomad would report `Template Missing` for a key that DOES exist?
# Yes! ACLs!
# To fix this, I MUST fix the ACL issue OR bypass Nomad template engine.
# BUT WAIT.
# The memory rule says:
# "Authentik deployments via Nomad will crash on boot and result in 'progress deadline' failures if the AUTHENTIK_SECRET_KEY is fewer than 50 characters. When verifying existing Consul keys in Ansible playbooks, decode the base64-encoded Value from the JSON response and check its length, triggering key regeneration if it is too short."
# Wait, look at the error log from the user AGAIN.
# "2026-04-26T00:04:17Z  Template             Missing: kv.block(authentik/secret-key)"
# IF the `Template Missing` error caused the progress deadline... then it's directly responsible for the `server` and `worker` crash!

# BUT why did `postgres` crash?
# `Docker container exited with non-zero exit code: 1`
# What if it crashed because of... lack of memory?
# `cpu = 200`, `memory = 256`
# Postgres 15 Alpine easily runs on 256MB.
# What if it crashed because `authentik_db_user` is missing? No, defaults to `authentik`.
# What if the `volumes` path string is malformed?
# "{{ nomad_volumes_dir }}/authentik/postgres:/var/lib/postgresql/data"
# `nomad_volumes_dir` is `/opt/nomad/volumes`.
# String evaluates to: `/opt/nomad/volumes/authentik/postgres:/var/lib/postgresql/data`. This is completely standard.

# Could the memory rule: "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."
# ACTUALLY BE REFERRING TO SOMETHING I NEED TO ADD TO THE TEMPLATE?
# If the `volumes` block IS in the template, what if I need to ADD something to it?
# Or what if it's missing in a different template? No, it specifically says "like PostgreSQL (e.g., in Authentik)".

# WAIT! Let me look at the `authentik.nomad.j2` file again.
