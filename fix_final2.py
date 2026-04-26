with open("ansible/roles/authentik/templates/authentik.nomad.j2", "r") as f:
    text = f.read()

# Make sure to bypass Nomad's KV lookup which fails due to missing ACL token OR missing key
# Wait! If the user's `main` branch had the diff `AUTHENTIK_SECRET_KEY="dev-secret-key..."`, maybe they were working around the Template Missing error too!
# But the PROPER way according to the playbook is to use the generated key.
# Let's fix the template missing error explicitly.
text = text.replace(
    'AUTHENTIK_SECRET_KEY="{{ \'{{\' }} key "authentik/secret-key" {{ \'}}\' }}"',
    'AUTHENTIK_SECRET_KEY="{{ authentik_generated_key.stdout if authentik_generated_key.stdout is defined and authentik_generated_key.stdout != \'\' else (authentik_consul_key.json[0].Value | b64decode) }}"'
)

# And add the restart blocks for redis and postgres, as instructed by the memory!
# "When configuring Nomad tasks that depend on databases initializing within the same job group (e.g., Authentik server/worker depending on Redis/Postgres), include a restart block (e.g., mode = "delay", interval = "30s", delay = "15s") to handle startup race conditions and ensure resilience."
new_lines = []
in_redis = False
in_postgres = False

for line in text.splitlines(True):
    if 'task "redis"' in line:
        in_redis = True
    if 'task "postgresql"' in line:
        in_postgres = True

    if in_redis and 'resources {' in line:
        new_lines.append('      restart {\n')
        new_lines.append('        interval = "30s"\n')
        new_lines.append('        delay    = "15s"\n')
        new_lines.append('        mode     = "delay"\n')
        new_lines.append('      }\n\n')
        in_redis = False

    if in_postgres and 'env {' in line:
        new_lines.append('      restart {\n')
        new_lines.append('        interval = "30s"\n')
        new_lines.append('        delay    = "15s"\n')
        new_lines.append('        mode     = "delay"\n')
        new_lines.append('      }\n\n')
        in_postgres = False

    new_lines.append(line)

with open("ansible/roles/authentik/templates/authentik.nomad.j2", "w") as f:
    f.writelines(new_lines)
