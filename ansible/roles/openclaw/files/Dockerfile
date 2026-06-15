FROM node:22-bookworm-slim

# Install system dependencies (curl for integration)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install openclaw global cli
RUN npm install -g openclaw@latest

# Set working directory
WORKDIR /app

# The entrypoint (can be overridden by Nomad)
RUN useradd -m -s /bin/bash appuser && chown -R appuser:appuser /app
USER appuser
CMD ["openclaw", "gateway", "--port", "18789"]
