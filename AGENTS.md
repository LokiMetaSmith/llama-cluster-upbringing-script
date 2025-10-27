# AI Agent Architectures

This project utilizes two distinct AI agent architectures: a "Mixture of Experts" for the runtime application and an "Ensemble of Agents" for the development workflow.

## 1. Runtime Architecture: A Mixture of Experts (MoE)

The production application uses a Mixture of Experts (MoE) architecture to handle a wide range of tasks efficiently. Instead of relying on a single, monolithic model, the system is composed of multiple specialized AI agents. A primary "Router" agent analyzes incoming user requests and delegates them to the most suitable expert. This approach allows the cluster to use smaller, specialized models for specific tasks, leading to faster response times, more accurate results, and better resource management.

### The Agent Hierarchy

#### a. The Router Agent (The Conductor)

The core of the system is the Router Agent, which runs within the main `pipecatapp` service. This agent's primary responsibility is not to answer complex questions itself, but to understand the user's intent and delegate the task to the appropriate downstream service or tool.

- **Role**: To classify incoming queries and route them to the correct specialist.
- **Implementation**: This agent is the main `TwinService` in `ansible/roles/pipecatapp/files/app.py`.
- **Prompt File**: `ansible/roles/pipecatapp/files/prompts/router.txt`
- **Key Behavior**: The Router is the only agent with access to the tool library. If a query requires interaction with the system (e.g., running code, accessing files), the Router will select and execute the appropriate tool. If the query falls into a specialized domain, it will use the `route_to_expert` tool to pass the query to a specialist. For general conversation, it will handle the query itself.

#### b. The Expert Agents (The Specialists)

Expert agents are specialized LLMs deployed as separate, independent services. They are designed to excel at a single, well-defined domain. They do not have access to tools and focus solely on processing the text-based queries routed to them. The system includes the following experts by default:

- **The Main Expert**: Handles general conversation, summarization, and acts as the fallback for the Router Agent.
- **The Coding Expert**: Handles code generation, debugging, and questions about algorithms and system architecture.
- **The Math Expert**: Solves math problems and answers logic-based questions.
- **The Extract Expert**: Parses text to find and format specific information, like names, dates, or other data points.

### Tool-Using Capabilities

**Only the Router Agent has access to the library of tools** (e.g., `ssh`, `code_runner`, `ansible`). This is a deliberate design choice for security and predictability. When the Router determines that a task requires interacting with the outside world, it will select and use the appropriate tool itself, rather than passing that capability down to a specialized expert. This concentrates the system's interactive capabilities in one place, making it easier to manage, monitor, and secure.

### Configuration and Customization

The modular design makes the system highly extensible and easy to adapt to new tasks and domains. The personality, instructions, and capabilities of each agent are defined in simple text files and YAML configuration.

You can easily create new experts by following these steps:

1.  **Add a new prompt file** to the `ansible/roles/pipecatapp/files/prompts/` directory (e.g., `legal_expert.txt`).
2.  **Define a new model list** for it in `group_vars/models.yaml` under the `expert_models` dictionary.
3.  **Add the new expert's name** to the `experts` list in `group_vars/all.yaml`.
4.  The ansible playbooks will automatically deploy a new service for your expert.

---

## 2. Development Workflow: An Ensemble of Agents

For code development, the project uses a workflow inspired by an "Ensemble of Agents," where each agent has a specific, well-defined role in the software development lifecycle. This structured approach ensures a thorough and methodical process, from understanding the initial request to delivering clean, functional code. Agent definitions are located in the `prompt_engineering/agents/` directory.

### The Agent Roles

#### a. Problem Scope Framing

This agent is responsible for the initial analysis of a user's request. It excels at clarifying ambiguity, defining the scope of work, exploring the codebase, and identifying constraints. This agent sets the foundation for a successful workflow by ensuring a shared understanding of the task.

#### b. Architecture Review

This agent acts as the guardian of the codebase's integrity. It analyzes the existing architecture, evaluates the impact of proposed changes, ensures scalability and maintainability, and recommends best practices.

#### c. New Task Review

This agent is responsible for reviewing the implementation of new tasks. It focuses on code quality, adherence to standards, functionality, and proper integration with the existing codebase, acting as a peer reviewer.

#### d. Debug and Analysis

This agent is the problem-solver of the ensemble. It is responsible for running existing tests, creating new ones, debugging issues, performing root cause analysis, and identifying performance bottlenecks.

#### e. Code Clean Up

This agent is dedicated to improving the quality and maintainability of the codebase. It focuses on refactoring, removing redundancy, improving readability, and applying best practices to reduce technical debt.

---

## Local Development and Testing

For an efficient local development and testing workflow, it's recommended to set up a dedicated Python virtual environment. This keeps the project's dependencies isolated from your global Python installation.

### Python Dependency Management

This project uses two key files for managing Python dependencies:

- `ansible/roles/python_deps/files/requirements.txt`: This file lists all the **runtime dependencies** needed for the `pipecatapp` application to function on the cluster nodes.
- `requirements-dev.txt`: This file contains all the **development and testing dependencies**, including tools like `pytest`, `ansible-lint`, and `yamllint`. This is the file you should use to set up your local environment.

### Recommended Setup Procedure

1. **Create and activate a Python virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. **Install development dependencies:**

    ```bash
    pip install -r requirements-dev.txt
    ```
