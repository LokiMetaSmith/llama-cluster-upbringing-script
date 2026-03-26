import json
import urllib.request
import urllib.error
import re
import os

class UpdateLitellmTool:
    """
    Tool for fetching litellm releases and updating the Nomad job file.
    The evaluation logic is left to the LLM agent using this tool.
    """

    def __init__(self):
        self.github_api_url = "https://api.github.com/repos/BerriAI/litellm/releases"
        self.file_to_update = "ansible/jobs/router.nomad.j2"
        self._schema = {
            "type": "function",
            "function": {
                "name": "update_litellm_tool",
                "description": "Tool to fetch litellm GitHub releases or update the ansible/jobs/router.nomad.j2 file with a chosen safe tag.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["fetch_releases", "update_nomad_file"],
                            "description": "Action to perform. 'fetch_releases' gets recent tags, 'update_nomad_file' applies the chosen tag."
                        },
                        "chosen_tag": {
                            "type": "string",
                            "description": "The specific tag to update to (e.g. 'v1.82.3-stable'). Required if action is 'update_nomad_file'."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    @property
    def schema(self):
        return self._schema

    def fetch_releases(self):
        req = urllib.request.Request(self.github_api_url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                # Only return the basic info to not overwhelm context
                summarized = []
                for r in data[:30]:
                    summarized.append({
                        "tag_name": r.get("tag_name"),
                        "published_at": r.get("published_at"),
                        "name": r.get("name")
                    })
                return json.dumps(summarized)
        except urllib.error.URLError as e:
            return json.dumps({"error": str(e)})

    def update_nomad_file(self, chosen_tag):
        if not os.path.exists(self.file_to_update):
            return json.dumps({"error": f"{self.file_to_update} not found."})

        with open(self.file_to_update, 'r') as f:
            content = f.read()

        pattern = r'(image\s*=\s*"ghcr\.io/berriai/litellm):[^"]+(")'
        docker_tag = chosen_tag if chosen_tag.startswith("main-") else f"main-{chosen_tag}"
        new_content = re.sub(pattern, rf'\1:{docker_tag}\2', content)

        if new_content != content:
            with open(self.file_to_update, 'w') as f:
                f.write(new_content)
            return json.dumps({"success": True, "message": f"Updated {self.file_to_update} to use tag: {docker_tag}"})
        else:
            return json.dumps({"error": f"No changes made to {self.file_to_update}. Pattern not found or tag already set."})

    def execute(self, action, chosen_tag=None, **kwargs):
        if action == "fetch_releases":
            return self.fetch_releases()
        elif action == "update_nomad_file":
            if not chosen_tag:
                return json.dumps({"error": "chosen_tag is required for update_nomad_file action."})
            return self.update_nomad_file(chosen_tag)
        else:
            return json.dumps({"error": f"Unknown action: {action}"})
