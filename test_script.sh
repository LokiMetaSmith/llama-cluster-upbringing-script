#!/bin/bash
export ANSIBLE_CONFIG="$(pwd)/ansible.cfg"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ansible-playbook -i local_inventory.ini playbooks/services/nomad_client.yaml
