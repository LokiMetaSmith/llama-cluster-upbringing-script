variable "job_name" {
  type    = string
  default = "llamacpp-rpc"
}

variable "service_name" {
  type    = string
  default = "llama-api"
}

variable "model_path" {
  type = string
}

job "{{ var.job_name }}" {
  datacenters = ["dc1"]
  # The user wants to run these in different namespaces
  # The namespace will be passed in via the command line, so I don't need to specify it here.
  # I'll leave it out so it defaults to the namespace from the `nomad job run` command.

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

      config {
        command = "/usr/local/bin/llama-server"
        args = [
          "--model", "{{ var.model_path }}",
          "--host", "0.0.0.0",
          "--port", "{{ env `NOMAD_PORT_http` }}",
        ]
      }

      resources {
        cpu    = 1000
        memory = 4096
      }

      volume_mount {
        volume      = "models"
        destination = "/opt/nomad/models"
        read_only   = true
      }
    }
  }
}
