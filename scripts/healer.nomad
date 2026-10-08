job "cluster-healer" {
  datacenters = ["dc1"]
  type        = "service"
  priority    = 90

  group "healer-group" {
    count = 1

    restart {
      attempts = 10
      interval = "10m"
      delay    = "15s"
      mode     = "delay"
    }

    reschedule {
      attempts  = 3
      interval  = "10m"
      delay     = "30s"
      unlimited = false
    }

    network {
      mode = "host"
    }

    task "healer-task" {
      driver = "raw_exec"

      env {
        NOMAD_ADDR        = "https://100.64.0.1:4646"
        NOMAD_CACERT      = "/etc/nomad.d/tls/ca.pem"
        NOMAD_CLIENT_CERT = "/etc/nomad.d/tls/cli.cert.pem"
        NOMAD_CLIENT_KEY  = "/etc/nomad.d/tls/cli.key.pem"
        CONSUL_HTTP_ADDR  = "http://127.0.0.1:8500"
        PYTHONPATH        = "/home/pipecatapp/llama-cluster-upbringing-script:/opt/pipecat-cluster"
      }

      config {
        command = "/bin/bash"
        args = [
          "-c",
          "cd /home/pipecatapp/llama-cluster-upbringing-script && if [ -d .venv ]; then source .venv/bin/activate; fi && python3 scripts/healer.py --watch --interval 15"
        ]
      }

      resources {
        cpu    = 200
        memory = 150
      }
    }
  }
}
