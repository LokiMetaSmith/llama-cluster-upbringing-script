import re

with open("pipecatapp/tools/autoloop_tool.py", "r") as f:
    content = f.read()

replacement = """        if os.getenv("AUTOLOOP_ALLOW_UNSANDBOXED", "false").lower() != "true":
            return json.dumps({"error": "AutoloopTool is currently restricted due to running unsandboxed. Set AUTOLOOP_ALLOW_UNSANDBOXED=true in your environment to override if you are in a trusted, airgapped environment."})

        try:"""

content = re.sub(r"        try:\n            from autoloop import AutoLoop", replacement + "\n            from autoloop import AutoLoop", content)

with open("pipecatapp/tools/autoloop_tool.py", "w") as f:
    f.write(content)
