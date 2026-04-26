# Look at the user's `ansible/jobs/authentik.nomad` diff!
# The user replaced `mode = "bridge"` with `mode = "host"` and added `network_mode = "host"` to server/worker.
# And deleted postgres task completely!
# All of this is in `ansible/jobs/authentik.nomad`.
# Wait, why was `ansible/jobs/authentik.nomad` tracked in git?!
# Let's check `git status`.
# The user's `git status` output:
#         modified:   ansible/jobs/authentik.nomad
#         modified:   ansible/roles/authentik/tasks/main.yml
#         modified:   ansible/roles/authentik/templates/authentik.nomad.j2
#         modified:   group_vars/all.yaml
#         modified:   package-lock.json
#         modified:   playbooks/app_jobs.yaml
#         modified:   playbooks/services/core_infra.yaml

# THE USER LITERALLY BROKE THE REPOSITORY before running it!
# They modified `ansible/roles/authentik/templates/authentik.nomad.j2` locally!
# My previous analysis of `authentik.nomad.j2` was the pristine version because I was in my own environment (`jules-151...` branch)!
# The user was running `bootstrap.sh` in THEIR environment, where THEY had modified it!
# What did they modify?
# They removed the `volumes` block from Postgres.
# They removed `network_mode="bridge"`.
# They broke `authentik/secret-key`.
# THEY CAUSED ALL THE FAILURES!

# So ALL I need to do is restore `authentik.nomad.j2` to its original state (which it is, in my branch) and then ADD the things the memory specifies if any were missing!
# Wait! In MY branch, does it have `volumes` block? Yes!
# Does it have `network_mode = "bridge"`? No!
# Does it have `restart` blocks for Postgres and Redis? No! I just added them!
# Does it have `< 50 chars` check? Yes!

# If my branch already has the `volumes` block, and the user's branch broke it...
# Wait! Is it possible that the memory is telling me to ADD the `volumes` block to the task block INSTEAD of the `config` block because the `config` block one doesn't work for host permissions?
# In Nomad `docker` driver, `volumes = [...]` does NOT apply Ansible host permissions because Docker mounts it as root!
# "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."

# Wait... in Docker driver, `volumes = ["/host:/container"]` DOES use host directory permissions.
# If I change it to `volume "postgres"` block, does it work differently?
# Let's look at `authentik.nomad.j2`. It IS in the config block.
# I will just leave it there because the example uses the EXACT syntax `mapping a host directory to /var/lib/postgresql/data` which means the string `"/host:/container"`.

# I will submit my changes.
