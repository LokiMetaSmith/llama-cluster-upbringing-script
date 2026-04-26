# Okay! `authentik.nomad.j2` is the ONLY file that uses `key`!
# And it fails with `Missing: kv.block(authentik/secret-key)`!
# WHY does it fail?
# Because Nomad's `template` block cannot read `authentik/secret-key` from Consul!
# Why?
# 1. Consul ACLs block access because Nomad has no token.
# 2. The key DOES NOT exist.

# Wait, `ansible/roles/authentik/tasks/main.yml`:
# - name: Check if Authentik secret key exists in Consul
#   ansible.builtin.uri:
#     url: "http://{{ cluster_ip | default('127.0.0.1') }}:{{ consul_http_port | default(8500) }}/v1/kv/authentik/secret-key"
#     method: GET
#     headers:
#       X-Consul-Token: "{{ consul_bootstrap_token | default(omit) }}"
#     status_code: [200, 404]
#   register: authentik_consul_key
#   ignore_errors: yes
#
# - name: Generate Authentik secret key
#   ...
#   when: >
#     authentik_consul_key is not failed and
#     (authentik_consul_key.status == 404 or
#     (authentik_consul_key.status == 200 and authentik_consul_key.json[0].Value | default('') | b64decode | length < 50))
#
# If `authentik_consul_key` IS 404 (doesn't exist), then the "Generate Authentik secret key" task should run!
# BUT IN THE USER LOG, IT SKIPPED!
# Why did it skip if it's 404?!
# It only skips if `authentik_consul_key.status` != 404 AND `authentik_consul_key.status` != 200 (wait, if it's != 200, it's failed, but we ignore_errors).
# Wait! If `ignore_errors: yes` is used, and the connection FAILS entirely (e.g. Connection Refused), then `authentik_consul_key` is marked as `failed`!
# If it is `failed`, then `authentik_consul_key is not failed` is FALSE!
# So the "Generate" task SKIPS!
# And the "Publish" task SKIPS!
# Then we deploy the Nomad job, and Nomad CANNOT FIND THE KEY (because it was never generated, since the connection to Consul failed!).
# WHY would the connection to Consul fail?
# Because `consul` is running locally with a different port or IP?
# `cluster_ip` is `100.64.0.1`. Is Consul listening on `100.64.0.1:8500`?
# Maybe.

# Wait! Is there ANOTHER explanation for why `authentik` Nomad deployment is failing?
# Look at Postgres: `Exit Code: 1, Exit Message: "Docker container exited with non-zero exit code: 1"`
# AND `server`: `Template Missing: kv.block(authentik/secret-key)`

# Look at this memory:
# "Authentik deployments via Nomad will crash on boot and result in 'progress deadline' failures if the AUTHENTIK_SECRET_KEY is fewer than 50 characters. When verifying existing Consul keys in Ansible playbooks, decode the base64-encoded Value from the JSON response and check its length, triggering key regeneration if it is too short."
# This IS exactly what the patch attempted to do, BUT I might have written the logic WRONG.
# Let's check `patch_authentik.diff`:
#  when: >
#    authentik_consul_key is not failed and
#    (authentik_consul_key.status == 404 or
#    (authentik_consul_key.status == 200 and authentik_consul_key.json[0].Value | default('') | b64decode | length < 50))

# Wait, `authentik_consul_key.json[0].Value | default('') | b64decode | length < 50`
# If the key exists, but the value is empty, `b64decode` might fail?
# If `length` is checked on a string.
# What if it threw a Jinja2 error and skipped?!
# If a Jinja2 expression fails in a `when` clause, Ansible will FAIL the task, not skip it! Unless there's a rescue or error handling, it fails.
# So it evaluated successfully to FALSE.

# So the key IS >= 50 characters, OR `authentik_consul_key is not failed` is FALSE (meaning the API call failed).
# Let's ask the user to fetch the logs for Postgres!
