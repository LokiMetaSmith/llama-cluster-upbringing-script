# Okay, 15432 is not used anywhere else in `group_vars/all.yaml`.

# Wait! Look at the Postgres memory rule ONE MORE TIME!
# "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."

# What if this memory rule means that previously the `volumes` block was MISSING in the base template, but I ALREADY added it or it was added?
# Wait! Let me check `git log -p ansible/roles/authentik/templates/authentik.nomad.j2`
