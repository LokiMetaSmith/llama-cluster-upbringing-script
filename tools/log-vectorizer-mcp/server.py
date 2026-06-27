import json
import math
import os
import re
import httpx
from typing import List
from mcp.server.fastmcp import FastMCP

# Initialize the MCP Server using FastMCP
app = FastMCP("log-vectorizer-mcp")

# Configuration via environment variables with defaults
LOCAL_EMBED_URL = os.environ.get("LOCAL_EMBED_URL", "http://localhost:11434/api/embeddings")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "nomic-embed-text")
DATABASE_FILE = os.environ.get("DATABASE_FILE", "/tmp/log_vectors.jsonl")

# Common timestamp patterns: ISO8601, Apache, Syslog, Python logging default, and Ansible task headers
TIMESTAMP_PATTERN = re.compile(
    r"^(?:"
    r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}"  # e.g. 2023-10-25 12:30:45 or 2023-10-25T12:30:45
    r"|\[\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2}" # e.g. [25/Oct/2023:12:30:45
    r"|[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}" # e.g. Oct 25 12:30:45
    r"|TASK \[" # Ansible task header
    r"|PLAY \[" # Ansible play header
    r"|RUNNING HANDLER \[" # Ansible handler header
    r")"
)

# Maximum lines allowed in a single chunk before forcing a split to avoid massive embeddings
MAX_LINES_PER_CHUNK = 200

def get_local_embedding(text: str) -> List[float]:
    """Generates embeddings using a local HTTP endpoint."""
    payload = {
        "model": EMBEDDING_MODEL,
        "prompt": text
    }
    with httpx.Client() as client:
        response = client.post(LOCAL_EMBED_URL, json=payload, timeout=60.0)
        response.raise_for_status()
        return response.json().get("embedding", [])

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Basic dot product for vector comparison."""
    dot_product = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot_product / (mag1 * mag2)

@app.tool()
async def ingest_log_file(filepath: str) -> str:
    """
    Reads a large log file, chunks it based on timestamps (keeping stack traces intact),
    vectorizes it, and saves it to a text-based JSONL database.
    """
    buffer = []
    chunk_count = 0

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as file, open(DATABASE_FILE, 'a', encoding='utf-8') as db:
            for line in file:
                # If we hit a new timestamp or the buffer exceeds the maximum allowed lines
                hit_boundary = TIMESTAMP_PATTERN.match(line) is not None
                hit_max_lines = len(buffer) >= MAX_LINES_PER_CHUNK

                if (hit_boundary or hit_max_lines) and buffer:
                    chunk_text = "".join(buffer).strip()
                    if chunk_text:
                        vector = get_local_embedding(chunk_text)

                        db_entry = {
                            "source": filepath,
                            "text": chunk_text,
                            "vector": vector
                        }
                        db.write(json.dumps(db_entry) + "\n")
                        chunk_count += 1

                    # Reset buffer
                    buffer = [line]
                else:
                    # Either it's the first line, or it's a continuation (like a stack trace)
                    buffer.append(line)

            # Handle the final buffer
            if buffer:
                chunk_text = "".join(buffer).strip()
                if chunk_text:
                    vector = get_local_embedding(chunk_text)
                    db_entry = {"source": filepath, "text": chunk_text, "vector": vector}
                    db.write(json.dumps(db_entry) + "\n")
                    chunk_count += 1

        return f"Successfully ingested {filepath}. Created {chunk_count} vectorized text chunks in {DATABASE_FILE}."
    except Exception as e:
        return f"Error ingesting log: {str(e)}"

@app.tool()
async def search_logs(query: str, top_k: int = 3) -> str:
    """
    Performs a semantic search over the vectorized log database.
    Agents should use this to find historical errors, stack traces, or context.
    """
    try:
        query_vector = get_local_embedding(query)
    except Exception as e:
        return f"Error generating embedding for query: {str(e)}"

    results = []

    try:
        if not os.path.exists(DATABASE_FILE):
            return f"Log database not found at {DATABASE_FILE}. Please run ingest_log_file first."

        with open(DATABASE_FILE, 'r', encoding='utf-8') as db:
            for line in db:
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                    score = cosine_similarity(query_vector, record.get("vector", []))
                    results.append((score, record.get("text", "")))
                except json.JSONDecodeError:
                    continue

        if not results:
            return "No log entries found in the database."

        # Sort by highest similarity
        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:top_k]

        formatted_output = f"Top {len(top_results)} relevant log chunks for query: '{query}'\n" + "-"*40 + "\n"
        for i, (score, text) in enumerate(top_results):
            formatted_output += f"--- Result {i+1} (Relevance: {score:.2f}) ---\n{text}\n\n"

        return formatted_output
    except Exception as e:
        return f"Error searching logs: {str(e)}"

if __name__ == "__main__":
    app.run(transport="stdio")
