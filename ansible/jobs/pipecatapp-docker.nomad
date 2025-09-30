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

    volume "snd" {
      type   = "host"
      source = "snd"
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
      driver = "docker"

      config {
        image = "pipecatapp:latest"
        ports = ["http"]
        # Mount volumes for models and config. Models are read-only.
        # Assumes /app is the WORKDIR in the container, where pipecat_config.json will be placed.
        volumes = [
          "/opt/nomad/models:/opt/nomad/models:ro",
          "/opt/pipecatapp/pipecat_config.json:/app/pipecat_config.json:ro",
        ]
        # Pass through the sound device to the container
        devices = [
          {
            host_path      = "/dev/snd"
            container_path = "/dev/snd"
          }
        ]
      }

      env {
        # This should match the service name of the main prima-expert job
        PRIMA_API_SERVICE_NAME = "{{ prima_api_service_name }}"
        # Set to "true" to enable the summarizer tool
        USE_SUMMARIZER = "{{ use_summarizer }}"
        # The vision and embedding models are now hardcoded in the application
        # to load from the unified /opt/nomad/models directory.
        STT_SERVICE = "{{ stt_service }}"
      }

      resources {
        cpu    = 1000 # 1 GHz
        memory = 1024 # 4 GB
      }
    }
  }
}
