with open('ansible/roles/docker_registry/templates/docker-registry.nomad.j2', 'r') as f:
    text = f.read()
for line in text.split('\n'):
    if 'volumes' in line:
        print(line)
