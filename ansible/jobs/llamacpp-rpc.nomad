job "llamacpp-rpc" {
  datacenters = ["dc1"]
  namespace   = "default"

  group "master" {
    count = 1

    # This block defines the volume for this task group.
    volume "models" {
      type      = "host"
      read_only = true
      source    = "models"
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
echo "Starting run_master.sh script..." >> /tmp/master-script.log

# Wait until at least one worker service is available
echo "Waiting for worker services to become available in Consul..." >> /tmp/master-script.log
while [ -z "$(/usr/local/bin/nomad service discover -address-type=ipv4 llama-cpp-rpc-worker 2>/dev/null)" ]; do
  echo "Still waiting for worker services..." >> /tmp/master-script.log
  sleep 5
done
echo "Worker services are available." >> /tmp/master-script.log

echo "Discovering worker IPs..." >> /tmp/master-script.log
WORKER_IPS=$(/usr/local/bin/nomad service discover -address-type=ipv4 llama-cpp-rpc-worker | tr '\n' ',' | sed 's/,$//')
echo "Worker IPs: $WORKER_IPS" >> /tmp/master-script.log
HEALTH_CHECK_URL="http://127.0.0.1:{{  env "NOMAD_PORT_http"  }}/health"

# Loop through the provided models and try to start the server
{% for model in llm_models_var %}
  echo "Attempting to start llama-server with model: {{ model.name }}"
  /usr/local/bin/llama-server \
    --model "/opt/nomad/models/llm/{{ model.filename }}" \
    --host 0.0.0.0 \
    --port {{  env "NOMAD_PORT_http"  }} \
    --rpc-servers $WORKER_IPS > /tmp/llama-server.log 2>&1 &

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
        cpu    = 1000
        memory = {% if llm_models_var[0].memory_mb is defined %}{{ llm_models_var[0].memory_mb }}{% else %}2048{% endif %}

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
      read_only = true
      source    = "models"
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
  --port {{ env "NOMAD_PORT_rpc" }}
EOH
        destination = "local/run_worker.sh"
        perms       = "0755"
      }

      config {
        command = "local/run_worker.sh"
      }

      resources {
        cpu    = 1000
        memory = {% if llm_models_var[0].memory_mb is defined %}{{ llm_models_var[0].memory_mb }}{% else %}2048{% endif %}

      }

      volume_mount {
        volume      = "models"
        destination = "/opt/nomad/models"
        read_only   = true
      }
    }
  }
}
