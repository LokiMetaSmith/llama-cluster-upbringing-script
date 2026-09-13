job "postgres" {
  datacenters = ["dc1"]
  type      = "service"
  priority  = 80

  update {
    max_parallel      = 1
    min_healthy_time = "30s"
    healthy_deadline = "5m"
  }

  group "postgres" {
    volume "postgres_data" {
      type      = "host"
      read_only = false
      source    = "postgres_data"
    }

    network {
      mode = "bridge"
      port "postgres" {
        to = 5432
      }
    }

    task "postgres" {
      driver = "docker"

      volume_mount {
        volume      = "postgres_data"
        destination = "/var/lib/postgresql/data"
        read_only   = false
      }

      config {
        image = "postgres:15-alpine"
      }
      template {
        data = <<EOH
POSTGRES_PASSWORD={% raw %}{{ key "authentik/db-password" }}{% endraw %}
EOH
        destination = "secrets/postgres.env"
        env         = true
      }
      env {
        POSTGRES_USER     = "authentik"
        POSTGRES_DB       = "authentik"
      }
      service {
        name = "postgres"
        port = "postgres"
        connect {
          sidecar_service {}
        }
        check {
          type     = "tcp"
          interval = "10s"
          timeout  = "2s"
        }
      }
      resources {
        cpu    = 200
        memory = 256
      }
    }
  }
}
