import yaml
import os
import sys
import json
import glob
import asyncio
from unittest.mock import patch, MagicMock

from openai import OpenAI

# Add the project root to the python path to allow importing app parts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# We need to import the TwinService to replicate its prompt construction logic
from ansible.roles.pipecatapp.files.app import TwinService

# --- Configuration ---
# Use a fast and cheap model for evaluation.
EVALUATION_MODEL = "gpt-3.5-turbo"
EVALUATION_SUITE_DIR = "prompt_engineering/evaluation_suite"


def load_test_suite(directory: str) -> list:
    """Loads all YAML test cases from a given directory."""
    test_cases = []
    for filepath in glob.glob(os.path.join(directory, "*.yaml")):
        with open(filepath, "r") as f:
            cases = yaml.safe_load(f)
            if isinstance(cases, list):
                test_cases.extend(cases)
    return test_cases


def construct_full_prompt(candidate_prompt: str, query: str) -> str:
    """
    Constructs the full prompt that would be sent to the LLM, by replicating
    the logic from TwinService.
    """
    # We instantiate a dummy TwinService to get access to its tool generation logic.
    # Most dependencies can be mocked as they are not needed for prompt construction.
    with patch('ansible.roles.pipecatapp.files.app.YOLOv8Detector'), \
         patch('ansible.roles.pipecatapp.files.app.MoondreamDetector'), \
         patch('ansible.roles.pipecatapp.files.app.PipelineRunner'):

        mock_runner = MagicMock()
        mock_vision_detector = MagicMock()

        # We need to mock the Consul call for service discovery.
        with patch('requests.get') as mock_requests_get:
            # Pretend there are no other experts to simplify the tool list.
            mock_requests_get.return_value.json.return_value = {}
            mock_requests_get.return_value.status_code = 200

            twin = TwinService(
                llm=None,  # Not needed for prompt construction
                vision_detector=mock_vision_detector,
                runner=mock_runner
            )

            # This is the prompt that lists all the tools.
            tools_prompt = twin.get_system_prompt("router").split(candidate_prompt)[-1]

    # Assemble the final prompt, similar to how TwinService does it.
    # We use the candidate prompt as the base, add the tools, and then the query.
    # We omit memory for simplicity in this evaluation context.
    full_prompt = f"""
    {candidate_prompt}
    {tools_prompt}

    Current user query: {query}
    """
    return full_prompt.strip()


async def evaluate_prompt(candidate_prompt: str) -> dict:
    """
    Evaluates a candidate prompt against the test suite and returns a fitness score.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)
    test_cases = load_test_suite(EVALUATION_SUITE_DIR)

    if not test_cases:
        return {"fitness": 0.0, "passed": 0, "total": 0, "error": "No test cases found."}

    passed_count = 0
    for case in test_cases:
        query = case["query"]
        full_prompt = construct_full_prompt(candidate_prompt, query)

        try:
            # Call the LLM with the constructed prompt
            response = client.chat.completions.create(
                model=EVALUATION_MODEL,
                messages=[{"role": "system", "content": full_prompt}],
                temperature=0.0,
            )
            llm_output = response.choices[0].message.content.strip()

            # Check against expectations
            passed = False
            if "expected_tool_call" in case:
                try:
                    tool_call = json.loads(llm_output)
                    if tool_call.get("tool") == case["expected_tool_call"]:
                        passed = True
                except json.JSONDecodeError:
                    # Not a valid JSON tool call, so it fails the check.
                    pass
            elif "expected_output_contains" in case:
                if case["expected_output_contains"] in llm_output:
                    passed = True

            if passed:
                passed_count += 1

        except Exception as e:
            # If the API call fails, the test case fails.
            print(f"Error during evaluation of query '{query}': {e}")
            continue

    fitness = (passed_count / len(test_cases)) if test_cases else 0.0

    return {
        "fitness": fitness,
        "passed": passed_count,
        "total": len(test_cases)
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python evaluator.py <candidate_prompt_text>")
        sys.exit(1)

    prompt_file = sys.argv[1]
    with open(prompt_file, 'r') as f:
        prompt = f.read()

    # openevolve runs async, so we need a loop to run our main function
    results = asyncio.run(evaluate_prompt(prompt))

    # The openevolve library expects a JSON object printed to stdout
    print(json.dumps(results))