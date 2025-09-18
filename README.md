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

1.  **Install Debian Trixie:** Perform a standard, minimal installation of Debian Trixie with an SSH server.
2.  **Clone this repository:** `git clone <repo_url>`
3.  **Configure Initial Settings:** Enter the `initial-setup` directory and edit the `setup.conf` file. You must provide the machine's desired `HOSTNAME`, a static IP address, and the `CONTROL_NODE_IP` (which should be the static IP of this same machine, as it will become the control node).
4.  **Run Setup Script:** Execute the script with root privileges: `sudo bash setup.sh`
5.  **Reboot.**

After rebooting, this node is ready for Ansible provisioning (see Section 3). It should be designated as both a `controller_node` and your `pxe_server` in the Ansible inventory.

### 2.2. Automated Setup (All Other Nodes)

Once your first node has been provisioned by Ansible and the `pxe_server` role has been applied to it, you can automatically install Debian on all other bare-metal machines in your cluster.

This system uses an advanced iPXE-over-HTTP method that is significantly faster and more reliable than traditional PXE. For detailed instructions on how to apply the Ansible role and prepare the client machines for network booting, see the **[iPXE Boot Server Setup Guide](PXE_BOOT_SETUP.md)**.

## 3. Easy Bootstrap (Single-Server Setup)

For development, testing, or bootstrapping the very first node of a new cluster, you can use the provided bootstrap script. This is the recommended method for getting started.

1.  **On your control node, install Ansible and Git:** `sudo apt install ansible git -y`
2.  **Clone this repository.**
3.  **Run the Bootstrap Script:**
    This script handles all the necessary steps to configure the local machine as a fully-functional, standalone agent and control node.
    ```bash
    ./bootstrap.sh
    ```
    - **What this does:** The script invokes Ansible with a special inventory file (`local_inventory.ini`) that targets only the local machine. It installs and configures all necessary system components (Consul, Nomad, Docker) and deploys the AI agent services.
    - You will be prompted for your `sudo` password, as the script needs administrative privileges to install and configure software.

This single node is now ready to be used as a standalone conversational AI agent. It can also serve as the primary "seed" node for a larger cluster. To expand your cluster, see the advanced guide below.

## 4. Advanced: Multi-Node Cluster Provisioning
If you are setting up a multi-node cluster, you will need to work with the Ansible inventory directly.

1.  **Configure Initial Inventory (`inventory.yaml`):** Edit the `inventory.yaml` file to define your *initial* controller nodes. While new worker nodes will be added to the cluster automatically, you must define the initial seed nodes for the control plane here.
    - Create a *host group* named `controller_nodes`. This group must contain at least one node that will act as the primary control node and Nomad server.
    - Create an empty *host group* named `worker_nodes`. This group will be populated automatically as new nodes join the cluster.
2.  **Run the Main Playbook:**
    Run the following command from the root of this repository. This will configure the initial control node(s) and prepare the cluster for auto-expansion.
    ```bash
    ansible-playbook -i inventory.yaml playbook.yaml --ask-become-pass
    ```
    - **`--ask-become-pass`**: This flag is important. It will prompt you for your `sudo` password, which Ansible needs to perform administrative tasks.
    - **What this does:** This playbook not only configures the cluster services (Consul, Nomad, etc.) but also automatically bootstraps the primary control node into a fully autonomous AI agent by deploying the necessary AI services.

## 4. AI Service Deployment
The system is designed to be self-bootstrapping. Once the main Ansible playbook has been run on the primary control node, the AI agent is deployed automatically.

### 4.1. Automated Agent Deployment
The `bootstrap_agent` role in the Ansible playbook handles the automatic deployment of the core AI services on the primary control node. This includes:
- **`llama.cpp` RPC Service:** The primary LLM backend for the agent.
- **`pipecat` Voice Agent:** The main application that orchestrates the agent's logic, memory, and tool use.

You can monitor the status of these services by running `nomad job status` on the control node.

Use the provided script to submit the core AI jobs to Nomad:
```bash
./start_services.sh

### 4.2. Advanced: Deploying Additional AI Experts
For advanced use cases, such as the Mixture-of-Experts (MoE) routing described in the Agent Architecture section, you may want to deploy additional, specialized LLM backends. You can do this manually using the Nomad CLI.

- **Example: Deploying a `prima.cpp` cluster for coding tasks:**
  ```bash
  # First, create a new namespace for the expert
  nomad namespace apply coding

  # Deploy the job to the new namespace, passing variables with -var
  nomad job run -namespace=coding \
    -var "job_name=prima-coding-expert" \
    -var "service_name=llama-api-coding" \
    -var "model_path=/path/to/coding.gguf" \
    /home/user/primacpp.nomad
  ```
The `TwinService` will automatically discover these new experts via Consul and make them available for routing.

## 5. Agent Architecture: The `TwinService`
The core of this application is the `TwinService`, a custom service that acts as the agent's "brain." It orchestrates the agent's responses, memory, and tool use.

### 5.1. Memory
- **Short-Term:** Remembers the last 10 conversational turns.
- **Long-Term:** Uses a FAISS vector store (`long_term_memory.faiss`) to remember key facts. It performs a semantic search over this memory to retrieve relevant context for new conversations.

### 5.2. Tool Use
The agent can use tools to perform actions and gather information. The `TwinService` dynamically provides the list of available tools to the LLM in its prompt, enabling the LLM to decide which tool to use based on the user's query.

#### Available Tools:
- **Vision (`vision.get_observation`)**
  - **Description:** Gets a real-time description of what is visible in the webcam.
  - **Requires:** A USB webcam connected to the node running the `pipecat-app` job.
  - **Example:** "What do you see?"
- **Master Control Program (`mcp.get_status`, `mcp.get_memory_summary`, etc.)**
  - **Description:** A tool for introspection and self-control.
  - **Examples:** "MCP, what is your status?", "Summarize your memory."
- **SSH (`ssh.run_command`)**
  - **Description:** Executes a command on a remote machine via SSH.
  - **Security Warning:** This is a very powerful tool. The credentials are not stored in the code but must be provided by the LLM. For this to work, the user running the agent must have an SSH key configured that allows passwordless access to the target machine. Exercise caution when enabling the LLM to use this tool.
  - **Example:** "Use ssh to run 'ls -l' on host 192.168.1.102 with user 'admin'."
- **Code Runner (`code_runner.run_python_code`)**
  - **Description:** Executes a block of Python code in a secure, sandboxed Docker container and returns the output.
  - **Note:** The Docker engine is installed automatically by the Ansible playbook.
  - **Example:** "Use the code runner to calculate the 100th Fibonacci number."
- **Ansible (`ansible.run_playbook`)**
  - **Description:** Runs an Ansible playbook to provision or manage nodes in the cluster. This is the primary tool for cluster self-management and expansion.
  - **Security Warning:** This is an extremely powerful tool that can make significant changes to the cluster. It is marked as a sensitive tool and requires user approval in the web UI if `APPROVAL_MODE` is enabled.
  - **Example:** "Use ansible to run the main playbook and limit it to the host 'AID-E-26'."
- **Web Browser (`web_browser.goto`, `web_browser.get_page_content`, etc.)**
  - **Description:** A tool for browsing the web.
  - **Examples:** "Use the web browser to go to google.com and tell me the content of the page."

### 5.3. Mixture of Experts (MoE) Routing
The agent is designed to function as a "Mixture of Experts." The primary LLM acts as a router, classifying the user's query and routing it to a specialized backend if appropriate.

- **How it Works:** The `TwinService` prompt instructs the router LLM to first decide if a query is general, technical, or creative. If it's technical, for example, the router's job is to call the `route_to_coding_expert` tool. The `TwinService` then sends the query to a separate LLM cluster that is running a coding-specific model.
- **Configuration:** To use this feature, you must deploy multiple LLM backends into their own isolated namespaces using the `-var` flag to customize them.
  - **Example:**
    ```bash
    # Create the namespaces
    nomad namespace apply general
    nomad namespace apply coding

    # Deploy a general-purpose model
    nomad job run -namespace=general \
      -var "job_name=prima-general-expert" \
      -var "service_name=llama-api-general" \
      -var "model_path=/path/to/general.gguf" \
      /home/user/primacpp.nomad

    # Deploy a coding model
    nomad job run -namespace=coding \
      -var "job_name=prima-coding-expert" \
      -var "service_name=llama-api-coding" \
      -var "model_path=/path/to/coding.gguf" \
      /home/user/primacpp.nomad
    ```
  - The `TwinService` discovers these experts across all namespaces using Consul.

### 5.4. Configuring Agent Personas
The personality and instructions for the main router agent and each expert agent are defined in simple text files located in the `ansible/roles/pipecatapp/files/prompts/` directory. You can edit these files to customize the behavior of each agent. For example, you can edit `coding_expert.txt` to give it a different programming specialty.

## 6. Mission Control Web UI
This project includes a web-based dashboard for real-time display and debugging.

### 6.1. Accessing the UI
Once the `pipecat-app` job is running, you can access the UI by navigating to the IP address of any node in your cluster on port 8000. For example: `http://192.168.1.101:8000`.

### 6.2. Features
- **Live Terminal:** The main feature is a retro-style web terminal that provides a live stream of the agent's logs.
- **LLM-Driven Visualizations:** The agent can use the terminal to display information in creative ways. For example, status updates may be rendered as large, colorful banners using `figlet` and `lolcat` style effects.
- **Status API:** An API endpoint at `/api/status` provides the real-time status of the agent's pipelines.

### 6.3. Advanced Features
The Mission Control UI and the agent have several advanced features for power users.

#### Debug Mode
To get more detailed insight into the agent's operations, you can enable Debug Mode.
- **How to Enable:** In the `pipecatapp.nomad` job file, set the `DEBUG_MODE` environment variable to `"true"`.
- **Functionality:** When enabled, the agent will produce verbose logs for every tool call, including the result returned by the tool. This is useful for debugging tool behavior.

#### Interactive Action Approval
For enhanced safety, you can run the agent in a mode that requires manual approval for sensitive actions.
- **How to Enable:** In the `pipecatapp.nomad` job file, set the `APPROVAL_MODE` environment variable to `"true"`.
- **Functionality:** When enabled, any attempt to use a sensitive tool (like `ssh` or `code_runner`) will pause execution. A prompt will appear in the web UI with details of the action. You must click "Approve" for the action to proceed. If you click "Deny", the action is cancelled, and the agent will respond that it was not permitted to perform the action.

#### State Management
You can save and load the agent's complete memory state (both short-term and long-term) directly from the web UI.
- **How to Use:**
  1.  In the header of the Mission Control UI, enter a name for your session in the "Enter save name..." input box.
  2.  Click **"Save State"** to create a snapshot of the agent's current memory. The state will be saved on the server in the `saved_states/` directory.
  3.  To restore a previous session, enter the name of the saved state and click **"Load State"**. This will replace the agent's current memory with the saved version.

## 7. Testing and Verification
- **Check Cluster Status:** `nomad node status`
- **Check Job Status:** `nomad job status`
- **View Logs:** `nomad job logs <job_name>` (e.g., `pipecatapp`, `prima-cluster`) or use the Mission Control Web UI.
- **Manual Test Scripts:** A set of scripts for manual testing of individual components is available in the `testing/` directory.

## 8. Performance Tuning & Service Selection
- **Model Selection:** The `prima.cpp` and `llamacpp-rpc` Nomad jobs are configured to use a placeholder model path. You will need to edit the job files to point to the GGUF model you want to use. Smaller models (3B, 7B) are recommended for better performance.
- **Network:** Wired gigabit ethernet is strongly recommended over Wi-Fi for reduced latency.
- **VAD Tuning:** The `RealtimeSTT` sensitivity can be tuned in `app.py` for better performance in noisy environments.
- **STT/TTS Service Selection:** You can choose which Speech-to-Text and Text-to-Speech services to use by setting environment variables in the `pipecatapp.nomad` job file.
  - `STT_SERVICE`: Set to `faster-whisper` for high-performance local transcription, or `deepgram` (default) to use the Deepgram API.
  - `TTS_SERVICE`: Set to `kittentts` for a fast, local TTS, or `elevenlabs` (default) to use the ElevenLabs API.
  - `EMBEDDING_MODEL_NAME`: Selects the sentence transformer model for the agent's long-term memory. Defaults to `all-MiniLM-L6-v2`. A good alternative is `google/embeddinggemma-300m`.

## 9. Benchmarking
This project includes two types of benchmarks.

### 9.1. Real-Time Latency Benchmark
Measures the end-to-end latency of a live conversation. Enable it by setting `BENCHMARK_MODE = "true"` in the `env` section of the `pipecatapp.nomad` job file. Results are printed to the job logs.

### 9.2. Standardized Performance Benchmark
Uses `llama-bench` to measure the raw inference speed (tokens/sec) of the deployed LLM backend.
1. Ensure an LLM backend is running.
2. Run the benchmark job, passing the path to your desired GGUF model using the `-var` flag:
   ```bash
   nomad job run -var "model_path=/path/to/your/model.gguf" /home/user/benchmark.nomad
   ```
3. View results in the job logs: `nomad job logs llama-benchmark`

## 10. Advanced Development: Prompt Evolution
For advanced users, this project includes a workflow for automatically improving the agent's core prompt using evolutionary algorithms. See `prompt_engineering/PROMPT_ENGINEERING.md` for details.
