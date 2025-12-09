#!/bin/bash
set -e

echo "Starting World Model Service Debug..."

CONTAINER_NAME="world-model-debug"
IMAGE_NAME="world-model-service:local"
DEBUG_PORT=12345

MQTT_CONTAINER_NAME="world-model-debug-mqtt"
MQTT_IMAGE="eclipse-mosquitto:2"
START_MQTT=false

# Cleanup function
cleanup() {
    if [ "$DEBUG_KEEP_ALIVE" = "true" ]; then
        echo "Skipping cleanup (DEBUG_KEEP_ALIVE=true). Containers left running."
        return
    fi

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

# Ensure NOMAD_ADDR is set correctly by sourcing the profile script
if [ -f "/etc/profile.d/nomad.sh" ]; then
    source "/etc/profile.d/nomad.sh"
fi

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
  -e NOMAD_ADDR="${NOMAD_ADDR:-http://$HOST_IP:4646}" \
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

echo "Verifying MQTT and State update..."
# Publish a test message using python inside the debug container (guaranteed to have paho-mqtt)
TEST_TOPIC="test/topic"
TEST_VALUE="verification_$(date +%s)"
TEST_PAYLOAD="{\"value\": \"$TEST_VALUE\"}"

echo "Publishing to $TEST_TOPIC with payload $TEST_PAYLOAD..."

# We use a python one-liner inside the container to publish
docker exec $CONTAINER_NAME python3 -c "
import paho.mqtt.client as mqtt
import os
import time

host = os.getenv('MQTT_HOST', 'localhost')
try:
    port = int(os.getenv('MQTT_PORT', '1883'))
except:
    port = 1883

print(f'Connecting to {host}:{port}...')
client = mqtt.Client()
client.connect(host, port, 60)
client.publish('$TEST_TOPIC', '$TEST_PAYLOAD', retain=True)
client.disconnect()
print('Message published.')
"

echo "Waiting for state update..."
sleep 2

echo "Querying state..."
STATE_RESPONSE=$(curl -s http://localhost:$DEBUG_PORT/state)
echo "State response: $STATE_RESPONSE"

if echo "$STATE_RESPONSE" | grep -q "$TEST_VALUE"; then
    echo "Success: State successfully updated via MQTT!"
else
    echo "Failure: State did not contain expected value '$TEST_VALUE'."
    echo "Container Logs:"
    docker logs --tail 50 $CONTAINER_NAME
    exit 1
fi

echo "=== Container Logs (tail) ==="
docker logs --tail 50 $CONTAINER_NAME
echo "======================"
