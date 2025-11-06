job "pipecat-app" {
  datacenters = ["dc1"]
  type        = "service"

  group "pipecat-group" {
    count = 1

    network {
      mode = "host"
      port "http" {}
    }

    service {
      name     = "pipecat-app"
      port     = "http"
      provider = "consul"

      check {
        type     = "http"
        path     = "/health"
        interval = "10s"
        timeout  = "2s"
      }
    }

    task "pipecat-task" {
      driver = "raw_exec"

      env {
        WEB_PORT = "${NOMAD_PORT_http}"
      }

      config {
        command = "/opt/pipecatapp/start_pipecat.sh"
      }

      resources {
        cpu    = 1000 # 1 GHz
        memory = 1024 # 1 GB
      }
    }
  }
}
