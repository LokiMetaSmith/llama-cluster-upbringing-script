job "vaultwarden" {
  datacenters = ["dc1"]
  type        = "service"

  group "vaultwarden" {
    count = 1

    network {
      mode = "bridge"
      port "http" {
        to = 80
      }
    }

    service {
      name = "vaultwarden"
      port = "http"
      check {
        type     = "http"
        path     = "/"
        interval = "10s"
        timeout  = "2s"
      }
    }

    task "vaultwarden" {
      driver = "docker"

      config {
        image = "vaultwarden/server:latest"
        ports = ["http"]
        volumes = [
          "/opt/nomad/volumes/vaultwarden:/data"
        ]
      }

      env {
        # SIGNUPS_ALLOWED = "false" # Uncomment to disable signups
      }

      resources {
        cpu    = 200
        memory = 256
      }
    }
  }
}
