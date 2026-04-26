# Wait! Let's address the Postgres crash.
# "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."

# Is it possible that `volumes` mapping works, BUT PostgreSQL 15 needs `PGDATA` to be set to a specific directory?
# In PostgreSQL, `PGDATA` defaults to `/var/lib/postgresql/data`.
# But in Alpine images, the data is sometimes placed in `/var/lib/postgresql/data/pgdata`.
# Wait, if we mount a host directory directly to `/var/lib/postgresql/data`, PostgreSQL init scripts see that the directory is NOT empty (because Docker creates it or it has `lost+found` or different permissions), and then fails!
# Actually, the fix for this is setting `PGDATA=/var/lib/postgresql/data/pgdata`!
# Let me look closely at the memory rule again.
# "explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."

# Is the memory explicitly saying I MUST have `volumes = ["{{ nomad_volumes_dir }}/authentik/postgres:/var/lib/postgresql/data"]` ?
# And it IS there.
# If it is there, why does it crash with Exit Code 1?
# Let's check `authentik.nomad.j2`.
with open("ansible/roles/authentik/templates/authentik.nomad.j2", "r") as f:
    text = f.read()

import re
print(re.search(r'task "postgresql" \{.*?\n    \}', text, re.DOTALL).group(0))
