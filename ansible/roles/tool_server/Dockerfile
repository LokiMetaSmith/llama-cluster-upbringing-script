FROM python:3.12-bookworm

WORKDIR /app

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
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libavfilter-dev \
    libswscale-dev \
    libswresample-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip

# Install pipecat-ai and its extras first
RUN pip install --no-cache-dir "pipecat-ai[all]"

# Now install the other requirements
RUN pip install --no-cache-dir \
    av==16.0.1 \
    ctranslate2==4.4.0 \
    docker \
    einops \
    espeakng_loader \
    faiss-cpu \
    fastapi \
    faster-whisper==1.2.1 \
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
    websockets \
    ultralytics \
    sentence_transformers

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]

