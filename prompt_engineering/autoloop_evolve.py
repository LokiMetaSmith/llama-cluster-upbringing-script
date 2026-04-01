import os
import argparse
import sys
import subprocess
import shutil

try:
    from autoloop import AutoLoop
except ImportError:
    print("autoloop-ai is not installed. Please run `uv pip install autoloop-ai` or `pip install autoloop-ai`")
    sys.exit(1)

def run_pytest_metric(target_path: str) -> float:
    """
    Runs the pytest suite and returns a score based on the pass rate.
    We need this because autoloop expects a function that returns a float.
    higher_is_better = True
    """
    # For now, we will run the evaluator.py script as a subprocess since it handles our logic.
    # Alternatively, we could just run pytest and count passed/failed.
    # Let's run a simple pytest command and calculate pass percentage.
    print(f"Evaluating {target_path}...")

    # Copy target_path to where tests expect it, if needed.
    # autoloop will modify the target_path in place.
    # We will just run pytest in the tests/ directory.
    # If the tests fail entirely (syntax error), score is 0.

    # We need to run pytest and parse output
    try:
        # --tb=no: don't print tracebacks
        # -q: quiet
        result = subprocess.run(
            ["pytest", "tests/", "-q", "--tb=no"],
            capture_output=True,
            text=True
        )
        output = result.stdout

        # Parse pytest output like "3 passed, 1 failed in 0.5s"
        passed = 0
        failed = 0

        lines = output.split('\n')
        for line in reversed(lines):
            if "passed" in line or "failed" in line or "error" in line:
                parts = line.split(',')
                for part in parts:
                    if "passed" in part:
                        try:
                            passed = int(part.strip().split(' ')[0])
                        except ValueError:
                            pass
                    elif "failed" in part or "error" in part:
                        try:
                            failed += int(part.strip().split(' ')[0])
                        except ValueError:
                            pass
                break # Found the summary line

        total = passed + failed
        if total == 0:
            return 0.0 # No tests ran? Or parsing failed. Return 0.

        score = passed / total
        return score

    except Exception as e:
        print(f"Error running pytest: {e}")
        return 0.0


def main():
    parser = argparse.ArgumentParser(description="Run linear optimization with autoloop-ai.")
    parser.add_argument(
        "--target",
        type=str,
        default="ansible/roles/pipecatapp/files/app.py",
        help="Path to the file to optimize."
    )
    parser.add_argument(
        "--directives",
        type=str,
        default="prompt_engineering/PROMPT_ENGINEERING.md",
        help="Path to plain text directives/goals file."
    )
    parser.add_argument(
        "--experiments",
        type=int,
        default=5,
        help="Number of iterations to run."
    )
    parser.add_argument(
        "--agent",
        type=str,
        default="claude",
        help="Agent backend for autoloop (claude, openai, etc.)"
    )

    args = parser.parse_args()

    if not os.path.exists(args.target):
        print(f"Target file {args.target} not found.")
        sys.exit(1)

    if not os.path.exists(args.directives):
        print(f"Directives file {args.directives} not found.")
        sys.exit(1)

    print(f"Starting autoloop on {args.target} for {args.experiments} experiments...")

    loop = AutoLoop(
        target=args.target,
        metric=run_pytest_metric,
        directives=args.directives,
        budget_seconds=300,
        agent=args.agent,
        higher_is_better=True,
        results_dir="./autoloop-results",
        verbose=True
    )

    loop.run(experiments=args.experiments)

if __name__ == "__main__":
    main()