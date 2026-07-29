FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# Set non-interactive timezone configuration
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up workspace
WORKDIR /app

# Install rustup/cargo if needed for native extensions, but prefer prebuilt wheels
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install Python dependencies required for moshi/personaplex
# Note: we use PyTorch with CUDA 12.1 support
RUN pip3 install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Clone and install the Moshi / PersonaPlex repository
# In a real scenario, this might point to a specific fork or tag
RUN git clone https://github.com/kyutai-labs/moshi.git /app/moshi \
    && cd /app/moshi \
    && pip3 install --no-cache-dir -e .

# The entrypoint expects the weights to be mounted or downloaded
# For PoC, we will assume the weights are loaded dynamically or mounted via host volume
EXPOSE 8080

# Command to run the moshi web server for streaming
CMD ["python3", "-m", "moshi.server", "--host", "0.0.0.0", "--port", "8080"]
