# AI Agent Architecture: A Mixture of Experts

This project utilizes a Mixture of Experts (MoE) architecture to handle a wide range of tasks efficiently. Instead of relying on a single, monolithic model, the system is composed of multiple specialized AI agents. A primary "Router" agent analyzes incoming user requests and delegates them to the most suitable expert.

This approach allows the cluster to use smaller, specialized models for specific tasks, leading to faster response times, more accurate results, and better resource management.

## The Agent Hierarchy

### 1. The Router Agent (The Conductor)

The core of the system is the Router Agent, which runs within the main `pipecatapp` service. This agent's primary responsibility is not to answer complex questions itself, but to understand the user's intent and delegate the task to the appropriate downstream service or tool.

- **Role**: To classify incoming queries and route them to the correct specialist.
- **Implementation**: This agent is the main `TwinService` in `ansible/roles/pipecatapp/files/app.py`.
- **Prompt File**: `ansible/roles/pipecatapp/files/prompts/router.txt`
- **Key Behavior**: The Router is the only agent with access to the tool library. If a query requires interaction with the system (e.g., running code, accessing files), the Router will select and execute the appropriate tool. If the query falls into a specialized domain, it will use the `route_to_expert` tool to pass the query to a specialist. For general conversation, it will handle the query itself.

### 2. The Expert Agents (The Specialists)

Expert agents are specialized LLMs deployed as separate, independent services. They are designed to excel at a single, well-defined domain. They do not have access to tools and focus solely on processing the text-based queries routed to them.

The system includes the following experts by default:

#### a. The Main Expert

This is the general-purpose, conversational agent. It is the default destination for any query that does not require a specialist.

- **Expert Name**: `main`
- **Role**: Handles general conversation, summarization, and acts as the fallback for the Router Agent.
- **Models**: Configured in `group_vars/models.yaml` under the `expert_models.main` key.

#### b. The Coding Expert

This agent is fine-tuned for programming and software development tasks.

- **Expert Name**: `coding`
- **Role**: Handles code generation, debugging, and questions about algorithms and system architecture.
- **Prompt File**: `ansible/roles/pipecatapp/files/prompts/coding_expert.txt`
- **Models**: Configured in `group_vars/models.yaml` under the `expert_models.coding` key.

#### c. The Math Expert

A specialist for mathematical and quantitative reasoning.

- **Expert Name**: `math`
- **Role**: Solves math problems and answers logic-based questions.
- **Prompt File**: `ansible/roles/pipecatapp/files/prompts/math_expert.txt`
- **Models**: Configured in `group_vars/models.yaml` under the `expert_models.math` key.

#### d. The Extract Expert

This agent is optimized for extracting structured data from unstructured text.

- **Expert Name**: `extract`
- **Role**: Parses text to find and format specific information, like names, dates, or other data points.
- **Prompt File**: `ansible/roles/pipecatapp/files/prompts/extract_expert.txt`
- **Models**: Configured in `group_vars/models.yaml` under the `expert_models.extract` key.

## Tool-Using Capabilities

**Only the Router Agent has access to the library of tools** (e.g., `ssh`, `code_runner`, `ansible`). This is a deliberate design choice for security and predictability. When the Router determines that a task requires interacting with the outside world, it will select and use the appropriate tool itself, rather than passing that capability down to a specialized expert. This concentrates the system's interactive capabilities in one place, making it easier to manage, monitor, and secure.

## Configuration and Customization

The modular design makes the system highly extensible and easy to adapt to new tasks and domains. The personality, instructions, and capabilities of each agent are defined in simple text files and YAML configuration.

- To change the behavior of the **Router Agent**, edit `ansible/roles/pipecatapp/files/prompts/router.txt`.
- To change the behavior of an **Expert Agent**, edit its corresponding file in the `ansible/roles/pipecatapp/files/prompts/` directory.

You can easily create new experts by following these steps:

1. **Add a new prompt file** to the `ansible/roles/pipecatapp/files/prompts/` directory (e.g., `legal_expert.txt`).
2. **Define a new model list** for it in `group_vars/models.yaml` under the `expert_models` dictionary.
3. **Add the new expert's name** to the `experts` list in `group_vars/all.yaml`.
4. The ansible playbooks will automatically deploy a new service for your expert.

## Local Development and Testing

For an efficient local development and testing workflow, it's recommended to set up a dedicated Python virtual environment. This keeps the project's dependencies isolated from your global Python installation.

### Python Dependency Management

This project uses two key files for managing Python dependencies:

- `ansible/roles/python_deps/files/requirements.txt`: This file lists all the **runtime dependencies** needed for the `pipecatapp` application to function on the cluster nodes. The main Ansible playbook automatically installs these into a virtual environment on each server as part of the provisioning process.

- `requirements-dev.txt`: This file contains all the **development and testing dependencies**, including tools like `pytest`, `ansible-lint`, and `yamllint`. This is the file you should use to set up your local environment.

### Recommended Setup Procedure

1. **Create and activate a Python virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. **Install development dependencies:**
    This command installs all the necessary tools for local testing and linting. This process is also documented in `scripts/README.md`.

    ```bash
    pip install -r requirements-dev.txt
    ```

By following this procedure, you will have all the necessary tools installed locally to run tests, lint the code, and validate your changes before deploying them to the cluster.
