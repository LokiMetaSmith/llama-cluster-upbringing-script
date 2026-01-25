# Use an official Python runtime as a parent image
FROM public.ecr.aws/docker/library/python:3.12-slim-bookworm

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
    libgl1-mesa-glx \
    libglib2.0-0 \
    libavif15 \
    gstreamer1.0-libav \
    libavcodec-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavformat-dev \
    libavutil-dev \
    libswresample-dev \
    libswscale-dev \
    pkg-config \
    git \
    libxcomposite1 \
    libxdamage1 \
    libgtk-3-0 \
    libatk1.0-0 \
    libnss3 \
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
RUN mkdir -p /tmp/faster-whisper-tiny.en
RUN git clone https://huggingface.co/Systran/faster-whisper-tiny.en /tmp/faster-whisper-tiny.en
RUN mkdir -p /opt/pipecatapp/faster-whisper-model
RUN cp -r /tmp/faster-whisper-tiny.en/* /opt/pipecatapp/faster-whisper-model/
RUN rm -rf /tmp/faster-whisper-tiny.en

# Copy the rest of the application source code
COPY . .

# Move the startup script to /opt/ to avoid being masked by bind mounts
RUN mv /opt/pipecatapp/start_pipecat.sh /opt/start_pipecat.sh && chmod +x /opt/start_pipecat.sh

# Set the entrypoint for the container
ENTRYPOINT ["/opt/start_pipecat.sh"]
