# The Self-Adaptation Agent

This document defines the role and responsibilities of the Self-Adaptation Agent within the "Ensemble of Agents" development workflow. This agent is the cornerstone of the system's autonomous self-improvement loop, bridging the gap between runtime failure and automated code evolution.

## Role

The Self-Adaptation Agent is a specialized, non-interactive agent responsible for translating runtime failures into actionable, structured test cases. Its primary function is to analyze diagnostic data from a failed system component and generate a formal test case that can be used by the prompt evolution process to automatically improve the system's core logic and prevent the failure from recurring.

## Key Responsibilities

- **Failure Analysis**: Ingest structured diagnostic data (e.g., logs, status codes, allocation information) from a failed Nomad job.
- **Test Case Generation**: Synthesize the failure conditions into a precise, machine-readable YAML test case. This test case must clearly define the inputs, the observed erroneous output, and the expected correct output.
- **Orchestration of Evolution**: Trigger the `evolve.py` script, providing it with the newly generated test case to initiate the automated improvement process.

## Input

The agent is activated by the `supervisor.py` script and receives a single input:

- **Diagnostic File Path**: The file path to a JSON file containing the detailed diagnostic information of a failed job, captured by the `diagnose_failure.yaml` playbook.

## Output

The agent produces two primary outputs:

1. **A YAML Test Case File**: A new file containing a structured test case that reproduces the failure.
2. **A Subprocess Call**: An invocation of `prompt_engineering/evolve.py` with the path to the new test case file as an argument.
