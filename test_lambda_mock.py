import sys
import os
import tempfile
sys.path.insert(0, os.path.abspath('scripts'))
sys.path.insert(0, os.path.abspath('tests/unit'))

import conftest
from unittest.mock import patch
import provisioning
import yaml as real_yaml

test_dir = tempfile.mkdtemp()
manifest_path = os.path.join(test_dir, "test_manifest.yaml")
data = [
    {"import_playbook": "playbooks/p1.yaml", "tags": ["t1"]},
    {"import_playbook": "playbooks/p2.yaml"}
]
with open(manifest_path, 'w') as f:
    real_yaml.dump(data, f)

with patch('provisioning.yaml.safe_load', side_effect=lambda f: real_yaml.load(f, Loader=real_yaml.SafeLoader)):
    playbooks = provisioning.load_playbooks_from_manifest(manifest_path)

print(playbooks)
