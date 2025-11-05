# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /opt/pipecatapp

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    portaudio19-dev \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 \
    rustc \
    cargo \
    libevent-2.1-7 \
    libgstreamer-plugins-bad1.0-0 \
    libflite1 \
    libavif16 \
    gstreamer1.0-libav \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python3 -m venv /opt/pipecatapp/venv
ENV PATH="/opt/pipecatapp/venv/bin:$PATH"

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install

# Download required AI models
RUN git clone https://huggingface.co/Systran/faster-whisper-tiny.en /opt/nomad/models/stt/faster-whisper-tiny.en
RUN git clone https://github.com/snakers4/silero-vad.git /root/.cache/torch/hub/snakers4_silero-vad_master

# Copy the rest of the application source code
COPY . .

# Make the startup script executable
RUN chmod +x /opt/pipecatapp/start_pipecat.sh

# Set the entrypoint for the container
ENTRYPOINT ["/opt/pipecatapp/start_pipecat.sh"]