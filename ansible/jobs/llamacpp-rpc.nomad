job "llamacpp-rpc" {
  datacenters = ["dc1"]
  namespace   = "default"

  group "master" {
    count = 1

    network {
      mode = "bridge"
      port "http" {}
    }

    service {
      name     = "llama-cpp-api"
      provider = "consul"
      port     = "http"
    }

    task "llama-master" {
      driver = "exec"

      template {
        data = <<EOH
#!/bin/bash
set -e

# Wait until at least one worker service is available
while [ -z "$(nomad service discover -address-type=ipv4 llama-cpp-rpc-worker 2>/dev/null)" ]; do
  echo "Waiting for worker services to become available in Consul..."
  sleep 5
done

WORKER_IPS=$(nomad service discover -address-type=ipv4 llama-cpp-rpc-worker | tr '\n' ',' | sed 's/,$//')
HEALTH_CHECK_URL="http://127.0.0.1:{{ env "NOMAD_PORT_http" }}/health"

# Loop through the provided models and try to start the server
{% for model in llm_models_var %}
  echo "Attempting to start llama-server with model: {{ model.name }}"
  /usr/local/bin/llama-server \
    --model "/opt/nomad/models/llm/{{ model.filename }}" \
    --host 0.0.0.0 \
    --port {{ env "NOMAD_PORT_http" }} \
    --rpc-servers $WORKER_IPS &

  SERVER_PID=$!
  echo "Server process started with PID $SERVER_PID. Waiting for it to become healthy..."

  # Health check loop
  HEALTHY=false
  for i in $(seq 1 12); do
    sleep 10
    if curl -s --fail $HEALTH_CHECK_URL > /dev/null; then
      echo "Server is healthy with model {{ model.name }}!"
      HEALTHY=true
      break
    else
      echo "Health check failed (attempt $i/12)..."
    fi
  done

  if [ "$HEALTHY" = true ]; then
    echo "Successfully started and health-checked llama-server with model: {{ model.name }}"
    wait $SERVER_PID # Keep the script running with the successful server
    exit 0
  else
    echo "Server failed to become healthy with model: {{ model.name }}. Killing process and trying next model."
    kill $SERVER_PID
    wait $SERVER_PID 2>/dev/null
  fi
{% endfor %}

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
        # Use the memory of the primary model for the master
        cpu    = 1000
        memory = {{ llm_models_var[0].memory_mb | default(2048) }}
      }

      volume_mount {
        volume      = "models"
        destination = "/opt/nomad/models"
        read_only   = true
      }
    }
  }

  # Note: This is a simplification. All workers will have the same resource profile
  # as the primary LLM. A more advanced setup would have a separate group per model.
  group "workers" {
    count = {{ llm_models_var[0].WORKER_COUNT | default(1) }}

    network {
      mode = "bridge"
      port "rpc" {}
    }

    service {
      name     = "llama-cpp-rpc-worker"
      provider = "consul"
      port     = "rpc"
    }

    task "llama-worker" {
      driver = "exec"

      config {
        # The worker will load the primary model. The master will delegate tasks
        # for any loaded model, but the worker itself needs a default model to load.
        command = "/usr/local/bin/llama-server"
        args = [
          "--model", "/opt/nomad/models/llm/{{ llm_models_var[0].filename }}",
          "--host", "0.0.0.0",
          "--port", "{{ env \"NOMAD_PORT_rpc\" }}",
        ]
      }

      resources {
        cpu    = 1000
        memory = {{ llm_models_var[0].memory_mb | default(2048) }}
      }

      volume_mount {
        volume      = "models"
        destination = "/opt/nomad/models"
        read_only   = true
      }
    }
  }

  # Common volume for all groups
  volume "models" {
    type      = "host"
    read_only = true
    source    = "/opt/nomad/models"
  }

  # All groups in this job will implicitly use the "models" volume
  # by referencing it in their task's volume_mount block.
}
