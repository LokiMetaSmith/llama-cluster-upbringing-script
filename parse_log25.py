# The task definition HAS `volumes`.
# BUT, is it possible that `volumes` is inside `config`, and Nomad 1.7.7 strictly requires the `volume` block in the `task` definition to apply Ansible permissions?
# Look at this specific wording:
# "explicitly include the volumes block in the task definition... to ensure that host volume permissions applied by Ansible take effect"
# What if it's currently NOT taking effect because Docker mounts it as `root` (or Docker daemon user) due to `volumes` in `config`?
# In Nomad, if you use the Nomad `volume` block, Nomad handles the mounting and ensures permissions.
# How do you define it?
# In the task:
#       volume_mount {
#         volume      = "postgres"
#         destination = "/var/lib/postgresql/data"
#       }
# Wait, the memory says "the volumes block" and gives the syntax `mapping a host directory to /var/lib/postgresql/data`. This syntax describes `volumes = ["...:/var/lib/postgresql/data"]`.
# So it MUST be `volumes` in `config`.

# What if `authentik_db_password` is what's failing because it defaults to `authentik_password` which might be invalid?
# No.

# WHAT IF I ALSO NEED TO ADD A `volumes` BLOCK TO `redis`?
# "like PostgreSQL (e.g., in Authentik)".
# Let's add it to Redis!
