job "gitea" {
  datacenters = ["dc1"]
  type        = "service"

  group "gitea-server" {
    count = 1

    network {
      port "http" {
        to = 3000
      }
      port "ssh" {
        to = 2222
      }
    }

    volume "gitea_data" {
      type      = "host"
      source    = "gitea_data"
      read_only = false
    }

    service {
      name = "gitea"
      port = "http"

      tags = [
        "gitea",
        "git",
        "http"
      ]

      check {
        type     = "http"
        path     = "/"
        interval = "10s"
        timeout  = "2s"
      }
    }

    service {
      name = "gitea-ssh"
      port = "ssh"

      tags = [
        "gitea",
        "git",
        "ssh"
      ]

      check {
        type     = "tcp"
        interval = "10s"
        timeout  = "2s"
      }
    }

    task "gitea" {
      driver = "docker"

      config {
        image = "gitea/gitea:latest"
        ports = ["http", "ssh"]
      }

      volume_mount {
        volume      = "gitea_data"
        destination = "/data"
      }

      env {
        USER_UID = "1000"
        USER_GID = "1000"
        # Database settings
        GITEA__database__DB_TYPE = "sqlite3"
        GITEA__database__PATH    = "/data/gitea/gitea.db"
        # Server settings
        GITEA__server__DOMAIN           = "gitea.service.consul"
        GITEA__server__ROOT_URL         = "http://gitea.service.consul:3000/"
        GITEA__server__SSH_DOMAIN       = "gitea.service.consul"
        GITEA__server__SSH_PORT         = "${NOMAD_PORT_ssh}"
        GITEA__server__SSH_LISTEN_PORT  = "2222"
      }

      resources {
        cpu    = 500
        memory = 512
      }
    }
  }
}
