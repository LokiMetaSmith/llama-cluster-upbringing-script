import re
with open("TODO.md", "r") as f:
    todos = f.read()
    print("ALL unchecked items in TODO.md:")
    print(re.findall(r"^[ \t]*- \[ \].*", todos, re.MULTILINE))
