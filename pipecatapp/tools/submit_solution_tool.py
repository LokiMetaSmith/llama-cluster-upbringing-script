import json
import logging

class SubmitSolutionTool:
    """
    A tool that allows a Worker Agent to submit a code solution or artifact.
    This does not write to the file system directly but formats the output
    so it can be parsed by the ExperimentTool/Judge.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def run(self, content: str, file_path: str = "solution.py", description: str = "") -> str:
        """
        Submits a solution artifact.

        Args:
            content (str): The code or text content of the solution.
            file_path (str): The intended file path for this content (e.g., 'src/app.py').
            description (str): A brief description of the changes.

        Returns:
            str: A formatted JSON string representing the artifact.
        """
        self.logger.info(f"Structuring solution artifact for {file_path}")

        artifact = {
            "type": "solution_artifact",
            "file_path": file_path,
            "content": content,
            "description": description
        }

        # We wrap it in a distinctive block or just return JSON.
        # Returning JSON is safest for programmatic parsing by ExperimentTool.
        return json.dumps(artifact)
