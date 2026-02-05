FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy source
COPY src/ .

# Install dependencies and the package itself
# We ignore nvidia-ml-py install errors if any (though usually it installs fine as python package)
RUN pip install --no-cache-dir . redis numpy cloudpickle tritonclient[http] tenacity statsd wrapt

# worker.py is in the root of the repo
CMD ["python3", "worker.py"]
