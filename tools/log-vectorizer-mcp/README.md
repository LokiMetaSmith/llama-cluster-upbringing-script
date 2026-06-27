# Log Vectorizer MCP Tool

A standalone Model Context Protocol (MCP) tool designed to help AI agents manage and query large log files without exhausting their context window limits.

This tool reads massive log files, chunks them intelligently using regex to keep multi-line stack traces intact, and vectorizes the text using a local embedding endpoint (e.g., Ollama or llama.cpp). The chunks are stored in a lightweight, easily transportable JSON Lines (`.jsonl`) database. Agents can then perform semantic searches to find relevant historical errors or context.

## Installation

This tool requires its own isolated environment to prevent dependency conflicts.

```bash
cd tools/log-vectorizer-mcp
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

The tool uses environment variables for configuration, allowing you to seamlessly integrate it with your local inference setup.

| Variable | Description | Default Value |
| --- | --- | --- |
| `LOCAL_EMBED_URL` | The HTTP endpoint for your local embedding model. | `http://localhost:11434/api/embeddings` |
| `EMBEDDING_MODEL` | The name of the embedding model to use. | `nomic-embed-text` |
| `DATABASE_FILE` | The path where the `.jsonl` database will be stored. | `/tmp/log_vectors.jsonl` |

## Usage

You can start the MCP server using standard MCP clients (like Claude Desktop or custom agents) that communicate over standard input/output (`stdio`).

```bash
python server.py
```

### Exposed MCP Tools

The server exposes the following tools to the agent:

#### 1. `ingest_log_file(filepath: str)`
Reads a large log file and parses it line-by-line. It groups lines into chunks based on common timestamp patterns (ISO8601, Apache, Syslog, etc.), ensuring that multi-line entries (like Python stack traces) remain together. It then generates an embedding for each chunk and appends it to the `.jsonl` database.
- **Agents should use this:** When new logs are generated or when investigating a pipeline failure.

#### 2. `search_logs(query: str, top_k: int = 3)`
Performs a semantic similarity search (using cosine similarity) over the vectorized log chunks in the database. Returns the most relevant log entries matching the query.
- **Agents should use this:** To find historical errors, specific stack traces, or context without needing to read the entire multi-megabyte log file.

## Agent Configuration (MCP Clients)

To allow an AI agent (like Jules or Claude Desktop) to use this tool, you must register it in the agent's MCP configuration file (e.g., `mcp.json` or `claude_desktop_config.json`).

Add the following entry under the `mcpServers` object to instruct the agent on how to launch the server via `stdio`. Be sure to update the `/path/to/repo` paths to match your actual system paths:

```json
{
  "mcpServers": {
    "log-vectorizer": {
      "command": "/path/to/repo/tools/log-vectorizer-mcp/venv/bin/python",
      "args": ["/path/to/repo/tools/log-vectorizer-mcp/server.py"],
      "env": {
        "LOCAL_EMBED_URL": "http://localhost:11434/api/embeddings",
        "EMBEDDING_MODEL": "nomic-embed-text",
        "DATABASE_FILE": "/tmp/log_vectors.jsonl"
      }
    }
  }
}
```

Once configured, the agent will automatically discover the `ingest_log_file` and `search_logs` tools. It can then autonomously decide to vectorize logs and search them to provide context without exceeding its token limits.
