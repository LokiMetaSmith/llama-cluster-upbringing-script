# Use a base image with Python 3.12
FROM python:3.12-slim

# Install system dependencies required for pipecat-ai and its extras
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libffi-dev \
    libssl-dev \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsndfile1 \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Upgrade pip and install pipecat-ai with all extras first
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir "pipecat-ai[all]"

# Copy the application code
COPY . .

# Install the remaining, non-conflicting application-specific dependencies
RUN pip install --no-cache-dir \
    ctranslate2==4.1.0 \
    docker \
    einops \
    espeakng_loader \
    faiss-cpu \
    fastapi \
    faster-whisper==1.0.1 \
    fugashi-plus \
    kittentts \
    "misaki[en]>=0.9.4" \
    num2words \
    onnxruntime \
    opencv-python-headless \
    paramiko \
    piper-tts \
    playwright \
    python-consul2 \
    python-dotenv \
    pyvips \
    pyvips-binary \
    realtimestt \
    langchain \
    soundfile \
    spacy \
    uvicorn \
    webrtcvad \
    websockets

# Install playwright browsers
RUN python -m playwright install --with-deps

# Command to run the application
CMD ["python", "tool_server.py"]
