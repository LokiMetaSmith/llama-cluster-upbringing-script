# Prompt Engineering Workflow

This directory contains the tools and workflows for automatically evolving and improving the agent's core prompt using the `openevolve` library.

## Overview

The process uses an evolutionary algorithm to iteratively mutate the agent's main system prompt and evaluate its performance against a test suite. This allows us to discover more effective prompts that lead to better agent behavior.

## Workflow

1.  **Define Test Cases:**
    Add or modify the YAML test cases in the `evaluation_suite/` directory. Each test case should define a user query and the expected outcome (e.g., a specific tool call or a keyword in the response).

2.  **Run the Evolution Script:**
    Execute the `evolve.py` script. This will:
    - Take the current best prompt as a starting point.
    - Use an LLM to generate mutations of the prompt.
    - For each new prompt, run the `evaluator.py` script to calculate a fitness score based on the test suite.
    - After many iterations, it will output the best-performing prompt it has found.

3.  **Update the Agent:**
    Once you have a new, improved prompt, manually copy it into the `get_tools_prompt` method in `app.py`.

## Running the Workflow

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"

# Run the evolution process
python prompt_engineering/evolve.py
```
