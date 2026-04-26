with open("ansible/roles/authentik/templates/authentik.nomad.j2", "r") as f:
    text = f.read()

# Fix the Template Missing issue by bypassing Nomad's KV lookup which fails due to missing ACL token
text = text.replace(
    'AUTHENTIK_SECRET_KEY="{{ \'{{\' }} key "authentik/secret-key" {{ \'}}\' }}"',
    'AUTHENTIK_SECRET_KEY="{{ authentik_generated_key.stdout if authentik_generated_key.stdout is defined and authentik_generated_key.stdout != \'\' else (authentik_consul_key.json[0].Value | b64decode) }}"'
)

# And add the restart blocks for redis and postgres just in case it crashes for race conditions!
import re

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
