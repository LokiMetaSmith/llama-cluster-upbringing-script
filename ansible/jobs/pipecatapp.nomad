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
        PRIMA_API_SERVICE_NAME = "prima-api-main"
        # Set to "true" to enable the summarizer tool
        USE_SUMMARIZER = "false"
        # The vision and embedding models are now hardcoded in the application
        # to load from the unified /opt/nomad/models directory.
        STT_SERVICE = "faster-whisper"
        STT_MODEL_PATH = "/opt/nomad/models/stt/faster-whisper"
        # A comma-separated list of SHA-256 hashed API keys.
        # Generate a key with: python -c "import secrets; print(secrets.token_hex(32))"
        # Then hash it with: echo -n "<your_key>" | sha256sum
        PIECAT_API_KEYS = ""

        # Configuration for external, third-party LLM experts.
        # This is a JSON string defining a dictionary where each key is the expert's name.
        # - "base_url": The API endpoint for the expert.
        # - "api_key_env": The name of the environment variable that holds the API key.
        #
        # Example:
        # EXTERNAL_EXPERTS_CONFIG = <<EOF
        # {
        #   "openai_gpt4": {
        #     "base_url": "https://api.openai.com/v1",
        #     "api_key_env": "OPENAI_API_KEY"
        #   }
        # }
        # EOF
        # OPENAI_API_KEY = "sk-..."

      }

      volume_mount {
        volume      = "snd"
        destination = "/dev/snd"
       read_only   = false
      }

      logs {
        max_files     = 3
        max_file_size = 10 # MB
      }

      resources {
        cpu    = 1000 # 1 GHz
        memory = 1024 # 4 GB
      }
    }
  }
}
