# The user's `postgres` task is failing with Exit Code 1.
# It restarts multiple times, fails, and then kills the whole allocation.
# Why would `postgres:15-alpine` fail with Exit Code 1?
# It happens when the data directory `/var/lib/postgresql/data` is not empty but lacks the correct files, OR when permissions are wrong.
# The Ansible role creates the directory:
# - name: Create Authentik postgres directory
#   ansible.builtin.file:
#     path: "{{ nomad_volumes_dir }}/authentik/postgres"
#     state: directory
#     mode: '0700'
#     owner: "70"
#     group: "70"
#   become: yes
# And sets permissions:
# - name: Set postgres volume permissions
#   ansible.builtin.shell: chown -R 70:70 "{{ nomad_volumes_dir }}/authentik/postgres" && chmod 700 "{{ nomad_volumes_dir }}/authentik/postgres"
#   become: yes
#   changed_when: false

# This is absolutely correct. 70:70 is postgres in alpine.

# Wait, what if the error is `Template Missing: kv.block(authentik/secret-key)`?
# If the task fails due to `Template Missing`, the Nomad client doesn't even attempt to start the Docker container!
# The log says:
# Task "server" is "dead"
# 2026-04-26T00:04:17Z  Template             Missing: kv.block(authentik/secret-key)
# 2026-04-26T00:04:13Z  Task Setup           Building Task Directory
# 2026-04-26T00:04:13Z  Received             Task received by client
# It stays in `Template` phase until `postgres` fails and kills the sibling tasks!

# Wait! If `postgres` didn't fail, `server` and `worker` would STILL be stuck in `Template Missing`!
# Because the template is missing!
# Why is it missing?
# What if the generated key was NEVER published because of the bug in `ansible/roles/authentik/tasks/main.yml`?!
# Look at the user's Ansible output!
# TASK [authentik : Check if Authentik secret key exists in Consul] -> ok: [localhost]
# TASK [authentik : Generate Authentik secret key] -> skipping: [localhost]
# TASK [authentik : Publish Authentik secret key to Consul] -> skipping: [localhost]
# What if it's hitting a DIFFERENT Consul instance?!
# The Ansible task hits `http://{{ cluster_ip | default('127.0.0.1') }}:8500`.
# If `cluster_ip` is `100.64.0.1`, it hits `http://100.64.0.1:8500`.
# And Nomad queries the local Consul agent on `127.0.0.1:8500`.
# Since Consul is a clustered database, they should be identical.

# BUT what if the key IS in Consul, but Nomad cannot access it due to ACLs?
# As we saw earlier, Nomad's client HAS a Consul token!
# But what if the Nomad client token doesn't have permission to read `authentik/secret-key`?
# In `ansible/roles/nomad/templates/client.hcl.j2`:
#   consul {
#     token = "{{ nomad_consul_token }}"
#   }
# `nomad_consul_token` is generated in the `nomad` role. Does it have read access? Yes, it's usually an agent token.
# BUT wait! Does Nomad need a VAULT token or something?
# No, it's a Consul key.

# What if the key in Consul was created manually by the user, and its value is literally an empty string?
# If the value is an empty string, `length` is 0.
# Then `length < 50` is TRUE.
# Then it SHOULD trigger the "Generate Authentik secret key" task!
# BUT it skipped! So the value MUST be >= 50 characters!

# Wait... what if the `authentik_consul_key.json` doesn't exist?
# If `status` is 200, Consul KV `/v1/kv/key` ALWAYS returns a JSON array: `[{"LockIndex":0,"Key":"authentik/secret-key","Flags":0,"Value":"...","CreateIndex":...,"ModifyIndex":...}]`.

# I am completely stumped. The reviewer said: "Without knowing the actual root cause (e.g., misconfigured database credentials, missing volumes, port conflicts, or application crashes), the agent blindly guessed a fix by adding restart { mode = "delay" } blocks to the job template."
# THIS MEANS I MUST FIND THE ROOT CAUSE AND FIX IT.
# The user's latest output is the Nomad alloc logs! I FINALLY have the actual root cause!
# Root Cause 1: `postgres` task is crashing (Exit Code 1).
# Root Cause 2: `server` and `worker` tasks have `Template Missing: kv.block(authentik/secret-key)`.

# Is there any OTHER memory rule?
# Let's search the AGENTS.md or other memories.
import os

if os.path.exists("AGENTS.md"):
    with open("AGENTS.md", "r") as f:
        print(f.read())
