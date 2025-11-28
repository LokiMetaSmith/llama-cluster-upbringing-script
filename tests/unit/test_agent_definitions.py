import os
import pytest

# Define the path to the agent definitions directory
AGENT_DEFS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "prompt_engineering", "agents")

# Check if the directory exists to avoid errors if it's removed later
if not os.path.isdir(AGENT_DEFS_DIR):
    pytest.skip("Agent definitions directory not found.", allow_module_level=True)

# Get a list of all markdown files in the directory
agent_files = [f for f in os.listdir(AGENT_DEFS_DIR) if f.endswith(".md")]

def parse_and_validate_agent_def(content, filename):
    """
    Parses the content of an agent definition file and validates its structure.
    Returns a list of validation error messages.
    """
    errors = []
    lines = [line.strip() for line in content.split('\n')]

    # State flags
    found_role_heading = False
    found_llm_heading = False
    found_model_spec = False

    # EVALUATOR_GENERATOR.md is a special case, it's a generator, not a definition.
    if "EVALUATOR_GENERATOR.md" in filename:
        return []

    for line in lines:
        if line == "## Role":
            found_role_heading = True
        elif line == "## Backing LLM Model":
            if not found_role_heading:
                errors.append("'## Backing LLM Model' section appears before '## Role' section.")
            found_llm_heading = True
        elif line.startswith("*") and "**Model:**" in line:
            if not found_llm_heading:
                errors.append("'Model' specification appears before '## Backing LLM Model' section.")
            found_model_spec = True

    if not found_role_heading:
        errors.append("Missing '## Role' section.")
    if not found_llm_heading:
        errors.append("Missing '## Backing LLM Model' section.")
    if not found_model_spec:
        errors.append("Missing 'Model' specification (e.g., '* **Model:** ...').")

    return errors


@pytest.mark.parametrize("filename", agent_files)
def test_agent_definition_schema(filename):
    """
    Validates the schema of an agent definition markdown file using a more robust parser.
    """
    filepath = os.path.join(AGENT_DEFS_DIR, filename)
    with open(filepath, 'r') as f:
        content = f.read()

    errors = parse_and_validate_agent_def(content, filename)

    assert not errors, f"Schema validation failed for {filename}:\n" + "\n".join(errors)