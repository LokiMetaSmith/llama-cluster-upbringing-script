with open("pipecatapp/tests/test_web_server_unit.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith("import pipecatapp.api_keys as api_keys") or line.startswith("api_keys.API_KEYS = set"):
        pass
    elif line.startswith("def test_health_check_init():"):
        new_lines.extend([
            "from pipecatapp.web_server import get_api_key\n",
            "app.dependency_overrides[get_api_key] = lambda: \"dev_key_123\"\n",
            "\n",
            "def test_health_check_init():\n"
        ])
    else:
        new_lines.append(line)

with open("pipecatapp/tests/test_web_server_unit.py", "w") as f:
    f.writelines(new_lines)
