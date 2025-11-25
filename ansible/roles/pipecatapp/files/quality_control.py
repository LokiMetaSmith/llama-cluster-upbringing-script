import subprocess
import tempfile
import os
import logging
import re

class ExpectimaxAgent:
    """
    A class to analyze pylint output and determine a probabilistic quality score.
    This simulates a utility-based decision process where different code issues
    have different negative weights.
    """

    def __init__(self):
        # Define the weights for different pylint issue types.
        # Errors are heavily penalized, warnings moderately, and so on.
        self.weights = {
            'error': 25.0,
            'warning': 5.0,
            'refactor': 2.0,
            'convention': 1.0,
        }
        # A baseline "perfect" score from which we subtract penalties.
        self.base_score = 100.0
        # A decay factor for normalizing the score into a probability.
        self.decay_factor = 0.05

    def decide(self, pylint_output: str) -> float:
        """
        Analyzes pylint output to produce a probabilistic score of code quality.
        Returns a float between 0.0 (bad) and 1.0 (good).
        """
        # The easiest path: pylint gives an explicit rating.
        match = re.search(r"Your code has been rated at ([-0-9.]+)/10", pylint_output)
        if match:
            try:
                score = float(match.group(1))
                # Normalize the score from a 0-10 scale to a 0.0-1.0 scale.
                return max(0.0, score / 10.0)
            except (ValueError, IndexError):
                # Fallback to manual calculation if parsing fails.
                pass

        # Manual calculation if the rating line isn't found.
        if "No issues found" in pylint_output:
            return 1.0
        if not pylint_output or "Error" in pylint_output:
            return 0.0 # Return a very low score for execution errors.

        total_penalty = 0
        # Count each type of issue. Pylint codes are C, R, W, E.
        # We search for lines starting with these codes, followed by a colon.
        total_penalty += len(re.findall(r"^\s*E\d+:", pylint_output, re.MULTILINE)) * self.weights['error']
        total_penalty += len(re.findall(r"^\s*W\d+:", pylint_output, re.MULTILINE)) * self.weights['warning']
        total_penalty += len(re.findall(r"^\s*R\d+:", pylint_output, re.MULTILINE)) * self.weights['refactor']
        total_penalty += len(re.findall(r"^\s*C\d+:", pylint_output, re.MULTILINE)) * self.weights['convention']

        # Use an exponential decay function to map the penalty to a 0-1 score.
        # This ensures the score is always between 0 and 1 and gracefully
        # handles high penalty values.
        quality_score = 1.0 * (2.71828 ** (-self.decay_factor * total_penalty))

        return quality_score


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
            # Create a temporary file with a .py extension for pylint
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
                tmp_file.write(code)
                tmp_filepath = tmp_file.name
        except Exception as e:
            logging.error(f"Failed to create temporary file for code analysis: {e}")
            pylint_report = f"Error: Could not create a temporary file for analysis. {e}"
            return {"pylint_report": pylint_report, "quality_score": 0.0}

        try:
            # Run pylint on the temporary file
            process = subprocess.run(
                ['pylint', tmp_filepath],
                capture_output=True,
                text=True,
                check=False
            )
            stdout = process.stdout
            stderr = process.stderr

            if stderr:
                # If there's an error running pylint, report it
                pylint_report = f"Pylint execution error:\n{stderr}"
            elif not stdout.strip():
                pylint_report = "Pylint analysis complete. No issues found."
            else:
                pylint_report = stdout
        except FileNotFoundError:
            pylint_report = "Error: The 'pylint' command was not found. Please ensure it is installed."
            logging.error(pylint_report)
        except Exception as e:
            pylint_report = f"An unexpected error occurred during code analysis: {e}"
            logging.error(pylint_report)
        finally:
            # Clean up the temporary file
            if tmp_filepath and os.path.exists(tmp_filepath):
                os.remove(tmp_filepath)

        # Get the final probabilistic score from the ExpectimaxAgent
        quality_score = self.expectimax_agent.decide(pylint_report)

        return {
            "pylint_report": pylint_report,
            "quality_score": quality_score
        }
