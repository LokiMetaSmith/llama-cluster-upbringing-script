import os
import sys
import json
import asyncio
import logging
from typing import Dict, Any, Tuple, Optional
import openai

# Add the parent directory to sys.path to import modules if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from prompt_engineering.evaluator import evaluate_code
    from prompt_engineering.evolve import select_parent_from_archive
except ImportError:
    from evaluator import evaluate_code
    from evolve import select_parent_from_archive

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SelfHarness:
    """
    Implements the Self-Harness algorithm (arXiv:2606.09498v1).
    1. Weakness Mining: Evaluate the current agent, extract logs/failures.
    2. Harness Proposal: Propose targeted modifications using an LLM.
    3. Proposal Validation: Evaluate the new harness and accept only if fitness improves.
    """

    def __init__(self, target_file: Optional[str] = None):
        if target_file is None:
            # If no target file is provided, grab the best parent from the evolutionary archive
            logging.info("No target file provided. Selecting parent from archive...")
            path, parent_id = select_parent_from_archive()
            self.target_file = path
            self.parent_id = parent_id
            if self.parent_id:
                os.environ["PARENT_AGENT_ID"] = self.parent_id
        else:
            self.target_file = target_file
            self.parent_id = None
        self.client = openai.AsyncOpenAI()

    async def _evaluate(self, code: str) -> Dict[str, Any]:
        """Wrapper around evaluator.evaluate_code."""
        # The evaluator expects JSON with 'code' and 'rationale'
        candidate = json.dumps({"code": code, "rationale": "Self-Harness evaluation"})
        return await evaluate_code(candidate)

    async def weakness_mining(self, baseline_code: str) -> Tuple[float, str]:
        """
        Stage 1: Evaluate the baseline code to find failures.
        Returns the baseline fitness and the evaluation logs (traces).
        """
        logging.info("Starting Weakness Mining stage...")
        result = await self._evaluate(baseline_code)
        fitness = result.get('fitness', 0.0)
        logs = result.get('log', '')
        details = result.get('details', '')

        logging.info(f"Baseline fitness: {fitness}")

        # Combine logs and details for context
        full_trace = f"Details:\n{details}\n\nLogs:\n{logs}"
        return fitness, full_trace

    async def harness_proposal(self, baseline_code: str, trace: str) -> str:
        """
        Stage 2: Use an LLM to propose a harness (code) modification
        specifically targeting the failures found in the trace.
        """
        logging.info("Starting Harness Proposal stage...")
        prompt = f"""
You are an expert Python programmer. An LLM agent's interaction harness (its core script)
has been tested and encountered failures.

Here is the execution trace/log showing the failures:
{trace[-3000:]} # Sending the tail of the trace to avoid context limits

Here is the current code for the agent:
```python
{baseline_code}
```

Your task is to analyze the trace, identify the specific model weakness or error,
and propose a minimal, targeted modification to the code to fix this specific failure.

Respond strictly with a JSON object containing two keys:
1. "rationale": A clear explanation of the weakness found and how your code fixes it.
2. "code": The full, complete, modified Python code.
"""
        response = await self.client.chat.completions.create(
            model="gpt-4o",  # Can be configured
            messages=[
                {"role": "system", "content": "You are a specialized debugging AI."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )

        content = response.choices[0].message.content
        return content

    async def proposal_validation(self, proposed_json: str, baseline_fitness: float) -> Tuple[bool, Dict[str, Any]]:
        """
        Stage 3: Evaluate the proposed change. Accept only if fitness is strictly > baseline_fitness
        (Regression testing).
        """
        logging.info("Starting Proposal Validation stage...")
        try:
            parsed = json.loads(proposed_json)
            proposed_code = parsed['code']
            rationale = parsed['rationale']
            logging.info(f"Proposed Fix Rationale: {rationale}")
        except Exception as e:
            logging.error(f"Failed to parse LLM proposal: {e}")
            return False, {}

        # Evaluate the proposed code
        result = await evaluate_code(proposed_json)
        new_fitness = result.get('fitness', 0.0)

        logging.info(f"Validation Result - Baseline Fitness: {baseline_fitness}, New Fitness: {new_fitness}")

        if new_fitness > baseline_fitness:
            logging.info("Proposal ACCEPTED! The modification improved performance.")
            return True, result
        else:
            logging.info("Proposal REJECTED! The modification did not improve performance.")
            return False, result

    async def run(self):
        """Executes the full Self-Harness loop."""
        with open(self.target_file, 'r') as f:
            baseline_code = f.read()

        # Stage 1
        baseline_fitness, trace = await self.weakness_mining(baseline_code)

        if baseline_fitness >= 1.0:
            logging.info("Baseline agent already has perfect fitness. Exiting.")
            return

        # Stage 2
        proposed_json = await self.harness_proposal(baseline_code, trace)

        # Stage 3
        accepted, final_result = await self.proposal_validation(proposed_json, baseline_fitness)

        if accepted:
            logging.info(f"New agent deployed with ID: {final_result.get('agent_id')}")
            # The evaluator automatically saves the accepted agent to the archive
        else:
            logging.info("Iteration complete. No improvements found.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run the Self-Harness improvement loop.")
    parser.add_argument("--target", type=str, default=None, help="Path to the agent code. If omitted, will select from the archive.")
    args = parser.parse_args()

    harness = SelfHarness(args.target)
    asyncio.run(harness.run())
