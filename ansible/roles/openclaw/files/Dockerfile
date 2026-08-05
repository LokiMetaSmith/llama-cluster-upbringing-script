FROM node:22-bookworm-slim

# Install system dependencies (curl for integration)
# We update sources to bypass invalid/expired signature issues due to system time
# being incorrectly set in the future.
RUN echo "Acquire::Check-Valid-Until \"false\";\nAcquire::AllowInsecureRepositories \"true\";\nAcquire::AllowDowngradeToInsecureRepositories \"true\";" > /etc/apt/apt.conf.d/99insecure && \
    sed -i 's/^Types: deb/Types: deb\nTrusted: yes/' /etc/apt/sources.list.d/debian.sources || true

RUN apt-get update && apt-get install -y --allow-unauthenticated curl && rm -rf /var/lib/apt/lists/*

# Install openclaw global cli
RUN npm install -g openclaw@latest

# Set working directory
WORKDIR /app

# The entrypoint (can be overridden by Nomad)
RUN useradd -m -s /bin/bash appuser && chown -R appuser:appuser /app
USER appuser
CMD ["openclaw", "gateway", "--port", "18789"]
