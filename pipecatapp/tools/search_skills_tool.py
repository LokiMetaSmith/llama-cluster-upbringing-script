from typing import Any
import logging
from pipecatapp.skill_library import SkillLibrary

logger = logging.getLogger("SearchSkillsTool")

class SearchSkillsTool:
    """Searches the persistent Skill Library for previously saved approaches, snippets, or code."""

    name = "search_skills"
    description = "Searches the persistent Skill Library for reusable approaches or code snippets. Call this when you need guidance on how to accomplish a specific technical task that might have been solved previously."
    input_schema = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Keywords related to the problem you are trying to solve (e.g., 'docker compose nginx')."
            }
        },
        "required": ["query"]
    }

    def __init__(self, db_path="skills.sqlite"):
        self.skill_lib = SkillLibrary(db_path=db_path)

    def run(self, query: str) -> Any:
        try:
            results = self.skill_lib.search_skills(query)
            if not results:
                return f"No skills found matching '{query}'."

            output = f"Found {len(results)} skill(s) matching '{query}':\n\n"
            for skill in results:
                output += f"--- Skill: {skill['name']} ---\n"
                output += f"Description: {skill['description']}\n"
                output += f"Content:\n{skill['content']}\n\n"

            return output
        except Exception as e:
            logger.error(f"Error searching skills: {e}")
            return f"Error searching skills for query '{query}': {e}"
