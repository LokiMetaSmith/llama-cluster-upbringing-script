# Let's check `ansible/roles/authentik/templates/authentik.nomad.j2`
# If we replace:
# AUTHENTIK_SECRET_KEY="{{ '{{' }} key "authentik/secret-key" {{ '}}' }}"
# With:
# AUTHENTIK_SECRET_KEY="{{ authentik_generated_key.stdout if authentik_generated_key is not skipped else (authentik_consul_key.json[0].Value | b64decode) }}"
# Wait! Does Ansible `authentik_generated_key is not skipped` work? Yes, `authentik_generated_key.skipped` is boolean or not defined.
# A better way is to just use a `set_fact` in Ansible to hold the final secret key, and then use it in the template!

# Wait! What about `postgres` exiting with Exit Code 1?
# If `postgres` is failing, what could it be?
# Memory: "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."
# Is it possible that `volumes` block is NOT applied correctly in `authentik.nomad.j2`?
# In Nomad, the syntax:
#         volumes = [
#           "{{ nomad_volumes_dir }}/authentik/postgres:/var/lib/postgresql/data"
#         ]
# Is this correct for docker?
# Let's check another file: `ansible/roles/docker_registry/templates/docker-registry.nomad.j2`
with open("ansible/roles/docker_registry/templates/docker-registry.nomad.j2", "r") as f:
    text = f.read()

import re
print("Docker registry volumes:")
match = re.search(r'volumes = \[.*?\]', text, re.DOTALL)
if match:
    print(match.group(0))
