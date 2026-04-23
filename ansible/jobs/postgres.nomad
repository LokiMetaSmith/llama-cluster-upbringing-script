job "postgres" {
  datacenters = ["dc1"]
  type      = "service"

  update {
    max_parallel      = 1
    min_healthy_time = "30s"
    healthy_deadline = "5m"
  }

  group "postgres" {
    network {
      mode = "bridge"
      port "postgres" {
        to = 5432
      }
    }

    task "postgres" {
      driver = "docker"
      config {
        image = "postgres:15-alpine"
      }
      template {
        data = <<EOH
{{ with secret "kv/data/authentik/config" }}
POSTGRES_PASSWORD={{ .Data.data.db_password }}
{{ end }}
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