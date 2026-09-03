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
      address_mode = "auto"
      address = "${attr.unique.network.ip-address}"
      name = "code-runner-service"
      port = "8000"

      connect {
        sidecar_service {}
      }

      check {
        address_mode = "host"
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
        volumes = [
          "/var/run/docker.sock:/var/run/docker.sock"
        ]
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
