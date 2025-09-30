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
      driver = "raw_exec"

      config {
        command = "/opt/pipecatapp/start_pipecat.sh"
      }

      env {
        # This should match the service name of the main prima-expert job
        PRIMA_API_SERVICE_NAME = "{{ prima_api_service_name | default('prima-api-main') }}"
        # Set to "true" to enable the summarizer tool
        USE_SUMMARIZER = "{{ use_summarizer | default('false') }}"
        # The vision and embedding models are now hardcoded in the application
        # to load from the unified /opt/nomad/models directory.
        STT_SERVICE = "{{ stt_service | default('faster-whisper') }}"
      }

      resources {
        cpu    = 1000 # 1 GHz
        memory = 1024 # 4 GB
      }

      volume_mount {
        volume      = "snd"
        destination = "/dev/snd"
        read_only   = false
      }
    }
  }
}
