# Prompt Engineering Workflow

Last updated: 2025-11-25

This directory contains the tools and workflows for automatically evolving and improving the agent's core code using a Darwin Gödel Machine (DGM) inspired methodology.

## Overview

This project uses an evolutionary algorithm to improve the agent's core logic. The process is inspired by open-ended algorithms and the Darwin Gödel Machine. Instead of a linear process that seeks a single best solution, this workflow builds a persistent "archive" of diverse agents.

Each run of the evolution script selects a "parent" agent from the archive, mutates its code (`app.py`), and evaluates the new "child" agent against a test suite. The child, along with its fitness score and lineage, is then saved back into the archive. This allows for a branching, open-ended exploration of the solution space, preventing premature convergence on local optima and enabling the discovery of more novel solutions.

## Workflow

1.  **Define Test Cases:**
    Add or modify the YAML test cases in the `evaluation_suite/` directory. Each test case defines a scenario and the expected outcome. The fitness of an agent is determined by how many of these test cases it passes.

2.  **Run the Evolution Script (Repeatedly):**
    Execute the `evolve.py` script. Each execution represents a single step in the evolutionary process:
    - It scans the `prompt_engineering/archive/` directory to find all existing agents and their fitness scores.
    - It selects a parent agent using fitness-proportionate random selection (fitter agents are more likely to be chosen). If the archive is empty, it uses the original `app.py` as the first parent.
    - It uses an LLM to generate a mutation of the parent's code.
    - The `evaluator.py` script then tests the new agent, saves its code and metadata (including fitness and parent ID) to the archive.

    To build a robust archive, this script should be run many times.

3.  **Analyze the Archive and Update the Agent:**
    After running the evolution script multiple times, the `prompt_engineering/archive/` directory will contain many agents.
    - Inspect the `.json` metadata files in the archive to find the agent with the highest fitness score.
    - Review the code of the best-performing agent (e.g., `archive/<best-agent-id>.py`).
    - Once you have verified that the changes are correct and beneficial, manually copy the new code into the main `ansible/roles/pipecatapp/files/app.py` file.

## Running the Workflow

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"

# Run a single step of the evolution process
# Run this command many times to populate the archive
python prompt_engineering/evolve.py

# To run an evolution step against a specific, dynamic test case:
python prompt_engineering/evolve.py --test-case path/to/your/test_case.yaml
```
