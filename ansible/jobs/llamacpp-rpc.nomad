job "llamacpp-rpc-{{ meta.JOB_NAME | default('default') }}" {
  datacenters = ["dc1"]
  namespace   = "{{ meta.NAMESPACE | default('default') }}"

  meta {
    NAMESPACE        = "{{ meta.NAMESPACE }}"
    JOB_NAME         = "{{ meta.JOB_NAME }}"
    API_SERVICE_NAME = "{{ meta.API_SERVICE_NAME }}"
    RPC_SERVICE_NAME = "{{ meta.RPC_SERVICE_NAME }}"
    MODEL_PATH       = "{{ meta.MODEL_PATH }}"
    WORKER_COUNT     = "{{ meta.WORKER_COUNT }}"
  }

  group "master" {
    count = 1

    network {
      mode = "bridge"
      port "http" {}
    }

    service {
      name     = "{{ meta.API_SERVICE_NAME }}"
      provider = "consul"
      port     = "http"

    }

    task "llama-master" {
      driver = "exec"

      template {
        data = <<EOH
#!/bin/bash
# Wait until at least one worker service is available
while [ -z "$(nomad service discover -address-type=ipv4 {{ meta.RPC_SERVICE_NAME }} 2>/dev/null)" ]; do
  echo "Waiting for worker services to become available in Consul..."
  sleep 5
done

# Discover the IP addresses and ports of the worker services
WORKER_IPS=$(nomad service discover -address-type=ipv4 {{ meta.RPC_SERVICE_NAME }} | tr '\n' ',' | sed 's/,$//')

# Launch the llama-server with the discovered worker IPs
/usr/local/bin/llama-server \
  --model {{ meta.MODEL_PATH }} \
  --host 0.0.0.0 \
  --port {% raw %}{{ env "NOMAD_PORT_http" }}{% endraw %} \
  --rpc-servers $WORKER_IPS
EOH
        destination = "local/run_master.sh"
        perms       = "0755"
      }

      config {
        command = "local/run_master.sh"
      }

      volume_mount {
        volume      = "models"
        destination = "/models"
        read_only   = true
      }
    }

    volume "models" {
      type      = "host"
      read_only = true
      source    = "/opt/nomad/models"
    }
  }

  group "workers" {
    count = {{ meta.WORKER_COUNT }}

    network {
      mode = "bridge"
      port "rpc" {}
    }

    service {
      name     = "{{ meta.RPC_SERVICE_NAME }}"
      provider = "consul"
      port     = "rpc"

    }

    task "llama-worker" {
      driver = "exec"

      config {
        command = "/usr/local/bin/llama-server"
        args = [
          "--model", "{{ meta.MODEL_PATH }}",
          "--host", "0.0.0.0",
          "--port", "{% raw %}{{ env \"NOMAD_PORT_rpc\" }}{% endraw %}",
        ]
      }

      volume_mount {
        volume      = "models"
        destination = "/models"
        read_only   = true
      }
    }

    volume "models" {
      type      = "host"
      read_only = true
      source    = "/opt/nomad/models"
    }
  }
}
