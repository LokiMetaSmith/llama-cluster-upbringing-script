with open("ansible/roles/authentik/templates/authentik.nomad.j2", "r") as f:
    for line in f.read().splitlines():
        if 'key ' in line:
            print(line)
