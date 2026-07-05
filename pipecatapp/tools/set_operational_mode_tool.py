from typing import Any, Optional
import logging
from pipecatapp.skill_library import SkillLibrary

logger = logging.getLogger("SetOperationalModeTool")

class SetOperationalModeTool:
    """
    Allows the agent to dynamically switch its operational mode by retrieving
    procedural instructions from the Skill Library and incorporating them into its context.
    """

    name = "set_operational_mode"
    description = (
        "Activates a specific operational mode (e.g., 'backpass', 'renovate') by retrieving "
        "its procedural guidelines from the Skill Library. Use this when you want to shift "
        "your execution rhythm or follow a specific multi-phase process."
    )
    input_schema = {
        "type": "object",
        "properties": {
            "mode_name": {
                "type": "string",
                "description": "The name of the operational mode/skill to activate (e.g., 'backpass')."
            }
        },
        "required": ["mode_name"]
    }

    def __init__(self, db_path="skills.sqlite"):
        self.skill_lib = SkillLibrary(db_path=db_path)

    def run(self, mode_name: str) -> str:
        try:
            skill = self.skill_lib.get_skill(mode_name)
            if not skill:
                available = self.skill_lib.search_skills("")
                names = [s['name'] for s in available]
                return f"Error: Mode '{mode_name}' not found. Available modes: {', '.join(names)}"

            content = skill['content']
            logger.info(f"Operational mode '{mode_name}' retrieved.")

            # The agent is expected to read this and append it to its system prompt or active context.
            return (
                f"MODE ACTIVATED: {mode_name}\n\n"
                "Please internalize the following procedural guidelines and follow them for the remainder of this task:\n\n"
                f"{content}\n\n"
                "You are now operating in this mode. Acknowledge and proceed with the first step of the rhythm."
            )
        except Exception as e:
            logger.error(f"Error setting operational mode: {e}")
            return f"Error activating mode '{mode_name}': {e}"
