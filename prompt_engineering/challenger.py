import os
import json
import logging
import argparse
import uuid
import datetime
from typing import Optional

# Use OpenAI compatible client (works with llama-server, vllm, or OpenAI)
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Challenger:
    """
    The Challenger agent (from the R-Few paper).
    Its goal is to generate synthetic, verifiable test cases to guide the evolution of the Solver (the agent).
    """

    def __init__(self, base_url: Optional[str] = None, api_key: str = "dummy", model: str = "gpt-4o"):
        """
        Args:
            base_url: The URL of the LLM API (e.g., http://localhost:8080/v1).
            api_key: The API key (dummy if local).
            model: The model identifier to use.
        """
        # Try to discover base_url from environment if not provided
        if not base_url:
            base_url = os.getenv("LLAMA_API_URL", "http://localhost:8080/v1")

        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
        self.synthetic_tests_dir = os.path.join(os.getcwd(), "tests", "integration", "synthetic")
        os.makedirs(self.synthetic_tests_dir, exist_ok=True)

    def generate_challenge(self, seed_test_path: str) -> str:
        """
        Generates a new synthetic test case based on a seed test.

        Args:
            seed_test_path: Path to an existing integration test file to use as a template (grounding).

        Returns:
            The file path of the generated synthetic test.
        """
        if not os.path.exists(seed_test_path):
             raise FileNotFoundError(f"Seed test not found: {seed_test_path}")

        with open(seed_test_path, 'r') as f:
            seed_code = f.read()

        prompt = f"""
You are an expert QA Engineer and Python Developer.
Your task is to generate a **new** integration test file based on the provided "seed" test.
The new test should verify the same application but introduce a slightly different scenario, edge case, or higher difficulty level.

**Goal:** Create a "Challenge" for the AI coding agent. The test should be valid Python code using `unittest` and `requests`.
It must use the same setup logic (e.g., `SETUP` method, environment variables) as the seed to ensuring it runs in the existing environment.

**Seed Test Code:**
```python
{seed_code}
```

**Instructions:**
1. Keep the `setUp` method exactly the same as the seed to ensure connectivity.
2. Change the test method(s) to check for a variation. Examples:
   - Check a different endpoint (if known).
   - Check for specific content in the response body.
   - Check performance (latency) with tighter constraints.
   - Check error handling (e.g., sending bad data if applicable).
3. Do NOT invent non-existent endpoints. Stick to the API structure implied by the seed.
4. Return ONLY the valid Python code for the new test file. Do not include markdown formatting or explanations.
"""

        logging.info(f"Generating synthetic challenge based on {seed_test_path}...")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI that generates Python unit tests."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            generated_code = response.choices[0].message.content.strip()

            # Clean up potential markdown blocks
            if generated_code.startswith("```python"):
                generated_code = generated_code.replace("```python", "", 1)
            if generated_code.startswith("```"):
                generated_code = generated_code.replace("```", "", 1)
            if generated_code.endswith("```"):
                generated_code = generated_code.rsplit("```", 1)[0]

            generated_code = generated_code.strip()

            # Save to file
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:6]
            filename = f"challenge_{timestamp}_{unique_id}.py"
            filepath = os.path.join(self.synthetic_tests_dir, filename)

            with open(filepath, "w") as f:
                f.write(generated_code)

            logging.info(f"Synthetic challenge saved to: {filepath}")
            return filepath

        except Exception as e:
            logging.error(f"Failed to generate challenge: {e}")
            raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Challenger Agent: Generates synthetic tests.")
    parser.add_argument("--seed", type=str, required=True, help="Path to the seed test file.")
    parser.add_argument("--model", type=str, default="gpt-4o", help="LLM model to use.")

    args = parser.parse_args()

    challenger = Challenger(model=args.model)
    new_test = challenger.generate_challenge(args.seed)
    print(f"Generated Test Path: {new_test}")
