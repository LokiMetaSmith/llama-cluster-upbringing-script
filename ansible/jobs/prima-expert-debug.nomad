# This is a Jinja2 template for a complete, distributed Prima expert.
# It is parameterized and can be used to deploy any expert model.
job "{{ job_name | default('prima-expert-main') }}" {
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
set -ex
echo "--- Starting prima-expert master in DEBUG MODE ---"

# For debugging, we are not discovering workers and are using a hardcoded model.
echo "Attempting to start llama-server with hardcoded model: Llama-3-8B-Instruct.gguf"

# Run the server in the foreground and redirect all output to Nomad's logs
/usr/local/bin/llama-server \
  --model "/opt/nomad/models/llm/Llama-3-8B-Instruct.gguf" \
  --host 0.0.0.0 \
  --port {{ '{{' }} env "NOMAD_PORT_http" {{ '}}' }} \
  --n-gpu-layers 999 \
  -fa auto \
  --mlock \
  2>&1

echo "--- llama-server exited ---"
exit 1 # Exit with an error to ensure the task is marked as failed
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

  # The worker group is not needed for this debug scenario
  # group "workers" { ... }
}
