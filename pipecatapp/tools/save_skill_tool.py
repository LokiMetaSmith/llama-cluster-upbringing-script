from typing import Any
import logging
from pipecatapp.skill_library import SkillLibrary

logger = logging.getLogger("SaveSkillTool")

class SaveSkillTool:
    """Saves a successfully executed approach or snippet as a skill in the Skill Library."""

    name = "save_skill"
    description = "Saves a reusable skill, approach, or code snippet into the persistent Skill Library. Use this tool if you successfully completed a novel task and believe the steps or logic would be useful for future tasks."
    input_schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "A short, unique, descriptive name for the skill (e.g., 'deploy_nginx_docker_compose')."
            },
            "description": {
                "type": "string",
                "description": "A brief summary of what this skill does and when to use it."
            },
            "content": {
                "type": "string",
                "description": "The detailed steps, code snippet, configuration, or approach."
            }
        },
        "required": ["name", "description", "content"]
    }

    def __init__(self, db_path="skills.sqlite"):
        self.skill_lib = SkillLibrary(db_path=db_path)

    def run(self, name: str, description: str, content: str) -> Any:
        try:
            success = self.skill_lib.save_skill(name, description, content)
            if success:
                logger.info(f"Skill '{name}' saved successfully.")
                return f"Successfully saved skill '{name}' to the Skill Library."
            else:
                return f"Failed to save skill '{name}' due to a database error."
        except Exception as e:
            logger.error(f"Error saving skill: {e}")
            return f"Error saving skill '{name}': {e}"
