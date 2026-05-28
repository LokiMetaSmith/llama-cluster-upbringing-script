import os
import logging

logger = logging.getLogger(__name__)

class ProjectOverviewTool:
    """
    A tool to quickly give an agent a project overview by reading README.md, AGENTS.md,
    and listing the root directory structure.
    """
    def __init__(self):
        self.name = "project_overview"
        self.description = "Provides a high-level project overview by returning the contents of key documentation files (like README.md and AGENTS.md) along with the root directory structure. Takes no arguments."

    def execute(self, arguments: dict = None) -> str:
        """
        Executes the tool.

        Args:
            arguments (dict, optional): Arguments for the tool (ignored).

        Returns:
            str: The project overview.
        """
        try:
            overview_parts = []

            # Find the root directory. Assuming this file is in pipecatapp/tools/
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

            # 1. List Root Directory
            overview_parts.append("=== Project Root Directory Structure ===")
            try:
                root_files = os.listdir(root_dir)
                root_files.sort()
                overview_parts.append("\n".join([f"- {f}" for f in root_files]))
            except Exception as e:
                overview_parts.append(f"Error listing root directory: {str(e)}")

            # 2. Read AGENTS.md
            agents_md_path = os.path.join(root_dir, "AGENTS.md")
            overview_parts.append("\n=== AGENTS.md ===")
            if os.path.exists(agents_md_path):
                with open(agents_md_path, 'r', encoding='utf-8') as f:
                    overview_parts.append(f.read())
            else:
                overview_parts.append("AGENTS.md not found.")

            # 3. Read README.md
            readme_md_path = os.path.join(root_dir, "README.md")
            overview_parts.append("\n=== README.md ===")
            if os.path.exists(readme_md_path):
                with open(readme_md_path, 'r', encoding='utf-8') as f:
                    overview_parts.append(f.read())
            else:
                overview_parts.append("README.md not found.")

            return "\n".join(overview_parts)

        except Exception as e:
            error_msg = f"Error generating project overview: {str(e)}"
            logger.error(error_msg)
            return error_msg
