FROM python:3.12-slim

# Install system dependencies. Docker is sometimes needed for local mode code execution
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# We need fastapi, uvicorn, docker, and llm-sandbox
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN pip install --no-cache-dir fastapi uvicorn docker llm-sandbox

# Copy the application code
COPY pipecatapp/ /app/pipecatapp/

# Setup Environment
ENV PYTHONPATH=/app
ENV PORT=8000

# Expose port
EXPOSE 8000

# Run the server
CMD ["python", "pipecatapp/services/code_runner/code_runner_server.py"]
