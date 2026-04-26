import re
with open("ansible/roles/authentik/templates/authentik.nomad.j2", "r") as f:
    text = f.read()

server_task = re.search(r'task "server" \{.*?\n    \}', text, re.DOTALL).group(0)
print(server_task)
