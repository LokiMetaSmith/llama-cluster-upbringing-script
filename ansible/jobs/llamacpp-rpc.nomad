job "llamacpp-rpc-{{ meta.JOB_NAME | default('default') }}" {
  datacenters = ["dc1"]
  namespace   = "{{ meta.NAMESPACE | default('default') }}"

  meta {
    NAMESPACE        = "default"
    JOB_NAME         = "Llama-3-8B-Instruct"
    API_SERVICE_NAME = "llama-api-Llama-3-8B-Instruct"
    RPC_SERVICE_NAME = "llama-rpc-worker-Llama-3-8B-Instruct"
    MODEL_PATH       = "/models/Meta-Llama-3-8B-Instruct.Q4_K_M.gguf"
    WORKER_COUNT     = "2"
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

      connect {
        sidecar_service {}
      }
    }

    task "llama-master" {
      driver = "exec"

      template {
        data = <<EOH
#!/bin/bash
# Discover the IP addresses and ports of the worker services
WORKER_IPS=$(nomad service discover -address-type=ipv4 {{ meta.RPC_SERVICE_NAME }} | tr '\n' ',' | sed 's/,$//')

# Launch the llama-server with the discovered worker IPs
/home/user/llama.cpp/build/bin/llama-server \
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
      source    = "models"
    }
  }

  group "workers" {
    count = {{ meta.WORKER_COUNT }}

    network {
      mode = "bridge"
      port = "rpc" {}
    }

    service {
      name     = "{{ meta.RPC_SERVICE_NAME }}"
      provider = "consul"
      port     = "rpc"

      connect {
        sidecar_service {}
      }
    }

    task "llama-worker" {
      driver = "exec"

      config {
        command = "/home/user/llama.cpp/build/bin/llama-server"
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
      source    = "models"
    }
  }
}
