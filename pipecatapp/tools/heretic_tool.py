import subprocess
import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class HereticTool:
    """
    A tool to modify the alignment (inhibit or disinhibit) of a language model using Heretic.
    """
    def __init__(self, root_dir: Optional[str] = None):
        self.root_dir = root_dir or os.getenv("EMPEROR_ROOT_DIR", os.getcwd())

    def align_model(self, model: str, harmful_dataset: str, harmless_dataset: str, reverse: bool = False, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Runs Heretic to adjust the inhibitions of a language model.

        Args:
            model: The Hugging Face model ID or path to the model on disk.
            harmful_dataset: Path to a dataset of prompts that tend to result in refusals.
            harmless_dataset: Path to a dataset of prompts that tend to not result in refusals.
            reverse: If True, increases inhibitions. If False, removes inhibitions (abliteration).
            output_dir: Optional directory to save the modified model. If not provided, it saves in the current directory.

        Returns:
            A dictionary containing the stdout, stderr, and returncode of the heretic command.
        """
        try:
            cmd = ["heretic", model]

            # Pass required datasets
            cmd.extend(["--harmful-dataset", harmful_dataset])
            cmd.extend(["--harmless-dataset", harmless_dataset])

            # Add reverse flag if requested
            if reverse:
                cmd.append("--reverse")

            # Determine output directory
            if output_dir:
                cmd.extend(["--save-path", output_dir])

            logger.info(f"Running Heretic: {' '.join(cmd)}")

            # Run the command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.root_dir
            )

            return {
                "command": " ".join(cmd),
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {"error": str(e)}
