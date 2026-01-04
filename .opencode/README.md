# OpenCode Configuration

This directory contains the configuration for using **OpenCode** with the Pipecat Cluster.

## Setup

1.  **Install OpenCode:** Ensure you have the `opencode` CLI tool installed in your environment.
2.  **Install Plugin:**
    ```bash
    npm install oh-my-opencode --save-dev
    ```
3.  **Configuration:** The configuration points to the local Pipecat cluster's "Router" service.
    *   **Endpoint:** `http://localhost:8081/v1`
    *   **Model:** `local/router` (mapped to the running `llama-server` instance).

## Usage

Run the agent:

```bash
opencode
```
