Last updated: 2025-10-12

# Distributed Conversational AI Pipeline for Legacy CPU Clusters

This project provides a complete solution for deploying a high-performance, low-latency conversational AI pipeline on a cluster of legacy, resource-constrained desktop computers. It uses Ansible for automated provisioning, Nomad for cluster orchestration, and a state-of-the-art AI stack to create a responsive, streaming, and embodied voice agent. For a detailed technical description of the system's layers, see the [Holistic Project Architecture](ARCHITECTURE.md) document.

## 1. System Requirements

- **Cluster Nodes:** 3 to 20 legacy desktop computers (Intel Core 2 Duo or similar, 8GB RAM, SSD recommended).
- **Control Node:** A machine to run Ansible for provisioning.
- **Recommended OS:** Debian Trixie, minimal install with SSH server.

## 2. Initial Machine Setup

Setting up a new cluster involves two main methods: a one-time manual setup for the first node, and a fully automated setup for all subsequent nodes.

### 2.1. Manual Setup (First Node / PXE Server)

The first node in your cluster requires a manual OS installation. This node will later be configured by Ansible to act as the PXE/iPXE boot server for all other nodes.

1. **Install Debian Trixie:** Perform a standard, minimal installation of Debian Trixie with an SSH server.
2. **Clone this repository:** `git clone <repo_url>`
3. **Configure Initial Settings:** Enter the `initial-setup` directory and edit the `setup.conf` file. You must provide the machine's desired `HOSTNAME`, a static IP address, and the `CONTROL_NODE_IP` (which should be the static IP of this same machine, as it will become the control node).
4. **Run Setup Script:** Execute the script with root privileges: `sudo bash setup.sh`
5. **Reboot.**

After rebooting, this node is ready for Ansible provisioning (see Section 3). It should be designated as both a `controller_node` and your `pxe_server` in the Ansible inventory.

### 2.2. Automated Setup (All Other Nodes)

Once your first node has been provisioned by Ansible and the `pxe_server` role has been applied to it, you can automatically install Debian on all other bare-metal machines in your cluster.

This system uses an advanced iPXE-over-HTTP method that is significantly faster and more reliable than traditional PXE. For detailed instructions on how to apply the Ansible role and prepare the client machines for network booting, see the **[iPXE Boot Server Setup Guide](PXE_BOOT_SETUP.md)**.

## 3. Easy Bootstrap (Single-Server Setup)

For development, testing, or bootstrapping the very first node of a new cluster, you can use the provided bootstrap script. This is the recommended method for getting started.

1. **On your control node, install Ansible and Git:** `sudo apt install ansible git -y`
2. **Clone this repository.**
3. **Run the Bootstrap Script:**
    This script handles all the necessary steps to configure the local machine as a fully-functional, standalone agent and control node.

    ```bash
    ./bootstrap.sh
    ```

    - **What this does:** The script invokes Ansible with a special inventory file (`local_inventory.ini`) that targets only the local machine. It installs and configures all necessary system components (Consul, Nomad, Docker) and deploys the AI agent services.
    - You will be prompted for your `sudo` password, as the script needs administrative privileges to install and configure software.

This single node is now ready to be used as a standalone conversational AI agent. It can also serve as the primary "seed" node for a larger cluster. To expand your cluster, see the advanced guide below.

## 4. Advanced: Multi-Node Cluster Provisioning

If you are setting up a multi-node cluster, you will need to work with the Ansible inventory directly.

1. **Configure Initial Inventory (`inventory.yaml`):** Edit the `inventory.yaml` file to define your *initial* controller nodes. While new worker nodes will be added to the cluster automatically, you must define the initial seed nodes for the control plane here.
    - Create a *host group* named `controller_nodes`. This group must contain at least one node that will act as the primary control node and Nomad server.
    - Create an empty *host group* named `worker_nodes`. This group will be populated automatically as new nodes join the cluster.
2. **Run the Main Playbook:**
    Run the following command from the root of this repository. This will configure the initial control node(s) and prepare the cluster for auto-expansion.

    ```bash
    ansible-playbook -i inventory.yaml playbook.yaml --ask-become-pass
    ```

    - **`--ask-become-pass`**: This flag is important. It will prompt you for your `sudo` password, which Ansible needs to perform administrative tasks.
    - **What this does:** This playbook not only aconfigures the cluster services (Consul, Nomad, etc.) but also automatically bootstraps the primary control node into a fully autonomous AI agent by deploying the necessary AI services.

## 5. Expanding the Control Plane (Adding Controllers)

This cluster is designed for resilience and scalability. As your needs grow, you may need to add more controller nodes to the control plane for higher availability. This process is fully automated.

**To promote an existing worker node to a controller:**

1. **Ensure the worker is part of the cluster:** The node you wish to promote must already be a provisioned worker and visible in `nomad node status`.
2. **Run the promotion playbook:**

    ```bash
    ansible-playbook promote_controller.yaml
    ```

3. **Enter the hostname:** You will be prompted to enter the exact hostname of the worker node you want to promote (e.g., `worker1`).

The playbook will handle everything:

- It safely modifies the `inventory.yaml` file to move the node from the `workers` group to the `controller_nodes` group.
- It stops the services on the target node, cleans up the old worker-specific state, and re-runs the `consul` and `nomad` configuration roles to re-provision it as a server.
- The node will automatically rejoin the cluster as a controller, strengthening the control plane.

## 6. Agent Architecture: The `TwinService`

The core of this application is the `TwinService`, a custom service that acts as the agent's "brain." It orchestrates the agent's responses, memory, and tool use.

### 6.1. Memory

- **Short-Term:** Remembers the last 10 conversational turns in a simple list.
- **Long-Term:** Uses a FAISS vector store (`long_term_memory.faiss`) to remember key facts. It performs a semantic search over this memory to retrieve relevant context for new conversations.

### 6.2. Tool Use

The agent can use tools to perform actions and gather information. The `TwinService` dynamically provides the list of available tools to the LLM in its prompt, enabling the LLM to decide which tool to use based on the user's query.

#### Available Tools

- **Vision (`vision.get_observation`)**: Gets a real-time description of what is visible in the webcam, powered by the Moondream2 model.
- **Master Control Program (`mcp.*`)**: Provides agent introspection and self-control, allowing it to check pipeline status (`get_status`) and manage memory (`get_memory_summary`, `clear_short_term_memory`).
- **SSH (`ssh.run_command`)**: Executes a command on a remote machine via SSH, using key-based or password authentication.
- **Code Runner (`code_runner.run_python_code`)**: Executes Python code in a secure, sandboxed Docker container.
- **Ansible (`ansible.run_playbook`)**: Runs an Ansible playbook to configure and manage the cluster.
- **Web Browser (`web_browser.*`)**: Provides a full web browser (via Playwright) for navigating (`goto`), reading (`get_page_content`), and interacting with websites (`click`, `type`).
- **Power (`power.set_idle_threshold`)**: Controls the cluster's power management policies by setting service idle thresholds.
- **Summarizer (`summarizer.get_summary`)**: Performs an extractive summary of the conversation to find the most relevant points related to a query.

### 6.3. Mixture of Experts (MoE) Routing

The agent is designed to function as a "Mixture of Experts." The primary `pipecat` agent acts as a router, classifying the user's query and routing it to a specialized backend expert if appropriate.

- **How it Works:** The `TwinService` prompt instructs the main agent to first classify the user's query. If it determines the query is best handled by a specialist (e.g., a 'coding' expert), it uses the `route_to_expert` tool. This tool call is intercepted by the `TwinService`, which then discovers the expert's API endpoint via Consul and forwards the query.
- **Configuration:** Deploying these specialized experts is done using the `deploy_expert.yaml` Ansible playbook. For detailed instructions, see the [Advanced AI Service Deployment](#72-advanced-deploying-additional-ai-experts) section below.

### 6.4. Configuring Agent Personas

The personality and instructions for the main router agent and each expert agent are defined in simple text files located in the `ansible/roles/pipecatapp/files/prompts/` directory. You can edit these files to customize the behavior of each agent. For example, you can edit `coding_expert.txt` to give it a different programming specialty.

## 7. AI Service Deployment

The system is designed to be self-bootstrapping. The `bootstrap.sh` script (or the main `playbook.yaml`) handles the deployment of the core AI services on the primary control node. This includes a default instance of the `llama-expert` job and the `pipecat` voice agent.

### 7.1. Start, Restart, or "Heal" Your Core Services

If a job has been stopped, or you just want to verify that everything is running as it should be, you now use your new, lightweight playbook. It will skip all the system setup and only manage the Nomad jobs.

```bash
ansible-playbook heal_cluster.yaml
```

If you make a change to a job file or need to restart the services from a clean state, it's best to purge the old jobs before running the start script again.

```bash
nomad job stop -purge llamacpp-rpc
nomad job stop -purge pipecat-app
```

### 7.2. Advanced: Deploying Additional AI Experts

The true power of this architecture is the ability to deploy multiple, specialized AI experts that the main `pipecat` agent can route queries to. With the new unified `llama-expert.nomad` job template, deploying a new expert is handled through a dedicated Ansible playbook.

1. **Define a Model List for Your Expert:**
    First, open `group_vars/models.yaml` and create a new list of models for your expert. For example, to create a `creative-writing` expert, you could add:

    ```yaml
    creative_writing_models:
      - name: "phi-3-mini-instruct"
        # ... other model details
    ```

2. **Deploy the Expert with Ansible:**
    Use the `deploy_expert.yaml` playbook to render the Nomad job with your custom parameters and launch it. You pass variables on the command line using the `-e` flag.

    - **Example: Deploying a `creative-writing` expert to the `creative` namespace:**

      ```bash
      ansible-playbook deploy_expert.yaml -e "job_name=creative-expert service_name=llama-api-creative namespace=creative model_list={{ creative_writing_models }} worker_count=2"
      ```

The `TwinService` in the `pipecatapp` will automatically discover any service registered in Consul with the `llama-api-` prefix and make it available for routing.

## 8. Advanced System Features

### 8.1. Power Management

To optimize resource usage on legacy hardware, this project includes an intelligent power management system.

- **How it Works:** A Python service, `power_agent.py`, uses an eBPF program (`traffic_monitor.c`) to monitor network traffic to specific services at the kernel level with minimal overhead.
- **Sleep/Wake:** If a monitored service is idle for a configurable period, the power agent automatically stops the corresponding Nomad job. When new traffic is detected, the agent restarts the job.
- **Configuration:** The agent can configure this behavior using the `power.set_idle_threshold` tool.

### 8.2. Mission Control Web UI

This project includes a web-based dashboard for real-time display and debugging. To access it, navigate to the IP address of any node in your cluster on port 8000 (e.g., `http://192.168.1.101:8000`). The UI provides:

- Real-time conversation logs.
- A request-approval interface for sensitive tool actions.
- The ability to save and load the agent's memory state.

## 9. Testing and Verification

- **Check Cluster Status:** `nomad node status`
- **Check Job Status:** `nomad job status`
- **View Logs:** `nomad alloc logs <allocation_id>` or use the Mission Control Web UI.

### Cluster Health Check

A dedicated health check job exists to verify the status of all running LLM experts. This provides a quick way to ensure the entire cluster is operational.

- **Run the check:** `ansible-playbook run_health_check.yaml`
- **View results:** `nomad job logs health-check`
- **Manual Test Scripts:** A set of scripts for manual testing of individual components is available in the `testing/` directory.

### 9.1. Code Quality and Linting

This project uses a suite of linters to ensure code quality and consistency. For detailed instructions on how to install the development dependencies and run the checks, please see the **[Linting Documentation](scripts/README.md)**.

To run all linters, use the following command:

```bash
npm run lint
```

## 10. Performance Tuning & Service Selection

- **Model Selection:** The `llama-expert.nomad` job is configured via Ansible variables in `group_vars/models.yaml`. You can define different model lists for different experts.
- **Network:** Wired gigabit ethernet is strongly recommended over Wi-Fi for reduced latency.
- **VAD Tuning:** The `RealtimeSTT` sensitivity can be tuned in `app.py` for better performance in noisy environments.
- **STT/TTS Service Selection:** You can choose which Speech-to-Text and Text-to-Speech services to use by setting environment variables in the `pipecatapp.nomad` job file.

## 11. Benchmarking

This project includes two types of benchmarks.

### 11.1. Real-Time Latency Benchmark

Measures the end-to-end latency of a live conversation. Enable it by setting `BENCHMARK_MODE = "true"` in the `env` section of the `pipecatapp.nomad` job file. Results are printed to the job logs.

### 11.2. Standardized Performance Benchmark

Uses `llama-bench` to measure the raw inference speed (tokens/sec) of the deployed LLM backend. Run the `benchmark.nomad` job to test the performance of the default model.

```bash
nomad job run /opt/nomad/jobs/benchmark.nomad
```

View results in the job logs: `nomad job logs llama-benchmark`

## 12. Advanced Development: Prompt Evolution

For advanced users, this project includes a workflow for automatically improving the agent's core prompt using evolutionary algorithms. See `prompt_engineering/PROMPT_ENGINEERING.md` for details.