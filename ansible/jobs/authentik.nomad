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
    volume "authentik_media" {
      type      = "host"
      read_only = false
      source    = "authentik_media"
    }

    volume "authentik_templates" {
      type      = "host"
      read_only = false
      source    = "authentik_templates"
    }

    volume "authentik_certs" {
      type      = "host"
      read_only = false
      source    = "authentik_certs"
    }

    network {
      mode = "bridge"
      port "http" {
        static = 19003
        to    = 9000
      }
    }

    task "server" {
      driver = "docker"

      volume_mount {
        volume      = "authentik_media"
        destination = "/media"
        read_only   = false
      }

      volume_mount {
        volume      = "authentik_templates"
        destination = "/templates"
        read_only   = false
      }

      config {
        image = "ghcr.io/goauthentik/server:2024.2.2"
        args  = ["server"]
        ports = ["http"]
      }
      template {
        data = <<EOH
AUTHENTIK_SECRET_KEY={% raw %}{{ key "authentik/secret-key" }}{% endraw %}
AUTHENTIK_POSTGRESQL__PASSWORD={% raw %}{{ key "authentik/db-password" }}{% endraw %}
EOH
        destination = "secrets/authentik.env"
        env         = true
      }
      env {
        AUTHENTIK_REDIS__HOST        = "{{ '{{' }} range service "redis" {{ '}}' }}{{ '{{' }} .Address {{ '}}' }}{{ '{{' }} end {{ '}}' }}"
        AUTHENTIK_REDIS__PORT        = "6379"
        AUTHENTIK_REDIS__PASSWORD    = ""
        AUTHENTIK_POSTGRESQL__HOST = "{{ '{{' }} range service "postgres" {{ '}}' }}{{ '{{' }} .Address {{ '}}' }}{{ '{{' }} end {{ '}}' }}"
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

      volume_mount {
        volume      = "authentik_media"
        destination = "/media"
        read_only   = false
      }

      volume_mount {
        volume      = "authentik_certs"
        destination = "/certs"
        read_only   = false
      }

      volume_mount {
        volume      = "authentik_templates"
        destination = "/templates"
        read_only   = false
      }

      config {
        image = "ghcr.io/goauthentik/server:2024.2.2"
        args  = ["worker"]
      }
      template {
        data = <<EOH
AUTHENTIK_SECRET_KEY={% raw %}{{ key "authentik/secret-key" }}{% endraw %}
AUTHENTIK_POSTGRESQL__PASSWORD={% raw %}{{ key "authentik/db-password" }}{% endraw %}
EOH
        destination = "secrets/authentik.env"
        env         = true
      }
      env {
        AUTHENTIK_REDIS__HOST        = "{{ '{{' }} range service "redis" {{ '}}' }}{{ '{{' }} .Address {{ '}}' }}{{ '{{' }} end {{ '}}' }}"
        AUTHENTIK_REDIS__PORT        = "6379"
        AUTHENTIK_REDIS__PASSWORD    = ""
        AUTHENTIK_POSTGRESQL__HOST = "{{ '{{' }} range service "postgres" {{ '}}' }}{{ '{{' }} .Address {{ '}}' }}{{ '{{' }} end {{ '}}' }}"
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
