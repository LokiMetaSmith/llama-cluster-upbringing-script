import json
from typing import Any, Optional
from pipecatapp.memory import MemoryStore

class SkillBuilderTool:
    """
    A tool for dynamically creating, updating, and managing markdown-based skills.
    Agents can use this tool to evolve their own capabilities through reflective learning.
    """

    def __init__(self, memory_store: Optional[MemoryStore] = None):
        if memory_store:
            self.memory_store = memory_store
        else:
            self.memory_store = MemoryStore()


    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "skillbuildertool"),
                "description": getattr(self, "description", "Tool SkillBuilderTool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform. Available: "
                        },
                        "kwargs": {
                            "type": "object",
                            "description": "Additional arguments for the action."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def execute(self, action: str, **kwargs):
        if False:
            pass
        else:
            return f"Unknown action: {action}"

    def execute(self, action: str, **kwargs: Any) -> str:
        """
        Executes a skill building action.

        Args:
            action: The action to perform ("create", "update", "read", "list", "delete").
            kwargs: Parameters for the action (name, description, content).
        """
        try:
            if action == "create" or action == "update":
                name = kwargs.get("name")
                description = kwargs.get("description")
                content = kwargs.get("content")

                if not name or not description or not content:
                    return "Error: 'name', 'description', and 'content' parameters are required."

                self.memory_store.save_skill(name, description, content)
                return f"Skill '{name}' successfully {'created' if action == 'create' else 'updated'}."

            elif action == "read":
                name = kwargs.get("name")
                if not name:
                    return "Error: 'name' parameter is required."

                skill = self.memory_store.get_skill(name)
                if skill:
                    return json.dumps(skill, indent=2)
                return f"Skill '{name}' not found."

            elif action == "scaffold_governed_skill":
                name = kwargs.get("name")
                description = kwargs.get("description")
                intent = kwargs.get("intent", "Operational prompt directives and execution rules.")
                evidence = kwargs.get("evidence", "Test execution logs and verification assertions required.")

                if not name or not description:
                    return "Error: 'name' and 'description' parameters are required for scaffold_governed_skill."

                skill_md = f"# Skill: {name}\n\n## Description\n{description}\n\n## Directives\n- Execute tasks under strict evidence criteria.\n"
                spec_md = f"# Spec: {name}\n\n## Intent\n{intent}\n\n## Scope & Limitations\n- Enforce evidence verification prior to step completion.\n"
                eval_md = f"# Eval: {name}\n\n## Quality Criteria\n- Zero prompt injection vulnerabilities.\n- Verification output logged to EVIDENCE.md.\n\n## Evidence Requirements\n{evidence}\n"

                self.memory_store.save_skill(f"{name}/SKILL", f"{description} (SKILL.md)", skill_md)
                self.memory_store.save_skill(f"{name}/SPEC", f"{description} (SPEC.md)", spec_md)
                self.memory_store.save_skill(f"{name}/EVAL", f"{description} (EVAL.md)", eval_md)

                return f"Governed skill package '{name}' successfully scaffolded with SKILL.md, SPEC.md, and EVAL.md."

            elif action == "list":
                skills = self.memory_store.list_skills()
                return json.dumps(skills, indent=2)

            elif action == "delete":
                name = kwargs.get("name")
                if not name:
                    return "Error: 'name' parameter is required."

                success = self.memory_store.delete_skill(name)
                if success:
                    return f"Skill '{name}' deleted successfully."
                return f"Skill '{name}' not found."

            else:
                return f"Error: Unknown action '{action}'. Valid actions are: create, update, read, list, delete."

        except Exception as e:
            return f"Error executing SkillBuilderTool: {str(e)}"
