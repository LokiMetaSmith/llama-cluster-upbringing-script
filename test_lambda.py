import yaml as real_yaml
import os
import tempfile

test_dir = tempfile.mkdtemp()
manifest_path = os.path.join(test_dir, "test_manifest.yaml")
data = [
    {"import_playbook": "playbooks/p1.yaml", "tags": ["t1"]},
    {"import_playbook": "playbooks/p2.yaml"}
]

with open(manifest_path, 'w') as f:
    real_yaml.dump(data, f)

with open(manifest_path, 'r') as f:
    result = real_yaml.load(f, Loader=real_yaml.SafeLoader)
    print("Result:", result)
    print("Type:", type(result))
    print("Is list:", isinstance(result, list))
    print("Len:", len(result) if isinstance(result, list) else 0)
