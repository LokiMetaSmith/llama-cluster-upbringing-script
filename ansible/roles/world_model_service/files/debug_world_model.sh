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
docker run -d --name $CONTAINER_NAME \
  --net=host \
  -e NOMAD_PORT_http=$DEBUG_PORT \
  -e PYTHONUNBUFFERED=1 \
  -e MQTT_HOST="localhost" \
  -e NOMAD_ADDR="http://localhost:4646" \
  $IMAGE_NAME

echo "Waiting for container to start..."
sleep 5

echo "Checking container status..."
if ! docker ps | grep -q $CONTAINER_NAME; then
    echo "Container failed to start!"
    docker logs $CONTAINER_NAME
    exit 1
fi

echo "Checking application health via HTTP (HOST)..."
if curl -v --max-time 5 http://localhost:$DEBUG_PORT/state; then
    echo "Success: Application is reachable via curl!"
else
    echo "Failure: Application is not responding to curl."
fi

echo "Checking application health via Python script (INTERNAL)..."
# Simulate Nomad script check: Execute python inside container
# We must pass the env var explicitly because docker exec doesn't inherit container env vars by default in the same way Nomad might expects?
# Actually, docker exec DOES NOT use container env vars for the command unless they are exported in the entrypoint or passed.
# But Nomad documentation says it runs in the task environment.
# Let's test WITH explicit env var first to verify the script logic.
if docker exec -e NOMAD_PORT_http=$DEBUG_PORT $CONTAINER_NAME /usr/local/bin/python -c "import httpx, os; httpx.get('http://127.0.0.1:' + os.environ['NOMAD_PORT_http'] + '/state').raise_for_status()"; then
    echo "Success: Internal python script check passed!"
else
    echo "Failure: Internal python script check failed."
fi

echo "=== Container Logs ==="
docker logs $CONTAINER_NAME
echo "======================"

echo "Stopping debug container..."
docker stop $CONTAINER_NAME
