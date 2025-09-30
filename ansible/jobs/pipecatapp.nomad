job "pipecat-app" {
  datacenters = ["dc1"]
  type        = "service"

  group "pipecat-group" {
    count = 1

    network {
      mode = "host"
      port "http" {
        to = 8000
      }
    }

    volume "pipecatapp" {
      type   = "host"
      source = "/opt/pipecatapp"
    }

    volume "models" {
      type   = "host"
      source = "/opt/nomad/models"
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
      driver = "raw_exec"

      config {
        command = "/opt/pipecatapp/start_pipecat.sh"
      }

      user = "root"

      env {
        # This should match the service name of the main prima-expert job
        PRIMA_API_SERVICE_NAME = "prima-api-main"
        # Set to "true" to enable the summarizer tool
        USE_SUMMARIZER = "false"
        # The vision and embedding models are now hardcoded in the application
        # to load from the unified /opt/nomad/models directory.
        STT_SERVICE = "faster-whisper"
        VISION_MODEL = "yolo"
        TORCH_HOME = "/opt/nomad/models"
        DEBUG_MODE = "true"
        APPROVAL_MODE = "true"
      }

      resources {
        cpu    = 1000 # 1 GHz
        memory = 1024 # 1 GB
      }

      volume_mount {
        volume      = "pipecatapp"
        destination = "/opt/pipecatapp"
        read_only   = false
      }

      volume_mount {
        volume      = "models"
        destination = "/opt/nomad/models"
        read_only   = true
      }
    }
  }
}
