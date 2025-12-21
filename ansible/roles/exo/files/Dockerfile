FROM python:3.12-slim-bookworm

# Install system dependencies
# git: for cloning
# curl: for generic fetching
# nodejs, npm: for dashboard build
# build-essential: for compiling python extensions if needed
RUN apt-get update && apt-get install -y \
    git \
    curl \
    nodejs \
    npm \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Arguments for build customization
ARG EXO_REPO_URL=https://github.com/exo-explore/exo.git
ARG EXO_VERSION=main

# Clone the repository
RUN git clone --depth 1 --branch ${EXO_VERSION} ${EXO_REPO_URL} .

# Build the dashboard
WORKDIR /app/dashboard
RUN npm install
RUN npm run build

# Return to root to setup Python environment
WORKDIR /app

# Configure uv
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies
# We use --no-dev to keep the image smaller, unless we need dev tools for evaluation
RUN uv sync --no-dev

# Expose the default port
EXPOSE 52415

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=52415

# Entrypoint
# We use `uv run` to ensure we use the managed environment
ENTRYPOINT ["uv", "run", "exo"]
