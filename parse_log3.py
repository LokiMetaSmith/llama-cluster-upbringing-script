# If Nomad is missing the Consul token, how do other templates in the project fetch Consul keys?
import os

for root, dirs, files in os.walk('ansible'):
    for file in files:
        if file.endswith('.nomad') or file.endswith('.j2'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            if '{{ key' in content:
                print(f"File {path} uses {{ key }}")
