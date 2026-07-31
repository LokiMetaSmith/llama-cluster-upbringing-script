with open("pipecatapp/tests/test_web_server_unit.py", "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if line.startswith("def test_health_check_init():"):
        new_lines.extend([
            "import pipecatapp.api_keys as api_keys\n",
            "api_keys.API_KEYS = set([api_keys.get_api_key_hash(\"dev_key_123\")])\n",
            "\n"
        ])
    if 'client.get("/api/cluster/metrics")' in line:
        line = line.replace('client.get("/api/cluster/metrics")', 'client.get("/api/cluster/metrics", headers={"Authorization": "Bearer dev_key_123"})')
    if 'client.get("/api/workflows/active")' in line:
        line = line.replace('client.get("/api/workflows/active")', 'client.get("/api/workflows/active", headers={"Authorization": "Bearer dev_key_123"})')

    new_lines.append(line)

with open("pipecatapp/tests/test_web_server_unit.py", "w") as f:
    f.writelines(new_lines)
