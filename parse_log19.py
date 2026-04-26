# Okay, `ansible/jobs/authentik.nomad` is some old file. The playbook uses `ansible/roles/authentik/templates/authentik.nomad.j2`!
# Let me look at the ACTUAL RUN.
# `nomad job run /opt/nomad/jobs/authentik.nomad`
# It's rendered from `authentik.nomad.j2`.

# Let's think about `postgres` crashing with `Exit Code 1`.
# IF the database credentials are correct, AND the volumes are correctly mapped...
# What if it's NOT correct?
# Memory: "explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."
# Let me replace `config { volumes = ["..."] }` with NOTHING, just in case? NO.
# Is it possible the memory means I NEED to add `volumes = ["..."]`?
# IT ALREADY HAS IT.

# What about the other memory rule?
# "Authentik is deployed via Nomad as a self-contained job group using bridge networking, relying on Consul DNS (redis.service.consul, postgres.service.consul) instead of hardcoded IPs. To prevent connection failures due to dynamic port assignments in Nomad bridge networks, Redis and Postgres must be explicitly mapped to static host ports in the network block (e.g., authentik_redis_port), and these exact ports must be passed to the Authentik server/worker tasks as environment variables (AUTHENTIK_REDIS__PORT, AUTHENTIK_POSTGRESQL__PORT)."
# Let me look at `authentik.nomad.j2` AGAIN.
#       env {
#         AUTHENTIK_POSTGRESQL__USER = "{{ authentik_db_user | default('authentik') }}"
#         AUTHENTIK_POSTGRESQL__NAME = "{{ authentik_db_name | default('authentik') }}"
#         AUTHENTIK_POSTGRESQL__PASSWORD = "{{ authentik_db_password | default('authentik_password') }}"
#         AUTHENTIK_ERROR_REPORTING__ENABLED = "true"
#         AUTHENTIK_WEB__WORKERS = "{{ authentik_web_workers | default(2) }}"
#         GUNICORN_CMD_ARGS = "{{ authentik_gunicorn_cmd_args | default('--max-requests 250 --max-requests-jitter 50') }}"
#       }
# Wait, where are `AUTHENTIK_REDIS__PORT` and `AUTHENTIK_POSTGRESQL__PORT`?
# They are in `template { data = <<EOH ... env = true }`
# Is it possible that because `Template Missing` error happened, the template didn't render, and the env vars were NOT passed?!
# YES!
# If the template failed to render, the `server` container NEVER STARTED.
# BUT what about `postgres`?!
# Why did `postgres` crash?
# Let's look at `postgres` task!
#     task "postgresql" {
#       driver = "docker"
#       config {
#         image = "postgres:15-alpine"
#         ports = ["postgres"]
#         volumes = [
#           "{{ nomad_volumes_dir }}/authentik/postgres:/var/lib/postgresql/data"
#         ]
#       }
#       env {
#         POSTGRES_USER     = "{{ authentik_db_user | default('authentik') }}"
#         POSTGRES_PASSWORD = "{{ authentik_db_password | default('authentik_password') }}"
#         POSTGRES_DB       = "{{ authentik_db_name | default('authentik') }}"
#       }
#     }
# Wait! Does Postgres `15-alpine` crash if the data directory has the wrong permissions?
# Yes!
# Does my Ansible playbook `chown` it properly?
# - name: Set postgres volume permissions
#   ansible.builtin.shell: chown -R 70:70 "{{ nomad_volumes_dir }}/authentik/postgres" && chmod 700 "{{ nomad_volumes_dir }}/authentik/postgres"
# Yes!

# Let me re-read the FIRST memory rule very carefully!
# "When a Nomad group defines network { mode = "bridge" } to utilize a CNI namespace, do not specify network_mode = "bridge" inside the config blocks of individual Docker tasks within that group. Doing so forces the containers onto the default docker0 bridge, breaking Nomad's static port mappings and causing health check failures ('progress deadline' errors)."
# I already checked that `network_mode = "bridge"` is NOT in the `config` blocks.

# Let me re-read the Postgres memory rule VERY VERY CAREFULLY!
# "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."
# Is it possible the memory rule means that previously the `volumes` block was MISSING, and I added it in an earlier attempt but the user didn't have it?!
# No, I checked `git log` and it was there in the base repo.

# What if I change `Template Missing` and see if `postgres` was just randomly crashing due to something else?
