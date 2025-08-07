This project uses Ansible to automate the setup of a freshly installed Linux machine to join a cluster of other computers to perform speech to text, run a low resource model, and then replay the response as text to speech.

## Prerequisites

Before you begin, ensure you have the following installed on your control machine:
*   **Ansible:** Required for running the playbook.
*   **Git:** Required for cloning this repository.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/KittenML/KittenTTS.git
    cd KittenTTS
    ```

2.  **Configure the Ansible inventory:**
    Edit the `inventory.yaml` file to match your cluster configuration. You will need to define `controller_nodes` and `worker_nodes`.

3.  **Run the Ansible playbook:**
    ```bash
    ansible-playbook playbook.yaml
    ```
    This will provision the machines in your inventory with all the necessary software and configurations.

## Components

This project uses the following main components:

*   **llama.cpp:** For running the low resource language model.
*   **whisper.cpp:** For performing speech to text.
*   **piper-tts:** For performing text to speech.
*   **KittenTTS:** An alternative text to speech engine.
*   **Paddler:** A load balancer for `llama.cpp` server instances.
*   **NFS:** For sharing files across the cluster.

## Docker

A `dockerfile` is provided to build a Docker image with all the necessary components.

To build the image:
```bash
docker buildx build . -t gpt-mpi:latest
```

To run the image:
```bash
docker run -itd gpt-mpi
```

To execute a command in the container:
```bash
docker container exec <container_name_or_ID> mpirun -hostfile hostfile -n 3 ./main -m ./models/ggml-vocal.bin -p "Whats the meaning of life?" -n 512
```
