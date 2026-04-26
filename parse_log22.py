# Okay!
# `authentik_password` is NOT in `defaults/main.yml`.
# Is it in `group_vars/all.yaml`?
# I searched `group_vars/all.yaml` earlier for `authentik_db_password` and found nothing.
# Let's search for `authentik_password`.
import os

with open("group_vars/all.yaml", "r") as f:
    if "authentik_password" in f.read():
        print("authentik_password found in group_vars")
    else:
        print("authentik_password NOT found in group_vars")
