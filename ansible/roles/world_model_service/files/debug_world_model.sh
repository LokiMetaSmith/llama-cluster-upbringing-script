#!/bin/bash
set -e

echo "Starting World Model Service Debug..."

CONTAINER_NAME="world-model-debug"
IMAGE_NAME="world-model-service:latest"
DEBUG_PORT=12345

MQTT_CONTAINER_NAME="world-model-debug-mqtt"
MQTT_IMAGE="eclipse-mosquitto:2"
START_MQTT=false

# Cleanup function
cleanup() {
    echo "Stopping debug container..."
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true

    if [ "$START_MQTT" = true ]; then
        echo "Stopping temporary MQTT container..."
        docker stop $MQTT_CONTAINER_NAME 2>/dev/null || true
        docker rm $MQTT_CONTAINER_NAME 2>/dev/null || true
    fi
}
trap cleanup EXIT

# Clean up previous run immediately
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Check for MQTT
echo "Checking for MQTT broker on port 1883..."
if nc -z localhost 1883 2>/dev/null; then
    echo "MQTT broker detected."
else
    echo "No MQTT broker detected. Starting temporary Mosquitto container..."
    START_MQTT=true

    # Clean up any potential stale mqtt container
    docker stop $MQTT_CONTAINER_NAME 2>/dev/null || true
    docker rm $MQTT_CONTAINER_NAME 2>/dev/null || true

    # Create a basic config for mosquitto to allow anonymous access (needed for debug)
    # and bind to all interfaces
    mkdir -p /tmp/mosquitto-debug
    echo "listener 1883 0.0.0.0" > /tmp/mosquitto-debug/mosquitto.conf
    echo "allow_anonymous true" >> /tmp/mosquitto-debug/mosquitto.conf

    docker run -d --name $MQTT_CONTAINER_NAME \
        --net=host \
        -v /tmp/mosquitto-debug/mosquitto.conf:/mosquitto/config/mosquitto.conf \
        $MQTT_IMAGE

    echo "Waiting for MQTT to start..."
    for i in {1..10}; do
        if nc -z localhost 1883 2>/dev/null; then
            echo "MQTT started."
            break
        fi
        sleep 1
    done
fi


# Run container
echo "Running world model container..."
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
    echo "Last logs:"
    docker logs --tail 20 $CONTAINER_NAME
    exit 1
fi

echo "=== Container Logs (tail) ==="
docker logs --tail 50 $CONTAINER_NAME
echo "======================"
echo "Press Ctrl+C to stop debugging (containers will be cleaned up)."
# Wait indefinitely so user can interact/inspect until they kill it
sleep infinity
