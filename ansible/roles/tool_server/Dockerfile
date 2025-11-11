FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y pkg-config libavdevice-dev ffmpeg
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tool_server.py"]
