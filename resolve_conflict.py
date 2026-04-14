import re
with open("pipecatapp/workflow/runner.py", "r") as f:
    text = f.read()

# I know what the text looks like exactly.
text = text.replace("<<<<<<< HEAD\\n            \\n            def replace_func(match):\\n                var_name = match.group(1)\\n                return str(global_inputs.get(var_name, match.group(0)))\\n            \\n=======\\n\\n            def replace_func(match):\\n                var_name = match.group(1)\\n                return str(global_inputs.get(var_name, match.group(0)))\\n\\n>>>>>>> origin/main", "            def replace_func(match):\\n                var_name = match.group(1)\\n                return str(global_inputs.get(var_name, match.group(0)))\\n")

# Wait let me just use git merge tool or simply re-checkout the file.
