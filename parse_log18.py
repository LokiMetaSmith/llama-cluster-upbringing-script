# AHA!
# `ansible/jobs/authentik.nomad` DOES NOT HAVE `task "postgresql"` AT ALL!!!
# Let's check `cat ansible/jobs/authentik.nomad`!
with open("ansible/jobs/authentik.nomad", "r") as f:
    text = f.read()
if 'task "postgresql"' in text:
    print("It HAS task postgresql")
else:
    print("It DOES NOT HAVE task postgresql")
