job "readeck" {
  datacenters = ["dc1"]
  type        = "service"

  group "readeck" {
    count = 1

    network {
      mode = "bridge"
      port "http" {
        to = 8000
      }
    }

    service {
      name = "readeck"
      port = "http"
      check {
        type     = "http"
        path     = "/"
        interval = "10s"
        timeout  = "2s"
      }
    }

    task "readeck" {
      driver = "docker"

      config {
        image = "codeberg.org/readeck/readeck:latest"
        ports = ["http"]
        volumes = [
          "/opt/nomad/volumes/readeck:/readeck"
        ]
      }

      resources {
        cpu    = 200
        memory = 512
      }
    }
  }
}
