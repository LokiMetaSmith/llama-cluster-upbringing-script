# Agent Definitions

This directory contains agent definitions.

## Files

- **ADAPTATION_AGENT.md**: The definition for the adaptation agent.
- **EVALUATOR_GENERATOR.md**: The definition for the evaluator generator.
- **architecture_review.md**: The definition for the architecture review agent.
- **code_clean_up.md**: The definition for the code clean up agent.
- **debug_and_analysis.md**: The definition for the debug and analysis agent.
- **new_task_review.md**: The definition for the new task review agent.
- **problem_scope_framing.md**: The definition for the problem scope framing agent.

## Role

This directory defines the roles and responsibilities of the various agents in the ensemble. Each file describes a specific agent, its tools, its sub-agent delegation capabilities, and the LLM model that powers it.

## Backing LLM Model

- **Model:** `claude-3-opus` (default)
- **Reasoning:** Unless otherwise specified, `claude-3-opus` is used for its superior reasoning and coding capabilities.
