variable "job_name" {
  type    = string
  default = "llama-server"
}

variable "service_name" {
  type    = string
  default = "llama-api"
}

variable "model_path" {
  type    = string
  # No default, this must be provided
}

variable "memory_mb" {
  type    = number
  default = 4096
}

job "{{ var.job_name }}" {
  datacenters = ["dc1"]
  # The namespace will be passed in via the command line,
  # so it is not specified here.

  group "expert" {
    count = 1

    volume "models" {
      type      = "host"
      source    = "models"
      read_only = true
    }

    network {
      mode = "bridge"
      port "http" {}
    }

    service {
      name     = "{{ var.service_name }}"
      provider = "consul"
      port     = "http"

      check {
        type     = "http"
        path     = "/health"
        interval = "15s"
        timeout  = "5s"
      }
    }

    task "llama-server" {
      driver = "exec"

      template {
        data = <<EOH
#!/bin/bash
set -e
echo "Starting llama-server for expert: {{ var.job_name }}"
/usr/local/bin/llama-server \
  --model "{{ var.model_path }}" \
  --host 0.0.0.0 \
  --port {{ env "NOMAD_PORT_http" }}
EOH
        destination = "local/run.sh"
        perms       = "0755"
      }

      config {
        command = "local/run.sh"
      }

      resources {
        cpu    = 1000
        memory = {{ var.memory_mb }}
      }

      volume_mount {
        volume      = "models"
        destination = "/opt/nomad/models"
        read_only   = true
      }
    }
  }
}
