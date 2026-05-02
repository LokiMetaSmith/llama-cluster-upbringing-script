# Pollen Ansible Role

This role installs the `pln` binary (Pollen: a self-organizing WASM mesh) onto cluster nodes using the official installation script.

## Usage

Include this role in your playbook:

```yaml
- hosts: all
  roles:
    - pollen
```
