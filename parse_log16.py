# Okay!
# I have found TWO issues from the Nomad logs:
# 1. `postgres` fails with Exit Code 1.
# 2. `server` fails with Template Missing: kv.block(authentik/secret-key).

# Wait! Does Nomad 1.7 require the `consul_token` inside the `template` block?
# NO. Nomad agents are configured with a Consul token.

# WHAT IF the `ansible` playbook creates the Consul key in the wrong datacenter or with the wrong path?
# URL: "http://{{ cluster_ip | default('127.0.0.1') }}:{{ consul_http_port | default(8500) }}/v1/kv/authentik/secret-key"
# This creates a key at `authentik/secret-key`.
# Nomad: `key "authentik/secret-key"`
# This matches perfectly!

# What if the `postgres` memory rule literally means:
# "When defining Nomad job templates for stateful services like PostgreSQL (e.g., in Authentik), explicitly include the volumes block in the task definition (e.g., mapping a host directory to /var/lib/postgresql/data) to ensure that host volume permissions applied by Ansible take effect and to prevent initialization failures such as Nomad 'progress deadline' timeouts."
# Wait, look closely: "explicitly include the volumes block in the task definition".
# If it is inside `config`, it is NOT in the "task definition" level in the context of Nomad 1.x syntax!
# In Nomad 1.x, the proper way to define a host volume is at the group level and `volume_mount` at the task level.
# BUT the memory specifically uses the syntax `volumes` AND says `mapping a host directory`. That implies it MUST be `volumes = [...]` in `config`.

# What if the Ansible playbook doesn't properly create the postgres directory?!
# In `ansible/roles/authentik/tasks/main.yml`:
# - name: Create Authentik postgres directory
#   ansible.builtin.file:
#     path: "{{ nomad_volumes_dir }}/authentik/postgres"
#     state: directory
#     mode: '0700'
#     owner: "70"
#     group: "70"
#   become: yes
# This looks perfect.

# What if `authentik.nomad.j2` has `volumes` mapped as `read_only` by mistake? No, it's just `"/host:/container"`.

# Wait! `Template Missing: kv.block(authentik/secret-key)`
# "Authentik deployments via Nomad will crash on boot and result in 'progress deadline' failures if the AUTHENTIK_SECRET_KEY is fewer than 50 characters."
# Is it possible that the key is actually less than 50 characters?
# No, `openssl rand -hex 50` creates a 100 character key.

# WHY does Nomad say the key is missing?!
# Because Nomad's `template` evaluates BEFORE the task runs!
# Is there a task dependency order?!
# Nomad jobs start all tasks concurrently unless `lifecycle` is used.
# Could the Ansible task that sets the Consul key be failing silently, but Nomad tries to read it?
# In the Ansible run:
# TASK [authentik : Check if Authentik secret key exists in Consul] -> ok
# TASK [authentik : Generate Authentik secret key] -> skipping
# TASK [authentik : Publish Authentik secret key to Consul] -> skipping
# This implies the key ALREADY EXISTS in Consul!
# IF IT EXISTS IN CONSUL, why is Nomad saying `Missing: kv.block`?!
# Maybe because Nomad is hitting a different Consul cluster/namespace/ACL!
# If it is ACL, then how does Nomad authenticate to Consul?
# Through its local agent token.
# Does the local agent token have permission to read `authentik/secret-key`?
# In Consul, tokens are assigned policies.
# If the policy doesn't allow reading `authentik/secret-key`, Nomad returns 404 Not Found to the template engine.
# And the template engine reports `Missing: kv.block(authentik/secret-key)`!
