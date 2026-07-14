FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (including git and curl)
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Clone the last30days-skill repository
RUN git clone --depth 1 https://github.com/mvanhorn/last30days-skill.git /app/last30days-skill

# Set python path to find the scripts
ENV PYTHONPATH=/app/last30days-skill/skills/last30days/scripts

# Install the dependencies for the microservice
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download external CLI dependencies for the last30days engine (like yt-dlp if needed, or we can handle it at runtime)
# The engine uses python libraries or tools. We can run its setup internally.
RUN pip install --no-cache-dir yt-dlp

COPY . .

EXPOSE 8008

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8008"]
