job "llamacpp-rpc-{{ meta.JOB_NAME | default('default') }}" {
  datacenters = ["dc1"]
  namespace   = "{{ meta.NAMESPACE | default('default') }}"

  meta {
    NAMESPACE         = "default"
    JOB_NAME          = "default"
    API_SERVICE_NAME  = "llama-api-default"
    RPC_SERVICE_NAME  = "llama-rpc-worker-default"
    MODEL_PATH        = "/path/to/your/default/model.gguf"
    WORKER_COUNT      = "2"
  }

  group "master" {
    count = 1

    network {
      port "http" {}
    }

    service {
      name     = "{{ meta.API_SERVICE_NAME | default('llama-api-default') }}"
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
WORKER_IPS=$(nomad service discover -address-type=ipv4 {{ meta.RPC_SERVICE_NAME | default('llama-rpc-worker-default') }} | tr '\n' ',' | sed 's/,$//')

/home/user/llama.cpp/build/bin/llama-server --model {{ meta.MODEL_PATH | default('/path/to/your/default/model.gguf') }} --host 0.0.0.0 --port {{ env "NOMAD_PORT_http" }} --rpc-servers $WORKER_IPS
EOH
        destination = "local/run_master.sh"
        perms       = "0755"
      }

      config {
        command = "local/run_master.sh"
      }
    }
  }

  group "workers" {
    count = "{{ meta.WORKER_COUNT | default('2') }}"

    network {
      port "rpc" {}
    }

    service {
      name     = "{{ meta.RPC_SERVICE_NAME | default('llama-rpc-worker-default') }}"
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
          "--model", "{{ meta.MODEL_PATH | default('/path/to/your/default/model.gguf') }}",
          "--host", "0.0.0.0",
          "--port", "{{ env \"NOMAD_PORT_rpc\" }}",
        ]
      }
    }
  }
}
