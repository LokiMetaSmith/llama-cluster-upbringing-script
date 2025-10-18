# Agent Definition: The Adaptation Agent

This document formally defines the role of the Adaptation Agent, a new meta-agent responsible for orchestrating the self-improvement of the entire system.

## Role

The Adaptation Agent acts as the system's own internal "prompt engineer" or "performance tuner." It is not a user-facing agent. Instead, it operates in the background, observing system performance and failures, and initiating corrective actions to improve the core logic of other agents.

## Backing LLM Model

* **Model:** `groq/llama3-70b-8192`
* **Parameters:**
    * Temperature: 0.7
    * Top-p: 0.9

## Core Responsibilities

1.  **Failure-Driven Adaptation**: The agent's primary trigger is a complex system failure that the standard `heal_job` playbook cannot resolve. When the `reflection/reflect.py` script determines it cannot fix an issue (e.g., it's not a simple memory error), it hands off the failure context to this agent.

2.  **Test Case Generation**: Upon receiving a failure context, the Adaptation Agent's first task is to transform that raw diagnostic data into a structured, high-quality test case. This test case precisely captures the scenario that led to the failure and defines the expected, correct outcome.

3.  **Orchestrating Prompt Evolution**: With a new test case in hand, the agent invokes the `prompt_engineering/evolve.py` workflow. It injects the new, failure-driven test case into the evaluation suite. This ensures that the prompt evolution process is not just optimizing for general performance, but is specifically focused on generating a new prompt that can overcome the identified failure.

4.  **Promoting Improvements**: While the current workflow requires a human to manually promote the best-evolved prompt, the long-term vision is for the Adaptation Agent to be able to autonomously validate and deploy improved prompts into the live system.

## Integration into the Architecture

-   **Trigger**: The `supervisor.py` script will invoke the `reflection/adaptation_manager.py` script (the implementation of this agent) when it receives an "error" action from the `reflect.py` script.
-   **Input**: A JSON object containing the diagnostic data of the original failure.
-   **Output**: An improved prompt file (`best_prompt.txt`) and a log of the evolutionary process. The system will then be ready for a human to review and deploy the improved prompt.

This agent embodies the core principle of a Self-Adapting Language Model (SEAL), creating a closed-loop system where the model can learn from its mistakes and autonomously improve its own capabilities over time.