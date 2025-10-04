job "expert-${meta.expert_name}" {
  datacenters = ["dc1"]
  namespace   = "default"

  meta {
    # This will be overridden by the `nomad run -meta` command
    expert_name = "main"
  }

  group "master" {
    count = 1

    volume "models" {
      type      = "host"
      source    = "models"
      read_only = true
    }

    network {
      mode = "host"
      port "http" {}
    }

    service {
      name     = "prima-api-${meta.expert_name}"
      provider = "consul"
      port     = "http"
      tags     = ["expert", "${meta.expert_name}"]

      check {
        type     = "http"
        path     = "/health"
        interval = "15s"
        timeout  = "5s"
      }
    }

    task "llama-server-master" {
      driver = "exec"

      template {
        data = <<EOH
#!/bin/bash
set -e
echo "Starting master server for expert: ${NOMAD_META_expert_name}"

# Discover worker services via Consul
echo "Discovering worker services from Consul..."
worker_ips=""
for i in {1..30}; do
  worker_ips=$(curl -s "http://127.0.0.1:8500/v1/health/service/expert-${NOMAD_META_expert_name}-worker?passing" | jq -r '[.[] | .Service | "\(.Address):\(.Port)"] | join(",")')
  if [ -n "$worker_ips" ]; then
    echo "Discovered Worker IPs: $worker_ips"
    break
  fi
  echo "No workers found yet, retrying in 10 seconds... (attempt $i/30)"
  sleep 10
done

rpc_args=""
if [ -n "$worker_ips" ]; then
  echo "Workers found. Configuring RPC."
  rpc_args="--rpc-servers $worker_ips"
else
  echo "No workers found after waiting. Starting in standalone mode."
fi

health_check_url="http://127.0.0.1:{{ env "NOMAD_PORT_http" }}/health"

echo "Fetching model configuration from Consul..."
MODEL_CONFIG_JSON=$(curl -s http://127.0.0.1:8500/v1/kv/config/models/${NOMAD_META_expert_name}?raw)

if [ -z "$MODEL_CONFIG_JSON" ] || [ "$MODEL_CONFIG_JSON" == "null" ]; then
  echo "Error: Could not fetch model configuration for expert '${NOMAD_META_expert_name}' from Consul."
  exit 1
fi

# Loop through the provided models for failover
for model_data in $(echo "$MODEL_CONFIG_JSON" | jq -c '.[]'); do
  model_name=$(echo "$model_data" | jq -r '.name')
  model_filename=$(echo "$model_data" | jq -r '.filename')

  echo "Attempting to start llama-server with model: $model_name"

  /usr/local/bin/llama-server \
    --model "/opt/nomad/models/llm/${model_filename}" \
    --host 0.0.0.0 \
    --port {{ env "NOMAD_PORT_http" }} \
    --n-gpu-layers 999 \
    --fa auto \
    --mlock \
    $rpc_args &

  server_pid=$!
  echo "Server process started with PID $server_pid. Waiting for it to become healthy..."

  healthy=false
  for i in {1..30}; do
    sleep 10
    if curl -s --fail $health_check_url > /dev/null; then
      echo "Server is healthy with model $model_name!"
      healthy=true
      break
    else
      echo "Health check failed (attempt $i/30)..."
    fi
  done

  if [ "$healthy" = true ]; then
    echo "Successfully started llama-server with model: $model_name"
    # Write the active model to Consul KV for other services to discover
    curl -X PUT --data "$model_name" "http://127.0.0.1:8500/v1/kv/experts/${NOMAD_META_expert_name}/active_model"
    wait $server_pid
    exit 0
  else
    echo "Server failed to become healthy with model: $model_name. Killing process PID $server_pid..."
    kill $server_pid
    wait $server_pid 2>/dev/null
  fi
done

echo "All models failed to start. Exiting."
exit 1
EOH
        destination = "local/run_master.sh"
        perms       = "0755"
      }

      config {
        command = "local/run_master.sh"
      }

      resources {
        cpu    = 2000
        memory = 16384
      }

      volume_mount {
        volume      = "models"
        destination = "/opt/nomad/models"
        read_only   = true
      }
    }
  }

  group "workers" {
    count = 1 # This can be parameterized later if needed

    network {
      mode = "host"
      port "rpc" {}
    }

    service {
      name     = "expert-${meta.expert_name}-worker"
      provider = "consul"
      port     = "rpc"

      check {
        type     = "tcp"
        interval = "15s"
        timeout  = "5s"
      }
    }

    task "rpc-server-worker" {
      driver = "exec"

      template {
        data = <<EOH
#!/bin/bash
set -e
/usr/local/bin/rpc-server --host 0.0.0.0 --port {{ env "NOMAD_PORT_rpc" }}
EOH
        destination = "local/run_rpc.sh"
        perms       = "0755"
      }

      config {
        command = "local/run_rpc.sh"
      }

      resources {
        cpu    = 500
        memory = 1024
      }
    }
  }
}