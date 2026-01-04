# OpenCode Configuration

This directory contains the configuration for using **OpenCode** with the Pipecat Cluster.

## Setup

1.  **Install Dependencies:** Run `npm install` in the project root. This will install the `oh-my-opencode` plugin automatically.
2.  **Configuration:** The configuration points to the local Pipecat cluster's "Router" service.
    *   **Endpoint:** `http://localhost:8081/v1`
    *   **Model:** `local/router` (mapped to the running `llama-server` instance).

## Usage

Run the agent:

```bash
opencode
```
