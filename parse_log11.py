# If `authentik_consul_key.status == 404`, it should NOT skip!
# But the user's log says "skipping".
# If it is skipping, `status` is NOT 404.
# And if the key doesn't exist, how could `status` be 200?!
# Answer: The Consul API `/v1/kv/authentik/secret-key` returns 404 if the key is missing.
# If `status` is 200, the key EXACTLY `authentik/secret-key` exists.
# If the key exists, WHY is Nomad saying `Missing: kv.block(authentik/secret-key)`?
# Because Nomad's `template` block evaluates BEFORE the task starts.
# Does Nomad have the Consul token?
# In `ansible/roles/nomad/templates/client.hcl.j2` or `server.hcl.j2`, does it have `consul { token = ... }`?
import os

with open("ansible/roles/nomad/templates/client.hcl.j2", "r") as f:
    if "consul {" in f.read():
        print("Consul block in Nomad client")

with open("ansible/roles/nomad/templates/server.hcl.j2", "r") as f:
    if "token" in f.read():
        print("Token in Nomad server")
