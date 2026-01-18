FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install "mcp[cli]" starlette uvicorn memory-graph

# Copy the wrapper code
COPY server.py .

# Expose the SSE port
EXPOSE 8000

# Run the server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
