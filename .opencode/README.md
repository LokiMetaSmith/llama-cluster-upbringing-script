# Oh My OpenCode Configuration

This directory contains the configuration for using **Oh My OpenCode** with the Pipecat Cluster.

## Setup

1.  **Install OpenCode:** Ensure you have the `opencode` CLI tool installed in your environment.
2.  **Install Plugin:** You may need to install the plugin package locally if it's not included in your global `opencode` installation:
    ```bash
    npm install oh-my-opencode --save-dev
    ```
3.  **Configuration:** The configuration files in this directory are set up to use the local Pipecat cluster's "Router" as the model provider.
4.  **Local Router:**
    *   The configuration expects an OpenAI-compatible endpoint at `http://localhost:8080/v1`.
    *   This usually corresponds to the `llama-server` (or `llamacpp-rpc-api`) running in your Nomad cluster.
    *   If your local service is on a different port (e.g., 8000), update `.opencode/opencode.json`.

## Usage

Run the agent with the `opencode` command:

```bash
opencode
```

Or invoke specific agents:

```bash
opencode run @Sisyphus "Optimize the memory usage of the twin service"
```

## Agents

The following agents are configured to route through the local cluster:

*   **Sisyphus:** Main orchestrator.
*   **Oracle:** Reasoning expert.
*   **Librarian:** Research expert.
*   **Explore:** Fast code exploration.
*   **Frontend-UI-UX-Engineer:** UI/UX specialist.
