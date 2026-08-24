import re
with open("TODO.md", "r") as f:
    todos = f.read()
    print("Unchecked TODOs in TODO.md:")
    print(re.findall(r"^- \[ \] .*", todos, re.MULTILINE))

with open("pipecatapp/TODO.md", "r") as f:
    todos = f.read()
    print("Unchecked TODOs in pipecatapp/TODO.md:")
    print(re.findall(r"^- \[ \] .*", todos, re.MULTILINE))

with open("modules/keystone-polyphony/TODO.md", "r") as f:
    todos = f.read()
    print("Unchecked TODOs in modules/keystone-polyphony/TODO.md:")
    print(re.findall(r"^- \[ \] .*", todos, re.MULTILINE))
