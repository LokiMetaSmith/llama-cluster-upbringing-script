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
    
      check {
        type     = "http"
        path     = "/health"
        interval = "10s"
        timeout  = "2s"
      }

    }

    task "pipecat-task" {
      driver = "exec"

      config {
        command = "/opt/pipecatapp/venv/bin/python3"
        args    = ["/opt/pipecatapp/app.py"]
      }

      env {
        # Set to "true" to enable the summarizer tool
        USE_SUMMARIZER = "false"
        # The vision and embedding models are now hardcoded in the application
        # to load from the unified /opt/nomad/models directory.
      }

      resources {
        cpu    = 1000 # 1 GHz
        memory = 4096 # 4 GB
      }
    }
  }
}
