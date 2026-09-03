job "helixdb" {
  datacenters = ["dc1"]
  type = "service"

  group "db" {
    count = 1

    network {
      port "http" {
        to = 6969
        static = 6969
      }
    }

    service {
      name = "helixdb"
      port = "http"
      tags = ["traefik.enable=true", "traefik.http.routers.helixdb.rule=Host(`helixdb.localhost`)", "traefik.http.routers.helixdb.entrypoints=web"]
      check {
        type     = "tcp"
        interval = "10s"
        timeout  = "2s"
      }
    }

    task "helix" {
      driver = "docker"

      config {
        image = "ghcr.io/helixdb/enterprise-dev:latest"
        ports = ["http"]
        args = ["--disk", "/data"]
        volumes = [
          "local/data:/data"
        ]
      }

      resources {
        cpu    = 500
        memory = 512
      }
    }
  }
}
