import os
from sentence_transformers import SentenceTransformer

# Preload models to ensure they are cached in the Docker image
models = [
    "sentence-transformers/all-MiniLM-L6-v2",
    "all-MiniLM-L6-v2"
]

for model_name in models:
    print(f"Downloading model: {model_name}")
    try:
        SentenceTransformer(model_name)
        print(f"Successfully downloaded: {model_name}")
    except Exception as e:
        print(f"Failed to download {model_name}: {e}")
        # Fail the build if download fails
        exit(1)
