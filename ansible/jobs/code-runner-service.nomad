job "code-runner-service" {
  datacenters = ["dc1"]
  type = "service"

  group "code-runner-group" {
    count = 1

    network {
      mode = "bridge"
      port "http" {
        to = 8000
      }
    }

    service {
      name = "code-runner-service"
      port = "8000"

      connect {
        sidecar_service {}
      }

      check {
        name     = "Code Runner Service HTTP Check"
        type     = "http"
        path     = "/docs"
        interval = "10s"
        timeout  = "2s"
      }
    }

    task "code-runner-server" {
      driver = "docker"

      config {
        image = "code-runner-service:local"
        ports = ["http"]
        # Required for CodeRunner to spin up isolated docker containers or interact with nomad
        mount {
          type     = "bind"
          source   = "/var/run/docker.sock"
          target   = "/var/run/docker.sock"
          readonly = false
        }
      }

      env {
        PORT = "8000"
      }

      resources {
        cpu    = 500 # 500 MHz
        memory = 512 # 512MB RAM
      }
    }
  }
}
