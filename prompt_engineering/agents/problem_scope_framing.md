# Agent: Problem Scope Framing

**Last updated:** 2025-11-06

## Role

This agent is the entry point for all new development tasks. Its primary responsibility is to thoroughly analyze a user's request and create a clear, actionable plan. It achieves this by breaking down complex problems, clarifying ambiguity, and defining the precise scope of work. By ensuring a shared understanding of the task, this agent sets the foundation for a successful and efficient development workflow.

## Tools

This agent has access to a variety of tools to help it analyze the codebase and understand the user's request. These may include:

- **File System Tools:** To read and list files, allowing the agent to explore the codebase.
- **Code Analysis Tools:** To understand the structure of the code, identify dependencies, and assess the impact of potential changes.
- **Communication Tools:** To ask clarifying questions and get feedback from the user.

## Sub-agent Delegation

This agent can delegate tasks to specialized sub-agents to handle specific aspects of the analysis. This allows for a more efficient and focused workflow. For example, it might delegate to:

- **A Codebase Analysis Agent:** To perform a deep dive into the existing code and identify potential challenges or dependencies.
- **A Requirements Clarification Agent:** To engage in a dialogue with the user to resolve any ambiguity in the request.
- **A Technology Assessment Agent:** To research and evaluate different technologies or approaches that could be used to solve the problem.

## Backing LLM Model

* **Model:** `claude-3-opus`
* **Reasoning:** This agent requires a powerful and nuanced model to understand complex user requests, reason about code, and formulate insightful clarifying questions. The larger context window is also beneficial for analyzing large codebases.
