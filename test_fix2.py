with open("ansible/roles/authentik/templates/authentik.nomad.j2", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'AUTHENTIK_SECRET_KEY="{{' in line and 'key "authentik/secret-key"' in line:
        new_lines.append('AUTHENTIK_SECRET_KEY="{{ authentik_generated_key.stdout | default(authentik_consul_key.json[0].Value | default(\'\') | b64decode) }}"\n')
    else:
        new_lines.append(line)

with open("ansible/roles/authentik/templates/authentik.nomad.j2", "w") as f:
    f.writelines(new_lines)
