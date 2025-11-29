# Debug Scripts

This directory contains documentation and scripts for debugging various components of the Pipecat cluster.

## World Model Service Debug Script

**Script Path:** `ansible/roles/world_model_service/files/debug_world_model.sh`

To use the `debug_world_model.sh` script, you generally need to ensure the Docker image it relies on (`world-model-service:latest`) is built and available on the machine where you are running the script.

### Usage

Here are the steps to run it manually (e.g., in a development environment or on the server):

1.  **Navigate to the directory**:
    ```bash
    cd ansible/roles/world_model_service/files/
    ```

2.  **Build the Docker image**:
    The script expects `world-model-service:latest` to exist. You can build it from the files in the current directory:
    ```bash
    docker build -t world-model-service:latest .
    ```

3.  **Run the script**:
    ```bash
    ./debug_world_model.sh
    ```

### What the script does

*   **Dependency Check**: Checks if an MQTT broker is running on port 1883.
    *   If **not found**, it automatically starts a temporary `eclipse-mosquitto:2` container configured for anonymous access.
*   **Cleanup**: Stops and removes any existing container named `world-model-debug` (and the temporary MQTT broker upon exit).
*   **Setup**: Detects the host IP using `hostname -I`.
*   **Execution**: Runs the service container with `network="host"` (mimicking Nomad's host network mode) and sets environment variables like `NOMAD_PORT_http` and `MQTT_HOST`.
*   **Verification**: Waits 5 seconds, then curls the `http://localhost:12345/health` endpoint to check if the service is up.
*   **Logging**: Prints the container logs to the console if the health check fails.
*   **Interactive Mode**: If successful, the script keeps running (tailing logs) until you press `Ctrl+C`. This allows you to interact with the service manually if needed.

## MQTT Connectivity Test Script

**Script Path:** `scripts/debug/test_mqtt_connection.py`

This script helps diagnose connectivity issues with the MQTT broker, especially when experiencing health check failures or restart loops in Nomad.

### Usage

1.  **Navigate to the directory**:
    ```bash
    cd scripts/debug/
    ```

2.  **Run the script**:
    ```bash
    python3 test_mqtt_connection.py
    ```

### What the script does

*   **IP Detection**: Automatically detects all IP addresses on the host (including `localhost` and `hostname -I`).
*   **Connectivity Check**: Continuously attempts to connect to port `1883` on all detected IPs.
*   **Loop**: Runs indefinitely (until `Ctrl+C`) to catch transient connectivity during service restart cycles.
*   **Reporting**: Prints a success message with the timestamp and IP address whenever a connection is successful.
