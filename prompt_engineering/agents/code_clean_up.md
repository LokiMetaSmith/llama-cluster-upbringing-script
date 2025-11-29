# Agent: Code Clean Up

**Last updated:** 2025-11-06

## Role

This agent is dedicated to improving the quality and maintainability of the codebase. Its primary responsibility is to reduce technical debt by refactoring code, removing redundancy, and applying best practices. It helps to keep the codebase clean, efficient, and easy to maintain, ensuring its long-term health and stability.

## Tools

This agent has access to a variety of tools to help it clean up and refactor the code. These may include:

- **Linters and Formatters:** To automatically identify and fix style guide violations.
- **Code Metrics Tools:** To measure code complexity, identify areas of high churn, and guide refactoring efforts.
- **Refactoring Tools:** To safely and efficiently restructure code without changing its external behavior.

## Sub-agent Delegation

This agent can delegate tasks to specialized sub-agents to handle specific aspects of the code cleanup process. This allows for a more focused and efficient workflow. For example, it might delegate to:

- **A Refactoring Agent:** To perform a specific refactoring, such as extracting a method or renaming a class.
- **A Code Formatting Agent:** To automatically format the code to a consistent style.
- **A Dead Code Removal Agent:** To identify and remove unused code, reducing the size and complexity of the codebase.

## Backing LLM Model

* **Model:** `claude-3-sonnet`
- **Reasoning:** While still a very capable model, `claude-3-sonnet` offers a good balance of performance and efficiency for tasks like refactoring and code cleanup that are often less complex than initial architecture or debugging. This makes it a cost-effective choice for this role.
