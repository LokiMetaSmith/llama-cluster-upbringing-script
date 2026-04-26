import re

with open("ansible/roles/authentik/templates/authentik.nomad.j2", "r") as f:
    text = f.read()

# Replace Nomad template fetch with Ansible template render
text = re.sub(r'AUTHENTIK_SECRET_KEY="\{\{ \'\{\{\' \}\} key "authentik/secret-key" \{\{ '\}\}' \}\}"',
              r'AUTHENTIK_SECRET_KEY="{{ authentik_generated_key.stdout | default(authentik_consul_key.json[0].Value | default("") | b64decode) }}"', text)

with open("ansible/roles/authentik/templates/authentik.nomad.j2", "w") as f:
    f.write(text)
