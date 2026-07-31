with open("pipecatapp/tests/test_web_server_unit.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip() == "mock_get_all_states.return_value = {":
        new_lines.extend([
            "    # Tests expect the mock to handle sanitize=True and return sanitized output\n",
            "    mock_get_all_states.return_value = {\n",
            "        \"runner1\": {\n",
            "            \"global_inputs\": {\"key\": \"sk-[REDACTED]\"},\n",
            "            \"node_outputs\": {}\n",
            "        }\n",
            "    }\n"
        ])
    elif line.strip() == "\"runner1\": {" or \
         line.strip() == "\"global_inputs\": {\"key\": \"sk-1234567890abcdef1234567890abcdef\"}," or \
         line.strip() == "\"node_outputs\": {}" or \
         (line.strip() == "}" and "node_outputs" in "".join(lines[new_lines.index(line) - 2:new_lines.index(line)])):
        pass
    else:
        new_lines.append(line)

with open("pipecatapp/tests/test_web_server_unit.py", "w") as f:
    f.writelines(new_lines)
