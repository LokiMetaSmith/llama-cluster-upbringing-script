# This is a Jinja2 template for a complete, distributed Prima expert.
# It is parameterized and can be used to deploy any expert model.
job "{{ job_name | default('prima-expert') }}" {
  datacenters = ["dc1"]
  namespace   = "{{ namespace | default('default') }}"

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
      name     = "{{ service_name | default('prima-api') }}"
      provider = "consul"
      port     = "http"

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
echo "Starting master server for expert: {{ job_name | default('prima-expert') }}"

# Discover worker services via Consul
echo "Discovering worker services from Consul..."
WORKER_IPS=$(curl -s "http://127.0.0.1:8500/v1/health/service/{{ job_name }}-worker?passing" | jq -r '.[].Service.Address' | tr '\n' ',' | sed 's/,$//')
echo "Discovered Worker IPs: $WORKER_IPS"

RPC_ARGS=""
if [ -n "$WORKER_IPS" ]; then
  echo "Workers found. Configuring RPC."
  RPC_ARGS="--rpc-servers $WORKER_IPS"
else
  echo "No workers found. Starting in standalone mode."
fi

HEALTH_CHECK_URL="http://127.0.0.1:{{ '{{' }} env "NOMAD_PORT_http" {{ '}}' }}/health"

# Loop through the provided models for failover
{% for model in model_list %}
  echo "Attempting to start llama-server with model: {{ model.name }}"

  /usr/local/bin/llama-server \
    --model "/opt/nomad/models/llm/{{ model.filename }}" \
    --host 0.0.0.0 \
    --port {{ '{{' }} env "NOMAD_PORT_http" {{ '}}' }} \
    $RPC_ARGS &

  SERVER_PID=$!
  echo "Server process started with PID $SERVER_PID. Waiting for it to become healthy..."

  HEALTHY=false
  for i in {1..12}; do
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
    echo "Successfully started llama-server with model: {{ model.name }}"
    # Write the active model to Consul KV for other services to discover
    curl -X PUT --data "{{ model.name }}" http://127.0.0.1:8500/v1/kv/active_model/{{ job_name }}
    wait $SERVER_PID
    exit 0
  else
    echo "Server failed to become healthy with model: {{ model.name }}. Killing process PID $SERVER_PID..."
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
        cpu    = 1000
        {%- set max_mem = [2048] -%}
        {%- for model in model_list -%}
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
    count = {{ worker_count | default(1) }}

    network {
      mode = "bridge"
      port "rpc" {}
    }

    service {
      name     = "{{ job_name }}-worker"
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
/usr/local/bin/rpc-server --host 0.0.0.0 --port {{ '{{' }} env "NOMAD_PORT_rpc" {{ '}}' }}
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
