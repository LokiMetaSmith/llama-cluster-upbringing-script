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

For the docker config image
//Create the Image
docker buildx build . -t gpt-mpi:latest
//Run the image to create a container
docker run -itd gpt-mpi
//Get Container ID or Name
docker ps -a
//Execute a command
docker container exec container_name-or-ID mpirun -hostfile hostfile -n 3 ./main -m ./models/ggml-vocal.bin -p "Whats the meaning of life?" -n 512
