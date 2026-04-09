from typing import Any

class DynamicSkillTool:
    """
    A wrapper tool that executes a dynamically loaded markdown skill.
    This acts as a bridge for skills retrieved from MemoryStore.
    """

    def __init__(self, name: str, description: str, content: str, code_runner: Any = None):
        """
        Args:
            name: The name of the skill.
            description: The description.
            content: The raw markdown content.
            code_runner: An instance of CodeRunnerTool to execute python snippets.
        """
        self.name = name
        self.description = description
        self.content = content
        self.code_runner = code_runner

    def execute(self, params: str) -> str:
        """
        Executes the skill.
        For now, this attempts to extract python code blocks from the markdown
        and runs them via the code_runner.

        Args:
            params: Parameters passed by the agent (JSON string).
        """
        if not self.code_runner:
            return "Error: No CodeRunnerTool provided to execute dynamic skill."

        import re
        # Find Python blocks in the markdown content
        code_blocks = re.findall(r'```python\n(.*?)\n```', self.content, re.DOTALL)

        if not code_blocks:
            return f"Skill '{self.name}' executed in knowledge mode (no python blocks found). Content:\n{self.content}"

        # Execute the first code block found
        # Pass params as an environment variable or wrapper?
        # For simplicity, we just inject the params as a dict in the code.
        script = f"PARAMS = {params}\n" + code_blocks[0]

        try:
            # We assume code_runner has an execute method that takes code=...
            result = self.code_runner.execute(language="python", code=script)
            return result
        except Exception as e:
            return f"Execution of skill '{self.name}' failed: {e}"
