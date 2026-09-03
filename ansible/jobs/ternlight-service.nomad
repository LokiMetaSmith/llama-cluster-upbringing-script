job "ternlight-service" {
  datacenters = ["dc1"]
  type = "service"

  group "ternlight-group" {
    count = 1

    network {
      mode = "bridge"
      port "http" {
        to = 8000
      }
    }

    service {
      name = "ternlight-service"
      port = "8000"

      connect {
        sidecar_service {}
      }

      check {
        name     = "Ternlight Service Health Check"
        type     = "http"
        path     = "/health"
        interval = "10s"
        timeout  = "2s"
      }
    }

    task "ternlight-server" {
      driver = "docker"

      config {
        image = "ternlight-service:local"
        ports = ["http"]
      }

      env {
        PORT = "8000"
      }

      resources {
        cpu    = 200 # 200 MHz - It's very light
        memory = 128 # 128MB RAM is plenty for 7MB model
      }
    }
  }
}
