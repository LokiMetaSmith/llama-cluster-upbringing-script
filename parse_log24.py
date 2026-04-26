# The memory rule says: "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition"

# Look at this:
#     task "postgresql" {
#       driver = "docker"
#       config {
#         image = "postgres:15-alpine"
#         ports = ["postgres"]
#         volumes = [
#           "{{ nomad_volumes_dir }}/authentik/postgres:/var/lib/postgresql/data"
#         ]
#       }

# What if "explicitly include the volumes block in the task definition" MEANS I need to use the `volumes` block AT THE TASK LEVEL??
# In Nomad, you can define an empty `volumes` mapping inside the task block? No.
# Wait! In Nomad `docker` driver, what if I must use the `mount` block?
# NO, it explicitly says "volumes block".
# Maybe it refers to adding a specific SELinux or AppArmor context?
# NO, it explicitly gives the example `(e.g., mapping a host directory to /var/lib/postgresql/data)`.

# I'm going to fix the `authentik_secret_key` issue first by bypassing Nomad's template.
