job "llamacpp-rpc-{{ meta.JOB_NAME | default \"default\" }}" {
  datacenters = ["dc1"]

  meta {
    JOB_NAME          = "default"
    API_SERVICE_NAME  = "llama-api-default"
    RPC_SERVICE_NAME  = "llama-rpc-worker-default"
    MODEL_PATH        = "/path/to/your/default/model.gguf"
    WORKER_COUNT      = "2"
  }

  group "master" {
    count = 1

    task "llama-master" {
      driver = "exec"

      template {
        data = <<EOH
#!/bin/bash
WORKER_IPS=$(nomad service discover -address-type=ipv4 {{ meta.RPC_SERVICE_NAME }} | tr '\n' ',' | sed 's/,$//')

/home/user/llama.cpp/build/bin/llama-server \
  --model {{ meta.MODEL_PATH }} \
  --host 0.0.0.0 \
  --port {{ env "NOMAD_PORT_http" }} \
  --rpc-servers $WORKER_IPS
EOH
        destination = "local/run_master.sh"
        perms       = "0755"
      }

      config {
        command = "local/run_master.sh"
      }

      service {
        name = meta.API_SERVICE_NAME
        port = "http"

        connect {
          sidecar_service {}
        }

        check {
          type     = "tcp"
          interval = "10s"
          timeout  = "2s"
        }
      }
    }
  }

  group "workers" {
    count = meta.WORKER_COUNT

    task "llama-worker" {
      driver = "exec"

      config {
        command = "/home/user/llama.cpp/build/bin/llama-server"
        args = [
          "--model", meta.MODEL_PATH,
          "--host", "0.0.0.0",
          "--port", env.NOMAD_PORT_rpc,
        ]
      }

      service {
        name = meta.RPC_SERVICE_NAME
        port = "rpc"

        connect {
          sidecar_service {}
        }
      }
    }
  }
}
