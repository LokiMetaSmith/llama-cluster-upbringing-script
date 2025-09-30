# Use the official Python 3.10 slim base image
FROM python:3.10-slim

# Set environment variables to prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=off

# Install system dependencies identified from the Ansible role
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    portaudio19-dev \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 \
    rustc \
    cargo \
    # Dependencies for Playwright
    libevent-2.1-7 \
    libgstreamer-plugins-bad1.0-0 \
    libflite1 \
    libavif16 \
    gstreamer1.0-libav \
    # Clean up apt cache to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /opt/pipecatapp

# Create a virtual environment
RUN python3 -m venv /opt/pipecatapp/venv

# Copy requirements file and install Python dependencies within the venv
COPY requirements.txt .
RUN . /opt/pipecatapp/venv/bin/activate && \
    pip install --upgrade pip setuptools wheel cython && \
    pip install -r requirements.txt

# Install Playwright browsers
RUN . /opt/pipecatapp/venv/bin/activate && \
    python -m playwright install

# Copy the rest of the application code
COPY . .

# Make the startup script executable
RUN chmod +x /opt/pipecatapp/start_pipecat.sh

# Set the entrypoint for the container
ENTRYPOINT ["/opt/pipecatapp/start_pipecat.sh"]