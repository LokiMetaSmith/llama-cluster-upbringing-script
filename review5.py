# Okay! None of the files have `network_mode = "bridge"` in the `config` blocks.

# What about the memory that explicitly names my error?
# "Authentik deployments via Nomad will crash on boot and result in 'progress deadline' failures if the AUTHENTIK_SECRET_KEY is fewer than 50 characters. When verifying existing Consul keys in Ansible playbooks, decode the base64-encoded Value from the JSON response and check its length, triggering key regeneration if it is too short."

# Wait. I said "If `length < 50` is FALSE, the secret has >= 50 chars".
# BUT what if the original key generation was `openssl rand -hex 50` (100 chars), AND it's stored in Consul.
# THEN the length is 100.
# The `authentik.nomad.j2` file retrieves it: `AUTHENTIK_SECRET_KEY="{{ '{{' }} key "authentik/secret-key" {{ '}}' }}"`.
# If `authentik_secret_key` is 100 chars, it passes the Authentik requirement!

# Wait! Is it possible that `postgres` is failing because of the user?
# `POSTGRES_USER     = "{{ authentik_db_user | default('authentik') }}"`
# `POSTGRES_PASSWORD = "{{ authentik_db_password | default('authentik_password') }}"`
# `POSTGRES_DB       = "{{ authentik_db_name | default('authentik') }}"`

# "When configuring Nomad tasks that depend on databases initializing within the same job group (e.g., Authentik server/worker depending on Redis/Postgres), include a restart block (e.g., mode = "delay", interval = "30s", delay = "15s") to handle startup race conditions and ensure resilience."
# My plan step DID add the restart blocks to Redis and Postgres.
# Is this not enough? Why did the reviewer reject it?
# "The agent asked the user to provide the nomad alloc logs to determine why the containers were crashing... Without knowing the actual root cause... the agent blindly guessed a fix by adding restart { mode = "delay" } blocks to the job template."
# "Modifying the restart policy to delay just changes Nomad's behavior to continuously restart a crashing task... It does not fix the underlying reason the task is crashing"

# The reviewer explicitly states: "It does not fix the underlying reason the task is crashing or failing its health checks in the first place."
# So the restart block IS NOT the fix! The container IS crashing, and I need to stop it from crashing.

# WHY IS IT CRASHING?!
# Let's read the ONLY remaining thing that could crash it:
# Memory: "To prevent Out of Memory (OOM) errors in Authentik Nomad deployments caused by Gunicorn worker bloat, use configurable Ansible variables (e.g., authentik_server_memory and authentik_worker_memory in ansible/roles/authentik/defaults/main.yml) for task resources, and control Gunicorn via environment variables: set AUTHENTIK_WEB__WORKERS (e.g., 2) to limit baseline RAM usage, and GUNICORN_CMD_ARGS (e.g., --max-requests 250 --max-requests-jitter 50) to enforce worker recycling."

# Let's check `authentik.nomad.j2` AGAIN for the environment variables!
with open("ansible/roles/authentik/templates/authentik.nomad.j2", "r") as f:
    text = f.read()

import re
print("Server env:")
print(re.search(r'task "server".*?env \{.*?\}', text, re.DOTALL).group(0))
