FROM python:3.11-slim

WORKDIR /app

# Install dependencies
# memorygraphMCP includes the core logic
# mcp[cli], starlette, uvicorn are needed for the FastMCP wrapper
RUN pip install "mcp[cli]" starlette uvicorn memorygraphMCP

# Copy the wrapper code
COPY server.py .

# Expose the SSE port
EXPOSE 8000

# Run the server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
