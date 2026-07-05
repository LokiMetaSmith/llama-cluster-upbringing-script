import sys
import os
import re
import logging

# Ensure we can import pipecatapp
sys.path.append(os.getcwd())

from pipecatapp.skill_library import SkillLibrary

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SkillIngestion")

def ingest_all_skills(db_path="skills.sqlite"):
    lib = SkillLibrary(db_path=db_path)
    resources_dir = "pipecatapp/resources/skills"

    if not os.path.exists(resources_dir):
        logger.error(f"Resources directory not found: {resources_dir}")
        return

    skills = {
        "backpass": "backpass.md",
        "renovate": "renovate.md",
        "scaffold-setup-skill": "scaffold-setup-skill.md"
    }

    for name, filename in skills.items():
        path = os.path.join(resources_dir, filename)
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()

                # Extract description from frontmatter
                description = "Procedural skill"
                match = re.search(r'description:\s*(.*)', content)
                if match:
                    description = match.group(1).strip()

                # Adapt scaffold-setup-skill
                if name == "scaffold-setup-skill":
                    content = adapt_scaffold_setup_skill(content)

                success = lib.save_skill(name, description, content)
                if success:
                    logger.info(f"Successfully ingested skill: {name}")
                else:
                    logger.error(f"Failed to ingest skill: {name}")
        else:
            logger.warning(f"Skill file missing: {path}")

def adapt_scaffold_setup_skill(content: str) -> str:
    """Adapts the scaffold-setup-skill markdown for the pipecatapp framework."""
    # Redirect output to internal SkillLibrary via save_skill tool
    content = re.sub(
        r'Write the output to:\s*```\s*<repo-root>/.claude/skills/setup/SKILL.md\s*```',
        "Use the `save_skill` tool to persist the generated setup skill to the internal SkillLibrary with a name like `setup-[project-name]`.",
        content, flags=re.DOTALL
    )

    # Simple replacement if regex didn't match exactly due to formatting variations
    content = content.replace(
        "Write the output to:\n\n```\n<repo-root>/.claude/skills/setup/SKILL.md\n```",
        "Use the `save_skill` tool to persist the generated setup skill to the internal SkillLibrary with a name like `setup-[project-name]`."
    )

    # Update coverage check path
    content = content.replace(
        "run `scripts/coverage_check.py <repo-root> <generated-skill-path>`",
        "run `python3 pipecatapp/utils/coverage_check.py <repo-root> <generated-skill-path>`"
    )

    return content

if __name__ == "__main__":
    ingest_all_skills()
