FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirement list (ensure it exists or we copy from root)
# For this service, we need fastapi, uvicorn, faiss-cpu, sentence-transformers, langchain_community
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN pip install --no-cache-dir fastapi uvicorn faiss-cpu sentence-transformers langchain_community chromadb

# Copy the application code
# We copy the entire pipecatapp since RAG_Tool depends on PMMMemory and utils
COPY pipecatapp/ /app/pipecatapp/

# Setup Environment
ENV PYTHONPATH=/app
ENV PORT=8000

# Expose port
EXPOSE 8000

# Run the RAG server
CMD ["python", "pipecatapp/services/rag/rag_server.py"]
