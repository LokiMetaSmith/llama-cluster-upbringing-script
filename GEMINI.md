# GEMINI.md

## Project Overview

This project provides a complete solution for deploying a high-performance, low-latency conversational AI pipeline on a cluster of legacy, resource-constrained desktop computers. It uses Ansible for automated provisioning, Nomad for cluster orchestration, and a state-of-the-art AI stack to create a responsive, streaming, and embodied voice agent.

The architecture is a multi-layered stack that includes:

*   **Layer 1: Bare-Metal & OS Provisioning:** Uses PXE/iPXE to automatically install Debian on bare-metal machines.
*   **Layer 2: System Configuration (Ansible):** Configures the base Debian installs into a functional, cohesive cluster.
*   **Layer 3: Application Orchestration (Nomad & Consul):** Deploys, manages, and scales the various services that make up the AI agent.
*   **Layer 4: The AI Application Stack:** The core Python application that constitutes the agent itself, built on the `pipecat` framework.
*   **Layer 5: Web UI & Control Plane:** A FastAPI and WebSocket-based web UI for real-time monitoring and interaction.
*   **Layer 6: External API Gateway:** Exposes the cluster's capabilities via an OpenAI-compatible REST API.
*   **Layer 7: Self-Adaptation Loop:** A closed-loop feedback system that allows the agent to learn from its own failures and autonomously improve its core programming.

The core of the application is the `TwinService`, which acts as the agent's "brain." It orchestrates the agent's responses, memory, and tool use. The agent can use a variety of tools, including `ssh`, a sandboxed `code_runner`, `ansible`, and a `vision` tool that uses YOLOv8 for real-time object detection. The system also features a Mixture of Experts (MoE) routing model, allowing the main agent to delegate queries to specialized backend experts.

## Building and Running

### Single-Node Setup (Bootstrap)

For development, testing, or bootstrapping the first node of a new cluster, use the provided bootstrap script.

```bash
./bootstrap.sh
```

This script configures the local machine as a fully-functional, standalone agent and control node.

### Multi-Node Cluster Provisioning

For a multi-node cluster, you will need to work with the Ansible inventory directly.

1.  **Configure Initial Inventory (`inventory.yaml`):** Define your initial controller nodes in the `inventory.yaml` file.
2.  **Run the Main Playbook:**

    ```bash
    ansible-playbook -i inventory.yaml playbook.yaml --ask-become-pass
    ```

### Testing and Verification

*   **Check Cluster Status:** `nomad node status`
*   **Check Job Status:** `nomad job status`
*   **View Logs:** `nomad alloc logs <allocation_id>` or use the Mission Control Web UI.
*   **Run Health Check:** `ansible-playbook run_health_check.yaml`

## Development Conventions

### Code Quality and Linting

The project uses a suite of linters to ensure code quality and consistency. To run all linters, use the following command:

```bash
npm run lint
```

### Prompt Engineering

The project includes a workflow for automatically improving the agent's core prompt using evolutionary algorithms. The workflow is as follows:

1.  **Define Test Cases:** Add or modify the YAML test cases in the `evaluation_suite/` directory.
2.  **Run the Evolution Script:**
    ```bash
    # Set your OpenAI API key
    export OPENAI_API_KEY="your-key-here"

    # Run the evolution process
    python prompt_engineering/evolve.py
    ```
3.  **Update the Agent:** Manually copy the new, improved prompt into the `get_system_prompt` method in `ansible/roles/pipecatapp/files/app.py`.
