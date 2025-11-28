#!/bin/bash
set -e

echo "Starting World Model Service Debug..."

CONTAINER_NAME="world-model-debug"
IMAGE_NAME="world-model-service:latest"
DEBUG_PORT=12345

# Clean up previous run
echo "Cleaning up previous container..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Run container
echo "Running container..."
# We use host networking to mimic Nomad environment, but set NOMAD_PORT_http manually.
# We also set PYTHONUNBUFFERED=1 to see logs.
# Using 'hostname -I' to get the host IP, similar to what advertise_ip would be in Nomad.
HOST_IP=$(hostname -I | awk '{print $1}')
echo "Detected Host IP: $HOST_IP"

docker run -d --name $CONTAINER_NAME \
  --net=host \
  -e NOMAD_PORT_http=$DEBUG_PORT \
  -e PYTHONUNBUFFERED=1 \
  -e MQTT_HOST="$HOST_IP" \
  -e NOMAD_ADDR="http://$HOST_IP:4646" \
  $IMAGE_NAME

echo "Waiting for container to start..."
sleep 5

echo "Checking container status..."
if ! docker ps | grep -q $CONTAINER_NAME; then
    echo "Container failed to start!"
    docker logs $CONTAINER_NAME
    exit 1
fi

echo "Checking application health at http://localhost:$DEBUG_PORT/health..."
if curl -v --fail --max-time 5 http://localhost:$DEBUG_PORT/health; then
    echo "Success: Application is healthy!"
else
    echo "Failure: Application is unhealthy or not responding."
fi

echo "=== Container Logs ==="
docker logs $CONTAINER_NAME
echo "======================"

echo "Stopping debug container..."
docker stop $CONTAINER_NAME
