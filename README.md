# Distributed Conversational AI Pipeline for Legacy CPU Clusters

Last updated: 2025-11-26

This project provides a complete solution for deploying a high-performance, low-latency conversational AI pipeline on a cluster of legacy, resource-constrained desktop computers. It uses Ansible for automated provisioning, Nomad for cluster orchestration, and a state-of-the-art AI stack to create a responsive, streaming, and embodied voice agent. For a detailed technical description of the system's layers, see the [Holistic Project Architecture](ARCHITECTURE.md) document.

## 1. System Requirements

- **Cluster Nodes:** 3 to 20 legacy desktop computers (Intel Core 2 Duo or similar, 8GB RAM, SSD recommended).
- **Control Node:** A machine to run Ansible for provisioning.
- **Recommended OS:** Debian Trixie, minimal install with SSH server.

## 2. Project Structure

A brief overview of the key directories in this repository:

- **/ansible**: Contains all Ansible playbooks, roles, and templates for provisioning and deploying the entire system.
  - **/ansible/roles**: Individual, reusable components for managing specific parts of the system (e.g., `nomad`, `consul`, `pipecatapp`).
  - **/ansible/roles/pipecatapp/files**: The core Python source code for the conversational agent, including `app.py`, `memory.py`, and the `tools` directory.
- **/prompt_engineering**: Scripts and tools for evaluating and improving the AI's prompts using evolutionary algorithms.
- **/reflection**: Scripts related to the agent's self-reflection and self-healing capabilities.
- **/scripts**: Utility and linting scripts for maintaining code quality.
- **/testing**: Contains unit and integration tests for the various components of the project.
- **/*.yaml**: Top-level Ansible playbook files (e.g., `playbook.yaml`, `heal_cluster.yaml`).
- **/group_vars**: Ansible configuration files that apply to all hosts, such as `all.yaml` and `models.yaml`.

## 3. Initial Machine Setup

Setting up a new cluster involves two main methods: a one-time manual setup for the first node, and a fully automated setup for all subsequent nodes.

### 3.1. Manual Setup (First Node / PXE Server)

The first node in your cluster requires a manual OS installation. This node will later be configured by Ansible to act as the PXE/iPXE boot server for all other nodes.

1. **Install Debian Trixie:** Perform a standard, minimal installation of Debian Trixie with an SSH server.
2. **Clone this repository:** `git clone <repo_url>`
3. **Configure Initial Settings:** Enter the `initial-setup` directory and edit the `setup.conf` file. You must provide the machine's desired `HOSTNAME`, a static IP address, and the `CONTROL_NODE_IP` (which should be the static IP of this same machine, as it will become the control node).
4. **Run Setup Script:** Execute the script with root privileges: `sudo bash setup.sh`
5. **Reboot.**

After rebooting, this node is ready for Ansible provisioning (see Section 4). It should be designated as both a `controller_node` and your `pxe_server` in the Ansible inventory.

### 3.2. Automated Setup (All Other Nodes)

Once your first node has been provisioned by Ansible and the `pxe_server` role has been applied to it, you can automatically install Debian on all other bare-metal machines in your cluster.

This system uses an advanced iPXE-over-HTTP method that is significantly faster and more reliable than traditional PXE. For detailed instructions on how to apply the Ansible role and prepare the client machines for network booting, see the **[iPXE Boot Server Setup Guide](PXE_BOOT_SETUP.md)**.

## 4. Easy Bootstrap (Single-Server Setup)

For development, testing, or bootstrapping the very first node of a new cluster, you can use the provided bootstrap script. This is the recommended method for getting started.

1. **On your control node, install Git:** `sudo apt install git -y`
2. **Clone this repository.**
3. **Run the Bootstrap Script:**
   This script is a powerful wrapper around Ansible that handles all necessary steps to configure the local machine as a fully-functional, standalone agent, a cluster controller, or a new worker node.

   **Basic Usage:**

   ```bash
   ./bootstrap.sh
   ```

   - **What this does:** By default, the script runs the complete end-to-end process to configure the local machine as a standalone agent and control node. It invokes a series of Ansible playbooks that install and configure all necessary system components (Consul, Nomad, Docker) and deploy the AI agent services.
   - You will be prompted for your `sudo` password, as the script needs administrative privileges to install and configure software.

   **Common Flags for Customizing the Bootstrap Process:**

   You can control the behavior of the bootstrap script with the following flags:

   - `--role <role>`: Specify the role for the node.
     - `all` (default): Full setup for a standalone control node.
     - `controller`: Sets up only the core infrastructure services (Consul, Nomad, etc.).
     - `worker`: Configures the node as a worker and requires `--controller-ip`.
   - `--controller-ip <ip>`: The IP address of the main controller node. **Required** when `--role` is `worker`.
   - `--tags <tag1,tag2>`: Run only specific parts of the Ansible playbook (e.g., `--tags nomad` would only run the Nomad configuration tasks).
   - `--external-model-server`: Skips the download and build steps for large language models. This is ideal for development or if you are using a remote model server.
   - `--purge-jobs`: Stops and purges all running Nomad jobs before starting the bootstrap process, ensuring a clean deployment.
   - `--clean`: **Use with caution.** This will permanently delete all untracked files in the repository (`git clean -fdx`), restoring it to a pristine state.
   - `--debug`: Enables verbose Ansible logging (`-vvvv`) and saves the full output to `playbook_output.log`.
   - `--continue`: If a previous bootstrap run failed, this flag will resume the process from the last successfully completed playbook, saving significant time.

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

- **SSH (`ssh`)**: Executes commands on remote machines.
- **Master Control Program (`mcp`)**: Provides agent introspection and self-control (e.g., status checks, memory management).
- **Vision (`vision`)**: Gets a real-time description of what is visible via the webcam.
- **Desktop Control (`desktop_control`)**: Provides full control over the desktop environment, including taking screenshots and performing mouse/keyboard actions.
- **Code Runner (`code_runner`)**: Executes Python code in a secure, sandboxed environment.
- **Smol Agent (`smol_agent_computer`)**: A tool for creating small, specialized agents.
- **Web Browser (`web_browser`)**: Enables web navigation and content interaction.
- **Ansible (`ansible`)**: Runs Ansible playbooks to manage the cluster.
- **Power (`power`)**: Controls the cluster's power management policies.
- **Term Everything (`term_everything`)**: Provides a terminal interface for interacting with the system.
- **RAG (`rag`)**: Searches the project's documentation to answer questions.
- **Home Assistant (`ha`)**: Controls smart home devices via Home Assistant.
- **Git (`git`)**: Interacts with Git repositories.
- **Orchestrator (`orchestrator`)**: Dispatches high-priority, complex jobs to the cluster.
- **LLxprt Code (`llxprt_code`)**: A specialized tool for code-related tasks.
- **Claude Clone (`claude_clone`)**: A tool for interacting with a Claude-like model.
- **Final Answer (`final_answer`)**: A tool to provide a final answer to the user.
- **Shell (`shell`)**: Executes shell commands.
- **Prompt Improver (`prompt_improver`)**: A tool for improving prompts.
- **Summarizer (`summarizer`)**: Summarizes conversation history (enabled via config).

### 6.3. Mixture of Experts (MoE) Routing

The agent is designed to function as a "Mixture of Experts." The primary `pipecat` agent acts as a router, classifying the user's query and routing it to a specialized backend expert if appropriate.

- **How it Works:** The `TwinService` prompt instructs the main agent to first classify the user's query. If it determines the query is best handled by a specialist (e.g., a 'coding' expert), it uses the `route_to_expert` tool. This tool call is intercepted by the `TwinService`, which then discovers the expert's API endpoint via Consul and forwards the query.
- **Configuration:** Deploying these specialized experts is done using the `deploy_expert.yaml` Ansible playbook. For detailed instructions, see the [Advanced AI Service Deployment](#82-advanced-deploying-additional-ai-experts) section below.

### 6.4. Configuring Agent Personas

The personality and instructions for the main router agent and each expert agent are defined in simple text files located in the `ansible/roles/pipecatapp/files/prompts/` directory. You can edit these files to customize the behavior of each agent. For example, you can edit `coding_expert.txt` to give it a different programming specialty.

## 7. Interacting with the Agent

There are two primary ways to interact with the conversational agent: the web interface and the Gemini CLI extension.

### 7.1. Web Interface

Navigate to the IP address of any node in your cluster on port 8000 (e.g., `http://192.168.1.101:8000`). The web UI provides real-time conversation logs, a request-approval interface, and the ability to save and load the agent's memory state.

### 7.2. Gemini CLI Extension

For command-line users, a Gemini CLI extension is provided to send messages directly to the agent.

#### 7.2.1. First-Time Setup

1. **Install the Gemini CLI:**

   ```bash
   npm install -g @google/gemini-cli
   ```

2. **Navigate to the extension directory:**

   ```bash
   cd pipecat-agent-extension
   ```

3. **Install dependencies and build the extension:**

   ```bash
   npm install
   npm run build
   ```

4. **Link the extension to your Gemini CLI installation:**

   ```bash
   gemini extensions link .
   ```

#### 7.2.2. Sending a Message

Once the extension is linked, you can use the custom `/pipecat:send` command to send a message to the agent:

```bash
gemini /pipecat:send "Your message here"
```

**Example:**

```bash
gemini /pipecat:send "Can you write a python script to list files in a directory?"
```

The agent will process this message as if you had typed it in the web UI.

### 7.3. Infrastructure Dashboards

In addition to the agent's interface, you can access the dashboards for the underlying infrastructure services.

#### 7.3.1. Consul UI (Service Mesh & KV Store)

- **URL:** `http://<node_ip>:8500`
- **Login:** Access requires the **SecretID** (management token).
- **Retrieving the Token:** Run this command on your controller node:
  ```bash
  sudo cat /etc/consul.d/management_token
  ```

#### 7.3.2. Nomad UI (Cluster Orchestration)

- **URL:** `http://<node_ip>:4646`

## 8. AI Service Deployment

The system is designed to be self-bootstrapping. The `bootstrap.sh` script (or the main `playbook.yaml`) handles the deployment of the core AI services on the primary control node. This includes a default instance of the `llama-expert` job and the `pipecat` voice agent.

### 8.1. Start, Restart, or "Heal" Your Core Services

If a job has been stopped, or you just want to verify that everything is running as it should be, you now use your new, lightweight playbook. It will skip all the system setup and only manage the Nomad jobs.

```bash
ansible-playbook heal_cluster.yaml
```

If you make a change to a job file or need to restart the services from a clean state, it's best to purge the old jobs before running the start script again.

```bash
nomad job stop -purge llamacpp-rpc
nomad job stop -purge pipecat-app
```

### 8.2. Advanced: Deploying Additional AI Experts

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

## 9. Advanced System Features

### 9.1. Power Management

To optimize resource usage on legacy hardware, this project includes an intelligent power management system.

- **How it Works:** A Python service, `power_agent.py`, uses an eBPF program (`traffic_monitor.c`) to monitor network traffic to specific services at the kernel level with minimal overhead.
- **Sleep/Wake:** If a monitored service is idle for a configurable period, the power agent automatically stops the corresponding Nomad job. When new traffic is detected, the agent restarts the job.
- **Configuration:** The agent can configure this behavior using the `power.set_idle_threshold` tool.

### 9.2. Mission Control Web UI

This project includes a web-based dashboard for real-time display and debugging. To access it, navigate to the IP address of any node in your cluster on port 8000 (e.g., `http://192.168.1.101:8000`). The UI provides:

- Real-time conversation logs.
- A request-approval interface for sensitive tool actions.
- The ability to save and load the agent's memory state.

## 10. Testing and Verification

- **Check Cluster Status:** `nomad node status`
- **Check Job Status:** `nomad job status`
- **View Logs:** `nomad alloc logs <allocation_id>` or use the Mission Control Web UI.

### Cluster Health Check

A dedicated health check job exists to verify the status of all running LLM experts. This provides a quick way to ensure the entire cluster is operational.

- **Run the check:** `ansible-playbook run_health_check.yaml`
- **View results:** `nomad job logs health-check`
- **Manual Test Scripts:** A set of scripts for manual testing of individual components is available in the `testing/` directory.

### 10.1. Code Quality and Linting

This project uses a suite of linters to ensure code quality and consistency. For detailed instructions on how to install the development dependencies and run the checks, please see the **[Linting Documentation](scripts/README.md)**.

To run all linters, use the following command:

```bash
npm run lint
```

## 11. Performance Tuning & Service Selection

- **Model Selection:** The `llama-expert.nomad` job is configured via Ansible variables in `group_vars/models.yaml`. You can define different model lists for different experts.
- **Network:** Wired gigabit ethernet is strongly recommended over Wi-Fi for reduced latency.
- **VAD Tuning:** The `RealtimeSTT` sensitivity can be tuned in `app.py` for better performance in noisy environments.
- **STT/TTS Service Selection:** You can choose which Speech-to-Text and Text-to-Speech services to use by setting environment variables in the `pipecatapp.nomad` job file.

## 12. Benchmarking

This project includes two types of benchmarks.

### 12.1. Real-Time Latency Benchmark

Measures the end-to-end latency of a live conversation. Enable it by setting `BENCHMARK_MODE = "true"` in the `env` section of the `pipecatapp.nomad` job file. Results are printed to the job logs.

### 12.2. Standardized Performance Benchmark

Uses `llama-bench` to measure the raw inference speed (tokens/sec) of the deployed LLM backend. Run the `benchmark.nomad` job to test the performance of the default model.

```bash
nomad job run /opt/nomad/jobs/benchmark.nomad
```

View results in the job logs: `nomad job logs llama-benchmark`

## 13. Advanced Development: Prompt Evolution

For advanced users, this project includes a workflow for automatically improving the agent's core prompt using evolutionary algorithms. See `prompt_engineering/PROMPT_ENGINEERING.md` for details.

## 14. Project Roadmap

This section outlines the major feature enhancements and maintenance tasks planned for the future.

- **Implement Graceful LLM Failover:** Enhance the `llama-expert.nomad` job to include a final, lightweight fallback model to ensure the expert service always starts with a basic capability.
- **Re-evaluate Consul Connect Service Mesh:** Once the core system is stable, create a new feature branch to attempt to re-enable `sidecar_service` in the Nomad job files and document the process and performance overhead.
- **Add Pre-flight System Health Checks:** Create a new Ansible role to perform non-destructive checks (filesystem writability, disk space, network connection) at the beginning of the main playbook.
- **Investigate Advanced Power Management:** Research and prototype a more advanced power management system using Wake-on-LAN, triggered by the `power_agent.py`.
- **Security Hardening:**
  - Remove passwordless sudo and require a password for the `target_user`.
  - Audit all services to ensure they run as dedicated, non-privileged users.
- **Monitoring and Observability:** Deploy a monitoring stack like Prometheus and Grafana to collect and visualize metrics from Nomad, Consul, and the application itself.
- **Web UI/UX Improvements:**
  - Replace ASCII art with a more dynamic animated character.
  - Add a "Clear Terminal" button to the UI.
  - Improve the status display to be more readable than a raw JSON dump.
- **Bolster Automated Testing:**
  - Implement Ansible Molecule tests for critical roles.
  - Expand end-to-end tests in `e2e-tests.yaml` to verify core agent functions.
  - Increase unit test coverage for Python tools.

## 15. Troubleshooting

For solutions to common issues, such as failing Nomad service checks or deployment errors, please refer to the **[Troubleshooting Guide](docs/TROUBLESHOOTING.md)**.
