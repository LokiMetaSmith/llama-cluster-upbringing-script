job "pipecat-app" {
  datacenters = ["dc1"]
  type        = "service"

  group "pipecat-group" {
    count = 1

    network {
      mode = "bridge"
      port "http" {
        to = 8000
      }
    }

    service {
      name = "pipecat-app-http"
      port = "http"
      provider = "consul"

    }

    task "pipecat-task" {
      driver = "exec"

      config {
        command = "/home/user/pipecatapp_venv/bin/python3"
        args    = ["/home/user/app.py"]
      }

      resources {
        cpu    = 1000 # 1 GHz
        memory = 4096 # 4 GB
      }
    }
  }
}
