# AI Agent Architectures

Last updated: 2026-01-23

This project utilizes two distinct AI agent architectures: a "Mixture of Experts" for the runtime application and an "Ensemble of Agents" for the development workflow.

## 1. Runtime Architecture: A Mixture of Experts (MoE)

The production application uses a Mixture of Experts (MoE) architecture to handle a wide range of tasks efficiently. Instead of relying on a single, monolithic model, the system is composed of multiple specialized AI agents.

### The Workflow Engine

The core of the system is the **Workflow Engine**, which runs within the main `pipecatapp` service (specifically the `TwinService`). The agent's behavior is no longer hardcoded; instead, it is defined by declarative workflows (YAML files).

- **Role**: To orchestrate the "thought process" of the agent, moving from input to summary, reasoning, tool execution, and final response.
- **Implementation**: The `WorkflowRunner` in `pipecatapp/workflow/runner.py` executes graphs defined in `pipecatapp/workflows/`.
- **Flexibility**: The system can switch between different workflows. The default workflow (`default_agent_loop.yaml`) is a tiered conversation loop, but more complex workflows can enable autonomous tool use and multi-step planning.

### The Agent Hierarchy

#### a. The Router / Main Agent

In the context of the workflow, the "Router" or "Main Agent" is the primary LLM node that analyzes the user's request.

- **Responsibility**: It classifies incoming queries and delegates them to the most suitable expert or tool.
- **Prompt File**: `ansible/roles/pipecatapp/files/prompts/router.txt` (used by `SystemPromptNode` in advanced workflows).
- **Tool Access**: The Main Agent is the only entity with direct access to the tool library. If a query requires interaction with the system (e.g., running code, accessing files), it selects and executes the appropriate tool.

#### b. The Expert Agents (The Specialists)

Expert agents are specialized LLMs deployed as separate, independent services. They are designed to excel at a single, well-defined domain. They do not have access to tools and focus solely on processing the text-based queries routed to them. The system includes the following experts by default:

- **The Main Expert**: Handles general conversation, summarization, and acts as the fallback.
- **The Coding Expert**: Handles code generation, debugging, and questions about algorithms and system architecture.
- **The Math Expert**: Solves math problems and answers logic-based questions.
- **The Extract Expert**: Parses text to find and format specific information.

### Tool-Using Capabilities

**Only the Router/Main Agent has access to the library of tools.** This concentrates the system's interactive capabilities in one place, making it easier to manage, monitor, and secure.

#### Built-in Capabilities

These are special capabilities integrated directly into the `TwinService` or prompt:

- **`vision`**: Gets a real-time description of what is visible via the webcam (using YOLOv8 or Moondream).
- **`route_to_expert`**: A virtual tool that allows the agent to forward a user's query to a specialized model (e.g., Coding, Math).

#### Available Tools

The following tools are available in `pipecatapp/tools/`:

- **`ansible`**: Runs Ansible playbooks to manage the cluster.
- **`archivist`**: Performs deep research on the agent's long-term memory.
- **`claude_clone`**: A tool for interacting with a Claude-like model.
- **`code_runner`**: Executes Python code in a secure, sandboxed environment.
- **`council`**: Convenes a council of AI experts to deliberate on a query.
- **`dependency_scanner`**: Scans Python packages for vulnerabilities using the OSV database.
- **`desktop_control`**: Provides full control over the desktop environment, including taking screenshots and performing mouse/keyboard actions.
- **`file_editor`**: Reads, writes, and patches files in the codebase.
- **`final_answer`**: A tool to provide a final answer to the user.
- **`git`**: Interacts with Git repositories.
- **`ha`**: Controls smart home devices via Home Assistant.
- **`llxprt_code`**: A specialized tool for code-related tasks.
- **`mcp`**: Provides agent introspection and self-control (e.g., status checks, memory management).
- **`open_workers`**: Manages and interacts with open worker agents.
- **`opencode`**: Interface for the OpenCode tool.
- **`orchestrator`**: Dispatches high-priority, complex jobs to the cluster.
- **`planner`**: Plans complex tasks and executes them.
- **`power`**: Controls the cluster's power management policies.
- **`project_mapper`**: Scans the codebase to generate a project structure map.
- **`prompt_improver`**: A tool for improving prompts.
- **`rag`**: Searches the project's documentation to answer questions.
- **`shell`**: Executes shell commands (uses a persistent tmux session).
- **`smol_agent_computer`**: A tool for creating small, specialized agents.
- **`ssh`**: Executes commands on remote machines.
- **`summarizer`**: Summarizes conversation history.
- **`swarm`**: Spawns multiple worker agents to perform tasks in parallel.
- **`term_everything`**: Provides a terminal interface for interacting with the system.
- **`vr`**: Tools for Virtual Reality interactions.
- **`web_browser`**: Enables web navigation and content interaction.

> **Note on Implementation History:** Previous versions of the agent relied on a hardcoded "Router" agent with a static list of tools. The current system has evolved to a dynamic, workflow-driven architecture, enabling more complex and varied agent behaviors.

### Configuration and Customization

The modular design makes the system highly extensible and easy to adapt to new tasks and domains. The system configuration is primarily handled through YAML files.

You can easily create new experts by following these steps:

1. **Define a new model list** for it in `group_vars/models.yaml` under the `expert_models` dictionary.
2. **Add the new expert's name** to the `experts` list in `group_vars/all.yaml`.
3. The ansible playbooks will automatically deploy a new service for your expert.

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

### Automated Code Review with Quibbler

To augment the peer review process, this project has integrated Quibbler, an AI-powered code reviewer. After making changes, developers should use the `run_quibbler.sh` script to get automated feedback on their work.

**Usage:**

```bash
./scripts/run_quibbler.sh "<user_instructions>" "<agent_plan>"
```

- `<user_instructions>`: The original instructions given to the agent.
- `<agent_plan>`: A summary of the changes made by the agent.

This script will run Quibbler to analyze the code changes and provide feedback, helping to ensure that the changes align with the user's intent and the project's coding standards.

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

### Bootstrapping the Environment

After setting up the Python environment, the next step is to run the `bootstrap.sh` script. This script automates the process of setting up the entire application stack, including all the necessary services and configurations, using Ansible.

**Basic Usage:**

To run the script with default settings, simply execute it from the root of the repository:

```bash
./bootstrap.sh
```

This will run a series of Ansible playbooks to provision the local environment.

**Common Flags:**

You can customize the bootstrap process using the following flags:

- `--external-model-server`: Use this flag to skip the download and build steps for large language models. This is useful for development when you don't need the full model capabilities or are using a remote model server.
- `--purge-jobs`: This flag will stop and purge all running Nomad jobs before starting the bootstrap process. This is useful for ensuring a clean deployment.
- `--debug`: If the script fails, use the `--debug` flag to enable verbose logging. The output will be saved to `playbook_output.log`, which can be used to diagnose the issue.
- `--continue`: If the bootstrap process is interrupted, you can use the `--continue` flag to resume from the last successfully completed playbook. This can save a significant amount of time by avoiding the need to rerun completed tasks.
