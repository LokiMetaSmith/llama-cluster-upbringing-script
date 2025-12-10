import os
import sys
import argparse
import logging
import asyncio
import subprocess
from challenger import Challenger

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_solver(test_case_path: str):
    """
    Runs the existing `evolve.py` script (the Solver) targeting the specific test case.
    """
    evolve_script = os.path.join(os.path.dirname(__file__), "evolve.py")

    cmd = [
        sys.executable,
        evolve_script,
        "--test-case", test_case_path,
        "--selection-method", "weighted",
        # We can add more args if needed
    ]

    logging.info(f"Starting Solver (evolve.py) targeting: {test_case_path}")
    try:
        # We run it as a subprocess to keep the environment clean and capture output
        result = subprocess.run(cmd, capture_output=True, text=True)

        logging.info("Solver finished.")
        if result.returncode == 0:
            logging.info("Solver execution successful (script ran without error).")
            # Note: The script success doesn't mean the agent passed the test,
            # we'd need to parse logs or check the archive metadata to be sure.
            # But for this loop, we assume the evolver does its best.
        else:
            logging.error(f"Solver script failed with code {result.returncode}")
            logging.error(f"Stderr: {result.stderr}")

        print(result.stdout)

    except Exception as e:
        logging.error(f"Failed to run solver: {e}")

def main():
    parser = argparse.ArgumentParser(description="R-Few Loop: Orchestrates Challenger and Solver.")
    parser.add_argument("--seed-test", type=str, required=True, help="Path to the initial seed test (grounding).")
    parser.add_argument("--iterations", type=int, default=1, help="Number of evolution loops to run.")
    parser.add_argument("--model", type=str, default="gpt-4o", help="Model for the Challenger.")

    args = parser.parse_args()

    # 1. Initialize Challenger
    challenger = Challenger(model=args.model)

    for i in range(args.iterations):
        logging.info(f"--- Starting R-Few Loop Iteration {i+1}/{args.iterations} ---")

        # 2. Generate Challenge (Challenger Step)
        try:
            synthetic_test_path = challenger.generate_challenge(args.seed_test)
        except Exception as e:
            logging.error(f"Stopping loop due to generation failure: {e}")
            break

        # 3. Solve Challenge (Solver Step)
        run_solver(synthetic_test_path)

        # 4. Curriculum / Feedback (Basic)
        # In a full implementation, we would check if the solver succeeded (fitness=1.0)
        # and if so, add this synthetic test to a "verified_pool" to be used as a seed
        # for future harder challenges.
        # For now, we simply leave it in the synthetic folder.

        logging.info(f"--- Completed Iteration {i+1} ---")

if __name__ == "__main__":
    main()
