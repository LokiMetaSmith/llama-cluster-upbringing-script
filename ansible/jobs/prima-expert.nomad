{% set final_worker_count = worker_count if worker_count is defined else 1 %}
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
      mode = "host"
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
worker_ips=""
for i in {1..12}; do
  {# djlint:off H022 #}
  worker_ips=$(curl -s "http://127.0.0.1:8500/v1/health/service/{{ job_name }}-worker?passing" | jq -r '[.[] | .Service | "\(.Address):\(.Port)"] | join(",")')
  {# djlint:on #}
  if [ -n "$worker_ips" ]; then
    echo "Discovered Worker IPs: $worker_ips"
    break
  fi
  echo "No workers found yet, retrying in 10 seconds... (attempt $i/12)"
  sleep 10
done

rpc_args=""
if [ -n "$worker_ips" ]; then
  echo "Workers found. Configuring RPC."
  rpc_args="--rpc-servers $worker_ips"
else
  echo "No workers found after waiting. Starting in standalone mode."
fi

{# djlint:off H022 #}
health_check_url="http://127.0.0.1:{{ '{{' }} env "NOMAD_PORT_http" {{ '}}' }}/health"
{# djlint:on #}

# Loop through the provided models for failover
{% for model in model_list %}
  echo "Attempting to start llama-server with model: {{ model.name }}"

  /usr/local/bin/llama-server \
    --model "/opt/nomad/models/llm/{{ model.filename }}" \
    --host 0.0.0.0 \
    --port {{ '{{' }} env "NOMAD_PORT_http" {{ '}}' }} \
    --n-gpu-layers 999 \
    --flash-attn auto \
    --mlock \
    $rpc_args &

  server_pid=$!
  echo "Server process started with PID $server_pid. Waiting for it to become healthy..."

  healthy=false
  for i in {1..12}; do
    sleep 10
    if curl -s --fail $health_check_url > /dev/null; then
      echo "Server is healthy with model {{ model.name }}!"
      healthy=true
      break
    else
      echo "Health check failed (attempt $i/12)..."
    fi
  done

  if [ "$healthy" = true ]; then
    echo "Successfully started llama-server with model: {{ model.name }}"
    # Write the active model to Consul KV for other services to discover
    {# djlint:off H022 #}
    curl -X PUT --data "{{ model.name }}" http://127.0.0.1:8500/v1/kv/active_model/{{ job_name }}
    {# djlint:on #}
    wait $server_pid
    exit 0
  else
    echo "Server failed to become healthy with model: {{ model.name }}. Killing process PID $server_pid..."
    kill $server_pid
    wait $server_pid 2>/dev/null
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
        memory = 8192 # Hardcoded for simplicity and stability
      }

      volume_mount {
        volume      = "models"
        destination = "/opt/nomad/models"
        read_only   = true
      }
    }
  }

  group "workers" {
    count = {{ final_worker_count }}

    network {
      mode = "host"
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
