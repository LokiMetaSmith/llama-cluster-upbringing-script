import re
with open("ansible/roles/authentik/templates/authentik.nomad.j2", "r") as f:
    text = f.read()

print("Postgres block:")
print(re.search(r'task "postgresql" \{.*?\n    \}', text, re.DOTALL).group(0))
