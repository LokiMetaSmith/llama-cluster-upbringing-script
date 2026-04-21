job "authentik" {
  datacenters = ["dc1"]
  type      = "service"

  update {
    max_parallel      = 1
    min_healthy_time = "30s"
    healthy_deadline = "10m"
    progress_deadline = "15m"
    canary          = 1
    auto_revert     = false
  }

  group "authentik" {
    network {
      mode = "bridge"
      port "http" {
        static = 19003
        to    = 9000
      }
    }

    task "server" {
      driver = "docker"
      config {
        image = "ghcr.io/goauthentik/server:2024.2.2"
        args  = ["server"]
        network_mode = "bridge"
        ports = ["http"]
        volumes = [
          "/opt/nomad/volumes/authentik/media:/media",
          "/opt/nomad/volumes/authentik/templates:/templates"
        ]
      }
      template {
        data = <<EOH
{{ with secret "kv/data/authentik/config" }}
AUTHENTIK_SECRET_KEY={{ .Data.data.secret_key }}
AUTHENTIK_POSTGRESQL__PASSWORD={{ .Data.data.db_password }}
{{ end }}
EOH
        destination = "secrets/authentik.env"
        env         = true
      }
      env {
        AUTHENTIK_REDIS__HOST        = "redis.service.consul"
        AUTHENTIK_REDIS__PORT        = "6379"
        AUTHENTIK_REDIS__PASSWORD    = ""
        AUTHENTIK_POSTGRESQL__HOST = "postgres.service.consul"
        AUTHENTIK_POSTGRESQL__PORT   = "5432"
        AUTHENTIK_POSTGRESQL__USER = "authentik"
        AUTHENTIK_POSTGRESQL__NAME = "authentik"
        AUTHENTIK_ERROR_REPORTING__ENABLED = "true"
      }
      service {
        name = "authentik"
        port = "http"
      }
      resources {
        cpu    = 500
        memory = 2048
      }
      restart {
        interval = "30s"
        delay    = "15s"
        mode    = "delay"
      }
    }

    task "worker" {
      driver = "docker"
      config {
        image = "ghcr.io/goauthentik/server:2024.2.2"
        args  = ["worker"]
        network_mode = "bridge"
        volumes = [
          "/opt/nomad/volumes/authentik/media:/media",
          "/opt/nomad/volumes/authentik/certs:/certs",
          "/opt/nomad/volumes/authentik/templates:/templates"
        ]
      }
      template {
        data = <<EOH
{{ with secret "kv/data/authentik/config" }}
AUTHENTIK_SECRET_KEY={{ .Data.data.secret_key }}
AUTHENTIK_POSTGRESQL__PASSWORD={{ .Data.data.db_password }}
{{ end }}
EOH
        destination = "secrets/authentik.env"
        env         = true
      }
      env {
        AUTHENTIK_REDIS__HOST        = "redis.service.consul"
        AUTHENTIK_REDIS__PORT        = "6379"
        AUTHENTIK_REDIS__PASSWORD    = ""
        AUTHENTIK_POSTGRESQL__HOST = "postgres.service.consul"
        AUTHENTIK_POSTGRESQL__PORT   = "5432"
        AUTHENTIK_POSTGRESQL__USER = "authentik"
        AUTHENTIK_POSTGRESQL__NAME = "authentik"
        AUTHENTIK_ERROR_REPORTING__ENABLED = "true"
      }
      resources {
        cpu    = 500
        memory = 1024
      }
      restart {
        interval = "30s"
        delay    = "15s"
        mode    = "delay"
      }
    }
  }
}