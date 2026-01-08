import subprocess
import sys

def check_versions():
    # Write the requirements to a temp file
    reqs = """
torch
torchvision
torchaudio
--extra-index-url https://pypi.org/simple
accelerate
ctranslate2==4.1.0
cython
docker
einops
espeakng_loader
faiss-cpu
fastapi
faster-whisper==1.0.3
fugashi-plus
huggingface-hub
httpx
kittentts
misaki[en]>=0.9.4
num2words
numpy
onnxruntime
opencv-python-headless
paramiko
pipecat-ai
pipecat-ai-whisker
pip
piper-tts
playwright
python-consul2
python-dotenv
pyvips
pyvips-binary
pyyaml
RealtimeSTT
requests
sentence-transformers
langchain
setuptools
soundfile
spacy
tenacity
ultralytics
uvicorn
webrtcvad
websockets
wheel
pylint
llm-sandbox[docker]
rank_bm25
fastapi
uvicorn
python-consul2
aiohttp
faiss-cpu
sentence-transformers
opencode-ai
pydantic
"""
    with open("temp_reqs.txt", "w") as f:
        f.write(reqs)

    # Use pip to resolve dependencies without installing
    # This might require pip-tools or just running pip install with --dry-run and verbose output
    # But --dry-run doesn't always show versions.
    # A better way is to use 'pip install --dry-run --report report.json -r temp_reqs.txt'

    cmd = [sys.executable, "-m", "pip", "install", "--dry-run", "--report", "report.json", "-r", "temp_reqs.txt"]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd)

if __name__ == "__main__":
    check_versions()
