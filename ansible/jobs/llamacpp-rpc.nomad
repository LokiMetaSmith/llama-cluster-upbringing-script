job "llamacpp-rpc" {
  datacenters = ["dc1"]
  namespace   = "default"

  group "master" {
    count = 1

    volume "models" {
      type      = "host"
      source    = "models"
      read_only = true
    }

    network {
      mode = "bridge"
      port "http" {}
    }

    service {
      name     = "llama-cpp-api"
      provider = "consul"
      port     = "http"

      check {
        type     = "http"
        path     = "/health"
        interval = "15s"
        timeout  = "5s"
      }
    }

    task "llama-master" {
      driver = "exec"

      template {
        data = <<EOH
#!/bin/bash
# --- Corrected and Improved Script ---

# It's better to log to stdout/stderr for Nomad to capture logs
echo "Starting run_master.sh script..."

# Wait until at least one worker service is healthy and registered in Consul
echo "Waiting for worker services to become available in Consul..."
while [ -z "$(curl -s "http://127.0.0.1:8500/v1/health/service/llama-cpp-rpc-worker?passing" | jq '.[0]')" ]; do
  echo "Still waiting for a healthy worker service..."
  sleep 5
done
echo "Worker services are available."

echo "Discovering worker IPs from Consul..."
# Use curl and jq to get a comma-separated list of healthy worker IPs
WORKER_IPS=$(curl -s "http://127.0.0.1:8500/v1/health/service/llama-cpp-rpc-worker?passing" | jq -r '.[].Service.Address' | tr '\n' ',' | sed 's/,$//')
echo "Discovered Worker IPs: $WORKER_IPS"

# The '{{ env ... }}' syntax is evaluated by Nomad's template engine at runtime
HEALTH_CHECK_URL="http://127.0.0.1:{{ '{{' }} env "NOMAD_PORT_http" {{ '}}' }}/health"

# This templating loop is processed by an external tool (e.g., Ansible/Terraform)
# before the job is submitted to Nomad.
{% for model in llm_models_var %}
  echo "Attempting to start llama-server with model: {{ model.name }}"

  # Start the server in the background, logging to stdout/stderr
  /usr/local/bin/llama-server \
    --model "/opt/nomad/models/llm/{{ model.filename }}" \
    --host 0.0.0.0 \
    --port {{ '{{' }} env "NOMAD_PORT_http" {{ '}}' }} \
    --rpc-servers "$WORKER_IPS" &

  SERVER_PID=$!
  echo "Server process started with PID $SERVER_PID. Waiting for it to become healthy..."

  # Health check loop
  HEALTHY=false
  for i in {1..12}; do
    sleep 10
    # Use curl's exit code to check health. -s for silent, --fail for error codes.
    if curl -s --fail $HEALTH_CHECK_URL > /dev/null; then
      echo "Server is healthy with model {{ model.name }}!"
      HEALTHY=true
      break
    else
      echo "Health check failed (attempt $i/12)..."
    fi
  done

  if [ "$HEALTHY" = true ]; then
    echo "Successfully started llama-server with model: {{ model.name }}"
    # This wait command keeps the Nomad task running by waiting for the server process to exit.
    wait $SERVER_PID
    exit 0
  else
    echo "Server failed to become healthy with model: {{ model.name }}. Killing process PID $SERVER_PID..."
    kill $SERVER_PID
    # Wait for the process to be fully cleaned up before trying the next model
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
        cpu    = 1000
{%- set max_mem = [2048] -%}
{%- for model in llm_models_var -%}
{%- if model.memory_mb is defined and model.memory_mb > max_mem[0] -%}
{%- set _ = max_mem.pop() -%}
{%- set _ = max_mem.append(model.memory_mb) -%}
{%- endif -%}
{%- endfor -%}
        memory = {{ max_mem[0] }}
      }

      volume_mount {
        volume      = "models"
        destination = "/opt/nomad/models"
        read_only   = true
      }
    }
  }

  group "workers" {
    count = {% if llm_models_var[0].WORKER_COUNT is defined %}{{ llm_models_var[0].WORKER_COUNT }}{% else %}1{% endif %}

    volume "models" {
      type      = "host"
      source    = "models"
      read_only = true
    }

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

      template {
        data = <<EOH
#!/bin/bash
/usr/local/bin/llama-server \
  --model "/opt/nomad/models/llm/{{ llm_models_var[0].filename }}" \
  --host 0.0.0.0 \
  --port {{ '{{' }} env "NOMAD_PORT_rpc" {{ '}}' }}
EOH
        destination = "local/run_worker.sh"
        perms       = "0755"
      }

      config {
        command = "local/run_worker.sh"
      }

      resources {
        cpu    = 1000
{%- set max_mem = [2048] -%}
{%- for model in llm_models_var -%}
{%- if model.memory_mb is defined and model.memory_mb > max_mem[0] -%}
{%- set _ = max_mem.pop() -%}
{%- set _ = max_mem.append(model.memory_mb) -%}
{%- endif -%}
{%- endfor -%}
        memory = {{ max_mem[0] }}
      }

      volume_mount {
        volume      = "models"
        destination = "/opt/nomad/models"
        read_only   = true
      }
    }
  }
}
