import re
with open("TODO.md", "r") as f:
    todos = f.read()
    print("Tasks without checkbox:")
    print(re.findall(r"^[ \t]*- (?!\[[ x]\]).*", todos, re.MULTILINE)[:20])
