# Okay, ALL jobs put `volumes = [ ... ]` inside the `config` block.
# So `volumes = [ ... ]` inside `config` IS correct.

# What about THIS:
# "To prevent Out of Memory (OOM) errors in Authentik Nomad deployments caused by Gunicorn worker bloat, use configurable Ansible variables (e.g., authentik_server_memory and authentik_worker_memory in ansible/roles/authentik/defaults/main.yml) for task resources, and control Gunicorn via environment variables: set AUTHENTIK_WEB__WORKERS (e.g., 2) to limit baseline RAM usage, and GUNICORN_CMD_ARGS (e.g., --max-requests 250 --max-requests-jitter 50) to enforce worker recycling."
# They are implemented in `authentik.nomad.j2` AND in `defaults/main.yml`.

# What if the `postgres` memory actually meant something else?
# "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."
# Could this mean that the `postgres` task does NOT have the `volumes` block AT ALL in the original version, and I was looking at a modified version?
# But `git diff` showed no changes to `authentik.nomad.j2` for `volumes`!

# WAIT! If I read the task `authentik` `main.yml`:
# - name: Set postgres volume permissions
#   ansible.builtin.shell: chown -R 70:70 "{{ nomad_volumes_dir }}/authentik/postgres" && chmod 700 "{{ nomad_volumes_dir }}/authentik/postgres"
# Does Nomad `docker` driver automatically set up the volume mappings?
# If `authentik.nomad.j2` ALREADY has it, then that is NOT the issue!

# What else?!
# Let's read the Memory REALLY REALLY carefully.
# "When a Nomad group defines network { mode = "bridge" } to utilize a CNI namespace, do not specify network_mode = "bridge" inside the config blocks of individual Docker tasks within that group. Doing so forces the containers onto the default docker0 bridge, breaking Nomad's static port mappings and causing health check failures ('progress deadline' errors)."

# Was `network_mode = "bridge"` specified inside the config blocks?!
# I checked `ansible/roles/authentik/templates/authentik.nomad.j2` and it WAS NOT THERE.
# BUT wait! Look at the first python script I ran:
# `grep -rn network_mode ansible/roles/authentik/templates/authentik.nomad.j2`
# output: `16:      mode = "{{ authentik_network_mode | default('bridge') }}"`
# That's in the `network { ... }` block! Not the `config { ... }` block!

# Is there ANY other file?!
# What about `ansible/jobs/authentik.nomad` ???
# Let's run: `cat ansible/jobs/authentik.nomad`
