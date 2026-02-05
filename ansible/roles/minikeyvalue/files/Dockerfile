FROM golang:1.20-alpine AS builder

WORKDIR /build
COPY src/ .
RUN go mod init github.com/geohot/minikeyvalue || true
RUN go mod tidy
RUN go build -o mkv main.go

FROM nginx:alpine

# Install Python3 and requests for the start script
RUN apk add --no-cache python3 py3-pip bash curl && \
    pip3 install requests

WORKDIR /app

# Copy binary from builder
COPY --from=builder /build/mkv /app/mkv

# Copy volume script
COPY volume /app/volume

# Copy start script
COPY start_master.py /app/start_master.py

# Make executable
RUN chmod +x /app/mkv /app/volume /app/start_master.py

# Create data directories
RUN mkdir -p /data/volume /data/indexdb
