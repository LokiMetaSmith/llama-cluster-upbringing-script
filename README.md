using latest distro from https://www.crunchbangplusplus.org/#download

Username is user, password is a standard password

Bookworm 12.0 MD5 71d02a8e55627ce43e217724dc6de6c5

sudo -u munge ${sbindir}/mungekey --verbose creates the munge.key that will authenticate the cluster

copy the files to the home directory and run ./script.sh

This assumes the name of every computer is AID-E-# where # is a number 0-20, change the hostname to your expected cluster configuration name.

## Setting up Distributed Llama

This section guides you through setting up the `distributed-llama` project, which allows for distributed inference of large language models.

### Prerequisites

Before you begin, ensure you have the following installed on your system:
*   **Git:** Required for cloning the `distributed-llama` repository.
*   **C++ Compiler:** A C++ compiler such as GCC or Clang is needed to build the project from source.
*   **Python 3:** May be required for certain scripts or utilities within the `distributed-llama` project.

These tools are essential for obtaining the source code and compiling the `distributed-llama` executables.

### Installation Script

To simplify the setup process, a shell script named `setup_distributed_llama.sh` is provided. This script automates:
1.  Cloning the `distributed-llama` repository from GitHub (https://github.com/b4rtaz/distributed-llama.git).
2.  Compiling the core components: `dllama` (the main application) and `dllama-api` (the API server).

### How to Run

1.  Make sure the script is executable: `chmod +x setup_distributed_llama.sh` (The script also attempts to do this itself).
2.  Run the script:
    ```bash
    ./setup_distributed_llama.sh
    ```
The script will create a directory named `distributed-llama-repo` in the current location, clone the repository into it, and then compile the project. You will see output messages indicating the progress and any potential errors.

### Basic Usage (after setup)

Once the `setup_distributed_llama.sh` script completes successfully, the compiled executables (`dllama` and `dllama-api`) will be located in the `distributed-llama-repo` directory.

**To run the distributed Llama, you will generally need to:**
1.  Obtain a compatible model and tokenizer.
2.  Start worker nodes.
3.  Start a root (inference) node, connecting it to the workers.

**Example commands (these are illustrative and require model/tokenizer paths and worker IPs):**

*   **Run a worker node (inside `distributed-llama-repo` directory):**
    ```bash
    ./dllama worker --port 9999 --nthreads 4
    ```
*   **Run a root node for inference (inside `distributed-llama-repo` directory):**
    ```bash
    ./dllama inference --model <path_to_model_gguf> --tokenizer <path_to_tokenizer> --workers <worker_ip:port>
    ```
*   **Run the API server (inside `distributed-llama-repo` directory):**
    ```bash
    ./dllama-api --model <path_to_model_gguf> --tokenizer <path_to_tokenizer> --host 0.0.0.0 --port 8080
    ```

**For detailed instructions** on model conversion, configuring and running a cluster with multiple workers, and other advanced usage, please refer to the official documentation within the `distributed-llama-repo` directory (look for a README or other documentation files) or visit the project's GitHub page: https://github.com/b4rtaz/distributed-llama.

### Running `llama-server` with RPC using `run.sh`

The `run.sh` script has been updated to facilitate running `llama-server` with RPC enabled. This allows for distributing the workload across multiple machines.

**Configuration:**

The `run.sh` script contains a commented-out command for `llama-server`. Before running it, you need to configure several placeholder variables:

*   `MODEL_PATH`: Path to your GGUF model file.
    *   Example: `MODEL_PATH="models/L3.3-Q4_K_M.gguf"`
*   `RPC_HOSTS`: Comma-separated list of your RPC server addresses and ports. These are the machines that will participate in the distributed inference.
    *   Example: `RPC_HOSTS="192.168.1.19:50052,192.168.1.15:50052"`
*   `CONTEXT_SIZE`: The size of the prompt context window.
    *   Example: `CONTEXT_SIZE=16384`
*   `N_GPU_LAYERS`: The number of model layers to offload to the GPU(s).
    *   Example: `N_GPU_LAYERS=200`
*   `OTHER_ARGS`: Any other additional arguments you want to pass to `llama-server`.
    *   Example: `OTHER_ARGS="--flash-attn --split-mode row --threads 12 --tensor-split 13,13,24"`

**How to Run:**

1.  **Edit `run.sh`**: Open the `run.sh` script in a text editor.
2.  **Set Variables**: Locate the commented-out `llama-server` section and update the placeholder variables (`MODEL_PATH`, `RPC_HOSTS`, `CONTEXT_SIZE`, `N_GPU_LAYERS`, `OTHER_ARGS`) with your specific configuration.
3.  **Uncomment Command**: Uncomment the line that starts with `llama-server -m "$MODEL_PATH" ...`
4.  **Make `run.sh` executable**: If you haven't already, run `chmod +x run.sh`.
5.  **Execute the script**:
    ```bash
    ./run.sh
    ```

This will start the `llama-server` with your specified configuration, enabling distributed inference via RPC. The script also reminds you to edit it if the default commented command is detected.

## Load Balancing with Paddler for llama.cpp

This section describes how to set up and use Paddler, a stateful load balancer specifically designed for `llama.cpp` server instances. Paddler helps distribute inference requests across multiple `llama.cpp` worker nodes, improving scalability and reliability.

The integration uses Ansible for deploying and configuring Paddler components:
*   **Paddler Balancer**: A central service that receives client requests and distributes them to available agents.
*   **Paddler Agent**: Runs on each worker node alongside the `llama.cpp` server instance, reporting its status and capacity to the balancer.

### Prerequisites

1.  **Paddler Installation**:
    *   The main `script.sh` has been updated to download and install the `paddler` binary to `/usr/local/bin/` on the target machines.

2.  **Ansible Inventory Configuration**:
    *   Your Ansible inventory file (e.g., `/etc/ansible/hosts/inventory.yaml` or a custom one) needs to define host groups for the Paddler components. The `playbook.yaml` expects:
        *   `controller_nodes`: A group containing the host(s) where the Paddler Balancer will run. Typically, this is a single host.
        *   `worker_nodes`: A group containing all hosts where `llama.cpp` server instances and Paddler Agents will run.
    *   Example `inventory.yaml` structure:
      ```yaml
      all:
        children:
          controller_nodes:
            hosts:
              paddler-controller-01: # ansible_host: <ip_of_controller_node>
          worker_nodes:
            hosts:
              llama-worker-01: # ansible_host: <ip_of_worker_node_1>
              llama-worker-02: # ansible_host: <ip_of_worker_node_2>
        vars:
          ansible_user: your_ssh_user # Example user
          # Other global vars if needed
      ```
    *   Ensure these groups are correctly defined and target the intended machines.

3.  **llama.cpp Server Configuration**:
    *   Crucially, each `llama.cpp` server instance that a Paddler Agent will manage **must** be started with the `--slots AVAILABLE_SLOTS` argument. `AVAILABLE_SLOTS` is an integer specifying how many parallel requests that `llama.cpp` instance can handle. This is essential for Paddler's capacity-aware load balancing.
    *   The `run.sh` script (used by the updated `playbook.yaml`) now primarily serves as a placeholder to guide users in setting up `llama-server` with RPC. If you are using Paddler, you will likely be managing `llama-server` instances as systemd services or via other means, ensuring the `--slots` argument is included in their startup command.

### Ansible Configuration for Paddler

The Paddler deployment is configured using Ansible variables. Default values are provided in the role defaults, but you can override them in your inventory (group_vars, host_vars) or directly in the playbook if needed.

**Key Variables for Paddler Agent (`ansible/paddler_agent/defaults/main.yaml`):**
*   `paddler_agent_user`: User to run the agent service (default: `"llamauser"`).
*   `paddler_agent_group`: Group for the agent service (default: `"llamauser"`).
*   `paddler_agent_llamacpp_port`: Port where the local `llama.cpp` server is listening (default: `8088`). The agent will try to connect to `127.0.0.1:{{paddler_agent_llamacpp_port}}`.
*   `paddler_agent_external_llamacpp_addr`: External address (IP:Port) of the llama.cpp instance this agent is managing. Defaults to `{{ ansible_default_ipv4.address }}:{{ paddler_agent_llamacpp_port }}`.
*   `paddler_agent_local_llamacpp_api_key`: API key if your `llama.cpp` server is secured with one (default: `""`).
*   `paddler_balancer_host`: Inventory hostname of the node running the Paddler Balancer (default: `"controller_node"`). The agent uses this to find and connect to the balancer's management interface.
*   `paddler_balancer_management_port`: Management port of the Paddler Balancer (default: `8085`).

**Key Variables for Paddler Balancer (`ansible/paddler_balancer/defaults/main.yaml`):**
*   `paddler_balancer_user`: User to run the balancer service (default: `"paddler"`).
*   `paddler_balancer_group`: Group for the balancer service (default: `"paddler"`).
*   `paddler_balancer_working_directory`: Working directory for the balancer (default: `"/opt/paddler"`).
*   `paddler_balancer_management_port`: Port for the balancer's management API where agents connect (default: `8085`).
*   `paddler_balancer_management_addr`: Address for the management API (default: `"0.0.0.0:{{ paddler_balancer_management_port }}"`).
*   `paddler_balancer_reverseproxy_port`: Port for the balancer's public reverse proxy, where clients send inference requests (default: `8080`).
*   `paddler_balancer_reverseproxy_addr`: Address for the reverse proxy (default: `"0.0.0.0:{{ paddler_balancer_reverseproxy_port }}"`).
*   `paddler_balancer_dashboard_enable`: Whether to enable the web dashboard (default: `true`).
*   `paddler_executable_path`: Path to the `paddler` binary (default: `"/usr/local/bin/paddler"`).

To override, for example, the `paddler_agent_llamacpp_port` for all worker nodes, you could add to your inventory:
```yaml
# inventory.yaml
all:
  children:
    worker_nodes:
      vars:
        paddler_agent_llamacpp_port: 8090 # If your llama.cpp workers use this port
      hosts:
        # ... worker hosts
```

### Deployment

Running the main Ansible playbook (`playbook.yaml`) will now automatically deploy and start the Paddler Balancer and Paddler Agent services on the respective nodes defined in your inventory (`controller_nodes` and `worker_nodes`).

```bash
ansible-playbook playbook.yaml
```

**Important**:
*   The playbook includes tasks to create necessary users and directories for Paddler services.
*   The `paddler-agent` systemd service is configured to start after a `llama-cpp.service`. If your `llama.cpp` service is named differently or not managed by systemd directly in a way the agent can depend on, ensure `llama.cpp` is running with `--slots` *before* the agent attempts to connect. The Ansible role for `paddler_agent` includes a debug message reminding you of the `--slots` requirement.

### Verification and Testing

After deployment, you can verify the Paddler setup:

1.  **Paddler Dashboard (if enabled):**
    *   Access the Paddler Balancer's web dashboard at `http://<balancer_ip>:{{paddler_balancer_management_port}}/dashboard` (e.g., `http://your_controller_node_ip:8085/dashboard`).
    *   You should see connected agents and their status (e.g., number of free slots).

2.  **`test_paddler.sh` Script:**
    *   A test script `test_paddler.sh` is provided in the repository root to perform basic checks.
    *   Make it executable: `chmod +x test_paddler.sh`
    *   Run the script, providing the balancer's public and management addresses. If the balancer is on `192.168.1.100`:
        ```bash
        ./test_paddler.sh http://192.168.1.100:8080 http://192.168.1.100:8085
        ```
        Or using environment variables:
        ```bash
        export PADDLER_PUBLIC_ADDR="http://192.168.1.100:8080"
        export PADDLER_MANAGEMENT_ADDR="http://192.168.1.100:8085"
        ./test_paddler.sh
        ```
    *   **What it tests:**
        *   Connectivity to the balancer's management API (`/api/v1/agents`) and checks if agent information is present.
        *   A simple `/completion` request sent through the balancer's public reverse proxy to a `llama.cpp` backend.
    *   **Successful Output:** The script will print `PASS` for each test and a final "All tests passed successfully!" message. If tests fail, it will print error details and exit with a non-zero code.

### Using the Paddler Load Balancer

Once Paddler is deployed and verified:

*   Client applications should send their `llama.cpp` API requests (e.g., for completions, embeddings) to the **Paddler Balancer's reverse proxy address**.
*   This is typically `http://<balancer_ip>:{{paddler_balancer_reverseproxy_port}}`. For example: `http://your_controller_node_ip:8080/completion`.
*   Paddler will then intelligently route the request to an available `llama.cpp` worker node that has free slots.

This setup replaces direct communication to individual `llama.cpp` instances or the RPC mechanism previously discussed if you opt for Paddler's HTTP-based load balancing.

For the docker config image
//Create the Image
docker buildx build . -t gpt-mpi:latest
//Run the image to create a container
docker run -itd gpt-mpi
//Get Container ID or Name
docker ps -a
//Execute a command
docker container exec container_name-or-ID mpirun -hostfile hostfile -n 3 ./main -m ./models/ggml-vocal.bin -p "Whats the meaning of life?" -n 512
