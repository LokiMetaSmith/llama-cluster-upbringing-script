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
