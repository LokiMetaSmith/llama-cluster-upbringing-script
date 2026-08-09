with open("pipecatapp/tools/__init__.py", "r") as f:
    content = f.read()

import re
content = re.sub(r'<<<<<<< HEAD\n]\n\n=======\n    "WorkspaceTool",\n]\nfrom \.workspace_tool import WorkspaceTool\n>>>>>>> origin/main', '    "WorkspaceTool",\n]\nfrom .workspace_tool import WorkspaceTool', content)

with open("pipecatapp/tools/__init__.py", "w") as f:
    f.write(content)
