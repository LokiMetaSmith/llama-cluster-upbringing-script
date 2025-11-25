import subprocess
import tempfile
import os
import logging

class ExpectimaxAgent:
    def __init__(self):
        pass

    def decide(self, pylint_output: str) -> float:
        """
        Analyzes pylint output to produce a probabilistic score of code quality.
        Returns a float between 0.0 (bad) and 1.0 (good).
        """
        if "No issues found" in pylint_output:
            return 1.0
        elif "error" in pylint_output.lower():
            return 0.1
        elif "warning" in pylint_output.lower():
            return 0.5
        else:
            return 0.8

class CodeQualityAnalyzer:
    def __init__(self):
        self.expectimax_agent = ExpectimaxAgent()

    def analyze(self, code: str) -> dict:
        """
        Analyzes the quality of the given Python code using pylint.
        Returns a dictionary containing the pylint report and a quality score.
        """
        if not code or not isinstance(code, str) or code.isspace():
            return {"pylint_report": "No code provided to analyze.", "quality_score": 0.0}

        tmp_filepath = None
        pylint_report = ""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
                tmp_file.write(code)
                tmp_filepath = tmp_file.name
        except Exception as e:
            logging.error(f"Failed to create temporary file for code analysis: {e}")
            pylint_report = f"Error: Could not create a temporary file for analysis. {e}"
            return {"pylint_report": pylint_report, "quality_score": 0.0}

        try:
            process = subprocess.run(
                ['pylint', tmp_filepath],
                capture_output=True,
                text=True,
                check=False
            )
            stdout = process.stdout
            stderr = process.stderr

            if stderr:
                pylint_report = f"Pylint execution error:\n{stderr}"
            elif not stdout.strip():
                pylint_report = "Pylint analysis complete. No issues found."
            else:
                pylint_report = stdout
        except FileNotFoundError:
            pylint_report = "Error: The 'pylint' command was not found."
            logging.error(pylint_report)
        except Exception as e:
            pylint_report = f"An unexpected error occurred during code analysis: {e}"
            logging.error(pylint_report)
        finally:
            if tmp_filepath and os.path.exists(tmp_filepath):
                os.remove(tmp_filepath)

        quality_score = self.expectimax_agent.decide(pylint_report)

        return {
            "pylint_report": pylint_report,
            "quality_score": quality_score
        }
