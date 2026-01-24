job "uptime-kuma" {
  datacenters = ["dc1"]
  type        = "service"

  group "uptime-kuma" {
    count = 1

    network {
      mode = "bridge"
      port "http" {
        to = 3001
      }
    }

    service {
      name = "uptime-kuma"
      port = "http"
      check {
        type     = "http"
        path     = "/"
        interval = "10s"
        timeout  = "2s"
      }
    }

    task "uptime-kuma" {
      driver = "docker"

      config {
        image = "louislam/uptime-kuma:1"
        ports = ["http"]
        volumes = [
          "/opt/nomad/volumes/uptime-kuma:/app/data"
        ]
      }

      resources {
        cpu    = 200
        memory = 256
      }
    }
  }
}
